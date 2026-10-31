#!/usr/bin/env python3
"""rvsim.py - golden-model instruction-set simulator (ISS) for RV32I.

Used as the *reference* to check the Logisim CPUs: we run the same machine code on
this simulator and on Logisim, then compare registers + data memory.
It also predicts how many clock cycles the 5-stage pipeline must take
(N + 4 fill + 1 per load-use stall + 2 per taken branch/jump), so the hazard
logic is checked, not only the final results.

  python3 rvsim.py prog.s            # assemble + run, print registers
  python3 rvsim.py prog.s --trace    # also print every executed instruction
"""
import sys, argparse
sys.path.insert(0, __import__('os').path.dirname(__file__))
import rvasm

MASK = 0xFFFFFFFF
DMEM_BYTES = rvasm.DMEM_BYTES
MMIO_BASE = 0xF0000000


def sx(v, bits):
    v &= (1 << bits) - 1
    return v - (1 << bits) if v >> (bits - 1) else v


def decode(ins):
    op = ins & 0x7F
    rd = (ins >> 7) & 31
    f3 = (ins >> 12) & 7
    rs1 = (ins >> 15) & 31
    rs2 = (ins >> 20) & 31
    f7 = ins >> 25
    imm_i = sx(ins >> 20, 12)
    imm_s = sx(((ins >> 25) << 5) | ((ins >> 7) & 31), 12)
    imm_b = sx((((ins >> 31) & 1) << 12) | (((ins >> 7) & 1) << 11) | (((ins >> 25) & 0x3F) << 5) |
               (((ins >> 8) & 0xF) << 1), 13)
    imm_u = ins & 0xFFFFF000
    imm_j = sx((((ins >> 31) & 1) << 20) | (((ins >> 12) & 0xFF) << 12) | (((ins >> 20) & 1) << 11) |
               (((ins >> 21) & 0x3FF) << 1), 21)
    return dict(op=op, rd=rd, f3=f3, rs1=rs1, rs2=rs2, f7=f7, i=imm_i, s=imm_s, b=imm_b, u=imm_u, j=imm_j)


def uses(d):
    """(uses_rs1, uses_rs2) exactly as the hardware decoder defines them."""
    op = d['op']
    u1 = op in (0x33, 0x13, 0x03, 0x23, 0x63, 0x67)
    u2 = op in (0x33, 0x23, 0x63)
    return u1, u2


