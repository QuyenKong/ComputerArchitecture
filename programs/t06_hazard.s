# t06_hazard.s - stresses forwarding, load-use stalls and flushes (pipeline)
        li   sp, 0x3FF0
        addi t0, zero, 1
        addi t0, t0, 1             # EX->EX forwarding (distance 1)
        addi t1, t0, 1             # distance 1 again
        add  t2, t0, t1            # rs1 from distance 2 (MEM->EX), rs2 from distance 1
        add  t3, t2, t0            # rs2 from distance 3 (WB -> ID bypass)
        add  t3, t3, t3            # both operands forwarded
        sw   t3, 0(sp)             # store data forwarded
        lw   t4, 0(sp)
        addi t5, t4, 1             # load-use -> 1 stall
        lw   t6, 0(sp)
        sw   t6, 4(sp)             # load -> store data: stall then forward
        lw   a0, 4(sp)
        beq  a0, t3, ok1           # load -> branch compare
        li   s11, 0xBAD
ok1:    lw   a1, 0(sp)
        addi a2, zero, 3
        add  a3, a1, a2            # load at distance 2 -> forward from WB, no stall
        addi a4, zero, 1
        addi a4, a4, 1
        addi a4, a4, 1
        addi a4, a4, 1             # chain of 4
        add  zero, a4, a4          # write x0: must not be forwarded
        add  a5, zero, a4          # reads 0, not the forwarded value
        lw   s0, 0(sp)
        add  s0, s0, s0            # load-use with rs1 == rs2
        li   s1, 0
        li   s2, 5
loop:   addi s1, s1, 1             # backward branch taken 4 times
        blt  s1, s2, loop
        jal  ra, fn                # jal + return, branch shadow must be flushed
        addi s3, s3, 100
        j    end
        addi s4, zero, 1           # never executed (flushed)
        addi s4, zero, 2
fn:     addi s3, zero, 7
        jalr zero, 0(ra)
        addi s5, zero, 1           # never executed
end:    la   s6, tgt
        sw   s6, 8(sp)
        lw   s7, 8(sp)
        jalr s8, s7, 0             # load-use into JALR base register
        li   s9, 1                 # skipped
tgt:    addi s10, s8, 0            # s10 = return address (forwarded link value)
        ebreak
