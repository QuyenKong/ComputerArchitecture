# t08_sort.s - bubble sort of 10 signed words in .data
        .data
arr:    .word 42, -7, 1000, 3, 0, -2048, 77, 77, 5, -1
        .text
        la   s0, arr
        li   s1, 10                # n
        addi s2, s1, -1            # i = n-1
outer:  blez s2, done
        li   t0, 0                 # j = 0
        mv   t1, s0                # p = &arr[0]
inner:  bge  t0, s2, next
        lw   t2, 0(t1)
        lw   t3, 4(t1)
        ble  t2, t3, noswap
        sw   t3, 0(t1)
        sw   t2, 4(t1)
noswap: addi t0, t0, 1
        addi t1, t1, 4
        j    inner
next:   addi s2, s2, -1
        j    outer
done:   lw   a0, 0(s0)             # smallest
        lw   a1, 36(s0)            # largest
        ebreak
