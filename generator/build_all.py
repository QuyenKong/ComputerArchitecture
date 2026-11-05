"""Build both CPU .circ files (and a modules-only library) from the generator."""
import sys, os, lgen, modules as M, cpu_single, cpu_pipeline
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
import rvasm

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'circ')
DEMO = os.path.join(os.path.dirname(__file__), '..', 'programs', 'demo.s')


def common():
    return [M.build_control(), M.build_regfile(), M.build_immgen(), M.build_alucontrol(), M.build_alu(),
            M.build_branch(), M.build_mmio(), M.build_storeunit(), M.build_loadunit(), M.build_counters(),
            M.build_ioctrl()]


def main():
    os.makedirs(os.path.join(OUT, 'extra'), exist_ok=True)
    words = rvasm.Assembler().assemble(open(DEMO).read())[0] if os.path.exists(DEMO) else [0x00100073]
    # the pipeline without forwarding/stall gets the same demo with NOPs inserted, so it runs correctly
    words_nop = rvasm.Assembler(nohazard=True).assemble(open(DEMO).read())[0] if os.path.exists(DEMO) else [0x00100073]

    def make_single():
        subs = common()
        top = cpu_single.build_single(subs, words)
        return [top] + subs, top.name

    def make_pipe():
        subs = common() + [M.build_pipereg(n) for n in M.PIPE_FIELDS] + \
            [M.build_forward(), M.build_hazard(), M.build_idbypass()]
        top = cpu_pipeline.build_pipeline(subs, words)
        return [top] + subs, top.name

    def make_naive():
        subs = common() + [M.build_pipereg(n) for n in M.PIPE_FIELDS] + \
            [M.build_forward(), M.build_hazard(), M.build_idbypass()]
        top = cpu_pipeline.build_pipeline(subs, words_nop, hazards=False)
        return [top] + subs, top.name

    for fn, name in ((make_single, 'RV32I_SingleCycle.circ'), (make_pipe, 'RV32I_Pipeline.circ'),
                     (make_naive, 'extra/RV32I_Pipeline_NoHazard.circ')):
        circs, main_ = lgen.build(fn)
        lgen.write_project(os.path.join(OUT, name), circs, main_)
        print('wrote', name, len(circs), 'circuits')


if __name__ == '__main__':
    main()
