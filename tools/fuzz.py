#!/usr/bin/env python3
"""fuzz.py - generate random (but always terminating) RV32I programs that are dense in
data hazards, load-use pairs, branches and calls; used to stress the pipeline.
  python3 tools/fuzz.py 20 programs/fuzz        # writes programs/fuzz/f000.s ...
"""
import random, sys, os

REGS = [f'x{i}' for i in range(1, 16)]
ALU_R = ['add', 'sub', 'and', 'or', 'xor', 'slt', 'sltu', 'sll', 'srl', 'sra']
ALU_I = ['addi', 'andi', 'ori', 'xori', 'slti', 'sltiu']
SH_I = ['slli', 'srli', 'srai']
BR = ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']


def gen(seed, n=120):
    rnd = random.Random(seed)
    r = lambda: rnd.choice(REGS[:8]) if rnd.random() < 0.7 else rnd.choice(REGS)   # few regs -> many hazards
    out = ['        li   x20, 0x1000            # data base', '        li   x21, 0x3FF0            # stack']
    for i in range(1, 16):
        out.append(f'        li   x{i}, {rnd.randint(-3000, 3000)}')
    lbl = 0
    i = 0
    while i < n:
        k = rnd.random()
        if k < 0.35:
            out.append(f'        {rnd.choice(ALU_R)} {r()}, {r()}, {r()}')
        elif k < 0.55:
            out.append(f'        {rnd.choice(ALU_I)} {r()}, {r()}, {rnd.randint(-2048, 2047)}')
        elif k < 0.6:
            out.append(f'        {rnd.choice(SH_I)} {r()}, {r()}, {rnd.randint(0, 31)}')
        elif k < 0.62:
            out.append(f'        {rnd.choice(["lui", "auipc"])} {r()}, {rnd.randint(0, 0xFFFFF)}')
        elif k < 0.75:
            off = rnd.randrange(0, 64) * 4
            op = rnd.choice(['lw', 'lw', 'lh', 'lhu', 'lb', 'lbu'])
            if op in ('lh', 'lhu'):
                off += rnd.choice([0, 2])
            if op in ('lb', 'lbu'):
                off += rnd.randrange(4)
            d = r()
            out.append(f'        {op} {d}, {off}(x20)')
            if rnd.random() < 0.6:                       # immediate use -> load-use hazard
                out.append(f'        add  {r()}, {d}, {r()}')
        elif k < 0.85:
            off = rnd.randrange(0, 64) * 4
            op = rnd.choice(['sw', 'sw', 'sh', 'sb'])
            if op == 'sh':
                off += rnd.choice([0, 2])
            if op == 'sb':
                off += rnd.randrange(4)
            out.append(f'        {op} {r()}, {off}(x20)')
        elif k < 0.93:                                   # forward branch over 1..3 instructions
            lbl += 1
            out.append(f'        {rnd.choice(BR)} {r()}, {r()}, L{lbl}')
            for _ in range(rnd.randint(1, 3)):
                out.append(f'        addi {r()}, {r()}, {rnd.randint(-50, 50)}')
            out.append(f'L{lbl}:')
        elif k < 0.97:                                   # small counted loop
            lbl += 1
            c = rnd.randint(1, 4)
            out.append(f'        li   x16, {c}')
            out.append(f'L{lbl}:')
            for _ in range(rnd.randint(1, 3)):
                out.append(f'        {rnd.choice(ALU_R)} {r()}, {r()}, {r()}')
            out.append('        addi x16, x16, -1')
            out.append(f'        bnez x16, L{lbl}')
        else:                                            # call a leaf function via jal / jalr
            lbl += 1
            if rnd.random() < 0.5:
                out.append(f'        jal  x18, F{lbl}')
            else:
                out.append(f'        la   x17, F{lbl}')
                out.append(f'        jalr x18, 0(x17)')
            out.append(f'        j    E{lbl}')
            out.append(f'F{lbl}:   {rnd.choice(ALU_R)} {r()}, {r()}, {r()}')
            out.append('        jalr x0, 0(x18)')
            out.append(f'E{lbl}:')
        i += 1
    out.append('        ebreak')
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    d = sys.argv[2] if len(sys.argv) > 2 else 'programs/fuzz'
    os.makedirs(d, exist_ok=True)
    for s in range(n):
        open(os.path.join(d, f'f{s:03d}.s'), 'w').write(f'# random program, seed {s}\n' + gen(s))
    print(f'{n} programs in {d}')
