# random program, seed 12
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 887
        li   x2, -797
        li   x3, 2386
        li   x4, 1334
        li   x5, 2459
        li   x6, -135
        li   x7, -1832
        li   x8, 126
        li   x9, -2912
        li   x10, 69
        li   x11, 952
        li   x12, -755
        li   x13, 2270
        li   x14, 770
        li   x15, 2657
        bne x3, x6, L1
        addi x4, x4, -41
L1:
        ori x2, x1, -220
        sltu x2, x3, x3
        la   x17, F2
        jalr x18, 0(x17)
        j    E2
F2:   srl x2, x7, x8
        jalr x0, 0(x18)
E2:
        xori x2, x13, 94
        ori x7, x2, 19
        slt x3, x7, x1
        sltu x4, x2, x4
        xor x5, x1, x6
        xor x8, x3, x6
        or x1, x15, x6
        add x4, x6, x9
        slt x11, x11, x8
        ori x8, x3, 1628
        add x8, x4, x9
        add x3, x5, x4
        sll x9, x5, x7
        addi x13, x6, 970
        lb x3, 197(x20)
        sb x7, 37(x20)
        sw x8, 180(x20)
        lw x7, 60(x20)
        add  x6, x7, x6
        sub x5, x7, x1
        sra x3, x6, x6
        or x6, x4, x5
        and x6, x8, x4
        addi x4, x7, 1555
        lb x1, 54(x20)
        add  x6, x1, x3
        or x3, x1, x6
        sra x6, x5, x7
        slti x6, x7, 1986
        xori x3, x4, 38
        xor x1, x11, x14
        lw x5, 156(x20)
        add x1, x3, x4
        lw x13, 148(x20)
        add  x10, x13, x6
        lhu x3, 100(x20)
        sltiu x6, x7, 1350
        beq x5, x3, L3
        addi x6, x7, 20
        addi x6, x14, -34
L3:
        or x2, x14, x4
        sra x1, x8, x8
        sh x6, 216(x20)
        li   x16, 3
L4:
        xor x8, x5, x4
        addi x16, x16, -1
        bnez x16, L4
        sltu x14, x6, x7
        sh x11, 248(x20)
        ori x6, x3, 1559
        lh x2, 130(x20)
        lh x5, 88(x20)
        add  x6, x5, x15
        srl x2, x7, x6
        lw x6, 176(x20)
        lb x2, 22(x20)
        ori x8, x11, 498
        sll x2, x4, x5
        lb x5, 109(x20)
        add  x7, x5, x7
        sltiu x4, x8, 734
        ori x2, x13, 344
        ori x3, x7, 526
        sltu x1, x8, x5
        or x7, x5, x4
        or x5, x9, x13
        or x9, x4, x8
        sra x1, x1, x7
        xori x8, x7, -1982
        sb x2, 189(x20)
        slti x5, x7, 244
        sw x11, 200(x20)
        xor x6, x6, x2
        sw x3, 56(x20)
        srl x3, x6, x4
        sw x8, 8(x20)
        lh x7, 84(x20)
        add  x15, x7, x6
        sra x7, x1, x1
        srl x1, x4, x11
        sw x2, 104(x20)
        auipc x11, 714008
        la   x17, F5
        jalr x18, 0(x17)
        j    E5
F5:   sltu x6, x1, x6
        jalr x0, 0(x18)
E5:
        lw x10, 244(x20)
        add  x8, x10, x3
        sltiu x9, x12, 706
        la   x17, F6
        jalr x18, 0(x17)
        j    E6
F6:   and x3, x8, x2
        jalr x0, 0(x18)
E6:
        sltu x5, x6, x8
        xori x4, x3, -868
        and x11, x3, x8
        lbu x2, 249(x20)
        sltiu x4, x8, -850
        bltu x4, x5, L7
        addi x3, x1, 4
        addi x8, x3, -25
L7:
        lbu x1, 92(x20)
        add  x3, x1, x4
        srl x9, x5, x3
        beq x1, x2, L8
        addi x6, x6, -35
L8:
        bltu x2, x7, L9
        addi x5, x2, -37
        addi x4, x5, 49
L9:
        sh x7, 244(x20)
        or x8, x7, x13
        lw x3, 32(x20)
        sll x5, x4, x4
        sltu x3, x13, x3
        slt x1, x5, x5
        add x7, x4, x3
        sra x12, x5, x3
        slt x2, x3, x10
        sub x9, x8, x3
        lhu x3, 172(x20)
        add  x15, x3, x8
        srl x13, x1, x3
        sltiu x2, x2, -1715
        sltiu x1, x7, 489
        lhu x8, 246(x20)
        add  x1, x8, x13
        jal  x18, F10
        j    E10
F10:   or x5, x2, x3
        jalr x0, 0(x18)
E10:
        sw x7, 8(x20)
        bltu x7, x6, L11
        addi x3, x3, -48
        addi x9, x4, 50
        addi x7, x8, -7
L11:
        lhu x1, 232(x20)
        add  x2, x1, x1
        or x1, x2, x8
        lb x15, 15(x20)
        add  x1, x15, x7
        srl x4, x4, x2
        bne x10, x4, L12
        addi x1, x3, 5
L12:
        sh x8, 192(x20)
        auipc x4, 303429
        sll x6, x4, x7
        lui x7, 57652
        sltiu x4, x1, 1607
        sw x2, 244(x20)
        lw x8, 4(x20)
        add  x6, x8, x10
        sb x7, 54(x20)
        ebreak
