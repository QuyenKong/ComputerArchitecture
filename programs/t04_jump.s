# t04_jump.s - JAL / JALR, calls and returns, jump tables
        li   sp, 0x3FF0
        li   a0, 5
        jal  ra, square            # a0 = 25
        mv   s0, a0
        li   a0, 7
        call square                # pseudo: jal ra, square
        mv   s1, a0
        la   t0, table             # jump table in .text
        lw   x0, 0(x0)             # (load into x0 - result discarded)
        li   t1, 2
        slli t1, t1, 2
        add  t0, t0, t1
        jalr ra, 0(t0)             # call table[2]
        mv   s2, a0
        jal  t2, next              # t2 = link address
next:   jalr t3, t2, 8             # jump to (t2 + 8): skips 1 instruction
        li   s3, 99                # skipped
        li   s4, 42
        la   t4, odd
        jalr t5, t4, 1             # target bit0 is cleared by hardware -> 'odd'
        li   s5, 1                 # skipped
odd:    li   s6, 77
        ebreak
square:
        mv   t6, a0
        li   a1, 0
sq1:    beqz t6, sq2
        add  a1, a1, a0
        addi t6, t6, -1
        j    sq1
sq2:    mv   a0, a1
        ret
table:  j    f0
        j    f1
        j    f2
f0:     li   a0, 100
        ret
f1:     li   a0, 101
        ret
f2:     li   a0, 102
        ret