class CPU:
    def __init__(self, text_words, data_bytes=None, stdin=''):
        self.imem = list(text_words)
        self.mem = bytearray(DMEM_BYTES)
        for a, b in (data_bytes or {}).items():
            self.mem[a % DMEM_BYTES] = b
        self.x = [0] * 32
        self.pc = 0
        self.instret = 0
        self.tty = ''
        self.rx = [ord(ch) & 0x7F for ch in stdin]   # UART RX queue (Logisim Keyboard)
        self.gpio_out = 0
        self.gpio_in = 0                              # DIP switches (all off)
        self.trace = []
        # pipeline timing model
        self.loaduse = 0
        self.redirects = 0
        self._prev_load_rd = None

    # ---- memory-mapped I/O: same register map as the IOController sub-circuit ----
    def io_word(self, addr):
        idx = (addr >> 2) & 7
        if idx == 1:
            return self.rx[0] if self.rx else 0
        if idx == 2:
            return 0b10 | (1 if self.rx else 0)
        if idx == 4:
            return self.gpio_out
        if idx == 5:
            return self.gpio_in & 0xFF
        return 0

    @staticmethod
    def extract(word, off, size, signed):
        v = (word >> (8 * off)) & ((1 << (8 * size)) - 1)
        return sx(v, 8 * size) & MASK if signed else v

    def load(self, addr, size, signed):
        if addr % size:
            raise RuntimeError(f'misaligned load @ {addr:#x} pc={self.pc:#x}')
        if addr >= MMIO_BASE:
            word = self.io_word(addr)
            if (addr >> 2) & 7 == 1 and self.rx:
                self.rx.pop(0)                       # reading RXDATA consumes the character
            return self.extract(word, addr & 3, size, signed)
        a = addr % DMEM_BYTES
        v = int.from_bytes(self.mem[a:a + size], 'little')
        return sx(v, 8 * size) & MASK if signed else v

    def store(self, addr, size, val):
        if addr % size:
            raise RuntimeError(f'misaligned store @ {addr:#x} pc={self.pc:#x}')
        if addr >= MMIO_BASE:
            old = self.io_word(addr)
            sh = 8 * (addr & 3)
            m = (((1 << (8 * size)) - 1) << sh) & MASK
            new = (old & ~m | (val << sh) & m) & MASK   # same read-modify-write as StoreUnit
            idx = (addr >> 2) & 7
            if idx == 0:
                self.tty += chr(new & 0x7F)
            elif idx == 4:
                self.gpio_out = new
            return
        a = addr % DMEM_BYTES
        self.mem[a:a + size] = (val & ((1 << (8 * size)) - 1)).to_bytes(size, 'little')

    def step(self):
        idx = self.pc >> 2
        if self.pc & 3 or idx >= len(self.imem):
            ins = 0
        else:
            ins = self.imem[idx]
        d = decode(ins)
        op, rd, f3, x = d['op'], d['rd'], d['f3'], self.x
        a, b = x[d['rs1']], x[d['rs2']]
        # --- timing model: load-use hazard against the previous instruction
        u1, u2 = uses(d)
        if self._prev_load_rd and ((u1 and d['rs1'] == self._prev_load_rd) or (u2 and d['rs2'] == self._prev_load_rd)):
            self.loaduse += 1
        self._prev_load_rd = rd if (op == 0x03 and rd != 0) else None
        nxt = (self.pc + 4) & MASK
        res = None
        redirect = op in (0x6F, 0x67) and ins & 3 == 3
        if ins & 3 != 3:
            pass                                   # not a 32-bit instruction -> NOP (bubble)
        elif op == 0x37:
            res = d['u']
        elif op == 0x17:
            res = (self.pc + d['u']) & MASK
        elif op == 0x6F:
            res, nxt = self.pc + 4, (self.pc + d['j']) & MASK
        elif op == 0x67:
            res, nxt = self.pc + 4, (a + d['i']) & MASK & ~1
        elif op == 0x63:
            sa, sb = sx(a, 32), sx(b, 32)
            take = {0: a == b, 1: a != b, 4: sa < sb, 5: sa >= sb, 6: a < b, 7: a >= b}.get(f3, False)
            if take:
                nxt = (self.pc + d['b']) & MASK
                redirect = True
        elif op == 0x03:
            addr = (a + d['i']) & MASK
            size = {0: 1, 1: 2, 2: 4, 4: 1, 5: 2}[f3]
            res = self.load(addr, size, f3 in (0, 1))
        elif op == 0x23:
            addr = (a + d['s']) & MASK
            self.store(addr, {0: 1, 1: 2, 2: 4}[f3], b)
        elif op in (0x13, 0x33):
            imm = op == 0x13
            bb = d['i'] & MASK if imm else b
            sh = bb & 31
            alt = (d['f7'] >> 5) & 1
            if f3 == 0:
                res = a - bb if (not imm and alt) else a + bb
            elif f3 == 1:
                res = a << sh
            elif f3 == 2:
                res = int(sx(a, 32) < sx(bb, 32))
            elif f3 == 3:
                res = int(a < bb)
            elif f3 == 4:
                res = a ^ bb
            elif f3 == 5:
                res = (sx(a, 32) >> sh) if alt else (a >> sh)
            elif f3 == 6:
                res = a | bb
            else:
                res = a & bb
        elif op == 0x73:
            return False                            # ecall / ebreak = HALT
        if res is not None and rd:
            x[rd] = res & MASK
        if redirect:
            self.redirects += 1                     # hardware flushes on every taken branch / jump
        self.trace.append((self.pc, ins))
        self.pc = nxt
        self.instret += 1
        return True

    def run(self, max_steps=200000):
        while self.step():
            if self.instret > max_steps:
                raise RuntimeError('did not halt (infinite loop?)')
        return self

    # expected cycle counts for the two hardware versions
    def cycles_single(self):
        return self.instret

    def cycles_pipeline(self):
        return self.instret + 4 + self.loaduse + 2 * self.redirects


def stdin_of(src):
    """programs may declare UART input with a comment line:  # STDIN: "text\\n" """
    import ast, re
    m = re.search(r'^#\s*STDIN:\s*(".*")\s*$', src, re.M)
    return ast.literal_eval(m.group(1)) if m else ''


def run_source(src, dump=False):
    asm = rvasm.Assembler(dump=dump)
    words, data, listing = asm.assemble(src)
    return CPU(words, data, stdin_of(src)).run(), words, data, listing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--trace', action='store_true')
    a = ap.parse_args()
    cpu, words, data, listing = run_source(open(a.src).read())
    if a.trace:
        for pc, ins in cpu.trace:
            print(f'{pc:08x}: {ins:08x}')
    for i in range(0, 32, 4):
        print('  '.join(f'x{j:<2}({rvasm.ABI[j]:>4}) = {cpu.x[j]:08x}' for j in range(i, i + 4)))
    print(f'instret={cpu.instret}  single-cycle cycles={cpu.cycles_single()}  pipeline cycles={cpu.cycles_pipeline()} '
          f'(load-use stalls={cpu.loaduse}, taken branches/jumps={cpu.redirects}, CPI={cpu.cycles_pipeline()/max(1,cpu.instret):.2f})')
    if cpu.tty:
        print('TTY output:', repr(cpu.tty))
    if cpu.gpio_out:
        print(f'GPIO_OUT = {cpu.gpio_out:#010x}')


if __name__ == '__main__':
    main()
