# random program, seed 0
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 155
        li   x2, 445
        li   x3, -2669
        li   x4, -879
        li   x5, 1188
        li   x6, 980
        li   x7, 317
        li   x8, -516
        li   x9, 904
        li   x10, -67
        li   x11, 1779
        li   x12, -1211
        li   x13, 1134
        li   x14, -1860
        li   x15, -692
        sub x5, x9, x13
        lui x2, 692473
        addi x6, x4, 1859
        slti x1, x7, -2039
        auipc x6, 132087
        sra x3, x8, x6
        bge x5, x9, L1
        addi x9, x5, 6
        addi x7, x4, -13
L1:
        and x5, x2, x3
        beq x15, x7, L2
        addi x4, x15, 36
        addi x7, x8, 13
        addi x6, x2, 12
L2:
        srli x4, x5, 7
        lw x1, 188(x20)
        add  x4, x1, x2
        or x2, x6, x2
        add x3, x8, x1
        li   x16, 1
L3:
        sltu x5, x2, x6
        sltu x8, x2, x7
        or x8, x15, x4
        addi x16, x16, -1
        bnez x16, L3
        li   x16, 1
L4:
        and x6, x2, x8
        and x7, x14, x5
        slt x5, x1, x2
        addi x16, x16, -1
        bnez x16, L4
        add x3, x8, x5
        lbu x7, 66(x20)
        sra x6, x4, x7
        lw x7, 212(x20)
        lhu x3, 84(x20)
        add  x15, x3, x1
        bge x8, x7, L5
        addi x2, x3, -49
L5:
        sltiu x1, x1, -1247
        sra x5, x3, x7
        lh x2, 10(x20)
        srl x11, x3, x1
        or x6, x10, x1
        sb x3, 255(x20)
        sra x3, x6, x6
        lb x3, 172(x20)
        add  x6, x3, x3
        sll x15, x3, x12
        sltu x5, x2, x8
        ori x2, x7, -1739
        and x11, x2, x2
        or x1, x5, x8
        sb x5, 108(x20)
        slli x6, x1, 28
        sw x5, 100(x20)
        add x13, x3, x8
        slti x2, x8, -833
        srai x8, x6, 31
        la   x17, F6
        jalr x18, 0(x17)
        j    E6
F6:   or x4, x6, x1
        jalr x0, 0(x18)
E6:
        ori x3, x10, 363
        lw x9, 240(x20)
        or x5, x8, x3
        sh x9, 234(x20)
        sub x2, x15, x5
        slti x8, x7, -135
        beq x1, x5, L7
        addi x6, x5, -12
        addi x7, x1, -30
        addi x3, x6, -43
L7:
        li   x16, 4
L8:
        and x2, x3, x6
        sltu x8, x1, x3
        addi x16, x16, -1
        bnez x16, L8
        sra x6, x6, x8
        add x8, x6, x5
        sb x14, 66(x20)
        li   x16, 1
L9:
        or x7, x4, x2
        add x1, x1, x11
        sra x4, x7, x2
        addi x16, x16, -1
        bnez x16, L9
        sra x2, x7, x7
        sb x1, 15(x20)
        ori x2, x2, 895
        lh x4, 176(x20)
        and x4, x2, x5
        addi x4, x3, 1671
        slt x5, x4, x8
        li   x16, 3
L10:
        slt x2, x5, x3
        and x6, x4, x5
        slt x1, x10, x2
        addi x16, x16, -1
        bnez x16, L10
        lhu x3, 66(x20)
        add  x6, x3, x8
        lhu x6, 30(x20)
        add  x8, x6, x3
        sw x3, 140(x20)
        sb x7, 229(x20)
        sll x3, x2, x4
        sll x1, x2, x11
        sra x8, x8, x4
        xori x1, x1, -2046
        srl x12, x2, x6
        or x1, x5, x6
        or x13, x7, x5
        slti x4, x7, 1256
        lh x3, 142(x20)
        add  x7, x3, x8
        xor x8, x4, x6
        addi x3, x1, -281
        sll x1, x2, x2
        lw x2, 200(x20)
        la   x17, F11
        jalr x18, 0(x17)
        j    E11
F11:   xor x4, x5, x7
        jalr x0, 0(x18)
E11:
        ori x6, x7, -836
        sltiu x6, x3, 1590
        sltu x8, x4, x8
        li   x16, 1
L12:
        add x2, x6, x3
        or x2, x9, x13
        addi x16, x16, -1
        bnez x16, L12
        blt x1, x7, L13
        addi x5, x4, -7
        addi x1, x6, -50
        addi x1, x7, 37
L13:
        sra x4, x6, x2
        sb x1, 166(x20)
        sub x6, x4, x5
        sltu x6, x4, x2
        sll x1, x7, x8
        addi x2, x3, 1343
        bne x2, x9, L14
        addi x3, x4, -34
        addi x5, x6, 5
L14:
        xor x4, x13, x8
        ori x1, x2, -635
        lw x1, 124(x20)
        addi x5, x6, -168
        lw x15, 144(x20)
        add  x6, x15, x8
        and x1, x6, x1
        sw x9, 200(x20)
        jal  x18, F15
        j    E15
F15:   or x13, x4, x3
        jalr x0, 0(x18)
E15:
        sh x2, 196(x20)
        lui x6, 1025924
        addi x9, x8, 1891
        sltiu x5, x7, -483
        sb x6, 148(x20)
        lh x4, 126(x20)
        add  x5, x4, x1
        lh x1, 76(x20)
        add  x4, x1, x6
        add x7, x4, x3
        andi x7, x7, 112
        sltiu x12, x1, -1044
        xori x3, x3, -1396
        and x1, x15, x3
        lb x8, 216(x20)
        lui x7, 57183
        lhu x3, 16(x20)
        add  x3, x3, x7
        sll x1, x5, x1
        sw x2, 132(x20)
        xori x5, x1, 32
        lbu x9, 149(x20)
        add  x5, x9, x6
        sh x15, 124(x20)
        add x1, x6, x5
        ebreak
