#!/usr/bin/env python3
"""gen_results.py - sinh bảng số liệu (.tex) và biểu đồ (.pdf) cho báo cáo từ golden model.

  python latex/scripts/gen_results.py

Mọi con số trong latex/generated/ đến từ tools/rvsim.py + tools/compare.py, không gõ tay.
run_tests.py đã kiểm tra số chu kỳ của mô hình khớp từng chu kỳ với Logisim trên cả ba file .circ.
"""
import glob, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import compare, rvasm  # noqa: E402

OUT = os.path.join(ROOT, 'latex', 'generated')
os.makedirs(OUT, exist_ok=True)
PROGS = sorted(glob.glob(os.path.join(ROOT, 'programs', '*.s')))


def tt(s):
    return r'\texttt{' + s.replace('_', r'\_') + '}'


def results():
    rows = []
    for f in PROGS:
        cpu, _, _ = compare.simulate(f)
        nh, _, _ = compare.simulate(f, nohazard=True)
        rows.append(dict(name=os.path.basename(f), n=cpu.instret, sc=cpu.cycles_single(),
                         nh=nh.cycles_pipeline(), nop=nh.instret - cpu.instret, pl=cpu.cycles_pipeline(),
                         lu=cpu.loaduse, br=cpu.redirects))
    return rows


