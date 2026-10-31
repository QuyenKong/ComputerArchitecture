# random program, seed 6
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 1700
        li   x2, -2340
        li   x3, 973
        li   x4, -857
        li   x5, -2699
        li   x6, -2997
        li   x7, -1808
        li   x8, 2429
        li   x9, 1804
        li   x10, 852
        li   x11, 56
        li   x12, -384
        li   x13, -2821
        li   x14, -767
        li   x15, 1004
        sw x5, 208(x20)
        lhu x6, 46(x20)
        sw x12, 224(x20)
        lw x10, 148(x20)
        sb x1, 185(x20)
        lb x2, 127(x20)
        add  x9, x2, x5
        or x4, x4, x15
        lw x1, 4(x20)
        srai x5, x7, 18
        sll x7, x7, x8
        sub x11, x8, x7
        sb x7, 218(x20)
        li   x16, 2
L1:
        xor x3, x2, x6
        or x8, x5, x15
        sltu x5, x8, x7
        addi x16, x16, -1
        bnez x16, L1
        sltiu x6, x3, 1032
        lh x12, 138(x20)
        li   x16, 3
L2:
        add x1, x2, x6
        slt x8, x1, x3
        xor x7, x13, x8
        addi x16, x16, -1
        bnez x16, L2
        or x6, x11, x6
        sub x1, x8, x2
        lb x5, 64(x20)
        bge x1, x3, L3
        addi x8, x8, 7
L3:
        srli x2, x5, 23
        add x5, x8, x6
        sub x4, x1, x6
        addi x12, x4, 1499
        sub x2, x3, x8
        lw x1, 64(x20)
        add  x3, x1, x3
        xori x4, x3, 1385
        lw x1, 160(x20)
        slli x14, x8, 0
        slti x3, x11, 1001
        and x3, x3, x1
        sll x2, x2, x1
        or x4, x12, x5
        sub x14, x8, x2
        lw x1, 88(x20)
        lbu x4, 218(x20)
        add  x13, x4, x4
        add x6, x2, x1
        sltiu x1, x6, 1520
        lh x6, 24(x20)
        add  x5, x6, x5
        and x3, x7, x7
        srai x15, x3, 19
        bne x2, x10, L4
        addi x13, x3, -35
L4:
        sltu x8, x7, x8
        beq x5, x5, L5
        addi x6, x5, -28
        addi x4, x2, -26
L5:
        andi x15, x9, -1636
        xori x15, x14, 1144
        bgeu x2, x1, L6
        addi x3, x9, -36
L6:
        sw x11, 44(x20)
        sh x4, 110(x20)
        and x3, x12, x10
        sra x4, x3, x11
        sub x1, x1, x8
        add x2, x6, x6
        and x8, x13, x3
        sll x3, x8, x8
        or x14, x6, x6
        xor x1, x4, x1
        xori x5, x1, 579
        or x4, x1, x5
        lw x3, 188(x20)
        add  x6, x3, x6
        or x6, x2, x1
        srai x8, x1, 30
        lb x6, 130(x20)
        add  x6, x6, x7
        bne x1, x6, L7
        addi x1, x2, -43
        addi x2, x5, -5
        addi x5, x6, -1
L7:
        sltiu x12, x2, 269
        sh x1, 230(x20)
        bltu x7, x5, L8
        addi x1, x3, 21
        addi x7, x4, -42
        addi x13, x3, -31
L8:
        add x10, x7, x8
        auipc x8, 404518
        sw x3, 56(x20)
        slti x5, x4, -199
        lw x2, 208(x20)
        slt x8, x7, x6
        slti x1, x3, 449
        sll x8, x3, x7
        lh x8, 236(x20)
        add  x10, x8, x7
        lbu x3, 14(x20)
        addi x2, x4, 15
        sb x1, 134(x20)
        auipc x8, 739625
        srl x1, x14, x2
        srli x8, x6, 9
        add x14, x7, x8
        ori x5, x12, -1594
        andi x1, x1, -1422
        lbu x2, 61(x20)
        add  x6, x2, x3
        addi x4, x5, -818
        lui x7, 450904
        lb x3, 211(x20)
        lbu x7, 102(x20)
        li   x16, 2
L9:
        xor x7, x1, x6
        addi x16, x16, -1
        bnez x16, L9
        ori x6, x5, -791
        auipc x8, 363542
        lw x5, 0(x20)
        add  x4, x5, x1
        li   x16, 1
L10:
        sltu x6, x5, x1
        sra x3, x6, x6
        addi x16, x16, -1
        bnez x16, L10
        la   x17, F11
        jalr x18, 0(x17)
        j    E11
F11:   add x4, x7, x1
        jalr x0, 0(x18)
E11:
        auipc x15, 856013
        slti x1, x4, -14
        xor x6, x4, x3
        srai x2, x1, 22
        xori x4, x7, 631
        bge x4, x2, L12
        addi x7, x8, -8
        addi x3, x2, -38
L12:
        bne x4, x1, L13
        addi x1, x1, -14
        addi x12, x13, 28
L13:
        sll x1, x6, x3
        xori x4, x4, -1103
        bgeu x1, x5, L14
        addi x10, x6, 48
        addi x6, x5, 1
        addi x6, x6, -25
L14:
        sltu x5, x6, x1
        sub x1, x6, x1
        add x5, x4, x2
        srai x6, x7, 4
        bgeu x3, x8, L15
        addi x10, x5, -44
L15:
        srli x13, x1, 19
        add x2, x1, x6
        sltiu x4, x11, 1286
        sw x2, 56(x20)
        xori x6, x4, -1940
        ori x3, x1, -1947
        sll x1, x5, x4
        slt x5, x1, x13
        sll x7, x7, x2
        ebreak
