# random program, seed 20
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 2921
        li   x2, 2621
        li   x3, -1762
        li   x4, -872
        li   x5, 2521
        li   x6, 2207
        li   x7, -2169
        li   x8, -318
        li   x9, 1693
        li   x10, -1613
        li   x11, -2779
        li   x12, 371
        li   x13, 332
        li   x14, -2386
        li   x15, -2155
        sll x8, x4, x6
        sub x8, x4, x1
        sub x5, x5, x2
        blt x14, x10, L1
        addi x5, x6, 26
L1:
        lbu x7, 78(x20)
        add  x2, x7, x7
        sub x1, x7, x3
        sh x13, 56(x20)
        sltu x9, x12, x3
        sll x1, x2, x5
        lbu x4, 152(x20)
        add  x1, x4, x3
        bne x2, x4, L2
        addi x4, x3, 21
L2:
        andi x8, x3, -504
        sb x5, 156(x20)
        sra x2, x1, x6
        lhu x2, 146(x20)
        add  x1, x2, x9
        srl x6, x3, x2
        add x4, x7, x2
        srli x8, x3, 24
        bltu x5, x8, L3
        addi x8, x4, -13
L3:
        ori x1, x2, 961
        sub x3, x1, x6
        and x7, x4, x7
        lb x2, 150(x20)
        and x4, x6, x6
        la   x17, F4
        jalr x18, 0(x17)
        j    E4
F4:   srl x2, x11, x4
        jalr x0, 0(x18)
E4:
        andi x5, x11, -579
        li   x16, 2
L5:
        xor x10, x2, x3
        addi x16, x16, -1
        bnez x16, L5
        or x11, x3, x2
        sub x1, x7, x9
        lbu x5, 49(x20)
        add  x3, x5, x8
        sw x2, 88(x20)
        sltu x5, x2, x12
        bne x14, x9, L6
        addi x14, x6, 16
        addi x3, x6, -13
L6:
        slt x3, x3, x3
        srai x2, x15, 26
        slli x8, x1, 11
        sb x5, 50(x20)
        li   x16, 1
L7:
        srl x8, x4, x3
        addi x16, x16, -1
        bnez x16, L7
        xori x1, x5, 886
        xor x7, x2, x6
        sra x14, x4, x8
        addi x4, x8, -1284
        sll x14, x5, x8
        sra x1, x3, x3
        add x4, x9, x7
        lbu x1, 173(x20)
        add  x8, x1, x3
        slt x5, x3, x5
        sw x1, 104(x20)
        li   x16, 2
L8:
        slt x6, x14, x1
        sll x5, x14, x5
        add x1, x5, x8
        addi x16, x16, -1
        bnez x16, L8
        lw x11, 140(x20)
        sltiu x7, x5, -1921
        la   x17, F9
        jalr x18, 0(x17)
        j    E9
F9:   srl x2, x1, x12
        jalr x0, 0(x18)
E9:
        sltu x1, x11, x1
        bne x6, x2, L10
        addi x2, x4, -18
        addi x8, x1, 46
        addi x2, x3, 24
L10:
        andi x4, x5, -1715
        slt x14, x15, x6
        addi x10, x4, 273
        sw x4, 72(x20)
        srl x1, x2, x8
        slti x1, x4, 281
        sh x7, 168(x20)
        lw x12, 104(x20)
        add  x6, x12, x7
        jal  x18, F11
        j    E11
F11:   and x1, x5, x8
        jalr x0, 0(x18)
E11:
        sub x1, x2, x7
        slti x5, x5, 518
        or x1, x1, x8
        slt x2, x10, x3
        sub x12, x3, x2
        slli x6, x8, 14
        bgeu x7, x5, L12
        addi x1, x2, 4
        addi x7, x4, 22
        addi x11, x14, 27
L12:
        lw x15, 160(x20)
        add  x4, x15, x1
        and x14, x7, x4
        xor x5, x2, x8
        lui x1, 453525
        slti x2, x7, 1902
        sw x3, 212(x20)
        sltiu x1, x4, -1289
        addi x10, x3, -263
        or x2, x5, x5
        sll x15, x1, x6
        xori x1, x7, -1191
        beq x12, x3, L13
        addi x8, x4, -10
L13:
        auipc x3, 736038
        srl x5, x14, x5
        bgeu x7, x1, L14
        addi x8, x6, 19
L14:
        bne x8, x4, L15
        addi x15, x2, 1
        addi x2, x10, 20
        addi x3, x3, 44
L15:
        sra x5, x13, x6
        la   x17, F16
        jalr x18, 0(x17)
        j    E16
F16:   sltu x5, x4, x1
        jalr x0, 0(x18)
E16:
        bge x8, x10, L17
        addi x5, x6, -13
        addi x8, x10, 30
        addi x5, x5, -24
L17:
        addi x5, x7, -1355
        beq x5, x1, L18
        addi x1, x5, 37
        addi x1, x8, -45
        addi x1, x1, 20
L18:
        li   x16, 2
L19:
        and x11, x1, x2
        or x3, x5, x2
        xor x7, x2, x1
        addi x16, x16, -1
        bnez x16, L19
        sltiu x1, x7, 844
        andi x1, x5, 611
        sll x5, x5, x2
        lw x4, 56(x20)
        lbu x4, 234(x20)
        add  x2, x4, x3
        srli x7, x6, 30
        and x8, x6, x12
        xor x4, x6, x7
        sra x6, x1, x8
        auipc x6, 739069
        lb x6, 156(x20)
        add  x6, x6, x9
        andi x15, x2, -1870
        ori x5, x3, -960
        sll x6, x11, x2
        sb x1, 217(x20)
        sltu x6, x2, x2
        ori x4, x1, -1989
        slt x8, x1, x4
        lhu x5, 240(x20)
        add  x5, x5, x6
        sll x6, x5, x9
        slti x13, x6, -1503
        sltu x6, x6, x5
        xori x10, x1, -1791
        addi x5, x3, -1152
        andi x8, x3, 795
        sw x5, 80(x20)
        blt x1, x8, L20
        addi x6, x3, -37
        addi x6, x5, 46
        addi x5, x13, 12
L20:
        sb x5, 119(x20)
        ebreak
