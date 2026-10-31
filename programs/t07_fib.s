# t07_fib.s - first 20 Fibonacci numbers stored to memory
        .data
fib:    .space 80
        .text
        la   s0, fib
        li   t0, 0                 # F(0)
        li   t1, 1                 # F(1)
        li   t2, 20                # count
loop:   sw   t0, 0(s0)
        add  t3, t0, t1
        mv   t0, t1
        mv   t1, t3
        addi s0, s0, 4
        addi t2, t2, -1
        bnez t2, loop
        mv   a0, t0                # F(20) = 6765
        ebreak
