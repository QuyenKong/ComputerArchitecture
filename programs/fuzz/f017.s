# random program, seed 17
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 1276
        li   x2, 392
        li   x3, -515
        li   x4, -5
        li   x5, -628
        li   x6, -1569
        li   x7, 2776
        li   x8, 2768
        li   x9, 1425
        li   x10, 2418
        li   x11, -721
        li   x12, -2098
        li   x13, -2780
        li   x14, -961
        li   x15, 147
        sh x7, 214(x20)
        srl x4, x4, x2
        bgeu x7, x8, L1
        addi x3, x7, 14
        addi x1, x1, 46
        addi x1, x6, 24
L1:
        sw x4, 204(x20)
        li   x16, 3
L2:
        xor x5, x3, x5
        addi x16, x16, -1
        bnez x16, L2
        blt x2, x10, L3
        addi x1, x6, -48
        addi x5, x1, 43
L3:
        xor x8, x3, x7
        xor x11, x4, x5
        sh x7, 160(x20)
        xor x11, x8, x2
        andi x5, x5, -1645
        lb x4, 251(x20)
        add  x8, x4, x8
        sb x6, 118(x20)
        srai x7, x6, 10
        bltu x6, x4, L4
        addi x8, x2, 16
        addi x3, x8, 14
L4:
        srl x1, x3, x14
        blt x4, x2, L5
        addi x1, x8, 40
        addi x10, x2, 49
        addi x14, x8, 18
L5:
        sw x13, 112(x20)
        add x1, x5, x6
        li   x16, 4
L6:
        add x6, x1, x5
        slt x6, x4, x14
        addi x16, x16, -1
        bnez x16, L6
        sub x2, x5, x8
        andi x3, x2, 1522
        xori x10, x3, -880
        srl x8, x15, x7
        or x3, x7, x8
        sh x4, 64(x20)
        sltiu x8, x2, 1050
        sub x2, x8, x3
        lhu x9, 158(x20)
        sltiu x5, x4, 977
        sb x5, 222(x20)
        sltiu x6, x1, 835
        lhu x5, 250(x20)
        add  x3, x5, x4
        slt x12, x4, x14
        xori x6, x13, -1024
        li   x16, 4
L7:
        sll x2, x7, x4
        sltu x6, x12, x6
        sltu x14, x1, x7
        addi x16, x16, -1
        bnez x16, L7
        bgeu x3, x5, L8
        addi x3, x1, -35
        addi x1, x5, 28
L8:
        lbu x1, 159(x20)
        srl x2, x5, x6
        bne x2, x6, L9
        addi x8, x4, -49
        addi x2, x3, -2
L9:
        srl x1, x2, x8
        or x8, x5, x2
        sb x5, 69(x20)
        slt x7, x1, x2
        bltu x12, x1, L10
        addi x8, x2, 42
        addi x14, x2, 36
L10:
        add x14, x10, x5
        lw x7, 40(x20)
        xori x5, x7, -989
        sh x8, 112(x20)
        or x4, x8, x7
        xori x4, x4, -2002
        xor x6, x7, x9
        slli x6, x6, 11
        jal  x18, F11
        j    E11
F11:   sra x4, x10, x8
        jalr x0, 0(x18)
E11:
        add x8, x8, x1
        bne x7, x4, L12
        addi x1, x8, -9
L12:
        or x12, x8, x3
        sll x2, x5, x5
        addi x5, x9, -310
        add x1, x6, x3
        sra x10, x1, x14
        lhu x8, 210(x20)
        add  x1, x8, x2
        lb x3, 147(x20)
        slt x3, x14, x6
        slti x5, x7, -280
        sra x5, x5, x6
        slt x5, x2, x2
        addi x6, x8, 554
        bge x8, x10, L13
        addi x7, x4, 20
L13:
        bne x11, x4, L14
        addi x5, x6, 7
        addi x6, x5, -15
L14:
        sll x8, x1, x3
        sltiu x4, x1, 1915
        sra x11, x5, x5
        lw x2, 16(x20)
        sh x15, 200(x20)
        bgeu x5, x5, L15
        addi x14, x5, 30
        addi x1, x12, -22
        addi x3, x1, -10
L15:
        sw x5, 188(x20)
        slli x6, x5, 17
        la   x17, F16
        jalr x18, 0(x17)
        j    E16
F16:   srl x4, x5, x3
        jalr x0, 0(x18)
E16:
        slti x5, x3, -1293
        or x6, x5, x1
        sltu x8, x3, x6
        sltiu x7, x1, -1097
        slt x4, x4, x2
        sw x3, 108(x20)
        sltiu x5, x2, 1917
        bgeu x7, x6, L17
        addi x4, x5, -1
        addi x5, x7, 31
        addi x4, x1, -26
L17:
        slt x5, x7, x5
        lw x5, 80(x20)
        add  x4, x5, x8
        li   x16, 2
L18:
        or x4, x2, x7
        addi x16, x16, -1
        bnez x16, L18
        add x3, x1, x6
        bge x2, x12, L19
        addi x7, x6, -20
        addi x3, x7, -46
L19:
        sltu x1, x6, x7
        lh x1, 190(x20)
        add  x3, x1, x6
        sra x1, x4, x2
        add x3, x6, x6
        sw x10, 12(x20)
        li   x16, 2
L20:
        sltu x9, x6, x14
        addi x16, x16, -1
        bnez x16, L20
        xor x8, x13, x4
        andi x3, x8, 2011
        sltiu x2, x3, 175
        add x3, x1, x3
        sw x1, 68(x20)
        xor x5, x5, x4
        addi x5, x6, 2030
        andi x8, x1, 1879
        sub x7, x5, x8
        bgeu x7, x6, L21
        addi x8, x1, -11
L21:
        jal  x18, F22
        j    E22
F22:   xor x5, x9, x7
        jalr x0, 0(x18)
E22:
        andi x2, x2, 727
        and x5, x4, x4
        sltiu x7, x8, 1729
        bltu x15, x15, L23
        addi x7, x6, -44
        addi x4, x1, -39
L23:
        xori x4, x7, -160
        slti x10, x7, -807
        lw x8, 164(x20)
        slt x5, x5, x14
        sll x1, x7, x5
        li   x16, 2
L24:
        srl x7, x4, x7
        addi x16, x16, -1
        bnez x16, L24
        blt x7, x5, L25
        addi x6, x4, -40
L25:
        ebreak
