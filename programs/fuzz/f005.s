# random program, seed 5
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, 2102
        li   x2, -908
        li   x3, -63
        li   x4, 2656
        li   x5, 2341
        li   x6, 1342
        li   x7, -2763
        li   x8, 814
        li   x9, -960
        li   x10, 2316
        li   x11, -2576
        li   x12, -1716
        li   x13, -2073
        li   x14, 45
        li   x15, 842
        bge x4, x4, L1
        addi x7, x2, -33
        addi x8, x1, -50
L1:
        or x3, x5, x4
        sltiu x3, x12, -436
        li   x16, 4
L2:
        add x3, x5, x5
        sra x6, x6, x8
        addi x16, x16, -1
        bnez x16, L2
        lhu x1, 94(x20)
        add  x12, x1, x7
        sltu x1, x3, x4
        or x8, x6, x5
        sh x2, 54(x20)
        srl x3, x2, x6
        sub x5, x3, x2
        la   x17, F3
        jalr x18, 0(x17)
        j    E3
F3:   sltu x6, x8, x3
        jalr x0, 0(x18)
E3:
        add x6, x3, x10
        li   x16, 4
L4:
        and x3, x7, x8
        addi x16, x16, -1
        bnez x16, L4
        bltu x9, x8, L5
        addi x8, x8, 1
        addi x2, x3, 30
        addi x14, x2, 12
L5:
        srl x6, x6, x1
        sh x5, 186(x20)
        li   x16, 3
L6:
        and x1, x5, x5
        sll x6, x6, x14
        sltu x3, x12, x6
        addi x16, x16, -1
        bnez x16, L6
        li   x16, 2
L7:
        and x6, x8, x2
        sltu x7, x5, x1
        or x8, x3, x3
        addi x16, x16, -1
        bnez x16, L7
        lhu x3, 20(x20)
        add  x8, x3, x1
        ori x2, x4, 1015
        sltu x14, x2, x6
        li   x16, 3
L8:
        xor x6, x5, x14
        addi x16, x16, -1
        bnez x16, L8
        sltu x11, x8, x7
        slli x10, x1, 24
        sra x9, x7, x4
        xori x7, x3, 80
        lhu x6, 154(x20)
        xor x1, x8, x1
        sw x5, 200(x20)
        sll x4, x3, x5
        sra x9, x2, x3
        srl x10, x1, x6
        lw x8, 64(x20)
        srl x7, x7, x8
        bge x4, x8, L9
        addi x1, x7, 24
L9:
        sll x3, x8, x9
        sra x1, x4, x2
        sh x7, 14(x20)
        lw x4, 24(x20)
        sw x12, 56(x20)
        bne x3, x3, L10
        addi x1, x7, 45
L10:
        add x2, x15, x1
        ori x8, x6, -1592
        xor x5, x9, x4
        srl x5, x3, x14
        sltiu x3, x11, 750
        add x2, x8, x8
        ori x1, x7, -1609
        sw x2, 216(x20)
        la   x17, F11
        jalr x18, 0(x17)
        j    E11
F11:   or x7, x4, x6
        jalr x0, 0(x18)
E11:
        sw x6, 192(x20)
        lh x4, 220(x20)
        addi x3, x1, 1966
        bge x6, x8, L12
        addi x10, x6, 9
        addi x4, x3, -41
L12:
        xori x8, x5, -1145
        and x11, x8, x6
        blt x1, x8, L13
        addi x3, x6, -13
        addi x4, x3, -46
L13:
        add x2, x6, x3
        ori x8, x4, -610
        lbu x5, 23(x20)
        add  x7, x5, x1
        slti x2, x4, 1975
        sll x4, x8, x1
        sltu x1, x4, x7
        or x6, x2, x3
        srai x1, x6, 31
        xori x3, x15, 471
        lb x8, 112(x20)
        add  x14, x8, x3
        sub x2, x10, x5
        or x4, x15, x2
        slt x1, x11, x3
        srli x1, x12, 27
        sltu x6, x3, x8
        lw x1, 144(x20)
        add  x3, x1, x7
        bltu x7, x4, L14
        addi x3, x3, 43
        addi x5, x3, 30
L14:
        lhu x6, 230(x20)
        add  x7, x6, x1
        sb x2, 83(x20)
        sltu x4, x1, x4
        ori x4, x4, 436
        srli x13, x6, 15
        sb x3, 31(x20)
        sb x7, 248(x20)
        xor x4, x13, x8
        bltu x4, x1, L15
        addi x3, x1, -10
L15:
        lb x7, 159(x20)
        add  x10, x7, x12
        slli x7, x1, 13
        sub x6, x7, x1
        or x2, x5, x12
        sb x4, 104(x20)
        srl x1, x7, x4
        bltu x6, x6, L16
        addi x4, x5, 29
L16:
        and x7, x4, x7
        xori x4, x5, -1357
        auipc x1, 312833
        sra x3, x6, x6
        lhu x2, 28(x20)
        add  x11, x2, x4
        bltu x8, x1, L17
        addi x2, x3, -3
L17:
        lui x8, 676870
        sw x2, 92(x20)
        slt x8, x12, x4
        slti x1, x6, -961
        lhu x2, 254(x20)
        add  x12, x2, x2
        sw x7, 180(x20)
        sll x2, x5, x2
        addi x4, x2, -854
        sub x7, x9, x14
        li   x16, 1
L18:
        slt x2, x3, x1
        add x8, x14, x1
        addi x16, x16, -1
        bnez x16, L18
        jal  x18, F19
        j    E19
F19:   sll x2, x10, x11
        jalr x0, 0(x18)
E19:
        addi x7, x9, 1513
        bgeu x1, x7, L20
        addi x7, x7, -49
        addi x13, x6, -32
        addi x4, x2, -3
L20:
        sltu x3, x5, x2
        sw x7, 232(x20)
        sltu x4, x8, x10
        xori x6, x1, -1931
        sltu x3, x6, x4
        srl x15, x2, x2
        lh x9, 190(x20)
        add  x4, x9, x3
        srl x7, x8, x1
        or x4, x1, x4
        sltu x13, x5, x2
        lb x15, 190(x20)
        add  x7, x15, x3
        ebreak
