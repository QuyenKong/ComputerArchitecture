# random program, seed 15
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1289
        li   x2, -2905
        li   x3, 1270
        li   x4, -2704
        li   x5, -1706
        li   x6, -1043
        li   x7, -2862
        li   x8, -2550
        li   x9, 2581
        li   x10, -1794
        li   x11, 2691
        li   x12, 8
        li   x13, -1037
        li   x14, -2041
        li   x15, -231
        ori x5, x4, 861
        sh x8, 114(x20)
        sw x6, 248(x20)
        ori x11, x2, 1968
        li   x16, 1
L1:
        and x1, x8, x2
        addi x16, x16, -1
        bnez x16, L1
        bge x8, x15, L2
        addi x4, x6, -40
        addi x5, x6, -1
        addi x6, x13, -41
L2:
        sb x8, 137(x20)
        addi x15, x2, 304
        sll x5, x8, x8
        add x2, x8, x8
        lbu x1, 128(x20)
        add  x7, x1, x1
        auipc x5, 64782
        sw x15, 196(x20)
        sltu x1, x4, x6
        or x6, x1, x4
        add x11, x12, x14
        lh x6, 204(x20)
        add  x9, x6, x2
        slti x3, x8, -739
        lh x2, 166(x20)
        lbu x7, 82(x20)
        add  x5, x7, x3
        sra x2, x5, x2
        sw x4, 224(x20)
        sra x1, x4, x3
        slti x3, x8, 1787
        andi x7, x8, -24
        lhu x3, 14(x20)
        add  x1, x3, x8
        ori x8, x5, 1149
        xori x2, x6, 1639
        blt x10, x2, L3
        addi x3, x9, 1
L3:
        lbu x8, 206(x20)
        add  x5, x8, x2
        or x5, x3, x4
        li   x16, 4
L4:
        sub x4, x7, x5
        sltu x8, x7, x14
        sll x6, x6, x7
        addi x16, x16, -1
        bnez x16, L4
        slt x3, x4, x2
        srl x5, x8, x8
        bne x8, x3, L5
        addi x4, x9, 18
        addi x6, x1, -17
        addi x4, x7, -8
L5:
        slti x6, x7, 1074
        sw x2, 240(x20)
        lhu x2, 84(x20)
        add  x7, x2, x4
        addi x1, x5, -1654
        addi x8, x8, -234
        lb x13, 87(x20)
        la   x17, F6
        jalr x18, 0(x17)
        j    E6
F6:   sltu x11, x1, x3
        jalr x0, 0(x18)
E6:
        slti x6, x13, -1160
        bne x1, x8, L7
        addi x7, x2, 29
L7:
        andi x1, x10, 807
        or x2, x3, x5
        andi x4, x3, -1737
        la   x17, F8
        jalr x18, 0(x17)
        j    E8
F8:   slt x8, x3, x6
        jalr x0, 0(x18)
E8:
        sb x11, 28(x20)
        sra x4, x6, x7
        lhu x4, 184(x20)
        or x4, x7, x1
        sw x7, 192(x20)
        add x3, x2, x8
        jal  x18, F9
        j    E9
F9:   sltu x8, x1, x12
        jalr x0, 0(x18)
E9:
        and x13, x3, x5
        srli x4, x13, 9
        slt x8, x5, x5
        ori x6, x4, 1260
        ori x4, x2, 922
        sh x13, 16(x20)
        beq x3, x15, L10
        addi x6, x14, -10
L10:
        xor x3, x1, x4
        lui x5, 444321
        lh x3, 216(x20)
        slt x13, x13, x3
        li   x16, 3
L11:
        sub x6, x3, x6
        addi x16, x16, -1
        bnez x16, L11
        lw x1, 196(x20)
        add  x4, x1, x13
        slli x4, x3, 3
        lhu x7, 28(x20)
        add  x8, x7, x8
        sll x4, x5, x2
        sra x4, x6, x6
        bltu x8, x8, L12
        addi x9, x8, -5
L12:
        sra x6, x8, x3
        lb x7, 236(x20)
        add  x12, x7, x15
        sh x7, 114(x20)
        sh x2, 232(x20)
        sh x3, 110(x20)
        xori x6, x3, 1665
        add x5, x4, x3
        lbu x14, 132(x20)
        add  x1, x14, x4
        sll x9, x14, x15
        srl x8, x5, x15
        xor x1, x2, x11
        srl x15, x2, x1
        and x14, x5, x3
        addi x15, x9, -922
        and x7, x2, x8
        ori x6, x7, 1529
        jal  x18, F13
        j    E13
F13:   sra x3, x6, x5
        jalr x0, 0(x18)
E13:
        addi x7, x4, 188
        lb x8, 232(x20)
        bge x1, x3, L14
        addi x2, x10, 37
        addi x8, x4, -44
L14:
        xori x1, x7, -945
        or x13, x4, x4
        lui x7, 11651
        jal  x18, F15
        j    E15
F15:   xor x4, x2, x3
        jalr x0, 0(x18)
E15:
        slti x15, x1, -1077
        xori x3, x8, -1403
        sll x4, x14, x13
        slti x2, x8, 1722
        srai x7, x8, 18
        sltu x6, x7, x12
        srl x1, x5, x13
        lb x5, 209(x20)
        li   x16, 2
L16:
        slt x2, x8, x1
        and x12, x5, x2
        addi x16, x16, -1
        bnez x16, L16
        or x12, x3, x5
        srl x4, x5, x2
        beq x5, x8, L17
        addi x4, x11, 33
L17:
        sh x6, 62(x20)
        auipc x2, 628606
        add x5, x1, x3
        slt x3, x5, x2
        sub x3, x5, x7
        slti x1, x3, 35
        and x8, x8, x6
        bge x2, x4, L18
        addi x3, x4, -44
        addi x12, x7, 46
        addi x3, x4, -12
L18:
        beq x13, x5, L19
        addi x4, x8, 46
L19:
        sltiu x3, x1, 233
        or x1, x6, x3
        ebreak