def write_tables(rows):
    ts, tp = compare.T_SINGLE, compare.T_PIPE
    lines = []
    for r in rows:
        lines.append(f"{tt(r['name'])} & {r['n']} & {r['sc']} & {r['nh']} & {r['nop']} & {r['pl']} & "
                     f"{r['lu']} & {r['br']} & {r['pl'] / r['n']:.2f} \\\\")
    tot = {k: sum(r[k] for r in rows) for k in ('n', 'sc', 'nh', 'nop', 'pl', 'lu', 'br')}
    lines.append(r'\midrule')
    lines.append(f"Tổng & {tot['n']} & {tot['sc']} & {tot['nh']} & {tot['nop']} & {tot['pl']} & "
                 f"{tot['lu']} & {tot['br']} & {tot['pl'] / tot['n']:.2f} \\\\")
    # \input bên trong tabular gây lỗi \noalign, nên sinh nguyên môi trường tabular
    head = [r'\begin{tabular}{@{}lrrrrrrrr@{}}', r'\toprule',
            r'Chương trình & Lệnh & SC & NH & NOP & PL & Load-use & Nhảy & CPI (PL) \\', r'\midrule']
    open(os.path.join(OUT, 'cycles_table.tex'), 'w', encoding='utf-8').write(
        '\n'.join(head + lines + [r'\bottomrule', r'\end{tabular}']) + '\n')

    lines = [r'\begin{tabular}{@{}lrrrrrr@{}}', r'\toprule',
             r'Chương trình & SC (ns) & NH (ns) & PL (ns) & SC/NH & SC/PL & NH/PL \\', r'\midrule']
    for r in rows:
        a, b, c = r['sc'] * ts / 1000, r['nh'] * tp / 1000, r['pl'] * tp / 1000
        lines.append(f"{tt(r['name'])} & {a:.1f} & {b:.1f} & {c:.1f} & {a / b:.2f} & {a / c:.2f} & {b / c:.2f} \\\\")
    lines += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(OUT, 'time_table.tex'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    # các con số dùng trong văn bản
    t09 = next(r for r in rows if r['name'] == 't09_recursion.s')
    demo = next(r for r in rows if r['name'] == 'demo.s')
    macros = {
        'TotN': tot['n'], 'TotSC': tot['sc'], 'TotNH': tot['nh'], 'TotNOP': tot['nop'], 'TotPL': tot['pl'],
        'TotLU': tot['lu'], 'TotBR': tot['br'],
        'TotCPI': f"{tot['pl'] / tot['n']:.2f}", 'TotCPINH': f"{tot['nh'] / tot['n']:.2f}",
        'NineN': t09['n'], 'NinePL': t09['pl'], 'NineNH': t09['nh'], 'NineNOP': t09['nop'],
        'NineLU': t09['lu'], 'NineBR': t09['br'], 'NineFlush': 2 * t09['br'],
        'NineCPI': f"{t09['pl'] / t09['n']:.2f}",
        'DemoN': demo['n'], 'DemoPL': demo['pl'], 'DemoNH': demo['nh'], 'DemoNOP': demo['nop'],
        'DemoLU': demo['lu'], 'DemoBR': demo['br'],
        'TSingle': ts, 'TPipe': tp, 'IdealSpeedup': f'{ts / tp:.2f}',
        'SpeedPL': f"{tot['sc'] * ts / (tot['pl'] * tp):.2f}", 'SpeedNH': f"{tot['sc'] * ts / (tot['nh'] * tp):.2f}",
        'SpeedPLNH': f"{tot['nh'] / tot['pl']:.2f}",
    }
    with open(os.path.join(OUT, 'numbers.tex'), 'w', encoding='utf-8') as fh:
        for k, v in macros.items():
            fh.write(f'\\newcommand{{\\res{k}}}{{{v}}}\n')


def diagram(path, nohazard, start, count, fname):
    """Giản đồ pipeline dạng tabular cho các lệnh thật thứ start..start+count-1."""
    cpu, text, inserted = compare.simulate(path, nohazard=nohazard)
    rows = compare.schedule(cpu.trace)
    for r in rows:
        if r['kind'] != 'flush' and r['pc'] in inserted:
            r['kind'] = 'nop'
    real = [i for i, r in enumerate(rows) if r['kind'] in ('ok', 'stall')]
    end = real[start + count] if start + count < len(real) else len(rows)
    rows = rows[real[start]:end]
    c0 = min(min(r['st']) for r in rows)
    c1 = max(max(r['st']) for r in rows)
    ncol = c1 - c0 + 1
    color = {'IF': 'cIF', 'ID': 'cID', 'EX': 'cEX', 'ME': 'cME', 'WB': 'cWB', '..': 'cST'}
    out = [r'\begin{tabular}{@{}l' + 'c' * ncol + r'l@{}}', r'\toprule',
           'Lệnh & ' + ' & '.join(str(c - c0 + 1) for c in range(c0, c1 + 1)) + r' & Ghi chú \\', r'\midrule']
    for r in rows:
        if r['kind'] == 'nop':
            name, note = r'\textit{nop (chèn)}', ''
        else:
            name = r'\texttt{' + text.get(r['pc'], '?').replace('_', r'\_') + '}'
            if r['kind'] == 'flush':
                name = r'\textcolor{gray}{' + name + '}'
                note = 'bị flush'
            else:
                note = 'stall' if r['kind'] == 'stall' else ''
                if r['jumped']:
                    note = (note + ', ' if note else '') + 'nhảy'
        cells = []
        for c in range(c0, c1 + 1):
            s = r['st'].get(c, '')
            if not s:
                cells.append('')
            else:
                lab = 'ID' if s == '..' else s
                cells.append(r'\cellcolor{' + color[s] + '}' + r'\tiny ' + lab)
        out.append(name + ' & ' + ' & '.join(cells) + f' & {note} \\\\')
    out += [r'\bottomrule', r'\end{tabular}']
    open(os.path.join(OUT, fname), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return c1 - c0 + 1


def plot(rows):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 9, 'font.family': 'DejaVu Sans'})
    sel = [r for r in rows if r['name'] != 't09_recursion.s']
    names = [r['name'].replace('.s', '') for r in sel]
    x = range(len(sel))
    w = 0.27
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    ax.bar([i - w for i in x], [r['sc'] for r in sel], w, label='Đơn chu kỳ (SC)', color='#4c78a8')
    ax.bar(list(x), [r['nh'] for r in sel], w, label='Pipeline + NOP (NH)', color='#f58518')
    ax.bar([i + w for i in x], [r['pl'] for r in sel], w, label='Pipeline đầy đủ (PL)', color='#54a24b')
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=30, ha='right')
    ax.set_ylabel('Số chu kỳ')
    ax.legend(frameon=False, ncol=3, loc='upper left')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'cycles.pdf'))

    ts, tp = compare.T_SINGLE, compare.T_PIPE
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    names = [r['name'].replace('.s', '') for r in rows]
    x = range(len(rows))
    ax.bar([i - 0.2 for i in x], [r['sc'] * ts / (r['nh'] * tp) for r in rows], 0.4,
           label='NH so với SC', color='#f58518')
    ax.bar([i + 0.2 for i in x], [r['sc'] * ts / (r['pl'] * tp) for r in rows], 0.4,
           label='PL so với SC', color='#54a24b')
    ax.axhline(ts / tp, color='gray', ls='--', lw=1)
    ax.text(len(rows) - 0.5, ts / tp + 0.05, f'lý tưởng {ts / tp:.2f}×', ha='right', va='bottom', color='gray')
    ax.set_xticks(list(x))
    ax.set_xticklabels(names, rotation=30, ha='right')
    ax.set_ylabel('Tăng tốc (lần)')
    ax.set_ylim(0, 4)
    ax.legend(frameon=False, ncol=2, loc='upper left')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(axis='y', alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'speedup.pdf'))


def main():
    rows = results()
    write_tables(rows)
    t06 = os.path.join(ROOT, 'programs', 't06_hazard.s')
    diagram(t06, False, 8, 7, 't06_pl.tex')
    diagram(t06, True, 8, 7, 't06_nh.tex')
    plot(rows)
    print('wrote', sorted(os.listdir(OUT)))


if __name__ == '__main__':
    main()
