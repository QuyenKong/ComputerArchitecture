# random program, seed 10
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 1680
        li   x2, -2734
        li   x3, 513
        li   x4, 953
        li   x5, 1735
        li   x6, -2879
        li   x7, -1312
        li   x8, 789
        li   x9, 1024
        li   x10, -727
        li   x11, 2353
        li   x12, -1688
        li   x13, -2719
        li   x14, 1265
        li   x15, 1014
        or x12, x1, x3
        auipc x5, 958044
        xor x3, x4, x10
        slti x3, x5, 951
        sh x2, 122(x20)
        lb x7, 165(x20)
        add  x5, x7, x11
        sub x6, x3, x2
        andi x7, x8, -38
        lb x5, 73(x20)
        add  x3, x5, x8
        sb x1, 165(x20)
        slt x5, x3, x8
        lbu x8, 122(x20)
        add  x8, x8, x3
        slti x7, x3, 1567
        sltu x14, x2, x2
        sra x8, x7, x15
        sltiu x8, x3, -104
        add x8, x2, x7
        bne x15, x2, L1
        addi x8, x7, 50
        addi x6, x4, 4
L1:
        sub x5, x8, x13
        lhu x6, 216(x20)
        add  x1, x6, x7
        bgeu x7, x14, L2
        addi x6, x4, 30
L2:
        lbu x5, 238(x20)
        add  x6, x5, x8
        bge x2, x6, L3
        addi x3, x7, 42
        addi x5, x6, 33
        addi x7, x5, 27
L3:
        and x1, x2, x4
        srli x13, x1, 25
        sra x6, x11, x1
        slt x7, x3, x2
        auipc x1, 732651
        sll x6, x8, x10
        xori x3, x7, 764
        li   x16, 4
L4:
        or x3, x3, x4
        sra x6, x1, x3
        addi x16, x16, -1
        bnez x16, L4
        or x3, x6, x5
        li   x16, 1
L5:
        sra x2, x4, x3
        sltu x8, x6, x3
        addi x16, x16, -1
        bnez x16, L5
        sb x7, 89(x20)
        li   x16, 4
L6:
        or x5, x9, x2
        addi x16, x16, -1
        bnez x16, L6
        srl x4, x1, x7
        lb x7, 51(x20)
        add  x2, x7, x4
        lw x1, 12(x20)
        add  x6, x1, x3
        lh x3, 182(x20)
        add  x4, x3, x4
        slti x7, x13, -1794
        sub x1, x3, x7
        sltu x3, x1, x1
        lhu x7, 234(x20)
        sltiu x11, x5, 26
        sll x5, x5, x2
        ori x13, x1, 79
        lb x11, 217(x20)
        add  x4, x11, x4
        sltu x1, x2, x8
        bne x3, x3, L7
        addi x3, x8, -31
        addi x7, x5, -23
L7:
        ori x7, x6, 551
        sll x6, x9, x2
        bgeu x1, x15, L8
        addi x8, x15, 34
        addi x2, x6, 8
L8:
        andi x13, x4, -70
        lw x10, 192(x20)
        add  x11, x10, x4
        la   x17, F9
        jalr x18, 0(x17)
        j    E9
F9:   and x10, x2, x8
        jalr x0, 0(x18)
E9:
        or x8, x3, x4
        xor x3, x7, x1
        xor x1, x5, x2
        bge x2, x3, L10
        addi x9, x1, 16
L10:
        sb x2, 132(x20)
        sw x1, 244(x20)
        xori x8, x5, -777
        andi x8, x8, -1858
        ori x8, x4, -221
        andi x1, x1, -1570
        xor x4, x8, x4
        and x8, x1, x6
        and x3, x4, x8
        sh x6, 150(x20)
        srli x2, x6, 31
        lh x4, 240(x20)
        add  x4, x4, x7
        lbu x8, 21(x20)
        add  x4, x8, x4
        bltu x8, x1, L11
        addi x5, x2, -19
        addi x3, x7, 40
        addi x7, x7, 2
L11:
        slt x3, x13, x1
        lw x7, 92(x20)
        slti x4, x12, 635
        sll x10, x11, x8
        sltu x2, x2, x2
        lw x6, 136(x20)
        andi x3, x15, -1934
        sw x10, 228(x20)
        lui x7, 507846
        addi x6, x5, -784
        lhu x1, 28(x20)
        add  x9, x1, x5
        lh x6, 184(x20)
        add  x12, x6, x5
        lh x7, 54(x20)
        add  x3, x7, x10
        add x6, x5, x4
        lw x3, 64(x20)
        add  x3, x3, x5
        xori x5, x5, -1458
        slt x11, x4, x4
        srli x5, x7, 21
        sltiu x6, x5, 1946
        blt x8, x14, L12
        addi x6, x2, -7
L12:
        sub x7, x3, x14
        srl x3, x4, x10
        lw x6, 60(x20)
        add x8, x1, x5
        slti x3, x5, 413
        and x1, x7, x1
        sra x5, x8, x6
        ori x1, x14, -1982
        sw x4, 4(x20)
        lhu x6, 248(x20)
        lb x6, 89(x20)
        add  x8, x6, x3
        ori x3, x8, 347
        sb x2, 30(x20)
        srl x2, x11, x3
        or x1, x5, x15
        slt x5, x7, x1
        slti x6, x11, -1760
        sra x8, x3, x8
        slt x1, x1, x5
        slt x1, x6, x5
        sltiu x7, x8, 553
        lh x6, 64(x20)
        sb x4, 144(x20)
        ori x5, x7, -1874
        sb x2, 117(x20)
        addi x1, x2, -1860
        sltiu x7, x5, -1129
        ebreak
