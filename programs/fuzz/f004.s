# random program, seed 4
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1067
        li   x2, -516
        li   x3, -2155
        li   x4, 2908
        li   x5, 244
        li   x6, 922
        li   x7, -1731
        li   x8, -2262
        li   x9, -2456
        li   x10, -2838
        li   x11, 289
        li   x12, 1500
        li   x13, -630
        li   x14, -2518
        li   x15, -1182
        ori x3, x5, -292
        li   x16, 1
L1:
        xor x4, x5, x6
        sub x6, x4, x8
        xor x5, x5, x5
        addi x16, x16, -1
        bnez x16, L1
        sb x7, 99(x20)
        andi x1, x8, 249
        sltiu x6, x4, -1504
        andi x8, x6, 1523
        lbu x2, 165(x20)
        lb x3, 141(x20)
        add  x6, x3, x5
        lw x6, 164(x20)
        sw x4, 208(x20)
        blt x7, x3, L2
        addi x6, x3, -4
        addi x6, x10, -38
L2:
        andi x4, x1, -1596
        lb x4, 76(x20)
        add  x5, x4, x7
        lhu x7, 100(x20)
        add  x8, x7, x7
        sw x5, 252(x20)
        srl x4, x5, x1
        blt x7, x11, L3
        addi x12, x8, -1
        addi x4, x10, -29
        addi x8, x11, -10
L3:
        sh x8, 110(x20)
        xor x11, x7, x3
        sw x12, 136(x20)
        lbu x4, 243(x20)
        and x5, x7, x9
        or x6, x9, x8
        bge x1, x2, L4
        addi x5, x3, -45
        addi x1, x6, -41
L4:
        srl x4, x5, x8
        bge x2, x13, L5
        addi x7, x8, -42
        addi x4, x8, 4
L5:
        srl x3, x3, x6
        add x1, x2, x8
        sw x7, 244(x20)
        sw x14, 180(x20)
        lb x8, 26(x20)
        srai x10, x7, 9
        sra x6, x2, x3
        slt x6, x2, x3
        slt x5, x10, x2
        sw x8, 48(x20)
        lw x8, 36(x20)
        lbu x4, 155(x20)
        lh x9, 156(x20)
        la   x17, F6
        jalr x18, 0(x17)
        j    E6
F6:   sltu x6, x7, x5
        jalr x0, 0(x18)
E6:
        srl x6, x7, x3
        xori x11, x10, 509
        blt x8, x13, L7
        addi x4, x3, -44
L7:
        sra x5, x4, x2
        slt x5, x5, x3
        lw x12, 212(x20)
        add  x1, x12, x9
        sltu x5, x2, x3
        blt x5, x6, L8
        addi x7, x5, 36
L8:
        and x2, x14, x4
        srli x9, x8, 24
        and x10, x8, x6
        sltu x1, x4, x5
        sh x15, 244(x20)
        sub x1, x8, x6
        bne x8, x4, L9
        addi x2, x3, 39
L9:
        srl x14, x14, x4
        lbu x3, 8(x20)
        add  x6, x3, x5
        bgeu x1, x8, L10
        addi x14, x5, 50
L10:
        sltu x4, x7, x5
        sltu x15, x6, x4
        srl x7, x5, x3
        auipc x3, 193210
        lbu x8, 129(x20)
        lhu x4, 4(x20)
        add  x6, x4, x3
        beq x3, x12, L11
        addi x13, x4, -17
L11:
        slt x6, x3, x4
        add x11, x15, x5
        lw x13, 252(x20)
        add  x8, x13, x6
        xori x13, x3, -796
        ori x4, x11, 770
        slti x4, x6, -533
        jal  x18, F12
        j    E12
F12:   add x5, x12, x8
        jalr x0, 0(x18)
E12:
        li   x16, 3
L13:
        sltu x7, x6, x8
        and x7, x6, x1
        sub x1, x4, x1
        addi x16, x16, -1
        bnez x16, L13
        lhu x3, 10(x20)
        sra x7, x9, x3
        lh x1, 178(x20)
        add  x4, x1, x2
        sra x3, x3, x1
        ori x2, x1, -826
        ori x5, x5, -335
        lb x5, 144(x20)
        slt x6, x7, x7
        sh x4, 16(x20)
        sw x1, 100(x20)
        blt x7, x6, L14
        addi x4, x1, 38
        addi x3, x3, -37
        addi x9, x6, 35
L14:
        sra x2, x1, x5
        xori x10, x3, 921
        andi x8, x8, -1836
        srai x5, x11, 28
        li   x16, 2
L15:
        and x5, x12, x8
        sra x6, x3, x4
        addi x16, x16, -1
        bnez x16, L15
        sw x2, 168(x20)
        jal  x18, F16
        j    E16
F16:   srl x1, x11, x4
        jalr x0, 0(x18)
E16:
        blt x7, x8, L17
        addi x2, x1, -38
        addi x7, x3, 5
        addi x1, x6, -7
L17:
        sltiu x6, x7, -292
        slti x2, x2, 1629
        andi x2, x3, -1008
        sltiu x7, x5, 1195
        bgeu x6, x9, L18
        addi x7, x6, -21
L18:
        srai x7, x6, 2
        sltiu x11, x3, 1873
        srl x7, x2, x1
        sh x12, 222(x20)
        and x3, x8, x13
        sll x12, x1, x11
        slti x3, x9, -606
        sh x4, 232(x20)
        sh x10, 78(x20)
        add x1, x4, x2
        andi x1, x9, -488
        add x6, x7, x6
        lb x1, 62(x20)
        add x7, x4, x7
        sltiu x2, x12, 1605
        lb x2, 219(x20)
        add  x8, x2, x8
        blt x7, x5, L19
        addi x5, x6, 39
        addi x2, x4, -30
L19:
        lbu x4, 197(x20)
        add  x2, x4, x1
        sll x1, x4, x4
        xor x5, x5, x7
        andi x10, x6, -489
        sw x3, 248(x20)
        add x4, x8, x6
        ebreak
