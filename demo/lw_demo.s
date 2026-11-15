# lw_demo.s - demo slide 13: theo dõi lệnh lw t4, 8(sp) (mã máy 0x00812E83) trên RV32I_SingleCycle.circ
# Không để trong programs/ để run_tests.py không đếm nó vào bộ test.
# Dựng mạch:  python tools/rvasm.py demo/lw_demo.s -o build/lw_demo --circ circ/RV32I_SingleCycle.circ --circ-out build/RV32I_SingleCycle_lw.circ
        .text
main:   addi sp, zero, 0x10         # PC 0x00: sp = 0x10
        lui  t0, 0x12345            # PC 0x04: t0 = 0x12345000
        addi t0, t0, 0x678          # PC 0x08: t0 = 0x12345678
        sw   t0, 8(sp)              # PC 0x0C: M[0x18] = 0x12345678 (ô RAM số 6)
        lw   t4, 8(sp)              # PC 0x10: 0x00812E83 -> t4 = M[sp + 8] = 0x12345678
        ebreak                      # PC 0x14: halt
