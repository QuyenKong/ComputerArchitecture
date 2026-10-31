"""modules.py - every building block of the RV32I CPUs as a Logisim sub-circuit.

Each builder returns a lgen.Circuit with a custom symbol (box) so that the top-level
CPU drawings stay clean.  Signal naming follows the textbook (Patterson & Hennessy,
RISC-V edition) where possible.
"""
from lgen import Circuit, Port

C_DATA = '#dbeafe'    # datapath blocks
C_CTRL = '#ffedd5'    # control blocks
C_STATE = '#dcfce7'   # state (registers)
C_MEM = '#ede9fe'     # memory interface
C_PIPE = '#fef9c3'    # pipeline registers
TXT = '#1e3a8a'       # annotation colour


def notes(c, x, y, lines, size=11, color=TXT, dy=16, bold_first=True, family='SansSerif'):
    for i, l in enumerate(lines):
        c.text(x, y + i * dy, l, size=size + (1 if (i == 0 and bold_first) else 0),
               bold=(i == 0 and bold_first), color=color, family=family if i else 'SansSerif')


def inputs(c, specs, x=120, y=100, dy=40, stub=30):
    """Input pins in a column; each drives a tunnel with the same name."""
    ports = {}
    for i, (name, w) in enumerate(specs):
        p = c.pin_in(name, w, x, y + i * dy)
        c.tun(p, name, stub)
        ports[name] = p
    return ports


def outputs(c, specs, x, y=100, dy=40, stub=30):
    ports = {}
    for i, (name, w) in enumerate(specs):
        p = c.pin_out(name, w, x, y + i * dy)
        c.tun(p, name, stub)
        ports[name] = p
    return ports


