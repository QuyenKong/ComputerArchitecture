# random program, seed 9
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 792
        li   x2, 2023
        li   x3, 58
        li   x4, -812
        li   x5, -1866
        li   x6, -1476
        li   x7, 2543
        li   x8, -2948
        li   x9, -229
        li   x10, 1118
        li   x11, 798
        li   x12, 1953
        li   x13, -2338
        li   x14, -264
        li   x15, 1540
        li   x16, 1
L1:
        sltu x8, x7, x4
        add x2, x7, x15
        sub x4, x7, x13
        addi x16, x16, -1
        bnez x16, L1
        or x6, x4, x1
        beq x14, x1, L2
        addi x2, x1, -35
L2:
        sw x2, 100(x20)
        add x8, x4, x7
        sub x3, x1, x3
        lw x7, 16(x20)
        sra x6, x9, x2
        beq x10, x4, L3
        addi x1, x6, -50
        addi x4, x5, -9
L3:
        sh x1, 156(x20)
        srl x8, x4, x2
        andi x7, x6, -909
        lbu x3, 86(x20)
        add  x2, x3, x1
        sll x7, x1, x6
        sll x3, x12, x2
        sll x7, x3, x5
        sh x5, 252(x20)
        andi x14, x4, -1942
        sll x7, x8, x5
        sltiu x7, x2, 412
        or x2, x8, x8
        bgeu x1, x8, L4
        addi x8, x1, 29
L4:
        srai x7, x2, 5
        sra x2, x6, x8
        sub x6, x8, x7
        la   x17, F5
        jalr x18, 0(x17)
        j    E5
F5:   sub x11, x3, x4
        jalr x0, 0(x18)
E5:
        add x2, x1, x4
        sltiu x1, x4, -1922
        slti x2, x7, -1575
        bge x10, x11, L6
        addi x3, x3, -5
L6:
        sw x15, 204(x20)
        sub x8, x6, x6
        bge x2, x8, L7
        addi x8, x3, -8
        addi x6, x6, 19
L7:
        or x11, x11, x8
        li   x16, 4
L8:
        srl x2, x7, x6
        addi x16, x16, -1
        bnez x16, L8
        sb x4, 48(x20)
        add x6, x3, x2
        xori x7, x3, 879
        ori x7, x3, -643
        add x7, x13, x5
        sll x4, x3, x6
        lb x1, 26(x20)
        add  x2, x1, x6
        srl x7, x4, x10
        slti x15, x6, 2016
        ori x7, x7, -486
        slli x2, x5, 15
        sw x9, 92(x20)
        or x3, x4, x6
        and x7, x7, x4
        sltiu x3, x15, -413
        lb x1, 193(x20)
        ori x3, x11, -1274
        xori x5, x6, -1934
        la   x17, F9
        jalr x18, 0(x17)
        j    E9
F9:   srl x2, x1, x2
        jalr x0, 0(x18)
E9:
        xor x3, x7, x6
        li   x16, 3
L10:
        srl x9, x3, x4
        sub x1, x8, x2
        addi x16, x16, -1
        bnez x16, L10
        sltu x3, x3, x7
        sltiu x6, x9, 1300
        srl x8, x7, x9
        addi x6, x11, -223
        ori x2, x13, 1292
        sltiu x2, x11, 594
        addi x2, x4, 1810
        add x1, x1, x2
        ori x3, x2, 475
        sltu x4, x5, x8
        sb x8, 160(x20)
        sb x8, 42(x20)
        srl x8, x8, x10
        sltiu x2, x10, 120
        sh x6, 84(x20)
        xori x13, x6, -609
        slt x6, x2, x6
        li   x16, 3
L11:
        sra x1, x8, x7
        addi x16, x16, -1
        bnez x16, L11
        xor x8, x4, x2
        slli x5, x5, 3
        andi x2, x2, -1061
        sh x4, 82(x20)
        lhu x5, 100(x20)
        add  x2, x5, x3
        lw x7, 92(x20)
        add  x2, x7, x7
        ori x6, x4, 885
        sltiu x2, x8, 963
        lb x5, 228(x20)
        slt x4, x3, x2
        sra x1, x3, x7
        xor x8, x3, x3
        srl x6, x2, x5
        lw x14, 0(x20)
        add  x6, x14, x5
        slt x4, x4, x7
        lw x12, 244(x20)
        lh x7, 98(x20)
        add  x11, x7, x4
        sub x1, x3, x11
        slt x5, x5, x1
        addi x13, x1, 109
        bltu x1, x7, L12
        addi x6, x3, -26
L12:
        la   x17, F13
        jalr x18, 0(x17)
        j    E13
F13:   sra x8, x8, x4
        jalr x0, 0(x18)
E13:
        xor x8, x3, x8
        slt x6, x2, x3
        slt x5, x5, x5
        andi x7, x7, 528
        andi x1, x6, -1498
        sb x10, 234(x20)
        lw x8, 168(x20)
        add  x13, x8, x4
        sltu x7, x1, x2
        addi x5, x1, 1834
        bge x6, x6, L14
        addi x1, x7, -7
        addi x8, x4, -20
L14:
        sltu x12, x2, x8
        lh x6, 98(x20)
        xor x5, x4, x6
        ori x3, x2, -1573
        sw x13, 172(x20)
        lh x6, 68(x20)
        sub x1, x4, x7
        add x2, x5, x14
        xori x6, x1, -2033
        sub x1, x2, x4
        lhu x2, 14(x20)
        andi x6, x2, -1631
        lb x6, 0(x20)
        add  x1, x6, x11
        srl x4, x5, x11
        ebreak
