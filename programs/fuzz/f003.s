# random program, seed 3
        li   x20, 0x1000            # data base
        li   x21, 0x3FF0            # stack
        li   x1, -1051
        li   x2, 1854
        li   x3, 1458
        li   x4, -1932
        li   x5, 30
        li   x6, 1947
        li   x7, 883
        li   x8, 2125
        li   x9, 1758
        li   x10, -2464
        li   x11, 1961
        li   x12, -2893
        li   x13, 843
        li   x14, -876
        li   x15, 1512
        sll x8, x3, x3
        bltu x1, x2, L1
        addi x10, x1, -16
L1:
        sltiu x7, x15, 1449
        slti x3, x2, -1755
        or x7, x14, x7
        srai x4, x11, 1
        bltu x3, x6, L2
        addi x10, x4, 31
        addi x10, x2, -42
        addi x8, x2, 2
L2:
        beq x7, x1, L3
        addi x1, x6, 20
        addi x5, x1, -11
        addi x2, x1, -25
L3:
        jal  x18, F4
        j    E4
F4:   xor x1, x6, x3
        jalr x0, 0(x18)
E4:
        bge x7, x2, L5
        addi x13, x7, 31
        addi x4, x7, -17
        addi x6, x7, 24
L5:
        sltu x3, x6, x6
        auipc x1, 127038
        li   x16, 1
L6:
        xor x5, x6, x3
        slt x14, x5, x2
        addi x16, x16, -1
        bnez x16, L6
        sw x4, 12(x20)
        lw x7, 136(x20)
        sra x6, x4, x3
        or x8, x2, x4
        sra x5, x2, x6
        srli x5, x7, 18
        xori x7, x1, 1862
        li   x16, 4
L7:
        or x8, x11, x5
        srl x4, x14, x5
        sub x1, x4, x15
        addi x16, x16, -1
        bnez x16, L7
        addi x2, x5, -90
        lw x10, 208(x20)
        add  x8, x10, x1
        andi x2, x5, -996
        sb x5, 3(x20)
        sra x7, x6, x1
        bne x1, x1, L8
        addi x8, x6, -41
        addi x7, x6, -17
        addi x6, x3, 21
L8:
        sltu x10, x6, x7
        lb x8, 23(x20)
        sltu x4, x5, x2
        sb x15, 113(x20)
        srl x5, x2, x12
        lbu x10, 192(x20)
        add  x12, x10, x3
        sltu x2, x7, x1
        sub x2, x5, x2
        sra x4, x2, x1
        srai x2, x3, 15
        sltiu x7, x7, 821
        slli x4, x7, 10
        slti x11, x11, 1914
        sltu x3, x8, x15
        lb x4, 225(x20)
        add  x4, x4, x9
        li   x16, 3
L9:
        sltu x5, x5, x8
        sltu x6, x8, x3
        sltu x8, x4, x1
        addi x16, x16, -1
        bnez x16, L9
        sltiu x7, x15, -1673
        andi x11, x11, -1481
        li   x16, 3
L10:
        or x3, x1, x5
        addi x16, x16, -1
        bnez x16, L10
        add x7, x2, x5
        sw x6, 148(x20)
        slt x7, x4, x8
        slti x5, x7, -1127
        slti x2, x6, 970
        sh x6, 148(x20)
        lbu x1, 59(x20)
        lbu x8, 93(x20)
        add  x3, x8, x11
        lb x8, 214(x20)
        add  x12, x8, x3
        sh x7, 200(x20)
        and x5, x6, x7
        addi x2, x2, -1125
        srai x4, x7, 8
        slli x13, x3, 11
        xor x5, x8, x14
        slti x5, x5, 1917
        or x1, x4, x8
        srl x8, x5, x15
        sll x10, x1, x4
        xori x6, x6, -948
        sra x1, x12, x13
        sub x7, x4, x2
        sw x12, 208(x20)
        sll x2, x7, x8
        sll x7, x8, x12
        slt x6, x4, x13
        slt x8, x3, x3
        srai x1, x3, 28
        addi x7, x7, -1779
        lw x7, 24(x20)
        add  x15, x7, x2
        andi x2, x2, -1623
        sh x5, 150(x20)
        slti x6, x6, 549
        sltu x10, x2, x2
        srl x1, x6, x8
        sll x11, x5, x11
        li   x16, 1
L11:
        and x2, x6, x7
        and x14, x14, x6
        addi x16, x16, -1
        bnez x16, L11
        blt x8, x8, L12
        addi x3, x7, 12
        addi x3, x1, 9
L12:
        sub x1, x14, x8
        bgeu x6, x4, L13
        addi x15, x5, -36
        addi x4, x1, -31
L13:
        li   x16, 2
L14:
        add x5, x4, x9
        sltu x6, x9, x8
        and x1, x2, x2
        addi x16, x16, -1
        bnez x16, L14
        xor x8, x2, x6
        sltiu x2, x8, 1060
        srl x5, x2, x4
        addi x11, x7, -1500
        lui x1, 702972
        sll x4, x4, x14
        bgeu x7, x4, L15
        addi x8, x7, 10
        addi x15, x1, -27
        addi x1, x5, 14
L15:
        sltiu x4, x5, 1980
        ori x4, x5, -877
        xor x8, x3, x5
        la   x17, F16
        jalr x18, 0(x17)
        j    E16
F16:   slt x7, x8, x4
        jalr x0, 0(x18)
E16:
        ori x8, x6, 388
        lw x3, 4(x20)
        add  x1, x3, x8
        ori x1, x4, -1940
        slt x10, x2, x5
        sll x5, x1, x3
        bltu x3, x14, L17
        addi x6, x5, -48
        addi x1, x1, 8
L17:
        sltiu x14, x10, 1346
        sltiu x3, x3, -1216
        ori x5, x8, 270
        li   x16, 2
L18:
        slt x1, x4, x15
        sra x1, x2, x5
        xor x2, x8, x14
        addi x16, x16, -1
        bnez x16, L18
        lh x7, 98(x20)
        addi x1, x6, 1167
        slli x5, x2, 31
        or x12, x2, x1
        li   x16, 1
L19:
        xor x8, x1, x8
        and x3, x8, x1
        addi x16, x16, -1
        bnez x16, L19
        add x3, x3, x1
        andi x7, x7, 1145
        add x3, x5, x6
        li   x16, 1
L20:
        add x3, x4, x8
        addi x16, x16, -1
        bnez x16, L20
        slt x6, x8, x8
        ori x8, x4, 373
        li   x16, 2
L21:
        and x4, x1, x3
        sub x3, x13, x6
        addi x16, x16, -1
        bnez x16, L21
        ebreak
