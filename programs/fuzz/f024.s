# random program, seed 24
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 2835
        li   x2, 136
        li   x3, 1774
        li   x4, -1505
        li   x5, -1212
        li   x6, -1630
        li   x7, -1410
        li   x8, -1613
        li   x9, 2495
        li   x10, 2584
        li   x11, -2249
        li   x12, 2782
        li   x13, -1761
        li   x14, 2788
        li   x15, -679
        lhu x11, 6(x20)
        add  x8, x11, x8
        lw x5, 252(x20)
        slt x2, x6, x1
        blt x2, x4, L1
        addi x3, x8, -14
        addi x5, x2, 23
        addi x3, x6, 11
L1:
        sra x3, x5, x13
        or x3, x4, x5
        xori x6, x3, 1512
        or x1, x8, x8
        addi x6, x13, 1034
        slti x7, x5, 434
        andi x2, x11, -1908
        bltu x7, x7, L2
        addi x7, x6, -10
        addi x1, x1, 11
L2:
        addi x4, x9, -303
        li   x16, 2
L3:
        add x2, x1, x8
        addi x16, x16, -1
        bnez x16, L3
        slt x2, x2, x2
        srai x5, x8, 29
        lbu x4, 209(x20)
        add  x8, x4, x5
        li   x16, 2
L4:
        sra x2, x4, x8
        sub x7, x10, x10
        slt x8, x3, x15
        addi x16, x16, -1
        bnez x16, L4
        or x4, x5, x4
        blt x8, x1, L5
        addi x5, x6, -21
L5:
        sh x8, 200(x20)
        sh x7, 230(x20)
        sub x1, x14, x11
        sh x13, 32(x20)
        lh x11, 108(x20)
        bltu x6, x8, L6
        addi x3, x3, -2
        addi x2, x1, -19
L6:
        xori x13, x4, 820
        li   x16, 1
L7:
        and x4, x4, x7
        or x5, x7, x8
        addi x16, x16, -1
        bnez x16, L7
        ori x4, x3, -2021
        li   x16, 2
L8:
        sub x4, x14, x6
        sra x1, x8, x3
        and x5, x4, x2
        addi x16, x16, -1
        bnez x16, L8
        sra x4, x4, x7
        sra x10, x2, x1
        sra x3, x6, x3
        ori x5, x4, -1229
        sw x2, 152(x20)
        bne x4, x10, L9
        addi x12, x5, 3
        addi x8, x5, -4
L9:
        lhu x15, 222(x20)
        add  x2, x15, x1
        sw x8, 72(x20)
        lh x5, 16(x20)
        sub x5, x6, x6
        sh x4, 180(x20)
        li   x16, 2
L10:
        or x7, x2, x7
        add x7, x7, x5
        and x6, x1, x3
        addi x16, x16, -1
        bnez x16, L10
        srai x3, x4, 14
        slt x10, x8, x15
        ori x4, x9, 1256
        beq x6, x4, L11
        addi x4, x5, -6
        addi x5, x3, -8
L11:
        sll x8, x14, x3
        li   x16, 2
L12:
        add x7, x7, x3
        or x5, x3, x3
        addi x16, x16, -1
        bnez x16, L12
        jal  x18, F13
        j    E13
F13:   add x2, x2, x4
        jalr x0, 0(x18)
E13:
        bgeu x7, x11, L14
        addi x6, x2, -44
        addi x6, x3, 9
L14:
        andi x2, x6, 110
        and x8, x10, x2
        add x5, x8, x3
        lbu x3, 100(x20)
        add  x1, x3, x2
        srai x1, x2, 0
        lb x7, 32(x20)
        add  x2, x7, x7
        jal  x18, F15
        j    E15
F15:   or x1, x6, x3
        jalr x0, 0(x18)
E15:
        and x4, x5, x5
        sltu x7, x6, x7
        li   x16, 4
L16:
        and x5, x3, x3
        sltu x2, x5, x8
        addi x16, x16, -1
        bnez x16, L16
        and x7, x6, x8
        sb x7, 221(x20)
        xor x6, x3, x7
        sltiu x5, x4, -730
        blt x6, x8, L17
        addi x6, x11, -29
        addi x5, x8, 38
        addi x5, x2, 32
L17:
        bne x5, x5, L18
        addi x7, x12, -4
        addi x7, x2, -21
        addi x7, x4, -20
L18:
        add x15, x3, x7
        slti x7, x8, 1624
        sub x2, x8, x5
        sltu x5, x10, x13
        slti x8, x3, 151
        sltu x1, x3, x5
        andi x7, x1, 1541
        slti x13, x6, -916
        add x6, x7, x3
        andi x1, x14, -1173
        lh x2, 254(x20)
        jal  x18, F19
        j    E19
F19:   add x6, x1, x8
        jalr x0, 0(x18)
E19:
        blt x3, x6, L20
        addi x5, x5, 27
        addi x2, x9, -12
        addi x13, x7, 0
L20:
        xori x1, x6, 156
        xori x5, x6, 1969
        sra x7, x8, x4
        li   x16, 2
L21:
        sll x1, x7, x5
        slt x1, x6, x2
        addi x16, x16, -1
        bnez x16, L21
        lw x1, 172(x20)
        slt x12, x4, x5
        sub x8, x8, x2
        sll x2, x8, x1
        xor x7, x6, x2
        sw x5, 96(x20)
        or x8, x8, x14
        xori x3, x11, 1069
        bge x5, x6, L22
        addi x8, x6, 8
L22:
        sh x1, 26(x20)
        slti x13, x7, 1339
        lw x5, 40(x20)
        and x6, x6, x3
        slti x13, x7, 1612
        ori x4, x5, -1948
        lb x8, 214(x20)
        add  x1, x8, x9
        lh x5, 86(x20)
        li   x16, 3
L23:
        slt x8, x1, x4
        srl x2, x3, x7
        xor x15, x5, x7
        addi x16, x16, -1
        bnez x16, L23
        add x2, x14, x7
        lw x3, 168(x20)
        srai x1, x4, 20
        ori x7, x6, -1076
        lb x4, 148(x20)
        sh x1, 148(x20)
        and x1, x8, x9
        sub x2, x5, x5
        sh x5, 220(x20)
        ori x12, x2, 53
        slti x7, x1, -1172
        sub x9, x8, x6
        slt x7, x7, x2
        bne x4, x7, L24
        addi x5, x10, 23
        addi x2, x3, -33
        addi x8, x7, 32
L24:
        bgeu x8, x6, L25
        addi x5, x3, 32
        addi x5, x5, -26
        addi x13, x3, -3
L25:
        lhu x3, 232(x20)
        add  x1, x3, x2
        addi x8, x6, 2046
        slt x5, x5, x3
        xor x7, x1, x3
        ebreak
