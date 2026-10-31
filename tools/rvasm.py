#!/usr/bin/env python3
"""rvasm.py - RV32I assembler for the Logisim RISC-V CPUs in this project.

Translates RISC-V assembly into machine code and writes Logisim memory images:
  <out>.text.hex  -> load into the instruction ROM  (right-click ROM > Load Image...)
  <out>.data.hex  -> load into the data RAM         (right-click RAM > Load Image...)
  <out>.lst       -> listing: address | machine code | source line
Optionally patches the ROM inside a .circ file directly (--circ IN --circ-out OUT).

Memory map used by the CPUs (Harvard: separate instruction / data memories)
  IMEM (ROM)  0x0000_0000 - 0x0000_0FFF   1024 instructions
  DMEM (RAM)  0x0000_0000 - 0x0000_3FFF   16 KiB, .data starts at 0x0000_0000
  MMIO TTY    0xF000_0000                 sb/sw here prints one ASCII char
Usage:
  python3 rvasm.py prog.s -o build/prog            # writes build/prog.text.hex, ...
  python3 rvasm.py prog.s -o build/prog --circ RV32I_SingleCycle.circ --circ-out run.circ
"""
import argparse, re, sys

REG_ALIAS = {'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7,
             's0': 8, 'fp': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14,
             'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21, 's6': 22,
             's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27, 't3': 28, 't4': 29,
             't5': 30, 't6': 31}
ABI = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0', 's1', 'a0', 'a1', 'a2', 'a3', 'a4',
       'a5', 'a6', 'a7', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 't3',
       't4', 't5', 't6']

OP = dict(LUI=0b0110111, AUIPC=0b0010111, JAL=0b1101111, JALR=0b1100111, BRANCH=0b1100011,
          LOAD=0b0000011, STORE=0b0100011, OPIMM=0b0010011, OP=0b0110011, SYSTEM=0b1110011,
          FENCE=0b0001111)
R_TYPE = {  # name: (funct3, funct7)
    'add': (0, 0x00), 'sub': (0, 0x20), 'sll': (1, 0), 'slt': (2, 0), 'sltu': (3, 0),
    'xor': (4, 0), 'srl': (5, 0x00), 'sra': (5, 0x20), 'or': (6, 0), 'and': (7, 0)}
I_ALU = {'addi': 0, 'slti': 2, 'sltiu': 3, 'xori': 4, 'ori': 6, 'andi': 7}
SHIFT_I = {'slli': (1, 0x00), 'srli': (5, 0x00), 'srai': (5, 0x20)}
LOADS = {'lb': 0, 'lh': 1, 'lw': 2, 'lbu': 4, 'lhu': 5}
STORES = {'sb': 0, 'sh': 1, 'sw': 2}
BRANCHES = {'beq': 0, 'bne': 1, 'blt': 4, 'bge': 5, 'bltu': 6, 'bgeu': 7}

TEXT_BASE, DATA_BASE = 0x0, 0x0
IMEM_WORDS, DMEM_BYTES = 1024, 16384
DUMP_BASE = 0x700   # test harness: registers x0..x31 are stored at 0x700..0x77C


class AsmError(Exception):
    pass


def reg(tok):
    t = tok.strip().lower()
    if t in REG_ALIAS:
        return REG_ALIAS[t]
    m = re.fullmatch(r'x(\d+)', t)
    if m and int(m.group(1)) < 32:
        return int(m.group(1))
    raise AsmError(f'bad register "{tok}"')


def split_operands(s):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch == ',' and depth == 0:
            out.append(cur.strip()); cur = ''
            continue
        depth += ch == '('
        depth -= ch == ')'
        cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


