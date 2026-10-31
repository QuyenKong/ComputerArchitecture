# random program, seed 22
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1851
        li   x2, -1013
        li   x3, -2807
        li   x4, 2022
        li   x5, 662
        li   x6, -1491
        li   x7, 2750
        li   x8, -2013
        li   x9, 2336
        li   x10, -169
        li   x11, -2348
        li   x12, -1102
        li   x13, -795
        li   x14, -2594
        li   x15, -384
        jal  x18, F1
        j    E1
F1:   srl x7, x1, x1
        jalr x0, 0(x18)
E1:
        srli x3, x10, 3
        lh x5, 168(x20)
        bgeu x5, x11, L2
        addi x1, x1, 3
        addi x9, x7, 0
        addi x3, x6, 0
L2:
        srli x7, x15, 27
        sll x7, x1, x4
        xori x8, x3, -1801
        ori x6, x8, -1746
        and x11, x11, x1
        sub x15, x1, x8
        lb x12, 70(x20)
        addi x6, x2, 72
        li   x16, 1
L3:
        srl x2, x3, x7
        addi x16, x16, -1
        bnez x16, L3
        lw x4, 88(x20)
        add  x4, x4, x8
        bne x2, x4, L4
        addi x3, x7, 29
        addi x4, x11, -2
L4:
        sltu x4, x2, x2
        li   x16, 2
L5:
        slt x8, x5, x8
        addi x16, x16, -1
        bnez x16, L5
        lw x8, 140(x20)
        srl x6, x1, x10
        lb x5, 90(x20)
        add  x3, x5, x8
        lb x6, 69(x20)
        sw x2, 196(x20)
        sltu x1, x3, x6
        bltu x6, x1, L6
        addi x11, x2, -38
L6:
        slli x5, x15, 26
        srai x6, x1, 14
        sh x1, 164(x20)
        slt x1, x2, x8
        sw x7, 88(x20)
        andi x5, x4, 1021
        bge x9, x2, L7
        addi x13, x3, 6
L7:
        or x2, x6, x9
        sltiu x7, x8, 1506
        lhu x11, 26(x20)
        add  x1, x11, x2
        sll x2, x8, x5
        lw x5, 8(x20)
        add  x4, x5, x6
        lb x11, 229(x20)
        srli x4, x4, 17
        lb x4, 21(x20)
        add  x6, x4, x2
        slli x6, x3, 2
        srai x2, x4, 25
        slt x5, x3, x6
        and x3, x5, x8
        sub x5, x8, x6
        and x11, x2, x1
        sh x2, 210(x20)
        sltu x6, x5, x6
        bltu x1, x2, L8
        addi x1, x7, 4
L8:
        sra x8, x5, x3
        li   x16, 1
L9:
        sll x6, x3, x3
        addi x16, x16, -1
        bnez x16, L9
        sub x7, x13, x5
        slt x6, x8, x3
        sltu x5, x6, x1
        sb x3, 233(x20)
        lw x2, 20(x20)
        add  x4, x2, x7
        xor x4, x10, x7
        slt x3, x5, x15
        lh x5, 182(x20)
        slli x4, x6, 16
        sub x4, x10, x5
        sltu x1, x1, x8
        sw x13, 208(x20)
        slt x6, x1, x8
        srl x6, x3, x6
        lb x1, 20(x20)
        add  x9, x1, x2
        slti x2, x8, 876
        andi x3, x5, -1591
        srli x5, x12, 7
        li   x16, 3
L10:
        xor x5, x6, x7
        srl x13, x2, x4
        addi x16, x16, -1
        bnez x16, L10
        sb x8, 120(x20)
        sb x6, 251(x20)
        li   x16, 1
L11:
        xor x3, x9, x8
        srl x8, x7, x4
        addi x16, x16, -1
        bnez x16, L11
        sb x5, 188(x20)
        lh x6, 52(x20)
        lhu x1, 18(x20)
        xori x7, x4, 876
        srl x6, x2, x7
        la   x17, F12
        jalr x18, 0(x17)
        j    E12
F12:   srl x3, x2, x5
        jalr x0, 0(x18)
E12:
        sltu x2, x14, x4
        andi x4, x3, 279
        xor x1, x6, x5
        xori x4, x4, -1649
        sub x3, x6, x5
        addi x3, x8, -297
        and x1, x4, x1
        ori x3, x10, 190
        slti x2, x3, 34
        lh x8, 194(x20)
        slt x11, x12, x3
        lhu x7, 104(x20)
        add  x7, x7, x6
        andi x15, x5, 1610
        xor x4, x3, x13
        sltu x8, x1, x5
        slti x2, x4, 624
        xori x7, x14, -322
        bge x4, x8, L13
        addi x13, x3, 31
L13:
        lw x2, 80(x20)
        add  x5, x2, x7
        sll x7, x7, x12
        bgeu x5, x15, L14
        addi x6, x8, -49
        addi x7, x8, -38
        addi x8, x1, 46
L14:
        sra x1, x6, x1
        addi x1, x8, -372
        sw x5, 204(x20)
        sw x2, 148(x20)
        sltu x3, x3, x6
        li   x16, 1
L15:
        sub x1, x1, x3
        add x1, x5, x8
        sra x1, x7, x10
        addi x16, x16, -1
        bnez x16, L15
        or x11, x3, x13
        blt x6, x8, L16
        addi x8, x6, 43
        addi x3, x1, -45
L16:
        or x4, x5, x1
        xori x13, x5, -1973
        lh x2, 230(x20)
        li   x16, 1
L17:
        sltu x5, x4, x2
        and x6, x6, x5
        addi x16, x16, -1
        bnez x16, L17
        sra x2, x1, x3
        lw x3, 4(x20)
        add  x10, x3, x5
        or x8, x6, x3
        xor x5, x3, x6
        sll x8, x7, x8
        or x8, x2, x5
        andi x7, x1, -2017
        xor x2, x1, x7
        bge x8, x4, L18
        addi x2, x7, 30
        addi x2, x8, 33
L18:
        ebreak
