#!/usr/bin/env python3
"""compare.py - so sánh 3 phiên bản CPU trên cùng một chương trình:
  SC  = circ/RV32I_SingleCycle.circ           (đơn chu kỳ)
  NH  = circ/extra/RV32I_Pipeline_NoHazard.circ (pipeline KHÔNG có forwarding/stall;
        chương trình được assembler chèn NOP: rvasm.py --nohazard)
  PL  = circ/RV32I_Pipeline.circ              (pipeline có ForwardUnit + HazardUnit)

  python tools/compare.py                          # bảng tổng hợp cho mọi programs/*.s
  python tools/compare.py programs/t06_hazard.s    # + giản đồ từng chu kỳ của NH và PL
  python tools/compare.py programs/t06_hazard.s --from 8 --count 14

Số chu kỳ lấy từ golden model rvsim.py; run_tests.py đã kiểm tra khớp từng chu kỳ với Logisim
cho cả 3 file .circ. Số chu kỳ ở đây không tính đoạn dump thanh ghi mà run_tests.py chèn thêm.
Giản đồ: IF ID EX ME WB = tầng; '..' = lệnh ở lại ID vì load-use stall;
  [F] = lệnh nạp sai đường, bị flush sau branch/jump nhảy; [nop] = NOP do assembler chèn.
Ghi chú cho biết toán hạng lấy từ đâu: EX/MEM, MEM/WB (forwarding), WB->ID (bypass), RF (register file).
"""
import argparse, glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rvasm, rvsim

# Trễ minh họa (ps) của từng tầng, dùng để quy số chu kỳ ra thời gian. Logisim KHÔNG mô phỏng trễ,
# nên đây chỉ là giả định kiểu sách giáo khoa (Patterson & Hennessy).
STAGE_PS = {'IF': 200, 'ID': 100, 'EX': 200, 'MEM': 200, 'WB': 100}
PIPE_REG_PS = 20
T_SINGLE = sum(STAGE_PS.values())
T_PIPE = max(STAGE_PS.values()) + PIPE_REG_PS
WRITES_RD = (0x33, 0x13, 0x03, 0x37, 0x17, 0x6F, 0x67)


def simulate(path, nohazard=False):
    src = open(path, encoding='utf-8').read()
    asm = rvasm.Assembler(nohazard=nohazard)
    words, data, listing = asm.assemble(src)
    cpu = rvsim.CPU(words, data, rvsim.stdin_of(src)).run()
    text = {pc: t for pc, _w, t, _ln, _raw in listing}
    inserted = {pc for pc, _w, t, _ln, raw in listing if raw.startswith('(nop chèn')}
    return cpu, text, inserted


def schedule(trace):
    """Lịch pipeline theo đúng mô hình phần cứng: branch/jump quyết định ở EX (flush 2 lệnh),
    load-use stall 1 chu kỳ. Trả về list dict(pc, kind, jumped, st={chu kỳ: tầng}, src)."""
    rows, last_write, prev = [], {}, None
    for i, (pc, ins) in enumerate(trace):
        jumped = i + 1 < len(trace) and trace[i + 1][0] != pc + 4
        d = rvsim.decode(ins)
        u1, u2 = rvsim.uses(d)
        op = d['op']
        stall = int(bool(prev and prev['load'] and prev['rd'] and
                         ((u1 and d['rs1'] == prev['rd']) or (u2 and d['rs2'] == prev['rd']))))
        ex = 3 if prev is None else prev['ex'] + 1 + stall + (2 if prev['jumped'] else 0)
        if prev and prev['jumped']:      # 2 lệnh nạp sai đường (PC+4, PC+8) bị flush
            e = prev['ex']
            rows.append(dict(pc=prev['pc'] + 4, kind='flush', jumped=False, st={e - 1: 'IF', e: 'ID'}, src=''))
            rows.append(dict(pc=prev['pc'] + 8, kind='flush', jumped=False, st={e: 'IF'}, src=''))
        st = {ex - 2 - stall: 'IF', ex - 1 - stall: 'ID', ex: 'EX', ex + 1: 'ME', ex + 2: 'WB'}
        if stall:
            st[ex - 1] = '..'
        srcs = []
        for used, r in ((u1, d['rs1']), (u2, d['rs2'])):
            if used and r:
                w = last_write.get(r)
                name = {1: 'EX/MEM', 2: 'MEM/WB', 3: 'WB->ID'}.get(ex - w) if w else None
                srcs.append(f'{rvasm.ABI[r]}:{name or "RF"}')
        writes = d['rd'] != 0 and op in WRITES_RD
        if writes:
            last_write[d['rd']] = ex
        rows.append(dict(pc=pc, kind='stall' if stall else 'ok', jumped=jumped, st=st, src=' '.join(srcs)))
        prev = dict(pc=pc, rd=d['rd'] if writes else 0, load=op == 0x03, ex=ex, jumped=jumped)
    return rows


