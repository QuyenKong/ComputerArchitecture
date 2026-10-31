# random program, seed 13
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -879
        li   x2, -619
        li   x3, 2613
        li   x4, 2603
        li   x5, -1479
        li   x6, 2341
        li   x7, -1112
        li   x8, 2457
        li   x9, -1795
        li   x10, -1156
        li   x11, 2250
        li   x12, -1466
        li   x13, -1934
        li   x14, -2420
        li   x15, 1352
        sw x1, 148(x20)
        la   x17, F1
        jalr x18, 0(x17)
        j    E1
F1:   sub x13, x5, x12
        jalr x0, 0(x18)
E1:
        andi x5, x4, 1939
        bltu x7, x7, L2
        addi x2, x5, 38
        addi x3, x8, 18
        addi x4, x6, -18
L2:
        ori x7, x10, 1973
        srai x4, x3, 4
        sltiu x7, x7, -1695
        sll x14, x5, x7
        lh x11, 128(x20)
        add  x3, x11, x12
        auipc x1, 81050
        sltiu x3, x3, -1129
        bne x1, x14, L3
        addi x1, x5, -35
        addi x5, x2, 10
L3:
        addi x6, x8, -221
        lw x3, 148(x20)
        or x4, x4, x7
        slt x6, x2, x1
        slli x5, x8, 24
        xor x3, x1, x3
        xor x5, x3, x8
        slti x1, x5, -989
        li   x16, 1
L4:
        and x9, x15, x4
        and x6, x5, x4
        addi x16, x16, -1
        bnez x16, L4
        or x4, x8, x7
        lw x6, 24(x20)
        add  x5, x6, x6
        add x1, x5, x6
        sw x5, 216(x20)
        beq x5, x7, L5
        addi x3, x8, -12
        addi x1, x5, -8
L5:
        or x14, x3, x13
        sh x8, 208(x20)
        sltu x14, x1, x3
        add x5, x8, x1
        sltu x1, x11, x3
        lh x2, 216(x20)
        add  x1, x2, x6
        lb x1, 27(x20)
        add  x15, x1, x6
        sw x2, 176(x20)
        and x3, x1, x3
        lui x15, 747226
        slti x7, x8, 249
        sub x11, x2, x15
        addi x8, x8, -1549
        or x6, x14, x4
        slti x4, x2, -1124
        lb x6, 35(x20)
        add  x3, x6, x4
        andi x7, x13, 1940
        bne x6, x3, L6
        addi x7, x5, -19
L6:
        sra x7, x5, x4
        sub x2, x5, x4
        lw x2, 48(x20)
        add  x9, x2, x8
        slt x2, x8, x2
        sb x3, 136(x20)
        lw x7, 68(x20)
        slt x6, x2, x3
        srai x1, x10, 27
        sb x10, 249(x20)
        li   x16, 1
L7:
        sltu x7, x2, x7
        and x10, x1, x8
        addi x16, x16, -1
        bnez x16, L7
        srl x12, x1, x4
        sltu x5, x1, x4
        lhu x4, 232(x20)
        add  x1, x4, x4
        sb x1, 97(x20)
        sltiu x7, x3, 1665
        sll x8, x1, x8
        lbu x4, 120(x20)
        add  x1, x4, x8
        andi x1, x2, 367
        sll x11, x1, x4
        sub x2, x3, x1
        lb x15, 193(x20)
        add  x6, x15, x3
        bne x2, x7, L8
        addi x7, x4, 49
        addi x8, x1, -37
        addi x8, x3, -17
L8:
        sll x9, x1, x3
        andi x1, x5, -1226
        slt x2, x2, x6
        and x8, x8, x1
        sltiu x6, x6, -1398
        bge x14, x4, L9
        addi x3, x5, 37
        addi x7, x8, -26
L9:
        srl x1, x8, x8
        add x2, x5, x2
        auipc x8, 43469
        lw x12, 168(x20)
        sb x7, 1(x20)
        and x6, x11, x5
        bltu x1, x3, L10
        addi x5, x7, 16
L10:
        lw x4, 4(x20)
        sub x4, x7, x8
        sh x5, 160(x20)
        lw x4, 220(x20)
        add  x6, x4, x2
        li   x16, 3
L11:
        or x6, x6, x8
        sltu x2, x7, x5
        addi x16, x16, -1
        bnez x16, L11
        sltu x2, x2, x1
        lhu x7, 182(x20)
        or x12, x14, x2
        lui x7, 859660
        slti x7, x5, 1628
        lh x8, 0(x20)
        li   x16, 3
L12:
        xor x14, x5, x1
        slt x13, x4, x14
        xor x14, x1, x3
        addi x16, x16, -1
        bnez x16, L12
        srli x7, x5, 11
        la   x17, F13
        jalr x18, 0(x17)
        j    E13
F13:   add x7, x4, x3
        jalr x0, 0(x18)
E13:
        li   x16, 3
L14:
        srl x9, x7, x7
        addi x16, x16, -1
        bnez x16, L14
        sb x5, 26(x20)
        sub x2, x5, x8
        sll x14, x5, x9
        bgeu x5, x6, L15
        addi x2, x7, 18
        addi x13, x6, 4
        addi x4, x1, 47
L15:
        slti x10, x13, 671
        xor x7, x1, x4
        lw x1, 104(x20)
        add  x4, x1, x2
        li   x16, 2
L16:
        srl x5, x8, x8
        addi x16, x16, -1
        bnez x16, L16
        sltu x1, x8, x8
        andi x1, x6, -1826
        and x7, x4, x4
        sub x1, x4, x11
        auipc x1, 176907
        sub x8, x6, x1
        sh x7, 66(x20)
        sltu x7, x2, x8
        srl x3, x10, x6
        slt x12, x8, x9
        slli x7, x7, 9
        add x10, x4, x3
        sub x8, x3, x7
        sra x4, x1, x4
        lhu x5, 122(x20)
        add  x7, x5, x12
        bltu x6, x8, L17
        addi x3, x4, 33
        addi x4, x3, -7
L17:
        xori x1, x7, 1013
        bge x8, x2, L18
        addi x8, x2, -21
        addi x2, x8, -39
        addi x7, x2, -47
L18:
        ebreak
