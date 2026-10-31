"""Reference (golden) models used to generate Logisim test vectors for each module."""
import random
M = 0xFFFFFFFF


def sx(v, b):
    v &= (1 << b) - 1
    return v - (1 << b) if v >> (b - 1) else v


def alu(a, b, ctrl):
    f3, alt = ctrl & 7, ctrl >> 3
    sh = b & 31
    if f3 == 0:
        return (a - b if alt else a + b) & M
    if f3 == 1:
        return (a << sh) & M
    if f3 == 2:
        return int(sx(a, 32) < sx(b, 32))
    if f3 == 3:
        return int(a < b)
    if f3 == 4:
        return a ^ b
    if f3 == 5:
        return (sx(a, 32) >> sh) & M if alt else a >> sh
    if f3 == 6:
        return a | b
    return a & b


EDGE = [0, 1, 2, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0xFFFFFFFE, 31, 32, 0x12345678, 0x0000FFFF, 0xFFFF0000]


def rnd32():
    return random.choice(EDGE) if random.random() < 0.3 else random.getrandbits(32)


def write_vec(path, header, rows):
    with open(path, 'w') as f:
        f.write(' '.join(f'{n}[{w}]' for n, w in header) + '\n')
        for r in rows:
            f.write(' '.join(v if isinstance(v, str) else f'0x{v:0{(w + 3) // 4}x}' for v, (n, w) in zip(r, header)) + '\n')


def alucontrol(aluop, f3, f7b5):
    if aluop & 2 == 0:
        return 0
    alt = f7b5 & 1 if (aluop & 1) == 0 or f3 == 5 else 0
    return (alt << 3) | f3


def branch(a, b, f3, br):
    kind = f3 >> 1
    c = [a == b, False, sx(a, 32) < sx(b, 32), a < b][kind]
    return int(bool(br) and (c ^ bool(f3 & 1)))


def immgen(ins, sel):
    if sel == 0:
        return sx(ins >> 20, 12) & M
    if sel == 1:
        return sx(((ins >> 25) << 5) | ((ins >> 7) & 31), 12) & M
    if sel == 2:
        return sx((((ins >> 31) & 1) << 12) | (((ins >> 7) & 1) << 11) | (((ins >> 25) & 0x3F) << 5) |
                  (((ins >> 8) & 0xF) << 1), 13) & M
    if sel == 3:
        return ins & 0xFFFFF000
    if sel == 4:
        return sx((((ins >> 31) & 1) << 20) | (((ins >> 12) & 0xFF) << 12) | (((ins >> 20) & 1) << 11) |
                  (((ins >> 21) & 0x3FF) << 1), 21) & M
    return 0


CLS = {0b00000: 'LOAD', 0b00100: 'OPIMM', 0b00101: 'AUIPC', 0b01000: 'STORE', 0b01100: 'OP', 0b01101: 'LUI',
       0b11000: 'BRANCH', 0b11001: 'JALR', 0b11011: 'JAL', 0b11100: 'SYSTEM'}


def control(ins):
    import modules
    out = {'rd': (ins >> 7) & 31, 'rs1': (ins >> 15) & 31, 'rs2': (ins >> 20) & 31, 'funct3': (ins >> 12) & 7,
           'f7b5': (ins >> 30) & 1}
    cls = CLS.get((ins >> 2) & 31) if ins & 3 == 3 else None
    bits = {name: int(cls in terms) for name, terms in modules.CTRL_BITS}
    for name, w in modules.CTRL_OUTS:
        if name in out:
            continue
        if name in modules.MULTI:
            out[name] = sum(bits[f'{name}{i}'] << i for i in range(modules.MULTI[name]))
        else:
            out[name] = bits[name]
    return out


def storeunit(old, wd, off, f3):
    sz = f3 & 3
    mask = [0xFF, 0xFFFF, M, M][sz]
    sh = off * 8
    Mk = (mask << sh) & M
    return ((old & ~Mk) | ((wd << sh) & Mk)) & M


def loadunit(word, off, f3):
    s = word >> (off * 8)
    return {0: sx(s, 8) & M, 1: sx(s, 16) & M, 4: s & 0xFF, 5: s & 0xFFFF}.get(f3, word)


def forward(rs1, rs2, mrd, mwe, wrd, wwe):
    def f(rs):
        m = mwe and mrd != 0 and mrd == rs
        w = wwe and wrd != 0 and wrd == rs
        return 1 if m else (2 if w else 0)
    return f(rs1), f(rs2)


def hazard(rs1, rs2, u1, u2, dh, erd, emr, red):
    lu = int(bool(emr and erd != 0 and ((erd == rs1 and u1) or (erd == rs2 and u2))))
    stall = lu | dh
    pcw = int((not stall) or red)
    return pcw, pcw, red, int(red or lu), stall, lu


def idbypass(rd1, rd2, rs1, rs2, wrd, wwe, wd):
    o1 = wd if (wwe and wrd and wrd == rs1) else rd1
    o2 = wd if (wwe and wrd and wrd == rs2) else rd2
    return o1, o2
