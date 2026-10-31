# t11_io.s - memory-mapped I/O: GPIO read/write + UART echo (keyboard -> uppercase -> TTY)
# STDIN: "Hi, io!\n"
        li   s0, 0xF0000000        # I/O base address
        li   t0, 0x1234
        sw   t0, 0x10(s0)          # GPIO_OUT = 0x1234 (hex display shows 1234)
        lw   s1, 0x10(s0)          # read back -> 0x00001234
        li   t1, 0xAB
        sb   t1, 0x12(s0)          # byte 2 of GPIO_OUT -> LEDs: GPIO_OUT = 0x00AB1234
        lw   s2, 0x10(s0)
        lbu  s3, 0x11(s0)          # byte 1 of GPIO_OUT -> 0x12
        lw   s4, 0x14(s0)          # GPIO_IN (DIP switches, all off = 0)
        li   s5, 0                 # number of characters received
wait:   lw   t2, 8(s0)             # UART_STATUS
        andi t2, t2, 1             # bit0 = a character is waiting
        beqz t2, wait
        lw   t3, 4(s0)             # UART_RXDATA (reading removes it from the queue)
        addi s5, s5, 1
        li   t4, 'a'
        blt  t3, t4, echo
        li   t4, 'z'
        bgt  t3, t4, echo
        addi t3, t3, -32           # a..z -> A..Z
echo:   sb   t3, 0(s0)             # UART_TXDATA
        li   t4, 10
        bne  t3, t4, wait          # stop after newline
        lw   s6, 8(s0)             # status now: 0b10 (TX ready, RX empty)
        sw   s5, 0x10(s0)          # show the count on the GPIO display
        ebreak
