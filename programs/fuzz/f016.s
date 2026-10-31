# random program, seed 16
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -39
        li   x2, 843
        li   x3, 936
        li   x4, -666
        li   x5, 415
        li   x6, -1144
        li   x7, 659
        li   x8, -2953
        li   x9, 354
        li   x10, 2387
        li   x11, 2824
        li   x12, -880
        li   x13, -1052
        li   x14, 2201
        li   x15, -1178
        xor x11, x5, x4
        li   x16, 3
L1:
        and x11, x8, x5
        addi x16, x16, -1
        bnez x16, L1
        la   x17, F2
        jalr x18, 0(x17)
        j    E2
F2:   slt x2, x7, x3
        jalr x0, 0(x18)
E2:
        li   x16, 3
L3:
        add x2, x13, x6
        or x5, x8, x3
        sll x1, x8, x8
        addi x16, x16, -1
        bnez x16, L3
        lhu x1, 60(x20)
        lh x7, 204(x20)
        sltiu x13, x2, -182
        sub x4, x1, x2
        lhu x12, 24(x20)
        add  x1, x12, x4
        beq x5, x1, L4
        addi x8, x1, -43
        addi x4, x5, 14
L4:
        andi x2, x8, 1507
        sltu x3, x7, x7
        sll x14, x7, x8
        xor x14, x5, x4
        xori x8, x8, -1397
        sh x8, 52(x20)
        lb x2, 26(x20)
        xori x4, x1, -2047
        sltu x4, x1, x1
        srl x4, x5, x4
        xori x8, x15, -633
        add x6, x11, x2
        and x12, x2, x13
        or x2, x2, x1
        slli x3, x7, 2
        sb x7, 59(x20)
        srli x6, x6, 12
        sb x1, 111(x20)
        srli x11, x1, 25
        and x6, x1, x7
        lbu x1, 228(x20)
        add  x4, x1, x5
        auipc x1, 107750
        srl x1, x6, x2
        srli x7, x10, 26
        sltiu x3, x5, 102
        sll x6, x5, x8
        sub x7, x8, x4
        add x1, x14, x7
        sra x15, x2, x14
        add x3, x5, x4
        or x9, x2, x1
        srai x4, x8, 31
        addi x12, x7, -1081
        sra x4, x5, x3
        slt x3, x4, x15
        la   x17, F5
        jalr x18, 0(x17)
        j    E5
F5:   sltu x5, x14, x15
        jalr x0, 0(x18)
E5:
        sltiu x13, x4, 697
        add x1, x8, x7
        slti x3, x4, -1891
        and x6, x1, x3
        sh x6, 126(x20)
        lh x7, 126(x20)
        sb x3, 105(x20)
        sub x4, x7, x8
        slt x6, x4, x5
        xor x6, x2, x5
        lh x5, 126(x20)
        slt x4, x6, x7
        andi x13, x4, -1291
        srli x3, x3, 13
        lb x7, 237(x20)
        or x13, x6, x9
        sw x1, 116(x20)
        sub x3, x7, x5
        and x6, x7, x12
        srai x9, x3, 22
        lhu x7, 214(x20)
        add  x13, x7, x10
        sw x2, 92(x20)
        sb x4, 192(x20)
        ori x13, x3, 275
        sra x6, x5, x4
        ori x4, x6, -1444
        sw x6, 232(x20)
        blt x8, x4, L6
        addi x4, x8, -12
        addi x6, x6, 35
L6:
        lui x6, 1032560
        sub x7, x5, x1
        sh x5, 148(x20)
        lhu x1, 70(x20)
        add  x5, x1, x8
        xori x15, x6, 537
        sw x13, 152(x20)
        xori x6, x1, -1516
        add x8, x12, x6
        slti x15, x6, 1070
        bgeu x4, x4, L7
        addi x2, x1, 46
        addi x8, x4, -25
L7:
        sb x5, 82(x20)
        andi x1, x4, 1558
        la   x17, F8
        jalr x18, 0(x17)
        j    E8
F8:   add x6, x4, x8
        jalr x0, 0(x18)
E8:
        sb x2, 56(x20)
        slt x2, x2, x13
        andi x1, x1, -644
        srl x7, x6, x3
        sub x1, x7, x1
        ori x4, x2, -261
        sltu x2, x10, x1
        lw x1, 136(x20)
        sw x3, 24(x20)
        lhu x8, 122(x20)
        xor x1, x6, x5
        lhu x8, 68(x20)
        srl x3, x6, x8
        addi x13, x6, -518
        ori x1, x14, -230
        lh x6, 2(x20)
        addi x12, x6, -1765
        ori x5, x12, -280
        sw x8, 36(x20)
        li   x16, 2
L9:
        add x2, x8, x1
        slt x5, x6, x4
        addi x16, x16, -1
        bnez x16, L9
        or x1, x7, x4
        or x6, x8, x4
        bge x3, x15, L10
        addi x3, x10, -26
        addi x2, x7, 41
        addi x8, x9, 25
L10:
        blt x6, x3, L11
        addi x14, x8, 46
        addi x5, x4, -31
L11:
        lui x12, 426193
        add x12, x1, x7
        lw x1, 68(x20)
        sltu x5, x3, x4
        lw x6, 156(x20)
        add  x7, x6, x9
        lw x6, 132(x20)
        add  x7, x6, x6
        lw x4, 200(x20)
        add  x4, x4, x6
        sll x15, x4, x8
        addi x5, x8, -1597
        ebreak
