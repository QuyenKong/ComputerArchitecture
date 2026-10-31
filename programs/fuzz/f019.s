# random program, seed 19
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 2547
        li   x2, -2646
        li   x3, 1263
        li   x4, -2012
        li   x5, 1190
        li   x6, -1366
        li   x7, 223
        li   x8, -156
        li   x9, 1335
        li   x10, -630
        li   x11, 1789
        li   x12, -1786
        li   x13, 1874
        li   x14, -862
        li   x15, -2118
        slt x14, x6, x1
        slli x15, x8, 24
        beq x7, x7, L1
        addi x5, x3, 31
        addi x4, x10, 43
L1:
        or x3, x8, x8
        sll x10, x8, x8
        slti x15, x2, -1836
        xori x5, x8, 276
        ori x8, x5, -1677
        xor x7, x2, x8
        lw x5, 8(x20)
        add  x7, x5, x8
        sb x3, 100(x20)
        sltu x5, x15, x6
        li   x16, 2
L2:
        srl x1, x11, x2
        or x8, x3, x13
        addi x16, x16, -1
        bnez x16, L2
        ori x5, x5, 1468
        sw x8, 28(x20)
        beq x2, x8, L3
        addi x6, x3, 6
        addi x6, x2, 31
        addi x8, x1, -4
L3:
        sltu x6, x5, x4
        andi x2, x9, -1303
        bltu x3, x4, L4
        addi x14, x4, -32
        addi x2, x8, -34
        addi x8, x7, 24
L4:
        sub x5, x8, x4
        srli x8, x4, 4
        xori x8, x8, -1641
        addi x5, x2, 1226
        andi x4, x3, 1863
        sltu x2, x1, x14
        sh x7, 40(x20)
        sll x1, x3, x1
        sll x6, x3, x9
        li   x16, 1
L5:
        sub x2, x2, x2
        addi x16, x16, -1
        bnez x16, L5
        sh x5, 250(x20)
        li   x16, 1
L6:
        add x3, x6, x5
        sll x4, x3, x7
        slt x8, x1, x13
        addi x16, x16, -1
        bnez x16, L6
        sltiu x3, x7, -656
        lw x3, 32(x20)
        slti x2, x9, 1533
        or x3, x4, x14
        li   x16, 3
L7:
        sltu x2, x7, x1
        sra x8, x5, x8
        addi x16, x16, -1
        bnez x16, L7
        bge x6, x3, L8
        addi x15, x1, 39
        addi x10, x2, 45
        addi x6, x8, 0
L8:
        addi x8, x1, 1904
        sll x3, x3, x14
        srl x5, x15, x7
        lb x4, 117(x20)
        add  x1, x4, x2
        sltiu x8, x7, 1280
        addi x6, x3, -442
        slt x5, x8, x6
        slti x7, x5, -1365
        addi x1, x4, 948
        sra x8, x5, x14
        lw x4, 160(x20)
        sw x12, 12(x20)
        sh x13, 106(x20)
        lui x3, 665196
        li   x16, 2
L9:
        and x2, x12, x6
        xor x5, x3, x6
        sra x1, x7, x5
        addi x16, x16, -1
        bnez x16, L9
        xori x6, x1, -95
        ori x2, x8, 1723
        bltu x2, x7, L10
        addi x7, x2, -36
        addi x4, x13, 17
L10:
        and x7, x9, x6
        sb x1, 79(x20)
        addi x3, x11, 1342
        addi x2, x2, -367
        li   x16, 3
L11:
        sra x3, x15, x4
        and x8, x8, x8
        sll x4, x8, x1
        addi x16, x16, -1
        bnez x16, L11
        sltiu x9, x6, 896
        xori x8, x6, 1699
        sh x4, 96(x20)
        slti x6, x3, -1048
        lui x1, 348016
        slli x7, x6, 11
        add x4, x7, x2
        slt x1, x8, x2
        slt x3, x4, x2
        srai x2, x1, 31
        sra x4, x13, x5
        sltiu x12, x4, -1923
        sra x5, x6, x5
        andi x2, x7, -889
        sra x4, x2, x1
        slti x10, x2, 635
        xor x3, x15, x7
        bge x8, x5, L12
        addi x4, x4, 30
        addi x12, x4, -8
L12:
        slt x7, x2, x5
        slt x3, x2, x14
        srl x7, x6, x1
        lb x4, 166(x20)
        add  x12, x4, x1
        lw x13, 232(x20)
        add  x5, x13, x12
        bgeu x7, x1, L13
        addi x5, x2, -40
        addi x4, x8, 18
L13:
        and x3, x7, x2
        srl x2, x8, x4
        andi x8, x7, 858
        andi x8, x4, -944
        add x3, x5, x3
        sltu x6, x4, x4
        bne x7, x3, L14
        addi x3, x3, -5
L14:
        lb x3, 42(x20)
        add  x5, x3, x2
        sw x4, 220(x20)
        li   x16, 4
L15:
        add x8, x7, x3
        xor x2, x12, x7
        slt x6, x1, x3
        addi x16, x16, -1
        bnez x16, L15
        slt x7, x2, x3
        lb x4, 13(x20)
        sll x14, x8, x2
        sra x8, x8, x2
        sll x12, x3, x8
        or x15, x3, x3
        sll x13, x5, x10
        bne x7, x6, L16
        addi x9, x6, 29
        addi x10, x7, 8
        addi x8, x7, -40
L16:
        addi x14, x6, -1917
        add x8, x3, x8
        lbu x3, 169(x20)
        ori x4, x6, -1918
        xori x5, x8, 897
        sw x4, 80(x20)
        sra x1, x1, x1
        slti x1, x1, 849
        bge x4, x2, L17
        addi x3, x3, 42
        addi x10, x3, -21
        addi x5, x4, -30
L17:
        slti x8, x8, -812
        or x3, x7, x15
        sw x4, 160(x20)
        sltiu x7, x6, -246
        sltiu x7, x14, 1405
        sltu x2, x3, x3
        bltu x6, x2, L18
        addi x8, x7, 40
L18:
        xori x12, x6, 77
        sw x13, 144(x20)
        ebreak
