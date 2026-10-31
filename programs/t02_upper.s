# t02_upper.s - LUI / AUIPC / large constants
        lui   a0, 0x12345
        lui   a1, 0xFFFFF
        auipc a2, 0                # a2 = PC of this instruction
        auipc a3, 1                # a3 = PC + 0x1000
        li    a4, 0xDEADBEEF
        li    a5, 0x00000800       # needs lui+addi with carry fix (0x800)
        li    a6, -2049
        li    a7, 0x7FFFF7FF
        lui   t0, 0x80000
        addi  t0, t0, -1           # 0x7FFFFFFF
        ebreak
