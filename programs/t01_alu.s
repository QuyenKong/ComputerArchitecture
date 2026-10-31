# t01_alu.s - every R-type and I-type ALU instruction, with edge cases
        li   s0, 0x7FFFFFFF        # largest positive int
        li   s1, 0x80000000        # most negative int
        li   s2, -1                # 0xFFFFFFFF
        li   s3, 12345
        li   s4, -678
        add  t0, s0, s3            # signed overflow wraps around
        sub  t1, s1, s3
        sub  t2, s4, s3
        and  t3, s3, s4
        or   t4, s3, s4
        xor  t5, s2, s3
        slt  t6, s4, s3            # -678 < 12345 -> 1
        slt  a0, s3, s4            # 0
        sltu a1, s4, s3            # 0xFFFFFD5A < 12345 unsigned -> 0
        sltu a2, s3, s4            # 1
        li   a7, 35
        sll  a3, s3, a7            # shift amount uses only low 5 bits (35 -> 3)
        srl  a4, s4, a7
        sra  a5, s4, a7
        sra  a6, s1, a7
        addi s5, s3, -2048
        addi s6, s3, 2047
        andi s7, s4, 0x0F0
        ori  s8, s3, -16
        xori s9, s4, -1            # NOT
        slti s10, s4, -677         # 1
        sltiu s11, s3, -1          # 12345 < 0xFFFFFFFF -> 1
        slli t0, s3, 31
        srli t1, s1, 31
        srai t2, s1, 31
        srai t3, s4, 4
        add  zero, s3, s3          # writes to x0 are ignored
        addi x0, x0, 5
        add  t4, zero, zero
        ebreak