# ---------------------------------------------------------------------------
# ALU
# ---------------------------------------------------------------------------
def build_alu():
    c = Circuit('ALU')
    inputs(c, [('A', 32), ('B', 32), ('ALUCtrl', 4)], x=120, y=120, dy=50)
    notes(c, 60, 40, ['ALU 32-bit  (Arithmetic Logic Unit)',
                      'ALUCtrl = {bit30, funct3}: ma hoa trung voi funct3 cua RISC-V -> ALUControl gan nhu chi la "noi day"'])
    # control splitter: ALUCtrl[2:0] = op (chon ket qua), ALUCtrl[3] = alt (SUB / SRA)
    sp = c.splitter(160, 330, 4, [(0, 2), (3, 3)], appear='right')
    c.tun(sp.p(0), 'ALUCtrl', 20)
    c.tun(sp.p(1), 'op', 20)
    c.tun(sp.p(2), 'alt', 20)
    c.text(120, 300, 'tach ALUCtrl', size=10, color=TXT)
    # shift amount = B[4:0] (RV32I chi dich 0..31)
    ss = c.splitter(160, 420, 32, [(0, 4)], appear='right')
    c.tun(ss.p(0), 'B', 20)
    c.tun(ss.p(1), 'shamt', 20)
    c.text(120, 400, 'shamt = B[4:0]', size=10, color=TXT)

    # functional units, one per row (output at x=UX)
    UX, Y0, DY = 560, 120, 70
    rows = {}
    order = [('add', 'Adder', {}), ('sub', 'Subtractor', {}),
             ('slt', 'Comparator', {'mode': 'twosComplement'}), ('sltu', 'Comparator', {'mode': 'unsigned'}),
             ('xor', 'XOR Gate', {'size': 30, 'inputs': 2}), ('or', 'OR Gate', {'size': 30, 'inputs': 2}),
             ('and', 'AND Gate', {'size': 30, 'inputs': 2}),
             ('sll', 'Shifter', {'shift': 'll'}), ('srl', 'Shifter', {'shift': 'lr'}),
             ('sra', 'Shifter', {'shift': 'ar'})]
    a_taps, b_taps, s_taps = [], [], []
    AX, BX = 380, 410
    for i, (nm, comp, at) in enumerate(order):
        y = Y0 + i * DY
        ux = UX if comp not in ('XOR Gate',) else UX + 10   # XOR symbol is 10px wider
        u = c.add(comp, ux, y, width=32, **at)
        pa, pb = u.p(0) if comp not in ('XOR Gate', 'OR Gate', 'AND Gate') else u.p(1), \
                 u.p(1) if comp not in ('XOR Gate', 'OR Gate', 'AND Gate') else u.p(2)
        c.path((AX, pa.y), pa)
        a_taps.append(pa.y)
        if comp == 'Shifter':
            c.path((BX, pb.y), pb)
            s_taps.append(pb.y)
        else:
            c.path((BX, pb.y), pb)
            b_taps.append(pb.y)
        if comp == 'Comparator':
            # '<' output is 1 bit -> zero-extend to 32 bit (SLT gives 0 or 1)
            ext = c.add('Bit Extender', ux + 60, y + 10, in_width=1, out_width=32, type='zero')
            c.wire(u.p(4), ext.p(1))
            rows[nm] = ext.p(0)
        elif comp in ('XOR Gate', 'OR Gate', 'AND Gate'):
            rows[nm] = u.p(0)
        elif comp in ('Adder', 'Subtractor'):
            rows[nm] = u.p(2)
        else:
            rows[nm] = u.p(2)
        if comp in ('Adder', 'Subtractor'):
            c.const(u.p(3), 0, 1, length=10)          # carry/borrow-in = 0
        c.text(ux + 8, y - 14, nm.upper(), size=10, bold=True, color='#7c2d12')
    # bus bars: A over all rows, B over arithmetic/logic rows, shamt over shifter rows
    c.bus_v(AX, [100] + a_taps)
    c.tun(Port(AX, 100, 32, 'N', 'i'), 'A', 20)
    c.bus_v(BX, [100] + b_taps)
    c.tun(Port(BX, 100, 32, 'N', 'i'), 'B', 20)
    sh_top = s_taps[0] - 30
    c.bus_v(BX, [sh_top] + s_taps)
    c.tun(Port(BX, sh_top, 5, 'W', 'i'), 'shamt', 20)

    # 2:1 muxes: ADD/SUB and SRL/SRA chosen by 'alt' (= instr bit 30)
    MX = 720
    m_as = c.add('Multiplexer', MX, rows['add'].y + 40, width=32, select=1, enable='false')
    c.path(rows['add'], (MX - 60, rows['add'].y), (MX - 60, m_as.p(0).y), m_as.p(0))
    c.path(rows['sub'], (MX - 50, rows['sub'].y), (MX - 50, m_as.p(1).y), m_as.p(1))
    c.tun(m_as.p(2), 'alt', 20)
    m_sh = c.add('Multiplexer', MX, rows['srl'].y + 40, width=32, select=1, enable='false')
    c.path(rows['srl'], (MX - 60, rows['srl'].y), (MX - 60, m_sh.p(0).y), m_sh.p(0))
    c.path(rows['sra'], (MX - 50, rows['sra'].y), (MX - 50, m_sh.p(1).y), m_sh.p(1))
    c.tun(m_sh.p(2), 'alt', 20)
    c.text(MX - 70, rows['add'].y - 20, 'alt=0: ADD  alt=1: SUB', size=10, color=TXT)
    c.text(MX - 70, rows['sra'].y + 70, 'alt=0: SRL  alt=1: SRA', size=10, color=TXT)

    # 8:1 result mux, input index == funct3
    RX = 960
    srcs = [m_as.p(3), rows['sll'], rows['slt'], rows['sltu'], rows['xor'], m_sh.p(3), rows['or'], rows['and']]
    mid = (Y0 + 9 * DY) // 2
    my = c.pick_y([s.y for s in srcs], -40, (mid // 10) * 10)
    mres = c.add('Multiplexer', RX, my, width=32, select=3, enable='false')
    c.fan_in([(s, mres.p(i)) for i, s in enumerate(srcs)], RX - 70)
    c.tun(mres.p(8), 'op', 20)
    for i, nm in enumerate(['0 ADD/SUB', '1 SLL', '2 SLT', '3 SLTU', '4 XOR', '5 SRL/SRA', '6 OR', '7 AND']):
        c.text(RX + 20, mres.p(0).y - 70 + i * 14, f'op={nm}', size=10, color=TXT)
    c.wire(mres.p(9), (RX + 120, mres.p(9).y))
    y_out = mres.p(9).y
    py = c.pin_out('Y', 32, RX + 120, y_out)
    c.box(110, 120, left=[('A', 30), ('B', 90)], right=[('Y', 60)], bottom=[('ALUCtrl', 60)],
          title='ALU', fill=C_DATA,
          shape=[(0, 0), (110, 30), (110, 90), (0, 120), (0, 70), (20, 60), (0, 50)])
    return c


# ---------------------------------------------------------------------------
# ALU Control
# ---------------------------------------------------------------------------
def build_alucontrol():
    c = Circuit('ALUControl')
    notes(c, 60, 40, ['ALU Control: (ALUOp, funct3, bit30) -> ALUCtrl[3:0] = {alt, op}',
                      'ALUOp 00: ADD (load/store/branch/jump/lui/auipc)   10: R-type   11: I-type',
                      'R-type: alt = bit30 (SUB/SRA).  I-type: alt = bit30 CHI KHI funct3=101 (SRAI);',
                      'voi ADDI bit30 la mot phan cua immediate nen phai bo qua (khong co SUBI).'], bold_first=True)
    inputs(c, [('ALUOp', 2), ('funct3', 3), ('f7b5', 1)], x=120, y=140, dy=50)
    sp = c.splitter(170, 330, 2, [(0, 0), (1, 1)])
    c.tun(sp.p(0), 'ALUOp', 20)
    c.tun(sp.p(1), 'aluop0', 20)
    c.tun(sp.p(2), 'aluop1', 40)
    # op = ALUOp[1] ? funct3 : 000
    m = c.add('Multiplexer', 440, 160, width=3, select=1, enable='false')
    c.const(m.p(0), 0, 3, 30)
    c.tun(m.p(1), 'funct3', 30)
    c.tun(m.p(2), 'aluop1', 20)
    c.tun(m.p(3), 'op', 30)
    c.text(360, 120, 'op = ALUOp[1] ? funct3 : 000', size=10, color=TXT)
    # is101 = (funct3 == 5)
    cmpc = c.add('Comparator', 440, 280, width=3, mode='unsigned')
    c.tun(cmpc.p(0), 'funct3', 30)
    c.const(cmpc.p(1), 5, 3, 30)
    c.text(360, 245, 'funct3 == 101 ?', size=10, color=TXT)
    # t = !ALUOp[0] | is101
    org = c.add('OR Gate', 560, 300, width=1, size=30, inputs=2, negate0='true')
    c.tun(org.p(1), 'aluop0', 30)
    c.wire(cmpc.p(3), org.p(2), mid=500)
    # alt = ALUOp[1] & f7b5 & t
    ag = c.add('AND Gate', 680, 260, width=1, size=30, inputs=3)
    c.tun(ag.p(1), 'aluop1', 30)
    c.tun(ag.p(2), 'f7b5', 60)
    c.wire(org.p(0), ag.p(3), mid=620)
    c.tun(ag.p(0), 'alt', 30)
    # ALUCtrl = {alt, op}
    cm = c.splitter(840, 220, 4, [(0, 2), (3, 3)], facing='west', appear='left')
    c.tun(cm.p(1), 'op', 30)
    c.tun(cm.p(2), 'alt', 30)
    po = c.pin_out('ALUCtrl', 4, 920, 220)
    c.wire(cm.p(0), po)
    c.box(110, 90, left=[('ALUOp', 20), ('funct3', 40), ('f7b5', 60)], right=[('ALUCtrl', 40)],
          title='ALU Ctrl', fill=C_CTRL, title_pos='bottom')
    return c


# ---------------------------------------------------------------------------
# Branch unit (branch comparator)
# ---------------------------------------------------------------------------
def build_branch():
    c = Circuit('BranchUnit')
    notes(c, 60, 40, ['Branch Unit: quyet dinh re nhanh (BEQ BNE BLT BGE BLTU BGEU)',
                      'funct3[2:1] chon phep so sanh: 00 = (A==B), 10 = A<B co dau, 11 = A<B khong dau',
                      'funct3[0] = 1 dao nguoc ket qua: BNE = !BEQ, BGE = !BLT, BGEU = !BLTU',
                      'Taken = Branch AND cond'])
    inputs(c, [('A', 32), ('B', 32), ('funct3', 3), ('Branch', 1)], x=120, y=140, dy=50)
    cu = c.add('Comparator', 420, 160, width=32, mode='unsigned')
    cs = c.add('Comparator', 420, 260, width=32, mode='twosComplement')
    for cc in (cu, cs):
        c.tun(cc.p(0), 'A', 30)
        c.tun(cc.p(1), 'B', 30)
    c.text(360, 125, 'unsigned', size=10, color=TXT)
    c.text(360, 225, 'signed (bu 2)', size=10, color=TXT)
    fs = c.splitter(170, 400, 3, [(0, 0), (1, 2)])
    c.tun(fs.p(0), 'funct3', 20)
    c.tun(fs.p(1), 'inv', 20)
    c.tun(fs.p(2), 'kind', 40)
    m = c.add('Multiplexer', 560, 220, width=1, select=2, enable='false')
    c.wire(cu.p(3), m.p(0), mid=470)          # 00: equal
    c.const(m.p(1), 0, 1, 20)                 # 01: unused
    c.wire(cs.p(4), m.p(2), mid=490)          # 10: signed less-than
    c.tun(cu.p(4), 'ltu', 20)
    c.tun(m.p(3), 'ltu', 20)
    c.tun(m.p(4), 'kind', 20)
    x = c.add('XOR Gate', 680, 230, width=1, size=30, inputs=2)
    c.wire(m.p(5), x.p(1))
    c.tun(x.p(2), 'inv', 20)
    a = c.add('AND Gate', 780, 240, width=1, size=30, inputs=2)
    c.wire(x.p(0), a.p(1), mid=720)
    c.tun(a.p(2), 'Branch', 20)
    po = c.pin_out('Taken', 1, 880, 240)
    c.wire(a.p(0), po)
    c.box(110, 100, left=[('A', 20), ('B', 40), ('funct3', 60), ('Branch', 80)], right=[('Taken', 50)],
          title='Branch', fill=C_CTRL, title_pos='bottom', label_size=9)
    return c


# ---------------------------------------------------------------------------
# Immediate generator
# ---------------------------------------------------------------------------
IMM_FIELDS = [('i7', 7, 7), ('i11_8', 8, 11), ('i14_12', 12, 14), ('i19_15', 15, 19), ('i20', 20, 20),
              ('i24_21', 21, 24), ('i30_25', 25, 30), ('i31', 31, 31)]


def build_immgen():
    c = Circuit('ImmGen')
    notes(c, 60, 40, ['Immediate Generator: ghep cac manh bit cua lenh thanh hang so 32-bit (sign-extend)',
                      'RISC-V co tinh "xao tron" bit cua B/J-type de bit dau (inst[31]) luon la bit dau cua imm',
                      'va cac manh bit nam o cung vi tri giua cac dang lenh -> phan cung chi can noi day + MUX.',
                      'ImmSel: 0=I  1=S  2=B  3=U  4=J'])
    inputs(c, [('Instr', 32), ('ImmSel', 3)], x=120, y=140, dy=60)
    # field splitter
    sp = c.splitter(220, 230, 32, [(lo, hi) for _, lo, hi in IMM_FIELDS], appear='right', spacing=2)
    c.tun(sp.p(0), 'Instr', 20)
    for i, (nm, lo, hi) in enumerate(IMM_FIELDS):
        c.tun(sp.p(i + 1), nm, 20)
        c.text(sp.p(i + 1).x + 75, sp.p(i + 1).y + 4, f'inst[{hi}:{lo}]' if hi != lo else f'inst[{hi}]', size=9, color=TXT)
    formats = [  # name, total bits, parts low->high: (tunnel or ('0', width)), extend
        ('I', 12, ['i20', 'i24_21', 'i30_25', 'i31'], 'sign'),
        ('S', 12, ['i7', 'i11_8', 'i30_25', 'i31'], 'sign'),
        ('B', 13, [('0', 1), 'i11_8', 'i30_25', 'i7', 'i31'], 'sign'),
        ('U', 32, [('0', 12), 'i14_12', 'i19_15', 'i20', 'i24_21', 'i30_25', 'i31'], None),
        ('J', 21, [('0', 1), 'i24_21', 'i30_25', 'i20', 'i14_12', 'i19_15', 'i31'], 'sign'),
    ]
    widths = {nm: hi - lo + 1 for nm, lo, hi in IMM_FIELDS}
    outs = []
    CX, Y = 640, 150
    for fname, total, parts, ext in formats:
        groups, b = [], 0
        for p in parts:
            w = p[1] if isinstance(p, tuple) else widths[p]
            groups.append((b, b + w - 1))
            b += w
        assert b == total, (fname, b)
        n = len(parts)
        cm = c.splitter(CX, Y + 20 * n, total, groups, facing='west', appear='left', spacing=2)
        for i, p in enumerate(parts):
            port = cm.p(i + 1)
            if isinstance(p, tuple):
                c.const(port, 0, p[1], 30)
            else:
                c.tun(port, p, 30)
        if ext:
            e = c.add('Bit Extender', CX + 80, cm.p(0).y, in_width=total, out_width=32, type='sign')
            c.wire(cm.p(0), e.p(1))
            outs.append(e.p(0))
        else:
            outs.append(cm.p(0))
        c.text(CX - 200, cm.p(1).y + 4, f'{fname}-type  imm[{total - 1}:0]', size=11, bold=True, color='#7c2d12')
        Y += 20 * n + 50
    ys = [o.y for o in outs]
    guess = (ys[0] + ys[-1]) // 20 * 10
    my = None
    for d in range(0, 400, 10):
        for yy in (guess + d, guess - d):
            dst = [yy - 40 + 10 * i for i in range(5)]
            if all(ys[i] != dst[j] for i in range(5) for j in range(5) if i != j):
                my = yy
                break
        if my is not None:
            break
    MX = 1000
    m = c.add('Multiplexer', MX, my, width=32, select=3, enable='false')
    c.fan_in([(o, m.p(i)) for i, o in enumerate(outs)], MX - 70)
    # inputs 5..7 unused -> tie to 0 through a small bus bar
    bx = MX - 50
    c.bus_v(bx, [m.p(5).y, m.p(6).y, m.p(7).y])
    for i in (5, 6, 7):
        c.path((bx, m.p(i).y), m.p(i))
    c.const(Port(bx, m.p(6).y, 32, 'W', 'i'), 0, 32, 10)
    c.tun(m.p(8), 'ImmSel', 20)
    c.text(MX + 20, m.p(0).y - 30, 'ImmSel: 0=I 1=S 2=B 3=U 4=J', size=10, color=TXT)
    po = c.pin_out('Imm', 32, MX + 100, my)
    c.wire(m.p(9), po)
    c.box(110, 60, left=[('Instr', 20), ('ImmSel', 40)], right=[('Imm', 30)], title='ImmGen', fill=C_DATA,
          title_pos='bottom', label_size=9)
    return c


# ---------------------------------------------------------------------------
# Main control (instruction decoder) - drawn as a PLA: one-hot decoder + OR plane
# ---------------------------------------------------------------------------
CLASSES = [('LOAD', 0b00000), ('OPIMM', 0b00100), ('AUIPC', 0b00101), ('STORE', 0b01000), ('OP', 0b01100),
           ('LUI', 0b01101), ('BRANCH', 0b11000), ('JALR', 0b11001), ('JAL', 0b11011), ('SYSTEM', 0b11100)]
CTRL_BITS = [
    ('RegWrite', ['OP', 'OPIMM', 'LOAD', 'JAL', 'JALR', 'LUI', 'AUIPC']),
    ('ASel0', ['BRANCH', 'JAL', 'AUIPC']), ('ASel1', ['LUI']),
    ('BSel', ['OPIMM', 'LOAD', 'STORE', 'BRANCH', 'JAL', 'JALR', 'LUI', 'AUIPC']),
    ('ALUOp0', ['OPIMM']), ('ALUOp1', ['OP', 'OPIMM']),
    ('ImmSel0', ['STORE', 'LUI', 'AUIPC']), ('ImmSel1', ['BRANCH', 'LUI', 'AUIPC']), ('ImmSel2', ['JAL']),
    ('MemRead', ['LOAD']), ('MemWrite', ['STORE']),
    ('WBSel0', ['LOAD']), ('WBSel1', ['JAL', 'JALR']),
    ('Branch', ['BRANCH']), ('Jal', ['JAL']), ('Jalr', ['JALR']), ('Halt', ['SYSTEM']),
    ('UseRs1', ['OP', 'OPIMM', 'LOAD', 'STORE', 'BRANCH', 'JALR']), ('UseRs2', ['OP', 'STORE', 'BRANCH']),
]
CTRL_OUTS = [('rd', 5), ('rs1', 5), ('rs2', 5), ('funct3', 3), ('f7b5', 1), ('RegWrite', 1), ('ASel', 2),
             ('BSel', 1), ('ALUOp', 2), ('ImmSel', 3), ('MemRead', 1), ('MemWrite', 1), ('WBSel', 2),
             ('Branch', 1), ('Jal', 1), ('Jalr', 1), ('Halt', 1), ('UseRs1', 1), ('UseRs2', 1)]
MULTI = {'ASel': 2, 'ALUOp': 2, 'ImmSel': 3, 'WBSel': 2}


def build_control():
    c = Circuit('Control')
    notes(c, 60, 40, ['Control Unit (Main Decoder) - ve theo kieu PLA:',
                      '1) Decoder 5->32 bien opcode[6:2] thanh 1 duong "one-hot" cho moi nhom lenh (chi bat khi opcode[1:0]=11)',
                      '2) Moi tin hieu dieu khien = OR cua cac nhom lenh can no (cot doc = nhom lenh, cham tron = co noi)',
                      'Lenh = 0x00000000 (bubble) -> opcode[1:0]=00 -> decoder tat -> moi tin hieu = 0 = NOP'])
    pin = c.pin_in('Instr', 32, 120, 140)
    c.tun(pin, 'Instr', 30)
    groups = [(0, 0), (1, 1), (2, 6), (7, 11), (12, 14), (15, 19), (20, 24), (30, 30)]
    gnames = ['q0', 'q1', 'opc', 'rd', 'funct3', 'rs1', 'rs2', 'f7b5']
    sp = c.splitter(200, 220, 32, groups, appear='right', spacing=2)
    c.tun(sp.p(0), 'Instr', 20)
    for i, g in enumerate(gnames):
        c.tun(sp.p(i + 1), g, 20)
    c.text(140, 210, 'tach truong lenh', size=10, color=TXT)
    va = c.add('AND Gate', 200, 440, width=1, size=30, inputs=2)
    c.tun(va.p(1), 'q0', 20)
    c.tun(va.p(2), 'q1', 50)
    c.tun(va.p(0), 'valid', 20)
    c.text(110, 410, 'valid = opcode[1:0]==11', size=10, color=TXT)

    DX, DY = 340, 640
    dec = c.add('Decoder', DX, DY, select=5, enable='true')
    c.tun(dec.p(32), 'opc', 20)
    c.path(dec.p(33), (DX - 10, DY + 20), (DX - 40, DY + 20))
    c.tun(Port(DX - 40, DY + 20, 1, 'W', 'i'), 'valid', 20)
    c.text(DX - 30, DY - 340, 'opcode[6:2]', size=10, color=TXT)
    # bars: lowest opcode index -> rightmost column so the drawing has no crossings
    BAR0 = 480
    ncls = len(CLASSES)
    barx = {nm: BAR0 + 40 * (ncls - 1 - k) for k, (nm, _) in enumerate(CLASSES)}
    bar_top = {}
    for nm, idx in CLASSES:
        p = dec.p(idx)
        c.path(p, (barx[nm], p.y))
        bar_top[nm] = p.y
        c.text(barx[nm] + 3, p.y - 3, nm, size=9, bold=True, color='#7c2d12')
    taps = {nm: [bar_top[nm]] for nm, _ in CLASSES}
    GX = BAR0 + 40 * ncls + 80          # OR gate output x
    y = DY + 60
    outx = GX
    for name, terms in CTRL_BITS:
        if len(terms) == 1:
            y += 10
            c.path((barx[terms[0]], y), (outx, y))
            taps[terms[0]].append(y)
            c.tun(Port(outx, y, 1, 'E', 'o'), name, 20)
            y += 20
            continue
        n = len(terms)
        size = 30 if n <= 3 else 50
        g = c.add('OR Gate', GX, 0, width=1, size=size, inputs=n)
        bx, by, bw, bh = g.bounds()
        c.comps.remove(g)
        gy = y - by + 5
        gy = (gy + 9) // 10 * 10
        g = c.add('OR Gate', GX, gy, width=1, size=size, inputs=n)
        for i, t in enumerate(terms):
            pi = g.p(i + 1)
            c.path((barx[t], pi.y), pi)
            taps[t].append(pi.y)
        c.tun(g.p(0), name, 20)
        y = (g.bounds()[1] + g.bounds()[3] + 20 + 9) // 10 * 10
    for nm, _ in CLASSES:
        c.bus_v(barx[nm], taps[nm])
    # output section
    OX = GX + 380
    oy = 140
    for name, w in CTRL_OUTS:
        po = c.pin_out(name, w, OX, oy)
        if name in MULTI:
            n = MULTI[name]
            cm = c.splitter(OX - 60, oy, n, [(i, i) for i in range(n)], facing='west', appear='left', spacing=2)
            c.wire(cm.p(0), po)
            for i in range(n):
                c.tun(cm.p(i + 1), f'{name}{i}', 20)
            oy += 40 + 20 * n
        else:
            c.tun(po, name, 30)
            oy += 40
    right = [(nm, 20 + 20 * i) for i, (nm, _) in enumerate(CTRL_OUTS)]
    c.box(120, 20 + 20 * len(CTRL_OUTS), left=[('Instr', 20)], right=right, title='Control',
          fill=C_CTRL, title_pos='center', label_size=9)
    # truth table as text
    tx = OX + 160
    notes(c, tx, 140, ['Bang chan ly (1 = bat):',
                       'nhom     opcode  RegW ASel BSel ALUOp ImmSel MemR MemW WBSel',
                       'OP       0110011  1    00   0    10    -      0    0    00',
                       'OP-IMM   0010011  1    00   1    11    I      0    0    00',
                       'LOAD     0000011  1    00   1    00    I      1    0    01',
                       'STORE    0100011  0    00   1    00    S      0    1    --',
                       'BRANCH   1100011  0    01   1    00    B      0    0    --',
                       'JAL      1101111  1    01   1    00    J      0    0    10',
                       'JALR     1100111  1    00   1    00    I      0    0    10',
                       'LUI      0110111  1    10   1    00    U      0    0    00',
                       'AUIPC    0010111  1    01   1    00    U      0    0    00',
                       'SYSTEM   1110011  0  (Halt = 1: ECALL/EBREAK dung CPU)',
                       'ASel: 0=rs1 1=PC 2=0   WBSel: 0=ALU 1=Mem 2=PC+4',
                       'ImmSel: 0=I 1=S 2=B 3=U 4=J'], size=10, family='Monospaced')
    return c


# ---------------------------------------------------------------------------
# Register file: 31 x 32-bit registers (x0 is hard-wired to 0)
# ---------------------------------------------------------------------------
ABI = ['zero', 'ra', 'sp', 'gp', 'tp', 't0', 't1', 't2', 's0', 's1', 'a0', 'a1', 'a2', 'a3', 'a4', 'a5',
       'a6', 'a7', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 't3', 't4', 't5', 't6']


def build_regfile():
    c = Circuit('RegisterFile')
    notes(c, 60, 40, ['Register File 32 x 32-bit: 2 cong doc (to hop, khong can clock) + 1 cong ghi (canh len CLK)',
                      'Ghi: Decoder 5->32 bien WA thanh one-hot, AND voi WE -> chi 1 thanh ghi duoc bat Enable',
                      'Doc: 2 MUX 32->1 chon theo RA1/RA2.  x0 khong phai thanh ghi: dau vao 0 cua MUX noi hang so 0'])
    inputs(c, [('RA1', 5), ('RA2', 5), ('WA', 5), ('WD', 32), ('WE', 1), ('CLK', 1)], x=120, y=140, dy=50)
    DX, DY = 330, 800
    dec = c.add('Decoder', DX, DY, select=5, enable='true')
    c.tun(dec.p(32), 'WA', 20)
    c.path(dec.p(33), (DX - 10, DY + 20), (DX - 40, DY + 20))
    c.tun(Port(DX - 40, DY + 20, 1, 'W', 'i'), 'WE', 20)
    for k in range(1, 32):
        c.tun(dec.p(k), f'we{k}', 20 if k % 2 else 60)
    c.text(DX - 40, DY - 345, 'write decoder', size=10, color=TXT)
    GX, GY, CW, CH = 560, 130, 230, 140
    regs = {}
    for k in range(32):
        col, row = k // 8, k % 8
        x, y = GX + col * CW, GY + row * CH
        if k == 0:
            c.text(x - 20, y + 30, 'x0 (zero)', size=11, bold=True, color='#7c2d12')
            c.text(x - 20, y + 48, 'khong luu tru:', size=10, color=TXT)
            c.text(x - 20, y + 64, 'doc luon = 0', size=10, color=TXT)
            continue
        r = c.add('Register', x, y, width=32, appearance='logisim_evolution', label=f'x{k}_{ABI[k]}')
        regs[k] = r
        c.tun(r.p(1), 'WD', 20)
        c.tun(r.p(4), f'we{k}', 20)
        c.tun(r.p(2), 'CLK', 20)
        c.const(r.p(3), 0, 1, 10)
        c.tun(r.p(0), f'x{k}', 20)
    MX = GX + 4 * CW + 200
    for name, my, rd in (('RA1', 520, 'RD1'), ('RA2', 1000, 'RD2')):
        m = c.add('Multiplexer', MX, my, width=32, select=5, enable='false')
        c.const(m.p(0), 0, 32, 20)
        for k in range(1, 32):
            c.tun(m.p(k), f'x{k}', 20 if k % 2 == 0 else 70)
        c.tun(m.p(32), name, 20)
        po = c.pin_out(rd, 32, MX + 80, my)
        c.wire(m.p(33), po)
        c.text(MX - 30, my - 185, f'read port {rd[-1]}', size=11, bold=True, color='#7c2d12')
    # symbol: shows all 32 registers live (visible-register elements)
    vis = []
    for k in range(32):
        col, row = k // 16, k % 16
        vx, vy = 50 + 85 + col * 135, 50 + 34 + row * 20
        if k == 0:
            vis.append(f'<text dominant-baseline="central" font-family="monospaced" font-size="10" '
                       f'text-anchor="start" x="{vx - 2}" y="{vy}">00000000</text>')
            vis.append(f'<text dominant-baseline="central" font-family="SansSerif" font-size="8" '
                       f'text-anchor="end" x="{vx - 6}" y="{vy}">x0 zero</text>')
            continue
        r = regs[k]
        vis.append(f'<visible-register x="{vx}" y="{vy - 6}" label="left" font-family="SansSerif" font-size="8" '
                   f'path="/Register({r.x},{r.y})"/>')
    c.box(300, 380, left=[('RA1', 40), ('RA2', 80), ('WA', 160), ('WD', 200), ('WE', 240), ('CLK', 340)],
          right=[('RD1', 60), ('RD2', 120)], title='Register File', title_pos='top', fill=C_STATE,
          extra_svg=''.join(vis), label_size=9)
    return c


# ---------------------------------------------------------------------------
# Memory interface: address decoder (RAM / MMIO), store merge, load extract
# ---------------------------------------------------------------------------
def build_mmio():
    c = Circuit('AddrDecode')
    notes(c, 60, 40, ['Address Decoder (memory map):',
                      '0x0000_0000-0x0000_3FFF : RAM 16 KiB  -> word address = Addr[13:2] (4096 tu 32-bit)',
                      '0xF000_0000-0xFFFF_FFFF : I/O (TTY)   -> ghi 1 byte ra man hinh TTY',
                      'Addr[1:0] = byte offset trong 1 word (dung cho LB/LH/SB/SH)'])
    inputs(c, [('Addr', 32), ('MemWrite', 1)], x=120, y=140, dy=60)
    sp = c.splitter(220, 280, 32, [(0, 1), (2, 13), (28, 31)], spacing=2)
    c.tun(sp.p(0), 'Addr', 20)
    c.tun(sp.p(1), 'Off', 20)
    c.tun(sp.p(2), 'WordAddr', 20)
    c.tun(sp.p(3), 'top', 20)
    cmp_ = c.add('Comparator', 460, 300, width=4, mode='unsigned')
    c.tun(cmp_.p(0), 'top', 20)
    c.const(cmp_.p(1), 0xF, 4, 20)
    c.tun(cmp_.p(3), 'IsIO', 20)
    c.text(400, 270, 'Addr[31:28] == 0xF ?', size=10, color=TXT)
    a1 = c.add('AND Gate', 460, 420, width=1, size=30, inputs=2, negate1='true')
    c.tun(a1.p(1), 'MemWrite', 20)
    c.tun(a1.p(2), 'IsIO', 10)
    c.tun(a1.p(0), 'RamWE', 20)
    a2 = c.add('AND Gate', 460, 500, width=1, size=30, inputs=2)
    c.tun(a2.p(1), 'MemWrite', 20)
    c.tun(a2.p(2), 'IsIO', 20)
    c.tun(a2.p(0), 'IoWE', 20)
    outputs(c, [('WordAddr', 12), ('Off', 2), ('RamWE', 1), ('IoWE', 1), ('IsIO', 1)], x=700, y=140, dy=50)
    c.box(110, 120, left=[('Addr', 30), ('MemWrite', 70)],
          right=[('WordAddr', 20), ('Off', 40), ('RamWE', 60), ('IoWE', 80), ('IsIO', 100)], title='AddrDec',
          fill=C_MEM, title_pos='bottom', label_size=9)
    return c


def _shamt8(c, x, y):
    """{Off, 000}: byte offset * 8 = shift amount (5 bit)"""
    cm = c.splitter(x, y, 5, [(0, 2), (3, 4)], facing='west', appear='left', spacing=2)
    c.const(cm.p(1), 0, 3, 20)
    c.tun(cm.p(2), 'Off', 20)
    c.tun(cm.p(0), 'sh', 20)
    c.text(x - 110, y - 60, 'sh = Off * 8 = {Off,000}', size=10, color=TXT)


def build_storeunit():
    c = Circuit('StoreUnit')
    notes(c, 60, 40, ['Store Unit (read-modify-write): RAM chi ghi duoc ca word 32-bit,',
                      'nen voi SB/SH ta doc word cu (Old), thay dung byte/halfword roi ghi lai ca word.',
                      'M = mask (0xFF / 0xFFFF / 0xFFFFFFFF) << sh ;  New = (Old AND ~M) OR ((WData << sh) AND M)'])
    inputs(c, [('Old', 32), ('WData', 32), ('Off', 2), ('funct3', 3)], x=120, y=140, dy=50)
    _shamt8(c, 340, 400)
    fs = c.splitter(220, 460, 3, [(0, 1)])
    c.tun(fs.p(0), 'funct3', 20)
    c.tun(fs.p(1), 'size', 20)
    m = c.add('Multiplexer', 560, 200, width=32, select=2, enable='false')
    for i, v in enumerate([0xFF, 0xFFFF, 0xFFFFFFFF, 0xFFFFFFFF]):
        c.const(m.p(i), v, 32, 20 if i % 2 == 0 else 100)
    c.tun(m.p(4), 'size', 20)
    c.text(430, 150, 'size: 00=SB 01=SH 10=SW', size=10, color=TXT)
    s1 = c.add('Shifter', 680, 210, width=32, shift='ll')
    c.wire(m.p(5), s1.p(0), mid=620)
    c.tun(s1.p(1), 'sh', 20)
    c.tun(s1.p(2), 'M', 20)
    s2 = c.add('Shifter', 680, 330, width=32, shift='ll')
    c.tun(s2.p(0), 'WData', 20)
    c.tun(s2.p(1), 'sh', 20)
    c.tun(s2.p(2), 'D', 20)
    a1 = c.add('AND Gate', 900, 210, width=32, size=30, inputs=2, negate1='true')
    c.tun(a1.p(1), 'Old', 20)
    c.tun(a1.p(2), 'M', 10)
    a2 = c.add('AND Gate', 900, 310, width=32, size=30, inputs=2)
    c.tun(a2.p(1), 'D', 20)
    c.tun(a2.p(2), 'M', 20)
    o = c.add('OR Gate', 1000, 260, width=32, size=30, inputs=2)
    c.wire(a1.p(0), o.p(1), mid=940)
    c.wire(a2.p(0), o.p(2), mid=940)
    po = c.pin_out('New', 32, 1080, 260)
    c.wire(o.p(0), po)
    c.text(830, 180, 'Old AND ~M (giu byte khac)', size=10, color=TXT)
    c.text(830, 350, 'D AND M (byte moi)', size=10, color=TXT)
    c.box(110, 100, left=[('Old', 20), ('WData', 40), ('Off', 60), ('funct3', 80)], right=[('New', 50)],
          title='Store', fill=C_MEM, title_pos='bottom', label_size=9)
    return c


def build_loadunit():
    c = Circuit('LoadUnit')
    notes(c, 60, 40, ['Load Unit: lay byte/halfword tu word doc ra va mo rong dau (sign) hoac them 0 (zero)',
                      'Word >> (Off*8) dua byte can lay ve vi tri thap nhat;  funct3 chon: 000 LB, 001 LH, 010 LW, 100 LBU, 101 LHU'])
    inputs(c, [('Word', 32), ('Off', 2), ('funct3', 3)], x=120, y=140, dy=50)
    _shamt8(c, 340, 400)
    s = c.add('Shifter', 480, 200, width=32, shift='lr')
    c.tun(s.p(0), 'Word', 20)
    c.tun(s.p(1), 'sh', 20)
    c.tun(s.p(2), 'S', 20)
    exts = []
    Y = 160
    for nm, w, t in (('LB', 8, 'sign'), ('LH', 16, 'sign'), ('LBU', 8, 'zero'), ('LHU', 16, 'zero')):
        sp = c.splitter(600, Y, 32, [(0, w - 1)])
        c.tun(sp.p(0), 'S', 20)
        e = c.add('Bit Extender', 720, Y + 10, in_width=w, out_width=32, type=t)
        c.wire(sp.p(1), e.p(1))
        exts.append(e.p(0))
        c.text(640, Y - 8, f'{nm}: {t}-extend S[{w - 1}:0]', size=10, color=TXT)
        Y += 80
    MX = 920
    m = c.add('Multiplexer', MX, 0, width=32, select=3, enable='false')
    c.comps.remove(m)
    srcs = {0: exts[0], 1: exts[1], 4: exts[2], 5: exts[3]}
    ys = [srcs[i].y if i in srcs else None for i in range(8)]
    my = None
    for d in range(0, 300, 10):
        for yy in (300 + d, 300 - d):
            dst = [yy - 40 + 10 * i for i in range(8)]
            if all(ys[i] is None or ys[i] != dst[j] for i in range(8) for j in range(8) if i != j):
                my = yy
                break
        if my:
            break
    m = c.add('Multiplexer', MX, my, width=32, select=3, enable='false')
    c.fan_in([(srcs[i], m.p(i)) for i in srcs], MX - 80)
    # LW and unused codes -> the raw word
    bx = MX - 50
    c.bus_v(bx, [m.p(2).y, m.p(3).y, m.p(6).y, m.p(7).y])
    for i in (2, 3, 6, 7):
        c.path((bx, m.p(i).y), m.p(i))
    c.path((bx, m.p(7).y), (bx, m.p(7).y + 60))
    c.tun(Port(bx, m.p(7).y + 60, 32, 'S', 'i'), 'Word', 10)
    c.tun(m.p(8), 'funct3', 20)
    po = c.pin_out('Data', 32, MX + 100, my)
    c.wire(m.p(9), po)
    c.text(MX + 10, my - 60, 'funct3 = 010 (LW): Word', size=10, color=TXT)
    c.box(110, 80, left=[('Word', 20), ('Off', 40), ('funct3', 60)], right=[('Data', 40)],
          title='Load', fill=C_MEM, title_pos='bottom', label_size=9)
    return c


# ---------------------------------------------------------------------------
# Performance counters (cycle / retired instructions) -> CPI = cycles / instret
# ---------------------------------------------------------------------------
def build_counters():
    c = Circuit('PerfCounters')
    notes(c, 60, 40, ['Performance counters: cycles dem moi canh len CLK khi CPU dang chay (Run=1),',
                      'instret dem so lenh da hoan thanh (Retire=1).  CPI = cycles / instret'])
    inputs(c, [('CLK', 1), ('Run', 1), ('Retire', 1)], x=120, y=140, dy=50)
    for i, (nm, en) in enumerate((('cycles', 'Run'), ('instret', 'en_i'))):
        y = 140 + i * 180
        r = c.add('Register', 400, y, width=32, appearance='logisim_evolution', label=nm)
        a = c.add('Adder', 360, y + 30, width=32)
        c.const(a.p(1), 1, 32, 20)
        c.const(a.p(3), 0, 1, 10)
        c.wire(a.p(2), r.p(1))
        c.tun(a.p(0), nm, 20)
        c.tun(r.p(0), nm, 20)
        c.tun(r.p(4), en, 20)
        c.tun(r.p(2), 'CLK', 20)
        c.const(r.p(3), 0, 1, 10)
    g = c.add('AND Gate', 280, 520, width=1, size=30, inputs=2)
    c.tun(g.p(1), 'Run', 20)
    c.tun(g.p(2), 'Retire', 20)
    c.tun(g.p(0), 'en_i', 20)
    outputs(c, [('cycles', 32), ('instret', 32)], x=640, y=170, dy=60)
    c.box(110, 80, left=[('CLK', 20), ('Run', 40), ('Retire', 60)], right=[('cycles', 30), ('instret', 50)],
          title='Perf', fill=C_STATE, title_pos='bottom', label_size=9)
    return c


# ---------------------------------------------------------------------------
# Pipeline registers
# ---------------------------------------------------------------------------
PIPE_FIELDS = {
    'IF_ID': [('valid', 1), ('pc', 32), ('pc4', 32), ('instr', 32)],
    'ID_EX': [('valid', 1), ('pc', 32), ('pc4', 32), ('instr', 32), ('rs1d', 32), ('rs2d', 32), ('imm', 32),
              ('rs1', 5), ('rs2', 5), ('rd', 5), ('funct3', 3), ('ALUCtrl', 4), ('ASel', 2), ('BSel', 1),
              ('RegWrite', 1), ('MemRead', 1), ('MemWrite', 1), ('WBSel', 2), ('Branch', 1), ('Jal', 1),
              ('Jalr', 1), ('Halt', 1)],
    'EX_MEM': [('valid', 1), ('pc', 32), ('instr', 32), ('exres', 32), ('sdata', 32), ('rd', 5), ('funct3', 3),
               ('RegWrite', 1), ('MemRead', 1), ('MemWrite', 1), ('MemToReg', 1), ('Halt', 1)],
    'MEM_WB': [('valid', 1), ('pc', 32), ('instr', 32), ('exres', 32), ('mdata', 32), ('rd', 5),
               ('RegWrite', 1), ('MemToReg', 1), ('Halt', 1)],
}


def build_pipereg(name):
    fields = PIPE_FIELDS[name]
    c = Circuit(name, title=name.replace('_', '/'))
    notes(c, 60, 40, [f'Pipeline register {name.replace("_", "/")}: luu toan bo thong tin cua 1 lenh giua 2 tang',
                      'EN = 0  -> giu nguyen gia tri (stall).   FLUSH = 1 -> nap 0 (bien lenh thanh bubble/NOP)',
                      'Moi gia tri 0 = an toan: valid=0, instr=0 (khong phai lenh hop le), moi tin hieu dieu khien = 0',
                      'en_eff = EN OR FLUSH (flush phai thang duoc ca stall)'])
    for i, (nm, w) in enumerate((('CLK', 1), ('EN', 1), ('FLUSH', 1))):
        p = c.pin_in(nm, w, 120 + 140 * i, 150)
        c.tun(p, nm, 20)
    g = c.add('OR Gate', 600, 150, width=1, size=30, inputs=2)
    c.tun(g.p(1), 'EN', 20)
    c.tun(g.p(2), 'FLUSH', 20)
    c.tun(g.p(0), 'en', 20)
    Y0, DY = 240, 110
    for i, (nm, w) in enumerate(fields):
        y = Y0 + i * DY
        pi = c.pin_in('D_' + nm, w, 160, y)
        m = c.add('Multiplexer', 300, y + 10, width=w, select=1, enable='false')
        c.wire(pi, m.p(0))
        c.const(m.p(1), 0, w, 20)
        c.tun(m.p(2), 'FLUSH', 10)
        r = c.add('Register', 420, y - 20, width=w, appearance='logisim_evolution', label=nm)
        c.path(m.p(3), r.p(1)) if m.p(3).y == r.p(1).y else c.wire(m.p(3), r.p(1))
        c.tun(r.p(4), 'en', 20)
        c.tun(r.p(2), 'CLK', 20)
        c.const(r.p(3), 0, 1, 10)
        po = c.pin_out('Q_' + nm, w, 600, r.p(0).y)
        c.wire(r.p(0), po)
    W, top = 70, 40
    H = top + 20 * len(fields) + 50
    left = [('D_' + nm, top + 20 * i, False) for i, (nm, _) in enumerate(fields)]
    right = [('Q_' + nm, top + 20 * i, False) for i, (nm, _) in enumerate(fields)]
    labels = ''.join(f'<text dominant-baseline="central" font-family="SansSerif" font-size="9" text-anchor="middle" '
                     f'x="{50 + W // 2}" y="{50 + top + 20 * i}">{nm}</text>' for i, (nm, _) in enumerate(fields))
    labels += ''.join(f'<text dominant-baseline="central" font-family="SansSerif" font-size="8" text-anchor="middle" '
                      f'x="{50 + ox}" y="{50 + H - 10}">{t}</text>' for ox, t in ((10, 'clk'), (35, 'en'), (60, 'fl')))
    c.box(W, H, left=left, right=right, bottom=[('CLK', 10, False), ('EN', 30, False), ('FLUSH', 60, False)],
          title=name.replace('_', '/'), title_pos='top', fill=C_PIPE, extra_svg=labels, title_size=11)
    return c


def _ne0_eq(c, a, b, x, y, out):
    """out = (a == b) AND (a != 0) for 5-bit register numbers"""
    e = c.add('Comparator', x, y, width=5, mode='unsigned')
    c.tun(e.p(0), a, 20)
    c.tun(e.p(1), b, 20)
    z = c.add('Comparator', x, y + 70, width=5, mode='unsigned')
    c.tun(z.p(0), a, 20)
    c.const(z.p(1), 0, 5, 20)
    g = c.add('AND Gate', x + 100, y + 30, width=1, size=30, inputs=2)
    c.wire(e.p(3), g.p(1), mid=x + 40)
    c.wire(z.p(2), g.p(2), mid=x + 50)            # a > 0  <=>  a != 0
    c.tun(g.p(0), out, 20)


def build_forward():
    c = Circuit('ForwardUnit')
    notes(c, 60, 40, ['Forwarding Unit (bypass): lay ket qua chua kip ghi vao Register File',
                      'FwdA/FwdB: 00 = gia tri doc tu ID/EX,  01 = tu EX/MEM (lenh truoc 1 lenh),  10 = tu MEM/WB (truoc 2 lenh)',
                      'Dieu kien: lenh truoc co RegWrite=1, rd != 0 va rd == rs.  EX/MEM uu tien hon (moi hon).'])
    inputs(c, [('rs1', 5), ('rs2', 5), ('M_rd', 5), ('M_RegWrite', 1), ('W_rd', 5), ('W_RegWrite', 1)],
           x=120, y=140, dy=50)
    row = 140
    for opnd in ('1', '2'):
        for st in ('M', 'W'):
            _ne0_eq(c, f'{st}_rd', f'rs{opnd}', 400, row, f'{st}eq{opnd}')
            g = c.add('AND Gate', 620, row + 30, width=1, size=30, inputs=2)
            c.tun(g.p(1), f'{st}eq{opnd}', 20)
            c.tun(g.p(2), f'{st}_RegWrite', 20)
            c.tun(g.p(0), f'{st}hit{opnd}', 20)
            row += 140
    for i, (opnd, out) in enumerate((('1', 'FwdA'), ('2', 'FwdB'))):
        y = 160 + i * 160
        g = c.add('AND Gate', 860, y + 20, width=1, size=30, inputs=2, negate1='true')
        c.tun(g.p(1), f'Whit{opnd}', 20)
        c.tun(g.p(2), f'Mhit{opnd}', 10)
        cm = c.splitter(960, y + 30, 2, [(0, 0), (1, 1)], facing='west', appear='left', spacing=2)
        c.tun(cm.p(1), f'Mhit{opnd}', 20)
        c.wire(g.p(0), cm.p(2), mid=930)
        po = c.pin_out(out, 2, 1040, y + 30)
        c.wire(cm.p(0), po)
    c.text(820, 140, 'bit0 = MEM hit, bit1 = WB hit AND NOT MEM hit', size=10, color=TXT)
    c.box(120, 140, left=[('rs1', 20), ('rs2', 40), ('M_rd', 70), ('M_RegWrite', 90), ('W_rd', 110),
                          ('W_RegWrite', 130)], right=[('FwdA', 40), ('FwdB', 100)], title='Forward',
          fill=C_CTRL, title_pos='center', label_size=8, subtitle=None)
    return c


def build_hazard():
    c = Circuit('HazardUnit')
    notes(c, 60, 40, ['Hazard Detection Unit',
                      'Load-use: lenh o EX la LOAD (MemRead) va lenh o ID can doc dung thanh ghi do -> chen 1 bubble',
                      '  (forwarding khong cuu duoc vi du lieu load chi co o cuoi tang MEM)',
                      'Control hazard: branch/jump duoc giai quyet o EX; neu nhay (Redirect=1) -> xoa 2 lenh da nap sai (IF/ID, ID/EX)',
                      'Halt o ID: dung nap lenh, cho EBREAK chay toi WB (khi do moi lenh truoc da xong)'])
    inputs(c, [('rs1', 5), ('rs2', 5), ('UseRs1', 1), ('UseRs2', 1), ('D_Halt', 1), ('E_rd', 5),
               ('E_MemRead', 1), ('Redirect', 1)], x=120, y=140, dy=50)
    _ne0_eq(c, 'E_rd', 'rs1', 400, 140, 'h1')
    _ne0_eq(c, 'E_rd', 'rs2', 400, 300, 'h2')
    a1 = c.add('AND Gate', 640, 180, width=1, size=30, inputs=2)
    c.tun(a1.p(1), 'h1', 20)
    c.tun(a1.p(2), 'UseRs1', 20)
    a2 = c.add('AND Gate', 640, 340, width=1, size=30, inputs=2)
    c.tun(a2.p(1), 'h2', 20)
    c.tun(a2.p(2), 'UseRs2', 20)
    o = c.add('OR Gate', 740, 260, width=1, size=30, inputs=2)
    c.path(a1.p(0), (690, a1.p(0).y), (690, o.p(1).y), o.p(1))
    c.path(a2.p(0), (700, a2.p(0).y), (700, o.p(2).y), o.p(2))
    lu = c.add('AND Gate', 840, 270, width=1, size=30, inputs=2)
    c.wire(o.p(0), lu.p(1), mid=780)
    c.tun(lu.p(2), 'E_MemRead', 20)
    c.tun(lu.p(0), 'LoadUse', 20)
    c.text(780, 230, 'LoadUse', size=10, bold=True, color='#7c2d12')
    s = c.add('OR Gate', 640, 480, width=1, size=30, inputs=2)
    c.tun(s.p(1), 'LoadUse', 20)
    c.tun(s.p(2), 'D_Halt', 20)
    c.tun(s.p(0), 'Stall', 20)
    w = c.add('OR Gate', 640, 560, width=1, size=30, inputs=2, negate0='true')
    c.tun(w.p(1), 'Stall', 20)
    c.tun(w.p(2), 'Redirect', 20)
    c.tun(w.p(0), 'PCWrite', 20)
    c.text(520, 600, 'PCWrite = IFID_Write = !Stall | Redirect', size=10, color=TXT)
    f = c.add('OR Gate', 640, 650, width=1, size=30, inputs=2)
    c.tun(f.p(1), 'Redirect', 20)
    c.tun(f.p(2), 'LoadUse', 20)
    c.tun(f.p(0), 'IDEX_Flush', 20)
    c.text(520, 690, 'IDEX_Flush = Redirect | LoadUse (chen bubble)', size=10, color=TXT)
    outs = [('PCWrite', 1), ('IFID_Write', 1), ('IFID_Flush', 1), ('IDEX_Flush', 1), ('Stall', 1), ('LoadUse', 1)]
    for i, (nm, wd) in enumerate(outs):
        po = c.pin_out(nm, wd, 1040, 160 + 50 * i)
        src = {'IFID_Write': 'PCWrite', 'IFID_Flush': 'Redirect'}.get(nm, nm)
        c.tun(po, src, 30)
    c.box(130, 180, left=[('rs1', 20), ('rs2', 40), ('UseRs1', 60), ('UseRs2', 80), ('D_Halt', 100), ('E_rd', 120),
                          ('E_MemRead', 140), ('Redirect', 160)],
          right=[('PCWrite', 30), ('IFID_Write', 50), ('IFID_Flush', 70), ('IDEX_Flush', 90), ('Stall', 130),
                 ('LoadUse', 150)], title='Hazard', fill=C_CTRL, title_pos='bottom', label_size=8)
    return c


def build_idbypass():
    c = Circuit('IDBypass')
    notes(c, 60, 40, ['WB -> ID bypass (write-through Register File)',
                      'Lenh o WB ghi thanh ghi o CANH LEN cuoi chu ky, nhung lenh o ID doc ngay trong chu ky do',
                      '-> neu cung thanh ghi thi lay thang du lieu dang ghi (W_data) thay vi gia tri cu.'])
    inputs(c, [('RD1', 32), ('RD2', 32), ('rs1', 5), ('rs2', 5), ('W_rd', 5), ('W_RegWrite', 1), ('W_data', 32)],
           x=120, y=140, dy=50)
    for i, opnd in enumerate(('1', '2')):
        y = 140 + 200 * i
        _ne0_eq(c, 'W_rd', f'rs{opnd}', 400, y, f'eq{opnd}')
        g = c.add('AND Gate', 620, y + 30, width=1, size=30, inputs=2)
        c.tun(g.p(1), f'eq{opnd}', 20)
        c.tun(g.p(2), 'W_RegWrite', 20)
        m = c.add('Multiplexer', 760, y + 40, width=32, select=1, enable='false')
        c.tun(m.p(0), f'RD{opnd}', 20)
        c.tun(m.p(1), 'W_data', 20)
        c.path(g.p(0), (g.p(0).x + 20, g.p(0).y), (g.p(0).x + 20, m.p(2).y + 20), (m.p(2).x, m.p(2).y + 20), m.p(2))
        po = c.pin_out(f'O{opnd}', 32, 860, y + 40)
        c.wire(m.p(3), po)
    c.box(110, 200, left=[('RD1', 20), ('RD2', 80), ('rs1', 100), ('rs2', 120), ('W_rd', 140), ('W_RegWrite', 160),
                          ('W_data', 180)], right=[('O1', 20), ('O2', 80)], title='WB Bypass',
          fill=C_CTRL, title_pos='bottom', label_size=8)
    return c




# ---------------------------------------------------------------------------
# Memory-mapped I/O controller: UART (TTY out + Keyboard in) and GPIO
# ---------------------------------------------------------------------------
IO_MAP = [  # index = Addr[4:2]
    (0, 'UART_TXDATA', 'W', 'ghi: in ky tu WData[6:0] ra TTY'),
    (1, 'UART_RXDATA', 'R', 'doc: lay 1 ky tu tu Keyboard (lay xong la mat khoi hang doi)'),
    (2, 'UART_STATUS', 'R', 'bit0 = co ky tu cho doc (RX avail), bit1 = TX san sang (luon 1)'),
    (4, 'GPIO_OUT', 'RW', '32-bit: [15:0] -> 4 LED 7 doan (hex), [23:16] -> 8 LED'),
    (5, 'GPIO_IN', 'R', '8 cong tac DIP'),
]


def build_ioctrl():
    c = Circuit('IOController', title='I/O')
    notes(c, 60, 40, ['I/O Controller (memory-mapped I/O): thiet bi ngoai vi chi la vai dia chi dac biet',
                      'Vung I/O: Addr[31:28] = 0xF.  Thanh ghi I/O chon bang Addr[4:2]:',
                      '0xF0000000 UART_TXDATA (W)   0xF0000004 UART_RXDATA (R)   0xF0000008 UART_STATUS (R)',
                      '0xF0000010 GPIO_OUT (R/W)    0xF0000014 GPIO_IN (R)       dia chi khac trong vung: doc = 0',
                      'Doc RXDATA lay ky tu ra khoi hang doi -> chi bat KbdRE khi la LENH LOAD that (MemRead=1)'])
    inputs(c, [('Addr', 32), ('WData', 32), ('MemWrite', 1), ('MemRead', 1), ('IsIO', 1), ('CLK', 1),
               ('KbdData', 7), ('KbdAvail', 1), ('GpioIn', 8)], x=120, y=160, dy=50)
    sp = c.splitter(240, 640, 32, [(2, 4)])
    c.tun(sp.p(0), 'Addr', 20)
    c.tun(sp.p(1), 'idx', 20)
    c.text(180, 620, 'idx = Addr[4:2]', size=10, color=TXT)
    DX, DY = 420, 330
    dec = c.add('Decoder', DX, DY, select=3, enable='true')
    c.tun(dec.p(8), 'idx', 20)
    c.path(dec.p(9), (DX - 10, DY + 20), (DX - 40, DY + 20))
    c.tun(Port(DX - 40, DY + 20, 1, 'W', 'i'), 'IsIO', 20)
    for i, nm in ((0, 'selTX'), (1, 'selRX'), (4, 'selGPIO')):
        c.tun(dec.p(i), nm, 20)
    c.text(DX - 30, DY - 100, 'chon thanh ghi I/O', size=10, color=TXT)
    for i, (out, a, b) in enumerate((('TxWE', 'MemWrite', 'selTX'), ('KbdRE', 'MemRead', 'selRX'),
                                      ('gpioWE', 'MemWrite', 'selGPIO'))):
        g = c.add('AND Gate', 640, 200 + 80 * i, width=1, size=30, inputs=2)
        c.tun(g.p(1), a, 20)
        c.tun(g.p(2), b, 20)
        c.tun(g.p(0), out, 20)
    # GPIO_OUT register
    r = c.add('Register', 640, 480, width=32, appearance='logisim_evolution', label='GPIO_OUT')
    c.tun(r.p(1), 'WData', 20)
    c.tun(r.p(4), 'gpioWE', 20)
    c.tun(r.p(2), 'CLK', 20)
    c.const(r.p(3), 0, 1, 10)
    c.tun(r.p(0), 'GpioOut', 20)
    # TX data = WData[6:0]
    ts = c.splitter(640, 660, 32, [(0, 6)])
    c.tun(ts.p(0), 'WData', 20)
    c.tun(ts.p(1), 'TxData', 20)
    # read sources
    e1 = c.add('Bit Extender', 900, 200, in_width=7, out_width=32, type='zero')
    c.tun(e1.p(1), 'KbdData', 20)
    c.tun(e1.p(0), 'r_rx', 20)
    st = c.splitter(900, 300, 32, [(0, 0), (1, 1), (2, 31)], facing='west', appear='left', spacing=2)
    c.tun(st.p(1), 'KbdAvail', 20)
    c.const(st.p(2), 1, 1, 20)
    c.const(st.p(3), 0, 30, 20)
    c.tun(st.p(0), 'r_status', 20)
    c.text(780, 230, 'STATUS = {0..., 1, KbdAvail}', size=10, color=TXT)
    e2 = c.add('Bit Extender', 900, 380, in_width=8, out_width=32, type='zero')
    c.tun(e2.p(1), 'GpioIn', 20)
    c.tun(e2.p(0), 'r_gpioin', 20)
    z = c.add('Constant', 880, 440, width=32, value='0x0')
    c.tun(z.p(0), 'zero', 20)
    m_ = c.add('Multiplexer', 1120, 300, width=32, select=3, enable='false')
    srcs = ['zero', 'r_rx', 'r_status', 'zero', 'GpioOut', 'r_gpioin', 'zero', 'zero']
    for i, s in enumerate(srcs):
        c.tun(m_.p(i), s, 20 if i % 2 == 0 else 70)
    c.tun(m_.p(8), 'idx', 20)
    c.text(1080, 230, 'doc I/O theo idx', size=10, color=TXT)
    po = c.pin_out('IoRData', 32, 1220, 300)
    c.wire(m_.p(9), po)
    outputs(c, [('TxWE', 1), ('TxData', 7), ('KbdRE', 1), ('GpioOut', 32)], x=1220, y=420, dy=50)
    c.box(130, 210, left=[('Addr', 20), ('WData', 40), ('MemWrite', 60), ('MemRead', 80), ('IsIO', 100),
                          ('CLK', 120), ('KbdData', 150), ('KbdAvail', 170), ('GpioIn', 190)],
          right=[('IoRData', 20), ('TxWE', 60), ('TxData', 80), ('KbdRE', 120), ('GpioOut', 160)],
          title='I/O Ctrl', subtitle='UART + GPIO', fill=C_MEM, title_pos='center', label_size=8)
    return c
