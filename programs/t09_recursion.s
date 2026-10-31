# t09_recursion.s - recursive factorial and fibonacci using the stack
        li   sp, 0x3FF0
        li   a0, 10
        call fact                  # 3628800 (needs software multiply)
        mv   s0, a0
        li   a0, 12
        call rfib                  # 144
        mv   s1, a0
        ebreak

# a0 = a0 * a1   (shift-and-add, unsigned)
mul:    li   t0, 0
mul1:   beqz a1, mul2
        andi t1, a1, 1
        beqz t1, mul3
        add  t0, t0, a0
mul3:   slli a0, a0, 1
        srli a1, a1, 1
        j    mul1
mul2:   mv   a0, t0
        ret

fact:   addi sp, sp, -8
        sw   ra, 4(sp)
        sw   a0, 0(sp)
        li   t0, 2
        blt  a0, t0, fbase
        addi a0, a0, -1
        call fact
        lw   a1, 0(sp)
        call mul
        j    fret
fbase:  li   a0, 1
fret:   lw   ra, 4(sp)
        addi sp, sp, 8
        ret

rfib:   li   t0, 2
        blt  a0, t0, rret
        addi sp, sp, -12
        sw   ra, 8(sp)
        sw   a0, 4(sp)
        addi a0, a0, -1
        call rfib
        sw   a0, 0(sp)
        lw   a0, 4(sp)
        addi a0, a0, -2
        call rfib
        lw   t1, 0(sp)
        add  a0, a0, t1
        lw   ra, 8(sp)
        addi sp, sp, 12
rret:   ret
