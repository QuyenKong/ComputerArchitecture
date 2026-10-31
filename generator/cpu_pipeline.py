"""5-stage pipelined RV32I CPU top level (IF ID EX MEM WB) with forwarding, load-use stall,
branch flush (predict not-taken, resolved in EX) and WB->ID bypass."""
import lgen, modules as M
from io_section import io_section
from lgen import Circuit, Port
from cpu_single import rom_contents


def pipe(c, sub, x, y, src, dst_prefix, clk='CLK', en=None, flush=None, ins=None):
    """place a pipeline register; inputs from nets src[field] (or const), outputs -> dst_prefix_field"""
    p = c.inst(sub, x, y)
    for f, w in M.PIPE_FIELDS[sub.name]:
        s = src.get(f)
        if isinstance(s, int):
            c.const(p.p('D_' + f), s, w, 30)
        else:
            c.tun(p.p('D_' + f), s, 30)
        c.tun(p.p('Q_' + f), f'{dst_prefix}_{f}', 30)
    c.tun(p.p('CLK'), clk, 20)
    for pn, v in (('EN', en), ('FLUSH', flush)):
        if isinstance(v, int):
            c.const(p.p(pn), v, 1, 20)
        else:
            c.tun(p.p(pn), v, 50 if pn == 'EN' else 80)
    return p


