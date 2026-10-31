# t03_branch.s - all six conditional branches, taken and not taken
        li   s0, -5
        li   s1, 3
        li   s2, -5
        li   t0, 0                 # bitmask of results
        beq  s0, s2, L1
        ori  t0, t0, 0x001         # must be skipped
L1:      beq  s0, s1, L2
        ori  t0, t0, 0x002         # executed
L2:      bne  s0, s1, L3
        ori  t0, t0, 0x004         # skipped
L3:      bne  s0, s2, L4
        ori  t0, t0, 0x008         # executed
L4:      blt  s0, s1, L5            # -5 < 3 signed -> taken
        ori  t0, t0, 0x010
L5:      blt  s1, s0, L6
        ori  t0, t0, 0x020         # executed
L6:      bge  s1, s0, L7            # taken
        ori  t0, t0, 0x040
L7:      bge  s0, s2, L8            # equal -> taken
        ori  t0, t0, 0x080
L8:      bltu s1, s0, L9            # 3 < 0xFFFFFFFB unsigned -> taken
        ori  t0, t0, 0x100
L9:      bltu s0, s1, L10
        ori  t0, t0, 0x200         # executed
L10:     bgeu s0, s1, L11           # taken
        ori  t0, t0, 0x400
L11:     bgeu s1, s0, L12
        addi t1, zero, 1           # executed
L12:     li   a0, 0                 # loop: sum 1..10 with a backward branch
        li   a1, 1
        li   a2, 11
L13:     add  a0, a0, a1
        addi a1, a1, 1
        bne  a1, a2, L13
        ebreak
