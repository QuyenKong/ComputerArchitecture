# random program, seed 23
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -626
        li   x2, -2316
        li   x3, -2861
        li   x4, 1849
        li   x5, -488
        li   x6, 471
        li   x7, 106
        li   x8, 1342
        li   x9, -67
        li   x10, -1933
        li   x11, 2947
        li   x12, -1428
        li   x13, -810
        li   x14, 641
        li   x15, -2885
        sll x2, x8, x7
        addi x1, x3, -279
        jal  x18, F1
        j    E1
F1:   slt x5, x6, x8
        jalr x0, 0(x18)
E1:
        sll x8, x3, x3
        sltiu x4, x2, -1241
        slti x5, x6, -1155
        ori x8, x5, -824
        sub x14, x6, x2
        li   x16, 2
L2:
        add x7, x3, x11
        add x13, x1, x8
        addi x16, x16, -1
        bnez x16, L2
        lw x7, 176(x20)
        add  x5, x7, x4
        sh x3, 232(x20)
        lh x1, 120(x20)
        add  x7, x1, x15
        auipc x4, 619190
        ori x9, x1, 285
        and x7, x2, x2
        srl x13, x5, x7
        and x7, x1, x8
        lhu x3, 42(x20)
        add  x2, x3, x1
        bge x1, x7, L3
        addi x7, x5, -15
        addi x6, x1, 3
L3:
        bgeu x5, x2, L4
        addi x5, x3, 14
        addi x8, x5, 22
L4:
        sw x2, 0(x20)
        sra x1, x2, x6
        srai x2, x7, 23
        sub x3, x2, x3
        jal  x18, F5
        j    E5
F5:   and x5, x5, x1
        jalr x0, 0(x18)
E5:
        sh x2, 52(x20)
        or x7, x13, x7
        lbu x3, 114(x20)
        add  x5, x3, x1
        ori x13, x3, -324
        sltu x6, x8, x10
        li   x16, 3
L6:
        slt x5, x3, x6
        addi x16, x16, -1
        bnez x16, L6
        slli x7, x3, 28
        la   x17, F7
        jalr x18, 0(x17)
        j    E7
F7:   sltu x8, x7, x5
        jalr x0, 0(x18)
E7:
        add x6, x12, x5
        lb x13, 72(x20)
        add  x2, x13, x7
        andi x13, x1, -340
        andi x13, x5, 281
        slti x9, x1, -245
        sw x3, 76(x20)
        lbu x2, 58(x20)
        slli x1, x15, 2
        ori x7, x11, -1992
        bne x11, x2, L8
        addi x3, x8, -43
        addi x15, x1, 26
        addi x13, x7, -45
L8:
        lw x6, 68(x20)
        li   x16, 4
L9:
        sll x6, x1, x4
        addi x16, x16, -1
        bnez x16, L9
        sub x3, x11, x10
        sw x4, 100(x20)
        sw x12, 136(x20)
        sw x6, 64(x20)
        srl x6, x2, x3
        xori x3, x4, 698
        sra x2, x12, x2
        srai x1, x1, 10
        blt x4, x6, L10
        addi x7, x13, -37
        addi x7, x1, -28
L10:
        srai x1, x6, 9
        slt x11, x12, x5
        xor x7, x3, x7
        lw x13, 76(x20)
        add  x8, x13, x1
        sh x4, 40(x20)
        blt x4, x5, L11
        addi x4, x11, -28
        addi x3, x6, 45
L11:
        sh x7, 210(x20)
        sb x2, 26(x20)
        and x2, x5, x6
        slt x8, x10, x7
        bgeu x1, x13, L12
        addi x14, x8, 19
L12:
        sltiu x8, x6, 1550
        sw x5, 72(x20)
        bltu x5, x10, L13
        addi x5, x8, -28
L13:
        sb x4, 221(x20)
        li   x16, 1
L14:
        sub x14, x5, x4
        or x5, x7, x3
        addi x16, x16, -1
        bnez x16, L14
        andi x1, x15, -310
        add x6, x1, x6
        srai x15, x5, 3
        sw x4, 68(x20)
        or x14, x8, x8
        sltiu x1, x9, -647
        srl x8, x1, x4
        sra x6, x9, x3
        addi x5, x12, 529
        lh x1, 156(x20)
        add  x7, x1, x7
        lb x3, 112(x20)
        add  x2, x3, x8
        slli x2, x2, 14
        and x7, x5, x4
        and x3, x6, x8
        sltu x4, x7, x4
        bne x1, x8, L15
        addi x8, x8, -41
L15:
        slt x7, x4, x3
        lw x8, 168(x20)
        add  x4, x8, x3
        lui x6, 165372
        srl x7, x6, x2
        slt x4, x3, x13
        slt x15, x3, x7
        ori x3, x7, 1182
        srli x3, x8, 7
        slli x2, x3, 1
        bne x12, x5, L16
        addi x6, x5, 39
        addi x4, x3, 32
        addi x6, x3, -36
L16:
        lw x1, 208(x20)
        add  x2, x1, x12
        la   x17, F17
        jalr x18, 0(x17)
        j    E17
F17:   and x1, x2, x1
        jalr x0, 0(x18)
E17:
        sra x6, x4, x2
        xori x1, x11, 1749
        addi x7, x3, -1446
        addi x12, x1, -1092
        bgeu x15, x4, L18
        addi x6, x15, -7
        addi x4, x6, 25
L18:
        xor x8, x13, x3
        sub x8, x3, x7
        sb x1, 148(x20)
        lw x8, 180(x20)
        add  x3, x8, x5
        ori x1, x8, 103
        bgeu x6, x11, L19
        addi x14, x11, -26
L19:
        sb x7, 200(x20)
        addi x8, x3, 410
        addi x5, x8, 1795
        addi x1, x4, 676
        sub x4, x4, x5
        sltiu x1, x2, -818
        xor x2, x8, x3
        bltu x4, x7, L20
        addi x2, x7, -41
        addi x4, x5, 33
L20:
        lui x6, 864043
        xor x5, x14, x4
        andi x8, x3, -1892
        ebreak