class Assembler:
    def __init__(self, dump=False):
        self.symbols = {}
        self.equs = set()
        self.dump = dump

    # ---- expressions --------------------------------------------------------
    def eval(self, expr, pc=0, need=True):
        e = expr.strip()
        m = re.fullmatch(r'%(hi|lo)\((.*)\)', e)
        if m:
            v = self.eval(m.group(2), pc, need)
            if v is None:
                return None
            hi, lo = self.split_hi_lo(v)
            return hi if m.group(1) == 'hi' else lo
        def repl_char(mm):
            return str(ord(mm.group(1).encode().decode('unicode_escape')))
        e = re.sub(r"'(\\?.)'", repl_char, e)
        names = re.findall(r'(?<![\w.$])[A-Za-z_.$][\w.$]*', e)
        env = {}
        for n in names:
            if n in self.symbols:
                env[n] = self.symbols[n]
            elif need:
                raise AsmError(f'undefined symbol "{n}"')
            else:
                return None
        safe = re.sub(r'(?<![\w.$])[A-Za-z_.$][\w.$]*', lambda mm: f'env[{mm.group(0)!r}]', e)
        try:
            return int(eval(safe, {'__builtins__': {}}, {'env': env}))
        except Exception:
            raise AsmError(f'bad expression "{expr}"')

    def li_short(self, expr):
        """Size decision for li must be identical in both passes: only expressions made of
        numbers and .equ constants (pre-scanned) can use the 1-instruction form."""
        names = re.findall(r"(?<![\w.$])[A-Za-z_.$][\w.$]*", re.sub(r"'(\\?.)'", '0', expr))
        if any(n not in self.equs for n in names):
            return False
        v = self.eval(expr)
        return -2048 <= v <= 2047

    def const_known(self, expr):
        try:
            return self.eval(expr, need=False)
        except AsmError:
            return None

    # ---- encoders -----------------------------------------------------------
    @staticmethod
    def enc_r(f7, rs2, rs1, f3, rd, op):
        return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op

    @staticmethod
    def enc_i(imm, rs1, f3, rd, op):
        if not -2048 <= imm <= 2047:
            raise AsmError(f'I-immediate {imm} out of range [-2048, 2047]')
        return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op

    @staticmethod
    def enc_s(imm, rs2, rs1, f3, op):
        if not -2048 <= imm <= 2047:
            raise AsmError(f'S-immediate {imm} out of range')
        imm &= 0xFFF
        return ((imm >> 5) << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | ((imm & 0x1F) << 7) | op

    @staticmethod
    def enc_b(off, rs2, rs1, f3, op):
        if off % 2 or not -4096 <= off <= 4094:
            raise AsmError(f'branch offset {off} out of range / misaligned')
        o = off & 0x1FFF
        return (((o >> 12) & 1) << 31) | (((o >> 5) & 0x3F) << 25) | (rs2 << 20) | (rs1 << 15) | \
               (f3 << 12) | (((o >> 1) & 0xF) << 8) | (((o >> 11) & 1) << 7) | op

    @staticmethod
    def enc_u(imm20, rd, op):
        return ((imm20 & 0xFFFFF) << 12) | (rd << 7) | op

    @staticmethod
    def enc_j(off, rd, op):
        if off % 2 or not -(1 << 20) <= off < (1 << 20):
            raise AsmError(f'jump offset {off} out of range')
        o = off & 0x1FFFFF
        return (((o >> 20) & 1) << 31) | (((o >> 1) & 0x3FF) << 21) | (((o >> 11) & 1) << 20) | \
               (((o >> 12) & 0xFF) << 12) | (rd << 7) | op

    @staticmethod
    def split_hi_lo(v):
        """value = (hi << 12) + sext(lo):  lui loads hi, addi adds the signed low 12 bits."""
        v &= 0xFFFFFFFF
        lo = v & 0xFFF
        if lo >= 0x800:
            lo -= 0x1000
        hi = ((v - lo) >> 12) & 0xFFFFF
        return hi, lo

    # ---- pseudo-instruction expansion (returns list of (mnemonic, operands)) --
    def expand(self, mn, ops, sizing):
        """Return list of real instructions. In sizing pass, symbols may be unknown."""
        P = lambda *x: [x]
        if mn == 'nop':
            return [('addi', ['x0', 'x0', '0'])]
        if mn == 'li':
            rd, expr = ops
            if self.li_short(expr):            # fits in 12 bits -> one addi
                return [('addi', [rd, 'x0', '0' if sizing else str(self.eval(expr))])]
            v = 0 if sizing else self.eval(expr)
            hi, lo = self.split_hi_lo(v)
            return [('lui', [rd, str(hi)]), ('addi', [rd, rd, str(lo)])]
        if mn == 'la':
            rd, expr = ops
            v = None if sizing else self.eval(expr)
            if v is None:
                return [('lui', [rd, '0']), ('addi', [rd, rd, '0'])]
            hi, lo = self.split_hi_lo(v)
            return [('lui', [rd, str(hi)]), ('addi', [rd, rd, str(lo)])]
        simple = {
            'mv': lambda: [('addi', [ops[0], ops[1], '0'])],
            'not': lambda: [('xori', [ops[0], ops[1], '-1'])],
            'neg': lambda: [('sub', [ops[0], 'x0', ops[1]])],
            'seqz': lambda: [('sltiu', [ops[0], ops[1], '1'])],
            'snez': lambda: [('sltu', [ops[0], 'x0', ops[1]])],
            'sltz': lambda: [('slt', [ops[0], ops[1], 'x0'])],
            'sgtz': lambda: [('slt', [ops[0], 'x0', ops[1]])],
            'beqz': lambda: [('beq', [ops[0], 'x0', ops[1]])],
            'bnez': lambda: [('bne', [ops[0], 'x0', ops[1]])],
            'blez': lambda: [('bge', ['x0', ops[0], ops[1]])],
            'bgez': lambda: [('bge', [ops[0], 'x0', ops[1]])],
            'bltz': lambda: [('blt', [ops[0], 'x0', ops[1]])],
            'bgtz': lambda: [('blt', ['x0', ops[0], ops[1]])],
            'bgt': lambda: [('blt', [ops[1], ops[0], ops[2]])],
            'ble': lambda: [('bge', [ops[1], ops[0], ops[2]])],
            'bgtu': lambda: [('bltu', [ops[1], ops[0], ops[2]])],
            'bleu': lambda: [('bgeu', [ops[1], ops[0], ops[2]])],
            'j': lambda: [('jal', ['x0', ops[0]])],
            'jr': lambda: [('jalr', ['x0', ops[0], '0'])],
            'ret': lambda: [('jalr', ['x0', 'ra', '0'])],
            'call': lambda: [('jal', ['ra', ops[0]])],
            'tail': lambda: [('jal', ['x0', ops[0]])],
            'halt': lambda: [('ebreak', [])],
        }
        if mn in simple:
            return simple[mn]()
        if mn == 'jal' and len(ops) == 1:
            return [('jal', ['ra', ops[0]])]
        if mn == 'jalr' and len(ops) == 1:
            return [('jalr', ['ra', ops[0], '0'])]
        if mn == 'jalr' and len(ops) == 2 and '(' in ops[1]:
            m = re.fullmatch(r'(.*)\((.*)\)', ops[1].strip())
            return [('jalr', [ops[0], m.group(2), m.group(1) or '0'])]
        if mn in ('ebreak', 'ecall') and self.dump:
            return [('jal', ['x0', '__dump'])]
        return [(mn, ops)]

    def encode(self, mn, ops, pc):
        n = len(ops)
        if mn in R_TYPE:
            f3, f7 = R_TYPE[mn]
            return self.enc_r(f7, reg(ops[2]), reg(ops[1]), f3, reg(ops[0]), OP['OP'])
        if mn in I_ALU:
            return self.enc_i(self.eval(ops[2], pc), reg(ops[1]), I_ALU[mn], reg(ops[0]), OP['OPIMM'])
        if mn in SHIFT_I:
            f3, f7 = SHIFT_I[mn]
            sh = self.eval(ops[2], pc)
            if not 0 <= sh < 32:
                raise AsmError('shift amount must be 0..31')
            return self.enc_r(f7, sh, reg(ops[1]), f3, reg(ops[0]), OP['OPIMM'])
        if mn in LOADS or mn in STORES or mn == 'jalr':
            if mn == 'jalr' and n == 3:
                rd, rs1, off = ops
            else:
                m = re.fullmatch(r'(.*)\((.*)\)', ops[1].strip())
                if not m:
                    raise AsmError(f'expected offset(reg) in "{ops[1]}"')
                off, rs1 = (m.group(1).strip() or '0'), m.group(2)
                rd = ops[0]
            imm = self.eval(off, pc)
            if mn in LOADS:
                return self.enc_i(imm, reg(rs1), LOADS[mn], reg(rd), OP['LOAD'])
            if mn == 'jalr':
                return self.enc_i(imm, reg(rs1), 0, reg(rd), OP['JALR'])
            return self.enc_s(imm, reg(rd), reg(rs1), STORES[mn], OP['STORE'])
        if mn in BRANCHES:
            return self.enc_b(self.eval(ops[2], pc) - pc, reg(ops[1]), reg(ops[0]), BRANCHES[mn], OP['BRANCH'])
        if mn == 'jal':
            return self.enc_j(self.eval(ops[1], pc) - pc, reg(ops[0]), OP['JAL'])
        if mn in ('lui', 'auipc'):
            v = self.eval(ops[1], pc)
            if not -(1 << 19) <= v < (1 << 20):
                raise AsmError('U-immediate out of range (20 bits)')
            return self.enc_u(v, reg(ops[0]), OP['LUI' if mn == 'lui' else 'AUIPC'])
        if mn == 'ecall':
            return OP['SYSTEM']
        if mn == 'ebreak':
            return (1 << 20) | OP['SYSTEM']
        if mn == 'fence':
            return OP['FENCE']
        raise AsmError(f'unknown instruction "{mn}"')

    # ---- driver -------------------------------------------------------------
    def parse_lines(self, src):
        items = []
        for ln, raw in enumerate(src.splitlines(), 1):
            line = re.split(r'#|//', raw, maxsplit=1)[0].strip() if '"' not in raw else raw.split('#')[0].strip()
            while True:
                m = re.match(r'^([A-Za-z_.$][\w.$]*)\s*:\s*(.*)$', line)
                if not m:
                    break
                items.append((ln, raw, 'label', m.group(1), None))
                line = m.group(2).strip()
            if not line:
                continue
            parts = line.split(None, 1)
            mn = parts[0].lower()
            rest = parts[1] if len(parts) > 1 else ''
            items.append((ln, raw, 'dir' if mn.startswith('.') else 'ins', mn, rest))
        return items

    def assemble(self, src):
        if self.dump:
            src += '\n.text\n__dump:\n' + ''.join(
                f'    sw x{i}, {DUMP_BASE + 4 * i}(x0)\n' for i in range(1, 32)) + '    .word 0x00100073\n'
        items = self.parse_lines(src)
        for ln, raw, kind, a, rest in items:          # pre-scan .equ constants
            if kind == 'dir' and a in ('.equ', '.set'):
                nm, ex = split_operands(rest)
                self.symbols[nm] = self.eval(ex)
                self.equs.add(nm)
        for sizing in (True, False):
            sec = 'text'
            lc = {'text': TEXT_BASE, 'data': DATA_BASE}
            text, data, listing = {}, {}, []
            for ln, raw, kind, a, rest in items:
                try:
                    if kind == 'label':
                        if sizing:
                            if a in self.symbols:
                                raise AsmError(f'duplicate label "{a}"')
                            self.symbols[a] = lc[sec]
                        continue
                    if kind == 'dir':
                        sec = self.directive(a, rest, sec, lc, data, text, sizing)
                        continue
                    if sec != 'text':
                        raise AsmError('instruction outside .text')
                    ops = split_operands(rest)
                    for mn, o in self.expand(a, ops, sizing):
                        pc = lc['text']
                        if not sizing:
                            word = self.encode(mn, o, pc) & 0xFFFFFFFF
                            text[pc] = word
                            listing.append((pc, word, f'{mn} {", ".join(o)}', ln, raw.strip()))
                        lc['text'] += 4
                except AsmError as e:
                    raise AsmError(f'line {ln}: {e}\n    {raw.strip()}')
        n = (max(text) // 4 + 1) if text else 0
        if n > IMEM_WORDS:
            raise AsmError(f'program too large: {n} words > {IMEM_WORDS}')
        words = [text.get(4 * i, 0) for i in range(n)]
        return words, data, listing

    def directive(self, d, rest, sec, lc, data, text, sizing):
        args = split_operands(rest) if rest else []
        if d in ('.text', '.data'):
            return d[1:]
        if d in ('.globl', '.global', '.section', '.type', '.size', '.option', '.file', '.attribute'):
            if d == '.section':
                return 'data' if 'data' in rest or 'bss' in rest else 'text'
            return sec
        if d in ('.equ', '.set'):
            return sec
        def emit(nbytes, val):
            addr = lc[sec]
            if sec == 'data':
                for i in range(nbytes):
                    data[addr + i] = (val >> (8 * i)) & 0xFF
            else:
                if nbytes != 4 or addr % 4:
                    raise AsmError('only aligned .word allowed in .text')
                text[addr] = val & 0xFFFFFFFF
            lc[sec] += nbytes
        if d in ('.word', '.half', '.byte', '.2byte', '.4byte'):
            n = {'.word': 4, '.4byte': 4, '.half': 2, '.2byte': 2, '.byte': 1}[d]
            for a in args:
                emit(n, 0 if sizing else self.eval(a))
            return sec
        if d in ('.space', '.zero', '.skip'):
            n = self.eval(args[0])
            for _ in range(n):
                emit(1, 0) if sec == 'data' else None
            if sec != 'data':
                lc[sec] += n
            return sec
        if d in ('.align', '.p2align', '.balign'):
            a = self.eval(args[0])
            al = a if d == '.balign' else (1 << a)
            while lc[sec] % al:
                if sec == 'data':
                    emit(1, 0)
                else:
                    emit(4, 0x13)
            return sec
        if d in ('.ascii', '.asciz', '.string'):
            s = bytes(rest.strip()[1:-1], 'utf-8').decode('unicode_escape').encode('latin-1')
            for b in s:
                emit(1, b)
            if d != '.ascii':
                emit(1, 0)
            return sec
        raise AsmError(f'unknown directive {d}')


def data_words(data):
    if not data:
        return []
    n = max(data) // 4 + 1
    return [sum(data.get(4 * i + k, 0) << (8 * k) for k in range(4)) for i in range(n)]


def write_hex(path, words):
    with open(path, 'w') as f:
        f.write('v3.0 hex words plain\n')
        for i in range(0, len(words), 8):
            f.write(' '.join(f'{w:08x}' for w in words[i:i + 8]) + '\n')


def circ_contents(words, addr_bits=10):
    body = ''
    for i in range(0, len(words), 8):
        body += ' '.join(f'{w:x}' for w in words[i:i + 8]) + '\n'
    return f'addr/data: {addr_bits} 32\n' + body


def patch_circ(circ_in, circ_out, words, rom_label='IMEM'):
    import xml.etree.ElementTree as ET
    txt = open(circ_in, encoding='utf-8').read()
    # find <comp ... name="ROM"> block that has label IMEM and replace contents
    pat = re.compile(r'(<comp lib="\d+" loc="\([^)]*\)" name="ROM">)(.*?)(</comp>)', re.S)
    count = 0

    def fix(m):
        nonlocal count
        body = m.group(2)
        if f'val="{rom_label}"' not in body:
            return m.group(0)
        count += 1
        body = re.sub(r'\s*<a name="contents">.*?</a>', '', body, flags=re.S)
        body = f'\n      <a name="contents">{circ_contents(words)}</a>' + body
        return m.group(1) + body + m.group(3)
    txt = pat.sub(fix, txt)
    if count == 0:
        raise AsmError(f'no ROM labelled {rom_label} in {circ_in}')
    open(circ_out, 'w', encoding='utf-8').write(txt)
    return count


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src')
    ap.add_argument('-o', '--out', help='output prefix (default: source name)')
    ap.add_argument('--dump', action='store_true', help='test mode: ebreak/ecall jump to a routine that '
                    'stores x1..x31 at 0x704..0x77C before halting')
    ap.add_argument('--circ', help='.circ file whose ROM (label IMEM) gets the program')
    ap.add_argument('--circ-out', help='where to write the patched .circ (default: overwrite --circ)')
    a = ap.parse_args()
    asm = Assembler(dump=a.dump)
    try:
        words, data, listing = asm.assemble(open(a.src, encoding='utf-8').read())
    except AsmError as e:
        print('error:', e, file=sys.stderr)
        sys.exit(1)
    out = a.out or re.sub(r'\.\w+$', '', a.src)
    write_hex(out + '.text.hex', words)
    write_hex(out + '.data.hex', data_words(data) or [0])
    with open(out + '.lst', 'w') as f:
        for pc, w, ins, ln, raw in listing:
            f.write(f'{pc:08x}:  {w:08x}   {ins:<28} # L{ln}: {raw}\n')
    print(f'{len(words)} instructions, {len(data)} data bytes -> {out}.text.hex / .data.hex / .lst')
    if a.circ:
        patch_circ(a.circ, a.circ_out or a.circ, words)
        print(f'ROM "IMEM" in {a.circ_out or a.circ} updated')


if __name__ == '__main__':
    main()
