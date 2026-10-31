# random program, seed 2
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -2537
        li   x2, -2250
        li   x3, -2305
        li   x4, -43
        li   x5, -1615
        li   x6, 2486
        li   x7, -476
        li   x8, -940
        li   x9, 1963
        li   x10, -1262
        li   x11, 1970
        li   x12, -2708
        li   x13, 1761
        li   x14, 2580
        li   x15, -1703
        la   x17, F1
        jalr x18, 0(x17)
        j    E1
F1:   srl x9, x9, x1
        jalr x0, 0(x18)
E1:
        blt x6, x7, L2
        addi x3, x1, -28
        addi x3, x6, 15
        addi x3, x8, 3
L2:
        lb x8, 186(x20)
        add  x12, x8, x11
        xori x8, x6, 1676
        bge x8, x4, L3
        addi x14, x5, 48
        addi x5, x7, -11
L3:
        lb x10, 250(x20)
        sw x4, 172(x20)
        jal  x18, F4
        j    E4
F4:   sra x5, x2, x3
        jalr x0, 0(x18)
E4:
        bne x15, x1, L5
        addi x3, x1, -40
L5:
        sub x1, x3, x3
        lhu x4, 0(x20)
        add  x6, x4, x11
        lh x5, 58(x20)
        add  x12, x5, x5
        sb x6, 77(x20)
        sb x7, 13(x20)
        ori x6, x7, -1901
        lbu x3, 68(x20)
        add  x4, x3, x1
        jal  x18, F6
        j    E6
F6:   sll x2, x6, x7
        jalr x0, 0(x18)
E6:
        add x7, x2, x2
        sub x4, x1, x8
        slti x4, x4, 1505
        addi x1, x15, -564
        bgeu x6, x2, L7
        addi x6, x7, -38
        addi x4, x11, -48
        addi x1, x8, 9
L7:
        sra x1, x6, x2
        sll x6, x8, x6
        addi x2, x6, 1155
        li   x16, 1
L8:
        sra x1, x8, x8
        addi x16, x16, -1
        bnez x16, L8
        slt x8, x12, x15
        sltiu x4, x5, 1455
        lb x3, 40(x20)
        sltu x13, x1, x5
        sltiu x6, x5, -1130
        sltu x4, x5, x3
        sltiu x6, x10, -863
        sltiu x7, x3, 1170
        xori x5, x15, 1328
        lh x15, 242(x20)
        sw x7, 112(x20)
        la   x17, F9
        jalr x18, 0(x17)
        j    E9
F9:   add x8, x2, x4
        jalr x0, 0(x18)
E9:
        lw x2, 196(x20)
        add  x4, x2, x4
        slti x7, x3, 1778
        lh x9, 36(x20)
        lbu x8, 250(x20)
        add  x6, x8, x7
        and x8, x8, x3
        srl x1, x7, x4
        blt x3, x5, L10
        addi x6, x5, 33
L10:
        lb x3, 45(x20)
        lw x8, 156(x20)
        add  x1, x8, x2
        lh x2, 192(x20)
        add  x8, x2, x5
        andi x8, x4, 188
        sub x8, x6, x3
        sh x6, 118(x20)
        sra x6, x13, x12
        li   x16, 3
L11:
        sra x2, x7, x5
        slt x2, x3, x7
        and x2, x6, x7
        addi x16, x16, -1
        bnez x16, L11
        slt x7, x8, x3
        andi x2, x13, -375
        and x5, x4, x4
        lh x1, 22(x20)
        sub x5, x2, x7
        add x8, x6, x2
        srai x8, x14, 29
        sltu x1, x8, x3
        srl x2, x8, x1
        slt x1, x2, x8
        sll x8, x1, x1
        srl x14, x6, x4
        sll x2, x8, x1
        auipc x7, 341828
        andi x4, x4, 388
        and x7, x5, x9
        xor x8, x4, x3
        lw x4, 52(x20)
        add  x1, x4, x1
        lb x14, 240(x20)
        sw x2, 160(x20)
        srl x13, x11, x8
        lw x12, 104(x20)
        sb x1, 35(x20)
        sltiu x11, x5, -1919
        slt x7, x4, x3
        lhu x5, 230(x20)
        srli x8, x6, 19
        slt x8, x3, x5
        bltu x5, x1, L12
        addi x1, x5, 42
L12:
        lw x1, 224(x20)
        add  x4, x1, x7
        lh x4, 228(x20)
        add  x4, x4, x6
        srai x7, x4, 3
        or x7, x2, x7
        xori x4, x2, -2019
        sltu x5, x6, x8
        srai x4, x1, 30
        and x4, x3, x2
        lbu x3, 45(x20)
        add  x5, x3, x6
        sh x6, 48(x20)
        sltiu x8, x9, -821
        slt x1, x1, x2
        lhu x3, 222(x20)
        add  x6, x3, x5
        add x10, x15, x2
        beq x15, x4, L13
        addi x1, x2, 14
        addi x10, x1, 17
        addi x7, x3, -31
L13:
        xori x1, x10, -552
        xori x10, x13, 1605
        sra x14, x1, x3
        la   x17, F14
        jalr x18, 0(x17)
        j    E14
F14:   sra x8, x4, x5
        jalr x0, 0(x18)
E14:
        sw x10, 180(x20)
        sh x9, 216(x20)
        ori x4, x8, 942
        slti x4, x3, 1727
        slt x4, x11, x7
        sra x8, x7, x6
        bltu x3, x3, L15
        addi x3, x6, 23
        addi x5, x5, 35
L15:
        add x1, x2, x6
        slt x3, x15, x2
        xori x4, x2, -1897
        xor x1, x7, x1
        bgeu x4, x6, L16
        addi x7, x8, 9
L16:
        sw x4, 40(x20)
        ori x3, x9, -206
        sll x5, x3, x8
        lbu x10, 93(x20)
        sw x12, 0(x20)
        sra x4, x5, x1
        sub x6, x2, x8
        ebreak
