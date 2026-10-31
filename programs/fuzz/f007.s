# random program, seed 7
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -348
        li   x2, -1765
        li   x3, 234
        li   x4, 2332
        li   x5, -2605
        li   x6, -2407
        li   x7, 1389
        li   x8, -2229
        li   x9, -5
        li   x10, 1774
        li   x11, -2525
        li   x12, 1156
        li   x13, -1242
        li   x14, -2693
        li   x15, -2296
        addi x7, x2, -220
        lb x4, 31(x20)
        add  x5, x4, x2
        srai x3, x4, 23
        sub x4, x7, x8
        srli x4, x12, 15
        xor x6, x5, x2
        sltu x6, x8, x2
        sh x8, 162(x20)
        sub x8, x2, x5
        lh x6, 230(x20)
        add  x3, x6, x8
        xor x4, x8, x8
        ori x14, x5, 1354
        la   x17, F1
        jalr x18, 0(x17)
        j    E1
F1:   sltu x3, x3, x4
        jalr x0, 0(x18)
E1:
        sra x5, x7, x6
        li   x16, 1
L2:
        srl x7, x8, x1
        or x4, x2, x1
        addi x16, x16, -1
        bnez x16, L2
        sra x2, x10, x4
        lui x6, 763706
        addi x8, x5, -1345
        slt x8, x3, x4
        li   x16, 3
L3:
        srl x13, x2, x5
        addi x16, x16, -1
        bnez x16, L3
        andi x4, x6, -221
        lui x14, 840296
        lw x6, 116(x20)
        la   x17, F4
        jalr x18, 0(x17)
        j    E4
F4:   sll x6, x6, x6
        jalr x0, 0(x18)
E4:
        sub x4, x8, x1
        sltiu x2, x2, 1134
        sb x6, 101(x20)
        sltu x2, x3, x1
        sll x3, x8, x6
        srl x1, x12, x3
        andi x4, x4, 351
        slti x7, x1, 850
        bgeu x7, x15, L5
        addi x3, x1, 6
        addi x10, x3, -28
        addi x2, x6, 37
L5:
        slti x2, x1, -13
        add x9, x1, x15
        slt x4, x8, x8
        andi x5, x15, -389
        sb x6, 68(x20)
        or x4, x2, x3
        li   x16, 3
L6:
        xor x8, x2, x8
        addi x16, x16, -1
        bnez x16, L6
        or x7, x7, x4
        addi x1, x8, 1560
        lh x2, 198(x20)
        add  x4, x2, x2
        xor x3, x3, x14
        blt x8, x2, L7
        addi x3, x2, -16
        addi x11, x5, -40
L7:
        lui x2, 951632
        srl x5, x1, x4
        li   x16, 2
L8:
        add x5, x4, x3
        xor x1, x1, x4
        addi x16, x16, -1
        bnez x16, L8
        andi x2, x7, 2007
        xori x5, x4, 759
        and x6, x14, x2
        lhu x7, 128(x20)
        lb x1, 145(x20)
        add  x8, x1, x6
        li   x16, 3
L9:
        add x5, x3, x7
        addi x16, x16, -1
        bnez x16, L9
        xor x4, x1, x2
        sra x1, x4, x3
        lh x3, 198(x20)
        add  x15, x3, x7
        lb x10, 68(x20)
        lw x3, 116(x20)
        li   x16, 4
L10:
        srl x1, x4, x1
        sll x12, x15, x2
        addi x16, x16, -1
        bnez x16, L10
        lh x4, 240(x20)
        sll x7, x5, x10
        lw x6, 100(x20)
        add  x5, x6, x3
        add x2, x8, x5
        xori x15, x5, -1345
        li   x16, 1
L11:
        sll x8, x7, x4
        sub x3, x5, x3
        addi x16, x16, -1
        bnez x16, L11
        auipc x12, 765855
        sll x3, x8, x7
        and x7, x6, x6
        sw x15, 60(x20)
        lh x2, 128(x20)
        add  x5, x2, x5
        xor x3, x5, x6
        slt x7, x13, x7
        bltu x2, x7, L12
        addi x3, x5, 12
        addi x3, x7, -7
L12:
        xor x11, x4, x7
        and x8, x8, x13
        andi x4, x6, -1302
        slt x4, x12, x7
        slti x5, x1, 2032
        slt x4, x4, x8
        ori x14, x3, -1784
        xori x8, x7, 1787
        jal  x18, F13
        j    E13
F13:   sub x3, x2, x12
        jalr x0, 0(x18)
E13:
        lw x1, 232(x20)
        add  x1, x1, x5
        li   x16, 3
L14:
        sltu x2, x5, x4
        sltu x1, x5, x5
        slt x4, x4, x1
        addi x16, x16, -1
        bnez x16, L14
        li   x16, 3
L15:
        add x7, x4, x6
        addi x16, x16, -1
        bnez x16, L15
        add x7, x7, x5
        lw x4, 32(x20)
        add  x4, x4, x5
        sw x8, 148(x20)
        lui x1, 306987
        beq x3, x1, L16
        addi x6, x2, -29
L16:
        and x8, x7, x6
        addi x5, x7, -1035
        slli x5, x7, 5
        sll x8, x6, x8
        sltu x7, x1, x1
        sub x6, x6, x10
        slt x5, x2, x4
        sll x7, x15, x8
        sll x5, x13, x4
        slt x2, x7, x4
        sltiu x6, x7, -1187
        jal  x18, F17
        j    E17
F17:   sub x7, x8, x3
        jalr x0, 0(x18)
E17:
        slti x4, x14, -1056
        sh x6, 150(x20)
        xor x4, x4, x4
        sltu x4, x4, x2
        lw x4, 16(x20)
        beq x4, x4, L18
        addi x10, x2, -3
        addi x3, x5, 49
        addi x1, x6, -23
L18:
        slt x4, x1, x4
        sb x5, 166(x20)
        add x9, x7, x7
        lbu x7, 76(x20)
        ori x7, x5, 878
        addi x13, x4, 1152
        lw x3, 104(x20)
        add  x7, x3, x6
        andi x1, x7, -1319
        srli x3, x5, 10
        addi x8, x13, -432
        add x8, x7, x3
        ebreak
