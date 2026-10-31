# random program, seed 11
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 705
        li   x2, 1585
        li   x3, 814
        li   x4, 701
        li   x5, 1160
        li   x6, 1811
        li   x7, -1445
        li   x8, -1488
        li   x9, 1193
        li   x10, 897
        li   x11, 2159
        li   x12, 2029
        li   x13, -1475
        li   x14, -2229
        li   x15, 658
        sub x1, x7, x11
        lb x2, 80(x20)
        add  x4, x2, x8
        sra x9, x5, x2
        ori x2, x6, -167
        addi x2, x5, 1118
        add x1, x1, x7
        slti x5, x5, 676
        sltu x2, x2, x8
        sw x4, 88(x20)
        la   x17, F1
        jalr x18, 0(x17)
        j    E1
F1:   sltu x2, x4, x5
        jalr x0, 0(x18)
E1:
        jal  x18, F2
        j    E2
F2:   and x2, x3, x5
        jalr x0, 0(x18)
E2:
        sra x5, x2, x4
        slt x8, x8, x3
        bne x5, x14, L3
        addi x4, x4, 37
        addi x15, x2, 3
        addi x2, x5, -20
L3:
        lh x10, 202(x20)
        add  x2, x10, x8
        srai x5, x4, 1
        sltu x1, x5, x3
        and x6, x3, x1
        ori x1, x2, 1902
        xor x2, x6, x15
        li   x16, 2
L4:
        slt x8, x14, x13
        add x10, x7, x1
        addi x16, x16, -1
        bnez x16, L4
        lui x2, 539394
        bgeu x8, x2, L5
        addi x1, x2, 11
        addi x2, x8, -18
        addi x6, x4, 16
L5:
        slt x8, x4, x5
        sltu x13, x15, x4
        srli x3, x1, 4
        li   x16, 3
L6:
        sub x5, x14, x8
        addi x16, x16, -1
        bnez x16, L6
        lh x5, 228(x20)
        xor x5, x1, x7
        addi x5, x3, -1664
        jal  x18, F7
        j    E7
F7:   sub x6, x11, x8
        jalr x0, 0(x18)
E7:
        add x9, x3, x6
        slti x3, x4, -1334
        sltiu x8, x1, 1038
        srai x13, x6, 29
        or x2, x7, x5
        ori x1, x2, -1744
        slti x5, x1, -260
        sb x6, 32(x20)
        lhu x15, 68(x20)
        sb x8, 224(x20)
        ori x9, x5, 505
        lh x9, 104(x20)
        add  x7, x9, x1
        lui x1, 840085
        slti x2, x2, 1711
        xori x8, x6, 1504
        bge x2, x1, L8
        addi x1, x3, -21
        addi x5, x6, -19
L8:
        lui x2, 525449
        lw x7, 220(x20)
        lui x9, 457900
        slti x3, x6, -565
        slt x4, x4, x3
        bne x5, x7, L9
        addi x3, x1, -38
        addi x6, x6, -36
L9:
        lb x8, 173(x20)
        add  x8, x8, x3
        and x5, x2, x3
        li   x16, 4
L10:
        sub x8, x6, x6
        addi x16, x16, -1
        bnez x16, L10
        add x3, x6, x7
        bltu x1, x2, L11
        addi x15, x7, 22
        addi x6, x5, -15
        addi x12, x3, 1
L11:
        slt x12, x7, x7
        and x6, x2, x6
        la   x17, F12
        jalr x18, 0(x17)
        j    E12
F12:   add x5, x7, x2
        jalr x0, 0(x18)
E12:
        xori x2, x10, -1862
        sub x5, x1, x11
        addi x5, x9, 1357
        li   x16, 1
L13:
        sll x2, x1, x3
        sltu x3, x9, x1
        sltu x7, x7, x6
        addi x16, x16, -1
        bnez x16, L13
        xori x5, x5, -1828
        or x3, x7, x6
        lb x4, 26(x20)
        add  x4, x4, x2
        li   x16, 4
L14:
        or x2, x7, x4
        addi x16, x16, -1
        bnez x16, L14
        blt x2, x3, L15
        addi x5, x7, -4
        addi x9, x3, -13
        addi x4, x5, 50
L15:
        ori x4, x4, -494
        li   x16, 2
L16:
        add x1, x7, x1
        sub x5, x2, x3
        srl x6, x6, x6
        addi x16, x16, -1
        bnez x16, L16
        andi x2, x8, -302
        sltiu x3, x6, 334
        sltiu x3, x6, -1254
        ori x2, x8, 1749
        add x4, x10, x5
        sltiu x3, x6, 953
        blt x10, x5, L17
        addi x5, x4, 1
        addi x12, x4, -40
L17:
        ori x7, x4, 968
        sw x8, 76(x20)
        blt x4, x3, L18
        addi x1, x7, -42
        addi x5, x2, -8
        addi x2, x2, -47
L18:
        lw x11, 72(x20)
        add  x8, x11, x9
        sll x6, x6, x8
        sltiu x1, x6, -2017
        sb x1, 44(x20)
        sb x3, 213(x20)
        jal  x18, F19
        j    E19
F19:   and x7, x5, x1
        jalr x0, 0(x18)
E19:
        sltiu x3, x3, -1538
        sb x4, 8(x20)
        or x8, x4, x5
        ori x8, x8, 1250
        blt x2, x4, L20
        addi x3, x7, 17
        addi x13, x1, 34
L20:
        beq x15, x4, L21
        addi x3, x6, -32
        addi x3, x5, 16
        addi x3, x3, -50
L21:
        and x2, x2, x12
        sltiu x5, x4, 1367
        sub x8, x7, x3
        li   x16, 3
L22:
        xor x5, x11, x6
        sub x2, x8, x13
        addi x16, x16, -1
        bnez x16, L22
        sw x12, 224(x20)
        lh x1, 120(x20)
        sw x7, 104(x20)
        li   x16, 3
L23:
        sltu x2, x4, x2
        slt x5, x6, x7
        addi x16, x16, -1
        bnez x16, L23
        and x3, x3, x7
        sll x2, x1, x2
        addi x7, x3, -365
        sb x10, 198(x20)
        sltu x6, x13, x1
        or x8, x7, x6
        sw x5, 52(x20)
        ori x3, x4, -433
        slli x4, x3, 15
        xori x6, x6, 132
        addi x3, x2, 117
        slt x2, x1, x6
        sra x3, x2, x7
        and x7, x1, x7
        andi x2, x3, 706
        ori x6, x1, -863
        xori x8, x7, 258
        xori x14, x7, -1087
        ebreak
