# random program, seed 18
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1516
        li   x2, -1994
        li   x3, 2418
        li   x4, 676
        li   x5, -260
        li   x6, -1039
        li   x7, -1379
        li   x8, 1010
        li   x9, 2146
        li   x10, 1047
        li   x11, -1502
        li   x12, 930
        li   x13, -580
        li   x14, 754
        li   x15, -833
        sub x3, x13, x4
        slt x4, x15, x14
        sltiu x1, x7, -243
        sh x10, 206(x20)
        lh x3, 58(x20)
        add  x13, x3, x4
        lw x8, 220(x20)
        add  x4, x8, x6
        sw x8, 240(x20)
        sub x2, x4, x13
        lw x14, 0(x20)
        xori x7, x7, 906
        slt x10, x3, x1
        bge x3, x7, L1
        addi x8, x1, 48
L1:
        auipc x7, 1005866
        auipc x14, 316391
        and x12, x8, x2
        li   x16, 2
L2:
        and x5, x3, x12
        or x5, x6, x6
        sub x6, x7, x7
        addi x16, x16, -1
        bnez x16, L2
        lh x1, 6(x20)
        add  x2, x1, x3
        sltiu x8, x6, 83
        sw x2, 236(x20)
        blt x2, x8, L3
        addi x9, x14, 1
        addi x8, x9, 32
        addi x14, x4, -48
L3:
        slt x10, x4, x3
        lw x4, 160(x20)
        addi x3, x3, 2043
        auipc x6, 117122
        auipc x12, 601573
        lw x4, 4(x20)
        add  x5, x4, x4
        sub x14, x8, x4
        sltiu x8, x4, 1593
        xor x3, x6, x12
        lh x2, 132(x20)
        bne x2, x5, L4
        addi x8, x2, -4
        addi x6, x6, -25
L4:
        xor x4, x10, x4
        add x6, x1, x3
        srl x6, x14, x5
        slt x8, x7, x2
        and x4, x4, x4
        ori x7, x6, 64
        bge x5, x7, L5
        addi x7, x2, 35
        addi x7, x14, 47
        addi x2, x6, 11
L5:
        srl x7, x9, x4
        lw x7, 40(x20)
        add  x6, x7, x6
        srai x3, x1, 20
        or x4, x8, x5
        sw x5, 72(x20)
        sltu x2, x6, x4
        lw x11, 12(x20)
        lui x1, 13039
        xori x2, x4, 1302
        ori x7, x1, 1060
        bge x6, x11, L6
        addi x7, x5, -30
        addi x5, x3, 33
        addi x11, x1, -47
L6:
        slt x5, x3, x7
        sw x7, 40(x20)
        bne x6, x1, L7
        addi x8, x7, -7
L7:
        sw x3, 216(x20)
        lh x4, 24(x20)
        add  x3, x4, x8
        slti x1, x6, 924
        srl x7, x9, x4
        lbu x4, 243(x20)
        add  x3, x4, x6
        srl x8, x7, x2
        sw x2, 156(x20)
        slti x7, x1, 343
        sw x4, 168(x20)
        sltiu x3, x4, -624
        add x10, x7, x8
        li   x16, 3
L8:
        and x5, x13, x3
        addi x16, x16, -1
        bnez x16, L8
        lb x1, 131(x20)
        add  x8, x1, x5
        bge x8, x8, L9
        addi x8, x8, 45
L9:
        sw x13, 176(x20)
        slli x5, x1, 30
        lw x13, 72(x20)
        add  x15, x13, x3
        slt x8, x13, x3
        li   x16, 2
L10:
        sltu x1, x7, x4
        slt x5, x4, x14
        addi x16, x16, -1
        bnez x16, L10
        sltu x5, x6, x1
        srl x7, x3, x2
        sub x1, x5, x8
        and x7, x4, x7
        srai x6, x4, 19
        srl x6, x7, x8
        lw x1, 96(x20)
        add  x5, x1, x2
        slti x1, x5, -2016
        lw x8, 212(x20)
        add  x2, x8, x15
        sra x2, x8, x3
        addi x7, x2, 1788
        sltiu x7, x4, -624
        add x5, x8, x1
        or x1, x1, x8
        andi x11, x5, 746
        bltu x7, x2, L11
        addi x5, x4, -12
L11:
        lw x3, 176(x20)
        add  x13, x3, x8
        ori x5, x5, 1133
        andi x1, x1, -1151
        lw x5, 64(x20)
        sltu x1, x5, x13
        srai x2, x4, 29
        bgeu x1, x2, L12
        addi x4, x8, 6
        addi x6, x5, -18
        addi x15, x6, 14
L12:
        or x6, x4, x8
        lb x5, 165(x20)
        lw x6, 220(x20)
        add  x5, x6, x10
        lh x2, 126(x20)
        add  x4, x2, x3
        lui x1, 678698
        sra x5, x7, x4
        bgeu x4, x14, L13
        addi x2, x7, -22
        addi x6, x8, -50
L13:
        addi x4, x3, 183
        andi x3, x11, -337
        lw x6, 164(x20)
        lbu x13, 73(x20)
        slt x5, x7, x6
        blt x3, x13, L14
        addi x15, x3, -50
        addi x6, x8, 37
L14:
        sub x2, x4, x5
        andi x5, x12, 1534
        slti x2, x1, -338
        xor x1, x7, x9
        or x8, x6, x6
        bltu x2, x6, L15
        addi x5, x1, -36
        addi x1, x3, -40
        addi x1, x5, -11
L15:
        sltu x1, x3, x3
        lw x8, 216(x20)
        add  x5, x8, x4
        lhu x6, 60(x20)
        add  x1, x6, x1
        srl x2, x2, x2
        sltu x11, x10, x5
        lbu x6, 75(x20)
        lh x8, 38(x20)
        add  x5, x8, x4
        ebreak
