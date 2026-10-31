# random program, seed 1
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1900
        li   x2, 1662
        li   x3, -2484
        li   x4, -911
        li   x5, -2035
        li   x6, 1058
        li   x7, 682
        li   x8, 868
        li   x9, 2337
        li   x10, 109
        li   x11, -1281
        li   x12, -2232
        li   x13, 996
        li   x14, -2768
        li   x15, 193
        addi x5, x4, -1211
        beq x1, x7, L1
        addi x7, x9, -22
        addi x8, x6, -21
        addi x8, x15, -48
L1:
        slti x2, x5, -1058
        lb x8, 217(x20)
        slti x8, x7, 1346
        lb x2, 186(x20)
        xori x1, x5, 1176
        lb x13, 85(x20)
        add  x9, x13, x6
        li   x16, 3
L2:
        xor x1, x3, x4
        sltu x8, x10, x7
        addi x16, x16, -1
        bnez x16, L2
        ori x1, x6, 1705
        slli x3, x13, 16
        sub x1, x5, x2
        sh x3, 94(x20)
        and x5, x6, x2
        sltu x4, x5, x9
        la   x17, F3
        jalr x18, 0(x17)
        j    E3
F3:   sltu x1, x7, x3
        jalr x0, 0(x18)
E3:
        slti x4, x11, 1645
        add x6, x7, x5
        or x5, x2, x5
        lb x1, 214(x20)
        add  x8, x1, x1
        ori x7, x8, -1193
        li   x16, 4
L4:
        srl x6, x7, x1
        and x6, x10, x6
        addi x16, x16, -1
        bnez x16, L4
        ori x7, x6, 1921
        sw x2, 120(x20)
        and x4, x6, x5
        ori x4, x10, 1956
        srl x6, x2, x3
        sw x7, 172(x20)
        srl x2, x6, x10
        addi x5, x1, 374
        add x2, x13, x4
        sw x3, 212(x20)
        lbu x7, 80(x20)
        ori x8, x4, 552
        add x15, x6, x6
        addi x10, x2, 0
        sra x15, x8, x5
        or x4, x5, x8
        sra x4, x5, x3
        sra x5, x2, x2
        add x7, x2, x1
        lh x3, 150(x20)
        add  x6, x3, x3
        and x14, x5, x5
        or x1, x14, x13
        lw x3, 104(x20)
        add  x4, x3, x2
        lhu x8, 230(x20)
        add  x3, x8, x1
        sw x6, 212(x20)
        srai x5, x5, 25
        slli x4, x3, 20
        sltiu x15, x4, -96
        sll x12, x5, x4
        sub x11, x3, x4
        xor x6, x8, x2
        bltu x3, x7, L5
        addi x12, x1, 13
L5:
        lhu x1, 176(x20)
        add  x5, x1, x5
        lw x10, 40(x20)
        lhu x7, 40(x20)
        bge x6, x8, L6
        addi x7, x11, -13
L6:
        sltu x1, x9, x1
        sra x5, x5, x4
        sra x14, x3, x8
        addi x10, x4, 278
        sw x1, 12(x20)
        sltiu x11, x6, 501
        sltiu x6, x8, 1634
        slti x8, x7, 1084
        add x11, x4, x8
        auipc x12, 640337
        lb x1, 229(x20)
        srli x2, x4, 18
        lbu x7, 209(x20)
        sw x5, 36(x20)
        sh x5, 208(x20)
        xori x5, x7, -1477
        sltiu x3, x3, -1286
        sltiu x5, x4, -105
        blt x6, x1, L7
        addi x5, x4, 0
L7:
        slli x5, x6, 14
        sra x14, x7, x7
        li   x16, 2
L8:
        or x3, x10, x3
        sra x8, x3, x15
        addi x16, x16, -1
        bnez x16, L8
        lh x4, 186(x20)
        sub x6, x2, x1
        sra x4, x8, x14
        lh x3, 226(x20)
        add  x8, x3, x3
        jal  x18, F9
        j    E9
F9:   xor x7, x5, x2
        jalr x0, 0(x18)
E9:
        beq x1, x6, L10
        addi x5, x7, -30
        addi x13, x1, -49
L10:
        sltiu x7, x2, 1743
        lw x1, 152(x20)
        add  x5, x1, x7
        add x3, x11, x4
        lh x11, 198(x20)
        sra x10, x7, x1
        bltu x4, x9, L11
        addi x2, x12, 28
        addi x13, x3, -38
L11:
        or x14, x2, x9
        ori x6, x1, 1583
        lbu x5, 203(x20)
        add  x2, x5, x7
        xor x3, x7, x14
        lhu x4, 48(x20)
        add  x7, x4, x10
        andi x8, x1, 338
        lh x2, 102(x20)
        add  x2, x2, x6
        ori x6, x9, -1978
        andi x6, x10, -1485
        ori x6, x7, -1408
        beq x8, x5, L12
        addi x12, x6, 1
L12:
        sra x9, x1, x4
        slli x7, x10, 3
        sw x2, 136(x20)
        lw x4, 40(x20)
        sltu x6, x8, x5
        or x4, x6, x4
        sh x7, 38(x20)
        xori x7, x8, -1996
        xor x1, x5, x6
        la   x17, F13
        jalr x18, 0(x17)
        j    E13
F13:   sra x5, x7, x5
        jalr x0, 0(x18)
E13:
        andi x3, x3, 22
        lbu x7, 216(x20)
        add  x1, x7, x15
        add x8, x6, x8
        sb x3, 196(x20)
        addi x14, x3, 304
        li   x16, 4
L14:
        srl x7, x7, x8
        or x8, x7, x2
        addi x16, x16, -1
        bnez x16, L14
        or x4, x2, x8
        ebreak
