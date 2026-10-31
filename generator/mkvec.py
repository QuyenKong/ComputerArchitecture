import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tests', 'vectors')
os.makedirs(OUT, exist_ok=True)
import random, refmodels as R
random.seed(11)
rows=[(op,f3,b,R.alucontrol(op,f3,b)) for op in range(4) for f3 in range(8) for b in range(2)]
R.write_vec(OUT+'/ALUControl.txt',[('ALUOp',2),('funct3',3),('f7b5',1),('ALUCtrl',4)],rows)
rows=[]
for _ in range(300):
    a=R.rnd32(); b=a if random.random()<0.2 else R.rnd32(); f3=random.randrange(8); br=random.randrange(2) if random.random()<0.3 else 1
    rows.append((a,b,f3,br,R.branch(a,b,f3,br)))
R.write_vec(OUT+'/BranchUnit.txt',[('A',32),('B',32),('funct3',3),('Branch',1),('Taken',1)],rows)
rows=[]
for _ in range(300):
    ins=random.getrandbits(32); sel=random.randrange(8)
    rows.append((ins,sel,R.immgen(ins,sel)))
R.write_vec(OUT+'/ImmGen.txt',[('Instr',32),('ImmSel',3),('Imm',32)],rows)
import modules
rows=[]
ops=list(R.CLS)+[1,2,3,0b11111,0b01110]
for _ in range(400):
    ins=random.getrandbits(32)
    if random.random()<0.85: ins=(ins & ~0x7f) | (random.choice(ops)<<2) | 3
    if random.random()<0.03: ins=0
    o=R.control(ins)
    rows.append([ins]+[o[n] for n,w in modules.CTRL_OUTS])
R.write_vec(OUT+'/Control.txt',[('Instr',32)]+modules.CTRL_OUTS,rows)
rows=[]
for _ in range(300):
    o,w=R.rnd32(),R.rnd32(); off=random.randrange(4); f3=random.randrange(8)
    rows.append((o,w,off,f3,R.storeunit(o,w,off,f3)))
R.write_vec(OUT+'/StoreUnit.txt',[('Old',32),('WData',32),('Off',2),('funct3',3),('New',32)],rows)
rows=[]
for _ in range(300):
    w=R.rnd32(); off=random.randrange(4); f3=random.randrange(8)
    rows.append((w,off,f3,R.loadunit(w,off,f3)))
R.write_vec(OUT+'/LoadUnit.txt',[('Word',32),('Off',2),('funct3',3),('Data',32)],rows)
rows=[]
for _ in range(200):
    a=R.rnd32() if random.random()<0.5 else (0xF0000000|random.getrandbits(28)); mw=random.randrange(2)
    io=int(a>>28==0xF)
    rows.append((a,mw,(a>>2)&0xFFF,a&3,mw&(1-io),mw&io,io))
R.write_vec(OUT+'/AddrDecode.txt',[('Addr',32),('MemWrite',1),('WordAddr',12),('Off',2),('RamWE',1),('IoWE',1),('IsIO',1)],rows)
# register file: sequential test, CLK driven by an input pin
regs=[0]*32; rows=[]; seq=1
for _ in range(200):
    ra1,ra2,wa=random.randrange(32),random.randrange(32),random.randrange(32)
    wd=R.rnd32(); we=int(random.random()<0.8)
    rows.append(['1',str(seq),ra1,ra2,wa,wd,we,0,regs[ra1],regs[ra2]]); seq+=1
    if we and wa: regs[wa]=wd
    rows.append(['1',str(seq),ra1,ra2,wa,wd,we,1,regs[ra1],regs[ra2]]); seq+=1
hdr=[('<set>',0),('<seq>',0),('RA1',5),('RA2',5),('WA',5),('WD',32),('WE',1),('CLK',1),('RD1',32),('RD2',32)]
with open(OUT+'/RegisterFile.txt','w') as f:
    f.write('<set> <seq> RA1[5] RA2[5] WA[5] WD[32] WE[1] CLK[1] RD1[32] RD2[32]\n')
    for r in rows:
        f.write(' '.join([r[0],r[1]]+[f'0x{v:x}' for v in r[2:]])+'\n')
rr=lambda: random.choice([0,1,2,5,random.randrange(32)])
rows=[]
for _ in range(400):
    a=(rr(),rr(),rr(),random.randrange(2),rr(),random.randrange(2)); rows.append(a+R.forward(*a))
R.write_vec(OUT+'/ForwardUnit.txt',[('rs1',5),('rs2',5),('M_rd',5),('M_RegWrite',1),('W_rd',5),('W_RegWrite',1),('FwdA',2),('FwdB',2)],rows)
rows=[]
for _ in range(400):
    a=(rr(),rr(),random.randrange(2),random.randrange(2),int(random.random()<0.15),rr(),random.randrange(2),int(random.random()<0.3)); rows.append(a+R.hazard(*a))
R.write_vec(OUT+'/HazardUnit.txt',[('rs1',5),('rs2',5),('UseRs1',1),('UseRs2',1),('D_Halt',1),('E_rd',5),('E_MemRead',1),('Redirect',1),
  ('PCWrite',1),('IFID_Write',1),('IFID_Flush',1),('IDEX_Flush',1),('Stall',1),('LoadUse',1)],rows)
rows=[]
for _ in range(300):
    a=(R.rnd32(),R.rnd32(),rr(),rr(),rr(),random.randrange(2),R.rnd32()); rows.append(a+R.idbypass(*a))
R.write_vec(OUT+'/IDBypass.txt',[('RD1',32),('RD2',32),('rs1',5),('rs2',5),('W_rd',5),('W_RegWrite',1),('W_data',32),('O1',32),('O2',32)],rows)

# IOController: sequential (GPIO_OUT register), CLK driven by the vector
gpio=0; rows=[]; seq=1
for _ in range(200):
    idx=random.choice([0,1,2,3,4,4,4,5,6,7]); addr=0xF0000000|(idx<<2)|random.choice([0,0,0,1,2,3])
    wd=R.rnd32(); mw=random.randrange(2); mr=random.randrange(2); isio=int(random.random()<0.85)
    kd=random.randrange(128); ka=random.randrange(2); gi=random.randrange(256)
    def outs():
        rd=[0,kd,0b10|ka,0,gpio,gi,0,0][idx] if True else 0
        return [rd, mw&isio&(idx==0), wd&0x7F, mr&isio&(idx==1), gpio]
    for clk in (0,1):
        if clk==1 and mw and isio and idx==4: gpio=wd
        rows.append(['1',str(seq),addr,wd,mw,mr,isio,clk,kd,ka,gi]+outs()); seq+=1
with open(OUT+'/IOController.txt','w') as f:
    f.write('<set> <seq> Addr[32] WData[32] MemWrite[1] MemRead[1] IsIO[1] CLK[1] KbdData[7] KbdAvail[1] GpioIn[8] IoRData[32] TxWE[1] TxData[7] KbdRE[1] GpioOut[32]\n')
    for r in rows:
        f.write(' '.join(r[:2]+[f'0x{int(v):x}' for v in r[2:]])+'\n')
