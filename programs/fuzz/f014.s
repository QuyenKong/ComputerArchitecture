# random program, seed 14
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -2125
        li   x2, 2045
        li   x3, 2755
        li   x4, 2341
        li   x5, 1318
        li   x6, -978
        li   x7, -780
        li   x8, -905
        li   x9, -616
        li   x10, -2406
        li   x11, 2394
        li   x12, 684
        li   x13, -518
        li   x14, 822
        li   x15, 2605
        bge x2, x6, L1
        addi x6, x11, 16
        addi x5, x2, -35
L1:
        slli x4, x7, 25
        srli x2, x11, 7
        srai x3, x12, 31
        andi x4, x5, 37
        sub x2, x7, x2
        sltiu x7, x8, 1718
        slti x5, x4, 1632
        bge x3, x5, L2
        addi x7, x7, -48
        addi x6, x5, -5
        addi x4, x8, -18
L2:
        sub x5, x1, x5
        ori x2, x3, -418
        xor x5, x4, x6
        slt x3, x4, x7
        sltu x6, x1, x7
        ori x2, x1, -896
        sll x7, x2, x6
        xori x4, x3, -848
        or x14, x6, x10
        lb x8, 23(x20)
        add  x6, x8, x2
        beq x2, x14, L3
        addi x2, x5, -45
        addi x7, x3, -50
        addi x8, x8, 41
L3:
        ori x5, x1, -120
        lh x7, 0(x20)
        add  x6, x7, x3
        sra x12, x4, x8
        sub x6, x7, x7
        la   x17, F4
        jalr x18, 0(x17)
        j    E4
F4:   sltu x8, x2, x14
        jalr x0, 0(x18)
E4:
        xor x2, x2, x1
        sra x7, x2, x3
        lbu x6, 233(x20)
        add  x6, x6, x5
        sra x3, x14, x5
        andi x1, x8, 942
        lbu x1, 189(x20)
        add  x3, x1, x4
        blt x10, x6, L5
        addi x6, x7, -36
L5:
        xor x5, x4, x4
        or x5, x2, x2
        slti x2, x9, -68
        srl x7, x2, x8
        sw x10, 40(x20)
        sub x8, x2, x6
        srl x5, x8, x13
        slt x8, x1, x4
        sub x3, x7, x2
        ori x4, x7, -794
        sh x4, 212(x20)
        sub x1, x4, x2
        add x5, x5, x4
        and x5, x1, x7
        lhu x12, 142(x20)
        add  x8, x12, x5
        la   x17, F6
        jalr x18, 0(x17)
        j    E6
F6:   or x5, x8, x1
        jalr x0, 0(x18)
E6:
        slti x7, x6, -1480
        sh x4, 4(x20)
        xori x7, x1, 1222
        srai x2, x4, 30
        li   x16, 4
L7:
        sll x7, x8, x5
        sltu x3, x5, x8
        add x1, x7, x3
        addi x16, x16, -1
        bnez x16, L7
        srai x1, x3, 2
        sub x4, x1, x2
        slli x9, x1, 21
        sra x10, x1, x8
        add x2, x4, x1
        sw x1, 64(x20)
        or x13, x3, x5
        sb x11, 241(x20)
        lb x8, 109(x20)
        add  x3, x8, x7
        and x7, x5, x6
        slt x4, x1, x6
        and x10, x7, x6
        addi x7, x4, 410
        slt x5, x5, x9
        sll x8, x2, x6
        slt x4, x4, x6
        xori x1, x5, 358
        li   x16, 2
L8:
        srl x15, x5, x2
        sub x5, x7, x6
        addi x16, x16, -1
        bnez x16, L8
        lw x3, 72(x20)
        sb x6, 102(x20)
        sb x7, 54(x20)
        la   x17, F9
        jalr x18, 0(x17)
        j    E9
F9:   sll x5, x13, x5
        jalr x0, 0(x18)
E9:
        sltiu x5, x8, 1185
        or x7, x9, x5
        add x5, x2, x1
        li   x16, 1
L10:
        and x2, x3, x9
        or x4, x4, x6
        and x10, x7, x2
        addi x16, x16, -1
        bnez x16, L10
        sll x4, x6, x6
        xor x13, x5, x5
        slti x2, x8, 1200
        sw x1, 144(x20)
        lhu x12, 238(x20)
        add  x7, x12, x15
        lh x5, 66(x20)
        sw x1, 20(x20)
        or x3, x10, x8
        sub x5, x6, x15
        sub x7, x7, x8
        srl x10, x2, x5
        add x6, x10, x2
        sw x3, 208(x20)
        bge x2, x4, L11
        addi x4, x11, -41
        addi x4, x4, 22
L11:
        xor x8, x3, x7
        xor x2, x8, x1
        bne x1, x3, L12
        addi x6, x4, 16
        addi x5, x1, -24
L12:
        sub x4, x6, x8
        sra x4, x8, x8
        lw x6, 56(x20)
        add  x1, x6, x1
        sltu x8, x15, x1
        sb x3, 81(x20)
        xori x5, x15, -1072
        sh x4, 48(x20)
        slti x6, x4, 761
        la   x17, F13
        jalr x18, 0(x17)
        j    E13
F13:   xor x1, x13, x6
        jalr x0, 0(x18)
E13:
        slti x2, x5, -1372
        xori x13, x1, -39
        lw x8, 160(x20)
        xori x3, x3, -661
        sll x7, x2, x8
        bgeu x7, x8, L14
        addi x8, x7, 33
        addi x3, x4, 43
        addi x13, x7, 46
L14:
        srli x2, x3, 4
        sra x4, x13, x7
        add x12, x8, x15
        jal  x18, F15
        j    E15
F15:   sltu x3, x7, x8
        jalr x0, 0(x18)
E15:
        xor x2, x3, x6
        slli x8, x8, 19
        lw x5, 56(x20)
        add  x1, x5, x2
        bge x4, x4, L16
        addi x5, x1, -45
        addi x6, x4, 50
        addi x7, x4, 17
L16:
        sub x9, x12, x4
        ebreak
