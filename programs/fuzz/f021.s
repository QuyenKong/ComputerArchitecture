# random program, seed 21
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1649
        li   x2, 424
        li   x3, 2650
        li   x4, 424
        li   x5, 2201
        li   x6, -696
        li   x7, 924
        li   x8, -1231
        li   x9, 888
        li   x10, 1198
        li   x11, -1497
        li   x12, 1137
        li   x13, 1321
        li   x14, -1067
        li   x15, -2974
        sra x3, x4, x12
        sltu x1, x9, x2
        lw x2, 188(x20)
        add  x8, x2, x6
        andi x1, x4, -1437
        sw x8, 104(x20)
        srli x3, x7, 18
        xori x6, x7, 128
        sub x8, x2, x4
        srli x2, x3, 22
        sh x3, 170(x20)
        and x6, x1, x4
        andi x10, x6, 1973
        sltiu x4, x2, 1550
        sw x1, 244(x20)
        bgeu x7, x7, L1
        addi x11, x3, 45
L1:
        lh x9, 24(x20)
        andi x6, x15, 972
        auipc x8, 645875
        sra x1, x3, x1
        slt x7, x7, x13
        bne x7, x1, L2
        addi x3, x2, 33
        addi x5, x6, 0
        addi x4, x3, -27
L2:
        bne x9, x10, L3
        addi x1, x1, -1
        addi x2, x3, 41
        addi x6, x4, -1
L3:
        xor x13, x2, x1
        sltiu x5, x4, -1526
        auipc x6, 136975
        sltu x2, x8, x1
        lhu x2, 226(x20)
        add  x7, x2, x5
        lbu x4, 207(x20)
        add  x4, x4, x2
        and x4, x11, x5
        sll x7, x12, x1
        or x7, x2, x2
        slti x12, x2, -685
        lbu x4, 106(x20)
        add  x6, x4, x3
        bltu x5, x3, L4
        addi x7, x5, 35
        addi x7, x2, -26
L4:
        jal  x18, F5
        j    E5
F5:   slt x15, x6, x1
        jalr x0, 0(x18)
E5:
        xori x4, x9, -837
        xor x6, x6, x7
        addi x7, x4, -204
        srai x15, x11, 4
        or x8, x10, x8
        sltiu x5, x5, 393
        lw x3, 4(x20)
        add  x4, x3, x6
        add x5, x7, x2
        slt x7, x4, x9
        ori x4, x6, -622
        slt x3, x8, x15
        add x2, x7, x8
        li   x16, 3
L6:
        slt x5, x7, x3
        addi x16, x16, -1
        bnez x16, L6
        srl x7, x5, x12
        sw x3, 184(x20)
        sltiu x6, x1, 1416
        li   x16, 1
L7:
        or x4, x9, x5
        sub x7, x8, x13
        or x5, x7, x8
        addi x16, x16, -1
        bnez x16, L7
        srl x4, x6, x5
        lw x7, 112(x20)
        add  x14, x7, x8
        or x9, x8, x1
        andi x8, x8, -1469
        beq x5, x8, L8
        addi x4, x6, -41
L8:
        lbu x5, 125(x20)
        add  x4, x5, x3
        sltiu x1, x6, 968
        and x5, x7, x1
        jal  x18, F9
        j    E9
F9:   sll x6, x1, x6
        jalr x0, 0(x18)
E9:
        sltu x11, x4, x4
        sll x13, x2, x3
        xor x6, x1, x4
        sra x3, x2, x2
        lw x4, 60(x20)
        add  x4, x4, x2
        sltu x1, x6, x11
        xori x8, x7, 1901
        sub x5, x12, x3
        slt x5, x5, x5
        srli x3, x3, 19
        sub x8, x1, x7
        addi x8, x6, -423
        xor x7, x1, x4
        or x6, x4, x8
        slt x7, x3, x8
        slt x14, x5, x2
        bne x5, x7, L10
        addi x1, x5, -16
L10:
        sra x4, x14, x4
        sb x11, 97(x20)
        bge x5, x9, L11
        addi x1, x3, 8
        addi x8, x6, -36
L11:
        sra x8, x5, x7
        li   x16, 1
L12:
        slt x7, x15, x6
        xor x3, x6, x3
        addi x16, x16, -1
        bnez x16, L12
        sw x6, 140(x20)
        slt x1, x1, x4
        sw x4, 164(x20)
        xor x6, x7, x5
        lw x4, 20(x20)
        add  x4, x4, x2
        auipc x3, 391881
        lw x15, 224(x20)
        add  x9, x15, x3
        sw x1, 60(x20)
        la   x17, F13
        jalr x18, 0(x17)
        j    E13
F13:   add x2, x8, x7
        jalr x0, 0(x18)
E13:
        slti x13, x5, -521
        srai x4, x3, 10
        bgeu x5, x7, L14
        addi x6, x1, -40
        addi x4, x8, -13
        addi x4, x8, -15
L14:
        sh x4, 162(x20)
        lw x3, 132(x20)
        add  x5, x3, x8
        slti x5, x2, 353
        slli x3, x4, 27
        lh x1, 200(x20)
        li   x16, 4
L15:
        xor x11, x7, x4
        addi x16, x16, -1
        bnez x16, L15
        slt x6, x1, x3
        li   x16, 2
L16:
        sub x4, x3, x2
        addi x16, x16, -1
        bnez x16, L16
        add x8, x10, x3
        li   x16, 4
L17:
        sll x3, x7, x8
        and x7, x4, x3
        addi x16, x16, -1
        bnez x16, L17
        slt x7, x6, x8
        sltu x5, x8, x2
        xori x8, x15, -1581
        sltiu x13, x12, 125
        xor x7, x7, x6
        bne x5, x5, L18
        addi x2, x2, 35
        addi x8, x8, -10
        addi x7, x4, 17
L18:
        and x2, x7, x7
        slti x3, x7, 1992
        or x4, x4, x7
        srai x2, x5, 5
        sw x4, 136(x20)
        bge x1, x8, L19
        addi x1, x3, -46
        addi x9, x7, -10
        addi x8, x15, -40
L19:
        srli x11, x6, 19
        add x3, x5, x3
        slti x1, x5, 1495
        ebreak
