# random program, seed 8
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1143
        li   x2, 34
        li   x3, 75
        li   x4, -1966
        li   x5, -1418
        li   x6, 2773
        li   x7, -2642
        li   x8, -2303
        li   x9, -1879
        li   x10, -973
        li   x11, 1148
        li   x12, -1285
        li   x13, 282
        li   x14, 2258
        li   x15, -2752
        xori x4, x7, -1315
        addi x9, x7, -1117
        lw x7, 48(x20)
        add  x4, x7, x8
        bltu x10, x10, L1
        addi x1, x4, -32
L1:
        li   x16, 4
L2:
        sra x5, x7, x2
        srl x6, x14, x4
        xor x5, x2, x14
        addi x16, x16, -1
        bnez x16, L2
        sltiu x6, x1, 374
        xor x5, x7, x7
        add x3, x1, x7
        and x4, x8, x2
        srli x1, x2, 23
        srl x3, x2, x3
        sra x5, x6, x8
        sra x3, x7, x2
        or x8, x7, x8
        lb x8, 224(x20)
        add  x8, x8, x4
        sub x1, x10, x11
        xori x4, x6, 1098
        lw x5, 100(x20)
        lw x2, 204(x20)
        add  x6, x2, x12
        bltu x6, x5, L3
        addi x4, x7, 24
        addi x5, x7, 28
        addi x6, x10, 24
L3:
        xori x2, x2, 2033
        lhu x5, 136(x20)
        srl x7, x4, x13
        xori x4, x2, -1134
        sltiu x7, x13, -928
        or x2, x8, x15
        sra x6, x11, x1
        sw x6, 40(x20)
        jal  x18, F4
        j    E4
F4:   or x10, x4, x6
        jalr x0, 0(x18)
E4:
        li   x16, 1
L5:
        sub x10, x3, x7
        and x2, x4, x3
        slt x2, x1, x3
        addi x16, x16, -1
        bnez x16, L5
        sh x8, 164(x20)
        sub x15, x4, x7
        and x1, x8, x5
        xori x6, x8, 954
        lh x8, 94(x20)
        sb x10, 142(x20)
        andi x11, x5, 1180
        slt x5, x1, x3
        sw x8, 4(x20)
        slli x14, x2, 23
        jal  x18, F6
        j    E6
F6:   sra x6, x6, x6
        jalr x0, 0(x18)
E6:
        lw x8, 244(x20)
        add  x6, x8, x7
        sltiu x3, x11, 517
        or x8, x3, x5
        sh x5, 226(x20)
        sll x2, x8, x2
        slti x6, x7, -384
        sltiu x3, x1, -1324
        sltiu x4, x7, 28
        li   x16, 2
L7:
        add x4, x1, x12
        addi x16, x16, -1
        bnez x16, L7
        and x5, x4, x2
        addi x11, x4, 1896
        bgeu x7, x7, L8
        addi x3, x6, 26
        addi x1, x4, -47
        addi x8, x3, -22
L8:
        xor x5, x7, x12
        lw x8, 108(x20)
        add  x4, x8, x2
        slti x9, x8, 940
        lui x4, 706364
        lui x4, 892657
        lh x5, 100(x20)
        add  x3, x5, x7
        sb x2, 162(x20)
        sll x1, x4, x1
        li   x16, 3
L9:
        sll x2, x2, x8
        xor x1, x2, x6
        addi x16, x16, -1
        bnez x16, L9
        ori x10, x8, 203
        lhu x4, 30(x20)
        sltiu x1, x7, 1628
        sltiu x2, x3, 652
        lb x3, 204(x20)
        add  x15, x3, x6
        addi x5, x4, 1816
        sltiu x8, x2, 346
        sltu x2, x8, x4
        lw x1, 224(x20)
        add  x8, x1, x2
        ori x2, x8, 1428
        slli x3, x3, 24
        ori x7, x7, 1803
        li   x16, 4
L10:
        sub x4, x5, x3
        addi x16, x16, -1
        bnez x16, L10
        srl x6, x6, x3
        slti x7, x5, -931
        add x3, x3, x8
        srl x8, x2, x8
        xori x5, x1, -1216
        sra x7, x5, x12
        sltiu x2, x1, -1908
        sub x4, x6, x6
        sw x4, 180(x20)
        ori x7, x1, -1125
        sw x4, 160(x20)
        la   x17, F11
        jalr x18, 0(x17)
        j    E11
F11:   slt x3, x6, x13
        jalr x0, 0(x18)
E11:
        sw x5, 152(x20)
        lb x5, 8(x20)
        add  x4, x5, x1
        lh x5, 66(x20)
        add  x5, x5, x11
        sll x4, x15, x6
        sw x6, 132(x20)
        beq x1, x7, L12
        addi x10, x1, 38
        addi x1, x14, -8
        addi x4, x9, 22
L12:
        li   x16, 4
L13:
        xor x7, x2, x9
        slt x8, x1, x14
        addi x16, x16, -1
        bnez x16, L13
        bgeu x4, x7, L14
        addi x5, x1, -12
        addi x7, x8, -8
L14:
        sra x3, x3, x3
        sw x11, 96(x20)
        slti x2, x5, 361
        sll x2, x5, x11
        sra x3, x1, x6
        xor x1, x11, x13
        addi x8, x7, -191
        lb x7, 187(x20)
        add  x2, x7, x6
        srl x8, x5, x15
        add x7, x1, x4
        addi x3, x8, 1996
        bgeu x1, x5, L15
        addi x6, x6, 14
L15:
        bge x4, x4, L16
        addi x2, x5, 2
        addi x11, x6, 3
L16:
        lhu x8, 178(x20)
        add  x6, x8, x7
        sll x4, x2, x1
        sw x4, 16(x20)
        xori x2, x6, 440
        slti x5, x3, 1249
        sw x4, 12(x20)
        lb x14, 109(x20)
        xor x3, x4, x5
        xori x3, x8, -1162
        sb x2, 180(x20)
        xor x3, x7, x7
        srl x3, x11, x12
        ebreak
