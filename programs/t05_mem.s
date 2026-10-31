# t05_mem.s - LW/SW and the optional byte/halfword loads and stores
        .data
words:  .word 0x11223344, 0x8899AABB, 0, 0
bytes:  .byte 0x80, 0x7F, 0xFF, 0x01
        .text
        la   s0, words
        lw   a0, 0(s0)
        lw   a1, 4(s0)
        lb   a2, 4(s0)             # 0xBB -> sign-extended 0xFFFFFFBB
        lbu  a3, 4(s0)             # 0x000000BB
        lb   a4, 7(s0)             # 0x88 -> 0xFFFFFF88
        lh   a5, 4(s0)             # 0xAABB -> 0xFFFFAABB
        lhu  a6, 6(s0)             # 0x8899
        lh   a7, 2(s0)             # 0x1122
        sw   a0, 8(s0)
        sb   a1, 12(s0)            # write single bytes into word 3
        sb   a0, 13(s0)
        sh   a6, 14(s0)
        lw   s1, 12(s0)            # = 0x88994433 ? -> bytes BB,44,99,88
        sh   a0, 8(s0)             # overwrite low half of word 2
        lw   s2, 8(s0)
        la   s3, bytes
        lbu  t0, 0(s3)
        lb   t1, 0(s3)
        lb   t2, 1(s3)
        lb   t3, 2(s3)
        lbu  t4, 3(s3)
        li   s4, 0x3000            # far address in RAM
        li   t5, 0xCAFEBABE
        sw   t5, -4(s4)
        lw   t6, -4(s4)
        sh   t5, 2(s4)
        lhu  s5, 2(s4)
        ebreak
