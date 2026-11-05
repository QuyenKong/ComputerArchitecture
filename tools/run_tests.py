#!/usr/bin/env python3
"""run_tests.py - run every program in programs/ on the Logisim CPU (headless) and on the
golden ISS (rvsim.py); compare all 32 registers, the whole data memory and the cycle count.

  python3 tools/run_tests.py circ/RV32I_SingleCycle.circ            # all tests
  python3 tools/run_tests.py circ/RV32I_Pipeline.circ -k t06        # only matching tests
Requires: java + logisim-evolution-4.1.0-all.jar (path via --jar or $LOGISIM_JAR)
"""
import argparse, glob, os, re, subprocess, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rvasm, rvsim

DUMP = rvasm.DUMP_BASE


def read_hex(path):
    words = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('v'):
            continue
        for tok in line.split():
            if '*' in tok:
                n, v = tok.split('*')
                words += [int(v, 16)] * int(n)
            else:
                words.append(int(tok, 16))
    return words


def run_one(src_path, circ, jar, pipeline, timeout=600, verbose=False, nohazard=False):
    src = open(src_path).read()
    asm = rvasm.Assembler(dump=True, nohazard=nohazard)
    words, data, _ = asm.assemble(src)
    stdin = rvsim.stdin_of(src)
    cpu = rvsim.CPU(words, data, stdin).run()
    exp_mem = [int.from_bytes(cpu.mem[i:i + 4], 'little') for i in range(0, rvsim.DMEM_BYTES, 4)]
    exp_cycles = cpu.cycles_pipeline() if pipeline else cpu.cycles_single()
    with tempfile.TemporaryDirectory() as td:
        c2 = os.path.join(td, 'cpu.circ')
        rvasm.patch_circ(circ, c2, words)
        dfile = os.path.join(td, 'data.hex')
        rvasm.write_hex(dfile, rvasm.data_words(data) or [0])
        ofile = os.path.join(td, 'ram.hex')
        t0 = time.time()
        p = subprocess.Popen(['java', '-Djava.awt.headless=true', '-jar', jar, c2, '-t', 'table,halt,tty',
                              '-l', dfile, '--save', ofile],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            # bytes, not text mode: on Windows text mode turns \n into \r\n before it reaches the Keyboard
            out, err = p.communicate(stdin.encode('latin-1'), timeout=timeout)
        except subprocess.TimeoutExpired:
            if os.name == 'nt':   # 'java' may be the javapath launcher: kill the whole process tree
                subprocess.run(['taskkill', '/F', '/T', '/PID', str(p.pid)], capture_output=True)
            p.kill()
            p.communicate()
            return False, f'CPU did not halt within {timeout}s (wrong branch/loop?)', time.time() - t0
        r = subprocess.CompletedProcess(p.args, p.returncode, out.decode('latin-1'), err.decode('latin-1'))
        dt = time.time() - t0
        lines = [l for l in r.stdout.splitlines() if l.strip()]
        if not os.path.exists(ofile):
            return False, f'no RAM dump (logisim stderr: {r.stderr[-400:]})', dt
        got = read_hex(ofile)
    got += [0] * (len(exp_mem) - len(got))
    errs = []
    for i in range(32):
        a = (DUMP + 4 * i) // 4
        if i and got[a] != exp_mem[a]:
            errs.append(f'x{i}({rvasm.ABI[i]}): logisim={got[a]:08x} expected={exp_mem[a]:08x}')
    for i, (g, e) in enumerate(zip(got, exp_mem)):
        if g != e and not (DUMP // 4 <= i < DUMP // 4 + 32):
            errs.append(f'mem[{4 * i:#06x}]: logisim={g:08x} expected={e:08x}')
    # table: values of output pins (halt excluded), find cycles/instret from the last row
    cyc = None
    vals = [re.sub(r'^.*?(?=[01]{4})', '', l) for l in lines if re.search(r'[01]{4}', l)]
    if vals:
        last = vals[-1].split('\t')
        nums = [int(v.replace(' ', ''), 2) for v in last]
        cyc = nums
    info = f'cycles={exp_cycles}  instret={cpu.instret}  CPI={exp_cycles / cpu.instret:.2f}'
    if cyc is not None:
        # output pins in table order: cycles, instret, pc, gpio
        if len(cyc) > 3 and cyc[3] != cpu.gpio_out:
            errs.append(f'GPIO_OUT mismatch: logisim={cyc[3]:#x} expected={cpu.gpio_out:#x}')
        if stdin:
            info = f'instret={cpu.instret} (UART input -> cycle count not checked)'
        elif cyc[0] != exp_cycles or cyc[1] != cpu.instret:
            errs.append(f'cycle/instret mismatch: logisim cycles={cyc[0]} instret={cyc[1]} '
                        f'expected cycles={exp_cycles} instret={cpu.instret}')
    # TTY characters are printed in front of the table rows -> collect the prefixes
    tty = ''.join(re.match(r'^(.*?)(?:[01]{4}(?:[ \t][01]{4})*)?$', l).group(1) for l in r.stdout.splitlines())
    if cpu.tty.replace('\n', '') != tty:
        errs.append(f'TTY mismatch: logisim={tty!r} expected={cpu.tty!r}')
    elif cpu.tty:
        info += f'  TTY={cpu.tty!r}'
    return (not errs), ('\n      '.join(errs[:12]) if errs else info), dt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('circ')
    ap.add_argument('-k', default='', help='only tests whose name contains this')
    ap.add_argument('--jar', default=os.environ.get('LOGISIM_JAR', 'logisim-evolution-4.1.0-all.jar'))
    ap.add_argument('--timeout', type=int, default=120, help='seconds per program')
    ap.add_argument('--programs', default=os.path.join(os.path.dirname(__file__), '..', 'programs'))
    ap.add_argument('--nohazard', action='store_true',
                    help='assemble with NOPs inserted for the pipeline without forwarding/stall')
    a = ap.parse_args()
    pipeline = 'ipeline' in os.path.basename(a.circ)
    files = sorted(f for f in glob.glob(os.path.join(a.programs, '*.s')) if a.k in os.path.basename(f))
    ok_all = True
    for f in files:
        ok, msg, dt = run_one(f, a.circ, a.jar, pipeline, timeout=a.timeout, nohazard=a.nohazard)
        ok_all &= ok
        print(f'{"PASS" if ok else "FAIL"}  {os.path.basename(f):24s} {dt:5.1f}s  {msg}')
    print('ALL PASSED' if ok_all else 'SOME TESTS FAILED')
    sys.exit(0 if ok_all else 1)


if __name__ == '__main__':
    main()
