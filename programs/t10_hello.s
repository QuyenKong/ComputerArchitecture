# t10_hello.s - print a string on the memory-mapped TTY (0xF0000000)
        .data
msg:    .asciz "Hello, RISC-V!\n"
        .text
        li   s0, 0xF0000000        # TTY address
        la   s1, msg
        li   a0, 0                 # number of characters printed
loop:   lbu  t0, 0(s1)
        beqz t0, done
        sb   t0, 0(s0)             # write to TTY
        addi s1, s1, 1
        addi a0, a0, 1
        j    loop
done:   ebreak
