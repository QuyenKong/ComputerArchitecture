"""Single-cycle RV32I CPU top level."""
import lgen, modules as M
from io_section import io_section
from lgen import Circuit, Port


def build_single(subs, rom_words):
    c = Circuit('RV32I_SingleCycle')
    S = {s.name: s for s in subs}
    M.notes(c, 40, 40, ['RV32I SINGLE-CYCLE CPU  (moi lenh chay xong trong 1 chu ky clock)',
                        'Chay: Simulate > Ticks Enabled (Ctrl+K) hoac nhan Ctrl+T de tung nua chu ky.  Reset: Ctrl+R',
                        'Nap chuong trinh: chuot phai ROM "IMEM" > Load Image... chon file *.text.hex (tools/rvasm.py)',
                        'CPU dung khi gap EBREAK/ECALL (halt = 1).  I/O: 0xF0000000 UART TX (TTY), 0xF0000004 RX (Keyboard), 0xF0000010 GPIO_OUT, 0xF0000014 GPIO_IN'],
            size=12)
    # stage labels
    for x, t in ((220, 'FETCH'), (800, 'DECODE / REGISTER READ'), (1560, 'EXECUTE'), (2050, 'MEMORY'),
                 (2650, 'WRITE BACK')):
        c.text(x, 150, t, size=16, bold=True, color='#9ca3af')
    # clock
    ck = c.add('Clock', 80, 1240, label='CLK')
    c.tun(ck.p(0), 'CLK', 20)
    # ---------------- FETCH ----------------
    nm = c.add('Multiplexer', 230, 530, width=32, select=1, enable='false')
    c.tun(nm.p(0), 'pc4', 30)
    c.tun(nm.p(1), 'target', 30)
    c.tun(nm.p(2), 'PCSel', 20)
    c.text(140, 480, 'next PC', size=10, color=M.TXT)
    pc = c.add('Register', 300, 500, width=32, appearance='logisim_evolution', label='PC')
    c.wire(nm.p(3), pc.p(1))
    c.tun(pc.p(4), 'PCEn', 30)
    c.tun(pc.p(2), 'CLK', 20)
    c.const(pc.p(3), 0, 1, 10)
    q = pc.p(0)
    c.path(q, (400, q.y))
    c.bus_v(400, [q.y - 140, q.y, q.y + 60])
    add4 = c.add('Adder', 520, q.y - 130, width=32)
    c.path((400, q.y - 140), add4.p(0))
    c.const(add4.p(1), 4, 32, 20)
    c.const(add4.p(3), 0, 1, 10)
    c.tun(add4.p(2), 'pc4', 30)
    c.text(470, q.y - 165, 'PC + 4', size=10, color=M.TXT)
    c.tun(Port(400, q.y + 60, 32, 'S', 'o'), 'PC', 20)
    sp = c.splitter(440, q.y, 32, [(2, 11)])
    c.path((400, q.y), sp.p(0))
    rom = c.add('ROM', 520, q.y - 10 - 10, addrWidth=10, dataWidth=32, appearance='classic', label='IMEM',
                contents=rom_contents(rom_words))
    c.wire(sp.p(1), rom.p(0))
    c.text(445, q.y + 40, 'PC[11:2]', size=10, color=M.TXT)
    c.text(445, q.y + 54, '(word index)', size=10, color=M.TXT)
    ins = rom.p(1)
    c.path(ins, (ins.x + 30, ins.y))
    c.bus_v(ins.x + 30, [ins.y, ins.y + 80])
    c.tun(Port(ins.x + 30, ins.y + 80, 32, 'S', 'o'), 'instr', 20)
    c.probe(Port(ins.x + 30, ins.y, 32, 'E', 'o'), length=30, label='instr')
    # ---------------- DECODE ----------------
    ctl = c.inst(S['Control'], 860, 180, label='')
    c.tun(ctl.p('Instr'), 'instr', 30)
    for name, w in M.CTRL_OUTS:
        if name in ('UseRs1', 'UseRs2'):
            continue
        c.tun(ctl.p(name), name, 20)
    rf = c.inst(S['RegisterFile'], 1080, 620)
    for pn, net in (('RA1', 'rs1'), ('RA2', 'rs2'), ('WA', 'rd'), ('WD', 'wbdata'), ('WE', 'RegWrite'), ('CLK', 'CLK')):
        c.tun(rf.p(pn), net, 30)
    c.tun(rf.p('RD1'), 'rs1d', 30)
    c.tun(rf.p('RD2'), 'rs2d', 30)
    ig = c.inst(S['ImmGen'], 1120, 1120)
    c.tun(ig.p('Instr'), 'instr', 30)
    c.tun(ig.p('ImmSel'), 'ImmSel', 30)
    c.tun(ig.p('Imm'), 'imm', 30)
    # ---------------- EXECUTE ----------------
    ac = c.inst(S['ALUControl'], 1560, 400)
    for pn in ('ALUOp', 'funct3', 'f7b5'):
        c.tun(ac.p(pn), pn, 30)
    am = c.add('Multiplexer', 1600, 650, width=32, select=2, enable='false')
    c.tun(am.p(0), 'rs1d', 30)
    c.tun(am.p(1), 'PC', 70)
    c.bus_v(am.p(2).x - 20, [am.p(2).y, am.p(3).y])
    c.path((am.p(2).x - 20, am.p(2).y), am.p(2))
    c.path((am.p(3).x - 20, am.p(3).y), am.p(3))
    c.const(Port(am.p(3).x - 20, am.p(3).y, 32, 'W', 'i'), 0, 32, 10)
    c.tun(am.p(4), 'ASel', 20)
    c.text(1500, 610, 'ASel: 0 rs1, 1 PC, 2 zero', size=10, color=M.TXT)
    bm = c.add('Multiplexer', 1600, 790, width=32, select=1, enable='false')
    c.tun(bm.p(0), 'rs2d', 30)
    c.tun(bm.p(1), 'imm', 30)
    c.tun(bm.p(2), 'BSel', 20)
    c.text(1500, 840, 'BSel: 0 rs2, 1 imm', size=10, color=M.TXT)
    alu = c.inst(S['ALU'], 1700, am.p(5).y - 30)
    c.wire(am.p(5), alu.p('A'))
    c.path(bm.p(3), (1650, bm.p(3).y), (1650, alu.p('B').y), alu.p('B'))
    c.tun(ac.p('ALUCtrl'), 'ALUCtrl', 30)
    c.tun(alu.p('ALUCtrl'), 'ALUCtrl', 30)
    ay = alu.p('Y')
    c.path(ay, (ay.x + 40, ay.y))
    c.bus_v(ay.x + 40, [ay.y - 60, ay.y, ay.y + 60])
    c.tun(Port(ay.x + 40, ay.y - 60, 32, 'N', 'o'), 'alu', 20)
    c.probe(Port(ay.x + 40, ay.y + 60, 32, 'S', 'o'), length=20, label='ALU_result', labelloc='east')
    # branch / next PC
    bu = c.inst(S['BranchUnit'], 1700, 960)
    for pn, net in (('A', 'rs1d'), ('B', 'rs2d'), ('funct3', 'funct3'), ('Branch', 'Branch')):
        c.tun(bu.p(pn), net, 30)
    og = c.add('OR Gate', 1980, bu.p('Taken').y - 10, width=1, size=30, inputs=3)
    c.wire(bu.p('Taken'), og.p(3))
    c.tun(og.p(1), 'Jal', 70)
    c.tun(og.p(2), 'Jalr', 30)
    c.tun(og.p(0), 'PCSel', 20)
    tg = c.add('AND Gate', 1920, 1120, width=32, size=30, inputs=2)
    c.tun(tg.p(1), 'alu', 30)
    c.const(tg.p(2), 0xFFFFFFFE, 32, 30)
    c.tun(tg.p(0), 'target', 20)
    c.text(1760, 1170, 'target = ALU & ~1 (branch/JAL: PC+imm, JALR: rs1+imm)', size=10, color=M.TXT)
    c.text(1760, 1060, 'PCSel = Taken | Jal | Jalr', size=10, color=M.TXT)
    # ---------------- MEMORY ----------------
    ad = c.inst(S['AddrDecode'], 2050, 420)
    c.tun(ad.p('Addr'), 'alu', 30)
    c.tun(ad.p('MemWrite'), 'MemWrite', 30)
    for pn in ('WordAddr', 'Off', 'RamWE', 'IsIO'):
        c.tun(ad.p(pn), pn, 20)
    ram = c.add('RAM', 2250, 600, addrWidth=12, dataWidth=32, appearance='classic', asyncread='true',
                databus='bibus', label='DMEM')
    c.tun(ram.p(0), 'WordAddr', 30)
    c.tun(ram.p(4), 'RamWE', 70)
    c.const(ram.p(3), 1, 1, 30)
    c.tun(ram.p(5), 'CLK', 30)
    c.tun(ram.p(1), 'ramout', 30)
    st = c.inst(S['StoreUnit'], 2050, 720)
    c.tun(st.p('Old'), 'memword', 30)
    c.tun(st.p('WData'), 'rs2d', 70)
    c.tun(st.p('Off'), 'Off', 30)
    c.tun(st.p('funct3'), 'funct3', 70)
    c.tun(st.p('New'), 'stnew', 30)
    c.tun(ram.p(2), 'stnew', 110)
    ld = c.inst(S['LoadUnit'], 2600, 560)
    c.tun(ld.p('Word'), 'memword', 30)
    c.tun(ld.p('Off'), 'Off', 30)
    c.tun(ld.p('funct3'), 'funct3', 70)
    c.tun(ld.p('Data'), 'loaddata', 30)
    # memory-mapped I/O: UART (TTY + Keyboard) and GPIO
    io_section(c, S, 2080, 1120, {'addr': 'alu', 'wdata': 'stnew', 'MemWrite': 'MemWrite', 'MemRead': 'MemRead',
                                  'IsIO': 'IsIO', 'ramout': 'ramout', 'memword': 'memword'})
    # ---------------- WRITE BACK ----------------
    wm = c.add('Multiplexer', 2850, 640, width=32, select=2, enable='false')
    c.tun(wm.p(0), 'alu', 30)
    c.tun(wm.p(1), 'loaddata', 80)
    c.tun(wm.p(2), 'pc4', 30)
    c.const(wm.p(3), 0, 32, 80)
    c.tun(wm.p(4), 'WBSel', 20)
    c.text(2740, 580, 'WBSel: 0 ALU, 1 Mem, 2 PC+4', size=10, color=M.TXT)
    wy = wm.p(5)
    c.path(wy, (wy.x + 40, wy.y))
    c.bus_v(wy.x + 40, [wy.y - 60, wy.y, wy.y + 60])
    c.tun(Port(wy.x + 40, wy.y - 60, 32, 'N', 'o'), 'wbdata', 20)
    c.probe(Port(wy.x + 40, wy.y + 60, 32, 'S', 'o'), length=20, label='WB_data', labelloc='east')
    # ---------------- halt / counters / outputs ----------------
    ng = c.add('NOT Gate', 300, 1240, width=1, size=20)
    c.tun(ng.p(1), 'Halt', 30)
    c.tun(ng.p(0), 'PCEn', 30)
    c.text(200, 1200, 'PCEn = !Halt (dung PC khi gap EBREAK)', size=10, color=M.TXT)
    pf = c.inst(S['PerfCounters'], 500, 1300)
    c.tun(pf.p('CLK'), 'CLK', 30)
    c.tun(pf.p('Run'), 'PCEn', 70)
    c.const(pf.p('Retire'), 1, 1, 30)
    c.tun(pf.p('cycles'), 'cycles', 30)
    c.tun(pf.p('instret'), 'instret', 70)
    for i, (nm_, w) in enumerate((('halt', 1), ('cycles', 32), ('instret', 32), ('pc', 32), ('gpio', 32))):
        po = c.pin_out(nm_, w, 900 + 200 * i, 1640)
        src = {'halt': 'Halt', 'pc': 'PC', 'gpio': 'IO_gpio'}.get(nm_, nm_)
        c.tun(po, src, 30)
    return c


def rom_contents(words, bits=10):
    body = ''
    for i in range(0, len(words), 8):
        body += ' '.join(f'{w:x}' for w in words[i:i + 8]) + '\n'
    return f'addr/data: {bits} 32\n' + body