def build_pipeline(subs, rom_words, hazards=True):
    S = {s.name: s for s in subs}
    c = Circuit('RV32I_Pipeline' if hazards else 'RV32I_Pipeline_NoHazard')
    M.notes(c, 40, 40, ['RV32I 5-STAGE PIPELINE CPU   IF -> ID -> EX -> MEM -> WB',
                        'Data hazard: Forwarding (EX/MEM->EX, MEM/WB->EX) + WB->ID bypass + Load-use stall 1 chu ky',
                        'Control hazard: du doan "khong nhay"; branch/JAL/JALR giai quyet o EX -> neu nhay thi flush 2 lenh (IF/ID, ID/EX)',
                        'Ten tunnel: F_ = Fetch, D_ = Decode, E_ = Execute, M_ = Memory, W_ = Writeback (gia tri dang o tang do)',
                        'Chay: Ctrl+K (auto tick) / Ctrl+T (1 nua chu ky).  Nap chuong trinh: chuot phai ROM IMEM > Load Image'],
            size=12)
    for x, t in ((260, 'IF'), (1200, 'ID'), (2370, 'EX'), (3270, 'MEM'), (3940, 'WB')):
        c.text(x, 200, t, size=28, bold=True, color='#9ca3af')
    ck = c.add('Clock', 80, 1500, label='CLK')
    c.tun(ck.p(0), 'CLK', 20)
    # ================= IF =================
    nm = c.add('Multiplexer', 230, 530, width=32, select=1, enable='false')
    c.tun(nm.p(0), 'F_pc4', 30)
    c.tun(nm.p(1), 'E_target', 30)
    c.tun(nm.p(2), 'E_Redirect', 20)
    c.text(140, 480, 'next PC', size=10, color=M.TXT)
    pc = c.add('Register', 300, 500, width=32, appearance='logisim_evolution', label='PC')
    c.wire(nm.p(3), pc.p(1))
    c.tun(pc.p(4), 'PCWrite', 30)
    c.tun(pc.p(2), 'CLK', 20)
    c.const(pc.p(3), 0, 1, 10)
    q = pc.p(0)
    c.path(q, (400, q.y))
    c.bus_v(400, [q.y - 140, q.y, q.y + 60])
    add4 = c.add('Adder', 520, q.y - 130, width=32)
    c.path((400, q.y - 140), add4.p(0))
    c.const(add4.p(1), 4, 32, 20)
    c.const(add4.p(3), 0, 1, 10)
    c.tun(add4.p(2), 'F_pc4', 30)
    c.tun(Port(400, q.y + 60, 32, 'S', 'o'), 'F_pc', 20)
    sp = c.splitter(440, q.y, 32, [(2, 11)])
    c.path((400, q.y), sp.p(0))
    rom = c.add('ROM', 520, q.y - 20, addrWidth=10, dataWidth=32, appearance='classic', label='IMEM',
                contents=rom_contents(rom_words))
    c.wire(sp.p(1), rom.p(0))
    c.text(445, q.y + 40, 'PC[11:2]', size=10, color=M.TXT)
    ins = rom.p(1)
    c.tun(ins, 'F_instr', 30)
    # ================= IF/ID =================
    pipe(c, S['IF_ID'], 860, 300, {'valid': 1, 'pc': 'F_pc', 'pc4': 'F_pc4', 'instr': 'F_instr'}, 'D',
         en='IFID_Write', flush='IFID_Flush')
    # ================= ID =================
    ctl = c.inst(S['Control'], 1060, 300)
    c.tun(ctl.p('Instr'), 'D_instr', 30)
    for name, w in M.CTRL_OUTS:
        c.tun(ctl.p(name), 'D_' + name, 20)
    rf = c.inst(S['RegisterFile'], 1340, 760)
    for pn, net in (('RA1', 'D_rs1'), ('RA2', 'D_rs2'), ('WA', 'W_rd'), ('WD', 'W_data'), ('WE', 'W_RegWrite'),
                    ('CLK', 'CLK')):
        c.tun(rf.p(pn), net, 30)
    by = c.inst(S['IDBypass'], 1760, 800)
    c.wire(rf.p('RD1'), by.p('RD1'))
    c.wire(rf.p('RD2'), by.p('RD2'))
    for pn, net in (('rs1', 'D_rs1'), ('rs2', 'D_rs2'), ('W_rd', 'W_rd'), ('W_RegWrite', 'W_RegWrite'),
                    ('W_data', 'W_data')):
        c.tun(by.p(pn), net, 20)
    c.tun(by.p('O1'), 'D_rs1d', 20)
    c.tun(by.p('O2'), 'D_rs2d', 20)
    ig = c.inst(S['ImmGen'], 1340, 1220)
    c.tun(ig.p('Instr'), 'D_instr', 30)
    c.tun(ig.p('ImmSel'), 'D_ImmSel', 30)
    c.tun(ig.p('Imm'), 'D_imm', 30)
    ac = c.inst(S['ALUControl'], 1340, 1360)
    for pn in ('ALUOp', 'funct3', 'f7b5'):
        c.tun(ac.p(pn), 'D_' + pn, 30)
    c.tun(ac.p('ALUCtrl'), 'D_ALUCtrl', 30)
    hz = c.inst(S['HazardUnit'], 1720, 1160)
    for pn, net in (('rs1', 'D_rs1'), ('rs2', 'D_rs2'), ('UseRs1', 'D_UseRs1'), ('UseRs2', 'D_UseRs2'),
                    ('D_Halt', 'D_Halt'), ('E_rd', 'E_rd'), ('E_MemRead', 'E_MemRead'), ('Redirect', 'E_Redirect')):
        if pn == 'E_MemRead' and not hazards:
            c.const(hz.p(pn), 0, 1, 30)              # NO load-use detection
            continue
        c.tun(hz.p(pn), net, 30 if pn in ('rs1', 'UseRs1', 'D_Halt', 'E_MemRead') else 80)
    for pn in ('PCWrite', 'IFID_Write', 'IFID_Flush', 'IDEX_Flush', 'Stall', 'LoadUse'):
        c.tun(hz.p(pn), pn, 30 if pn in ('PCWrite', 'IFID_Flush', 'Stall') else 80)
    # ================= ID/EX =================
    src = {f: 'D_' + f for f, _ in M.PIPE_FIELDS['ID_EX']}
    src.update({'rs1d': 'D_rs1d', 'rs2d': 'D_rs2d', 'imm': 'D_imm', 'ALUCtrl': 'D_ALUCtrl'})
    pipe(c, S['ID_EX'], 1980, 300, src, 'E', en=1, flush='IDEX_Flush')
    # ================= EX =================
    fw = c.inst(S['ForwardUnit'], 2520, 300)
    for pn, net in (('rs1', 'E_rs1'), ('rs2', 'E_rs2'), ('M_rd', 'M_rd'), ('M_RegWrite', 'M_RegWrite'),
                    ('W_rd', 'W_rd'), ('W_RegWrite', 'W_RegWrite')):
        c.tun(fw.p(pn), net, 30 if pn in ('rs1', 'M_rd', 'W_rd') else 80)
    c.tun(fw.p('FwdA'), 'FwdA', 30)
    c.tun(fw.p('FwdB'), 'FwdB', 30)
    fa = c.add('Multiplexer', 2420, 620, width=32, select=2, enable='false')
    fb = c.add('Multiplexer', 2420, 760, width=32, select=2, enable='false')
    for m_, opnd, out in ((fa, 'rs1d', 'E_fa'), (fb, 'rs2d', 'E_fb')):
        c.tun(m_.p(0), f'E_{opnd}', 30)
        c.tun(m_.p(1), 'M_exres', 80)
        c.tun(m_.p(2), 'W_data', 30)
        c.const(m_.p(3), 0, 32, 80)
        if hazards:
            c.tun(m_.p(4), 'FwdA' if m_ is fa else 'FwdB', 20)
        else:
            c.const(m_.p(4), 0, 2, 20)              # NO forwarding: always take the ID/EX value
        o = m_.p(5)
        c.path(o, (o.x + 20, o.y))
    c.text(2300, 580, 'Fwd: 0 ID/EX, 1 EX/MEM, 2 MEM/WB', size=10, color=M.TXT)
    # fa -> ASel mux, fb -> BSel mux
    am = c.add('Multiplexer', 2560, 650, width=32, select=2, enable='false')
    c.path((2440, fa.p(5).y), (2440, am.p(0).y), am.p(0))
    c.bus_v(2440, [fa.p(5).y - 60, fa.p(5).y])
    c.tun(Port(2440, fa.p(5).y - 60, 32, 'N', 'o'), 'E_fa', 10)
    c.tun(am.p(1), 'E_pc', 70)
    c.bus_v(am.p(2).x - 20, [am.p(2).y, am.p(3).y])
    c.path((am.p(2).x - 20, am.p(2).y), am.p(2))
    c.path((am.p(3).x - 20, am.p(3).y), am.p(3))
    c.const(Port(am.p(3).x - 20, am.p(3).y, 32, 'W', 'i'), 0, 32, 10)
    c.tun(am.p(4), 'E_ASel', 20)
    bm = c.add('Multiplexer', 2560, 790, width=32, select=1, enable='false')
    c.bus_v(2440, [fb.p(5).y, bm.p(0).y, fb.p(5).y + 120])
    c.path((2440, bm.p(0).y), bm.p(0))
    c.tun(Port(2440, fb.p(5).y + 120, 32, 'S', 'o'), 'E_fb', 10)
    c.tun(bm.p(1), 'E_imm', 30)
    c.tun(bm.p(2), 'E_BSel', 20)
    c.text(2510, 600, 'ASel', size=10, color=M.TXT)
    c.text(2540, 870, 'BSel', size=10, color=M.TXT)
    alu = c.inst(S['ALU'], 2640, am.p(5).y - 30)
    c.wire(am.p(5), alu.p('A'))
    c.path(bm.p(3), (2600, bm.p(3).y), (2600, alu.p('B').y), alu.p('B'))
    c.tun(alu.p('ALUCtrl'), 'E_ALUCtrl', 30)
    ay = alu.p('Y')
    c.path(ay, (ay.x + 40, ay.y))
    c.bus_v(ay.x + 40, [ay.y - 60, ay.y, ay.y + 60])
    c.tun(Port(ay.x + 40, ay.y - 60, 32, 'N', 'o'), 'E_alu', 20)
    c.probe(Port(ay.x + 40, ay.y + 60, 32, 'S', 'o'), length=20, label='E_alu', labelloc='east')
    bu = c.inst(S['BranchUnit'], 2640, 1000)
    c.tun(bu.p('A'), 'E_fa', 30)
    c.tun(bu.p('B'), 'E_fb', 70)
    c.tun(bu.p('funct3'), 'E_funct3', 30)
    c.tun(bu.p('Branch'), 'E_Branch', 70)
    og = c.add('OR Gate', 2920, bu.p('Taken').y - 10, width=1, size=30, inputs=3)
    c.wire(bu.p('Taken'), og.p(3))
    c.tun(og.p(1), 'E_Jal', 70)
    c.tun(og.p(2), 'E_Jalr', 30)
    c.tun(og.p(0), 'E_Redirect', 20)
    tg = c.add('AND Gate', 2860, 1160, width=32, size=30, inputs=2)
    c.tun(tg.p(1), 'E_alu', 30)
    c.const(tg.p(2), 0xFFFFFFFE, 32, 30)
    c.tun(tg.p(0), 'E_target', 20)
    c.text(2680, 1210, 'Redirect = Taken|Jal|Jalr ; target = ALU & ~1', size=10, color=M.TXT)
    # exres = WBSel[1] ? pc4 : alu   (value forwarded / written back, also the memory address)
    ws = c.splitter(2560, 1300, 2, [(0, 0), (1, 1)], spacing=2)
    c.tun(ws.p(0), 'E_WBSel', 20)
    c.tun(ws.p(1), 'E_MemToReg', 20)
    c.tun(ws.p(2), 'E_isLink', 20)
    xm = c.add('Multiplexer', 2880, 1320, width=32, select=1, enable='false')
    c.tun(xm.p(0), 'E_alu', 30)
    c.tun(xm.p(1), 'E_pc4', 30)
    c.tun(xm.p(2), 'E_isLink', 20)
    c.tun(xm.p(3), 'E_exres', 30)
    c.text(2680, 1260, 'exres = (JAL/JALR) ? PC+4 : ALU', size=10, color=M.TXT)
    # ================= EX/MEM =================
    src = {'valid': 'E_valid', 'pc': 'E_pc', 'instr': 'E_instr', 'exres': 'E_exres', 'sdata': 'E_fb',
           'rd': 'E_rd', 'funct3': 'E_funct3', 'RegWrite': 'E_RegWrite', 'MemRead': 'E_MemRead', 'MemWrite': 'E_MemWrite', 'MemToReg': 'E_MemToReg', 'Halt': 'E_Halt'}
    pipe(c, S['EX_MEM'], 3080, 300, src, 'M', en=1, flush=0)
    # ================= MEM =================
    ad = c.inst(S['AddrDecode'], 3340, 160)
    c.tun(ad.p('Addr'), 'M_exres', 30)
    c.tun(ad.p('MemWrite'), 'M_MemWrite', 30)
    for pn in ('WordAddr', 'Off', 'RamWE', 'IsIO'):
        c.tun(ad.p(pn), 'M_' + pn, 20)
    ram = c.add('RAM', 3380, 560, addrWidth=12, dataWidth=32, appearance='classic', asyncread='true',
                databus='bibus', label='DMEM')
    c.tun(ram.p(0), 'M_WordAddr', 30)
    c.tun(ram.p(4), 'M_RamWE', 70)
    c.const(ram.p(3), 1, 1, 30)
    c.tun(ram.p(5), 'CLK', 30)
    c.tun(ram.p(1), 'M_ramout', 30)
    st = c.inst(S['StoreUnit'], 3200, 700)
    c.tun(st.p('Old'), 'M_memword', 30)
    c.tun(st.p('WData'), 'M_sdata', 70)
    c.tun(st.p('Off'), 'M_Off', 30)
    c.tun(st.p('funct3'), 'M_funct3', 70)
    c.tun(st.p('New'), 'M_stnew', 30)
    c.tun(ram.p(2), 'M_stnew', 110)
    ld = c.inst(S['LoadUnit'], 3380, 860)
    c.tun(ld.p('Word'), 'M_memword', 30)
    c.tun(ld.p('Off'), 'M_Off', 70)
    c.tun(ld.p('funct3'), 'M_funct3', 30)
    c.tun(ld.p('Data'), 'M_mdata', 30)
    io_section(c, S, 3220, 1160, {'addr': 'M_exres', 'wdata': 'M_stnew', 'MemWrite': 'M_MemWrite',
                                  'MemRead': 'M_MemRead', 'IsIO': 'M_IsIO', 'ramout': 'M_ramout',
                                  'memword': 'M_memword'})
    # ================= MEM/WB =================
    src = {'valid': 'M_valid', 'pc': 'M_pc', 'instr': 'M_instr', 'exres': 'M_exres', 'mdata': 'M_mdata',
           'rd': 'M_rd', 'RegWrite': 'M_RegWrite', 'MemToReg': 'M_MemToReg', 'Halt': 'M_Halt'}
    pipe(c, S['MEM_WB'], 3820, 300, src, 'W', en=1, flush=0)
    # ================= WB =================
    wm = c.add('Multiplexer', 4080, 420, width=32, select=1, enable='false')
    c.tun(wm.p(0), 'W_exres', 30)
    c.tun(wm.p(1), 'W_mdata', 30)
    c.tun(wm.p(2), 'W_MemToReg', 20)
    wy = wm.p(3)
    c.path(wy, (wy.x + 40, wy.y))
    c.bus_v(wy.x + 40, [wy.y - 60, wy.y, wy.y + 60])
    c.tun(Port(wy.x + 40, wy.y - 60, 32, 'N', 'o'), 'W_data', 20)
    c.probe(Port(wy.x + 40, wy.y + 60, 32, 'S', 'o'), length=20, label='W_data', labelloc='east')
    # ================= pipeline monitor: which instruction is in which stage =================
    MX, MY = 260, 1700
    c.text(MX - 120, MY - 60, 'PIPELINE MONITOR (PC va ma lenh o tung tang; instr = 00000000 la bubble)',
           size=13, bold=True, color='#7c2d12')
    for i, st_ in enumerate(('F', 'D', 'E', 'M', 'W')):
        x = MX + i * 300
        c.text(x - 80, MY - 25, {'F': 'IF', 'D': 'ID', 'E': 'EX', 'M': 'MEM', 'W': 'WB'}[st_], size=14, bold=True,
               color='#374151')
        for j, f in enumerate(('pc', 'instr')):
            pt = Port(x, MY + j * 40, 32, 'W', 'i')
            c.add('Probe', x, MY + j * 40, radix=16, facing='west', appearance='classic', label=f'{st_}_{f}',
                  labelloc='east')
            c.tun(pt, f'{st_}_{f}', 20)
    for i, nm_ in enumerate(('Stall', 'LoadUse', 'E_Redirect', 'FwdA', 'FwdB')):
        x = MX + i * 300
        c.add('Probe', x, MY + 100, radix=2, facing='west', appearance='classic', label=nm_, labelloc='east')
        c.tun(Port(x, MY + 100, 2 if nm_.startswith('Fwd') else 1, 'W', 'i'), nm_, 20)
    # ================= halt / counters / outputs =================
    ng = c.add('NOT Gate', 300, 1500, width=1, size=20)
    c.tun(ng.p(1), 'W_Halt', 30)
    c.tun(ng.p(0), 'Run', 30)
    pf = c.inst(S['PerfCounters'], 500, 1460)
    c.tun(pf.p('CLK'), 'CLK', 30)
    c.tun(pf.p('Run'), 'Run', 70)
    c.tun(pf.p('Retire'), 'W_valid', 30)
    c.tun(pf.p('cycles'), 'cycles', 30)
    c.tun(pf.p('instret'), 'instret', 70)
    for i, (nm_, w) in enumerate((('halt', 1), ('cycles', 32), ('instret', 32), ('pc', 32), ('gpio', 32))):
        po = c.pin_out(nm_, w, 900 + 200 * i, 1560)
        c.tun(po, {'halt': 'W_Halt', 'pc': 'F_pc', 'gpio': 'IO_gpio'}.get(nm_, nm_), 30)
    return c