def print_diagram(cpu, text, inserted, start, count):
    """Vẽ các lệnh 'thật' thứ start..start+count-1 (không đếm NOP chèn và lệnh bị flush)."""
    rows = schedule(cpu.trace)
    for r in rows:
        if r['kind'] != 'flush' and r['pc'] in inserted:
            r['kind'] = 'nop'
    real = [i for i, r in enumerate(rows) if r['kind'] in ('ok', 'stall')]
    if start >= len(real):
        return
    end = real[start + count] if start + count < len(real) else len(rows)
    rows = rows[real[start]:end]
    c0 = min(min(r['st']) for r in rows)
    c1 = max(max(r['st']) for r in rows)
    w = 24
    print(f'{"lệnh":{w}} ' + ''.join(f'{c % 100:>3}' for c in range(c0, c1 + 1)) + '   ghi chú')
    for r in rows:
        name = {'flush': '[F] ', 'nop': '[nop] '}.get(r['kind'], '') + (text.get(r['pc'], '?')
                                                                      if r['kind'] != 'nop' else '')
        cells = ''.join(f'{r["st"].get(c, ""):>3}' for c in range(c0, c1 + 1))
        if r['kind'] == 'flush':
            note = 'bị flush (thành bubble)'
        elif r['kind'] == 'nop':
            note = 'assembler chèn để chờ kết quả lệnh trước'
        else:
            note = ('LOAD-USE STALL  ' if r['kind'] == 'stall' else '') + r['src']
            if r['jumped']:
                note += '  -> NHẢY: flush 2 lệnh sau'
        print(f'{name[:w]:{w}} {cells}   {note.strip()}')


def summary(files):
    print(f'Giả định trễ (ps): {STAGE_PS}, thanh ghi pipeline {PIPE_REG_PS} ps')
    print(f'  => chu kỳ clock: đơn chu kỳ (SC) {T_SINGLE} ps, pipeline (NH, PL) {T_PIPE} ps')
    print('  NH = pipeline không forwarding/stall + NOP chèn sẵn;  PL = pipeline có ForwardUnit + HazardUnit\n')
    hdr = (f'{"chương trình":16} {"lệnh":>5} | {"SC":>5} | {"NH":>5} {"+nop":>5} | {"PL":>5} {"stall":>5} '
           f'{"nhảy":>4} | {"SC ns":>6} {"NH ns":>6} {"PL ns":>6} | {"NH/SC":>6} {"PL/SC":>6} {"PL/NH":>6}')
    print(hdr)
    print('-' * len(hdr))
    for f in files:
        cpu, _, _ = simulate(f)
        nh, _, _ = simulate(f, nohazard=True)
        n, sc, pl, nc = cpu.instret, cpu.cycles_single(), cpu.cycles_pipeline(), nh.cycles_pipeline()
        ts, tn, tp = sc * T_SINGLE / 1000, nc * T_PIPE / 1000, pl * T_PIPE / 1000
        print(f'{os.path.basename(f):16} {n:5} | {sc:5} | {nc:5} {nh.instret - n:5} | {pl:5} {cpu.loaduse:5} '
              f'{cpu.redirects:4} | {ts:6.1f} {tn:6.1f} {tp:6.1f} | {ts / tn:5.2f}x {ts / tp:5.2f}x {tn / tp:5.2f}x')
    print('\nCột SC/NH/PL là số chu kỳ. "+nop" = số NOP chèn đã thực thi. NH/SC, PL/SC = tăng tốc so với '
          'đơn chu kỳ; PL/NH = phần cứng xử lý hazard nhanh hơn cách chèn NOP bao nhiêu lần.')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('src', nargs='?')
    ap.add_argument('--from', dest='start', type=int, default=0, help='bắt đầu giản đồ từ lệnh thứ mấy (đếm từ 0)')
    ap.add_argument('--count', type=int, default=16, help='số lệnh hiển thị trong giản đồ')
    a = ap.parse_args()
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'programs')
    files = [a.src] if a.src else sorted(glob.glob(os.path.join(root, '*.s')))
    summary(files)
    if a.src:
        rng = f'lệnh {a.start}..{a.start + a.count - 1}'
        for title, nohaz in (('NH: pipeline KHÔNG có forwarding/stall, assembler chèn NOP', True),
                             ('PL: pipeline CÓ ForwardUnit + HazardUnit', False)):
            cpu, text, inserted = simulate(a.src, nohazard=nohaz)
            print(f'\n=== {title} ({os.path.basename(a.src)}, {rng}) ===\n')
            print_diagram(cpu, text, inserted, a.start, a.count)
        print('\nSC: mỗi lệnh chiếm trọn 1 chu kỳ dài (IF+ID+EX+MEM+WB liền một mạch), không có 2 lệnh nào chạy chồng nhau.')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
