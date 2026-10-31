# demo.s - default program in the IMEM ROM of both CPUs
# 1) Fibonacci F(0..11) into data memory, 2) sum them, 3) print a message on the TTY,
# 4) show the sum on the GPIO hex display and turn on the 8 GPIO LEDs
# (no initialised .data -> runs directly in Logisim without loading a RAM image)
        .data
fib:    .space 48
        .text
main:   li   sp, 0x3FF0            # stack pointer (top of RAM)
        la   s0, fib               # s0 = &fib[0]
        li   t0, 0                 # F(n)
        li   t1, 1                 # F(n+1)
        li   t2, 12                # 12 numbers
fibl:   sw   t0, 0(s0)
        add  t3, t0, t1            # data hazard: t3 needs t0,t1 (forwarding)
        mv   t0, t1
        mv   t1, t3
        addi s0, s0, 4
        addi t2, t2, -1
        bnez t2, fibl              # taken 11 times -> flush 2 instructions each time
        la   s0, fib               # sum the array back
        li   a0, 0
        li   t2, 12
suml:   lw   t4, 0(s0)
        add  a0, a0, t4            # load-use hazard -> 1 stall
        addi s0, s0, 4
        addi t2, t2, -1
        bnez t2, suml              # a0 = 0+1+1+2+...+89 = 232 (0xE8)
        li   s1, 0xF0000000        # TTY
        li   t5, 72             # 'H'
        sb   t5, 0(s1)
        li   t5, 101            # 'e'
        sb   t5, 0(s1)
        li   t5, 108            # 'l'
        sb   t5, 0(s1)
        li   t5, 108            # 'l'
        sb   t5, 0(s1)
        li   t5, 111            # 'o'
        sb   t5, 0(s1)
        li   t5, 32             # ' '
        sb   t5, 0(s1)
        li   t5, 82             # 'R'
        sb   t5, 0(s1)
        li   t5, 73             # 'I'
        sb   t5, 0(s1)
        li   t5, 83             # 'S'
        sb   t5, 0(s1)
        li   t5, 67             # 'C'
        sb   t5, 0(s1)
        li   t5, 45             # '-'
        sb   t5, 0(s1)
        li   t5, 86             # 'V'
        sb   t5, 0(s1)
        li   t5, 33             # '!'
        sb   t5, 0(s1)
        li   t5, 10             # newline
        sb   t5, 0(s1)
        sw   a0, 0x10(s1)          # GPIO_OUT[15:0] = 0x00E8 -> hex display shows 00E8
        li   t5, 0xFF
        sb   t5, 0x12(s1)          # GPIO_OUT[23:16] = 0xFF -> all 8 LEDs on
        ebreak                     # halt
