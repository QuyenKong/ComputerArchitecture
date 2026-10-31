---
title: "Bộ câu hỏi trình bày và phản biện — CPU RISC-V RV32I"
subtitle: "Bùi Phạm Sơn Hà · Nguyễn Đức Anh · Quyền Đức Công — dùng cho buổi dạy lại (T5 5/11) và bảo vệ thử (T7 7/11)"
---

# 0. Cách dùng

Mỗi người lần lượt làm **người trình bày** về mảng của mình. Mỗi phiên khoảng 55–60 phút, gồm 3 phần:

| Phần | Thời lượng | Ai làm gì |
|---|---|---|
| **Trình bày** | 20–25 phút | Người trình bày giảng mảng của mình cho 2 người nghe, có demo trên Logisim (dàn ý ở đầu mỗi phiên bên dưới) |
| **Pha 1 · Người nghe phản biện** | 15–20 phút | 2 người nghe hỏi người trình bày, mỗi người dùng bộ 6 câu của mình. Câu khó, kiểu thầy hỏi: "nếu… thì sao", trade-off, câu bẫy |
| **Pha 2 · Người trình bày kiểm tra lại** | 15 phút | Người trình bày hỏi ngược 2 người nghe 7 câu để xem họ hiểu tới đâu. Hai người nghe trả lời xen kẽ: câu lẻ một người, câu chẵn người kia |

**Luật chơi**

- Người bị hỏi **không được xem** cột đáp án. Chỉ người hỏi cầm đáp án để chấm.
- Chấm: nói đúng và giải thích được "vì sao" = **Đạt**. Chỉ nói được "cái gì" = **Nửa**. Sai hoặc không trả lời được = **Chưa**.
- **Pha 1**: câu nào người trình bày bị "Chưa" thì người đó phải bổ sung vào cheat sheet và trả lời lại vào buổi bảo vệ thử T7.
- **Pha 2**: người nghe nào có từ 3 câu "Chưa" trở lên thì người trình bày giảng lại riêng phần đó (10 phút) trước khi sang phiên tiếp theo.
- Đáp án là mức tối thiểu. Trả lời sâu hơn thì càng tốt.

| Phiên | Người trình bày | Người nghe |
|---|---|---|
| 1 | Bùi Phạm Sơn Hà | Đức Anh, Công |
| 2 | Nguyễn Đức Anh | Hà, Công |
| 3 | Quyền Đức Công | Hà, Đức Anh |

# Phiên 1 — Bùi Phạm Sơn Hà trình bày: Fetch, Decode, Control hazard

## Dàn ý trình bày

- 6 định dạng lệnh RISC-V; vị trí cố định của opcode, rd, funct3, rs1, rs2; vì sao bit của B/J bị xáo trộn
- Giải mã tay 2 lệnh trên bảng: `0x00500513` và `0xFCB50CE3`
- Bảng tín hiệu điều khiển 10 nhóm lệnh; khối Control vẽ theo kiểu decoder + cổng OR; điều kiện `opcode[1:0] = 11`
- ImmGen: ghép immediate I/S/B/U/J, sign-extend; ALUControl và bẫy ADDI/bit 30
- PC, PC+4, next-PC, `target = ALU & ~1`
- Pipeline: load-use stall, flush khi nhảy (mất 2 chu kỳ), ưu tiên Redirect > Stall, halt. Demo trên Pipeline Monitor

**Hà tự ôn trước buổi** (phải trả lời trôi chảy được):

- Vì sao decoder chỉ bật khi `opcode[1:0] = 11`? Lệnh `0x00000000` làm gì?
- Ghép immediate của BEQ từ các bit lệnh thế nào? Vì sao không lưu bit 0?
- Vì sao ADDI có bit 30 = 1 không bị hiểu thành SUB?
- BEQ nhảy mất mấy chu kỳ? Những thanh ghi nào bị flush?
- Khi load-use: PC, IF/ID, ID/EX mỗi cái làm gì? Vì sao Redirect được ưu tiên hơn Stall?

## Pha 1 · Người nghe phản biện Hà

### Nguyễn Đức Anh hỏi Hà

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | Gặp lệnh `fence` (opcode 0001111) hoặc một lệnh rác, Control sinh tín hiệu gì? | `opcode[6:2]` = 00011 không thuộc 10 nhóm được dùng, nên không cổng OR nào bật: mọi tín hiệu = 0, lệnh chạy như NOP. Nếu `opcode[1:0] ≠ 11` thì decoder bị tắt hẳn |
| 2 | Nếu lỡ để JAL có ASel = rs1 thay vì PC thì `jal ra, func` sai thế nào? | ALU tính `x[rs1] + imm` thay vì `PC + imm`. Ở JAL, bit [19:15] là một phần của immediate chứ không phải rs1, nên CPU nhảy tới một địa chỉ vô nghĩa |
| 3 | LUI chỉ cần `rd = imm`. Vì sao phải có ASel = 2 (ép A = 0) mà không để A = rs1? | Ở U-type, bit [19:15] là một phần immediate, không phải rs1 = x0. Để A = rs1 thì ALU cộng thêm một thanh ghi ngẫu nhiên. Phải ép A = 0 |
| 4 | HazardUnit dùng `UseRs1`/`UseRs2`. Bỏ hai tín hiệu này thì CPU **sai** hay chỉ **chậm**? | Chỉ chậm. Không có chúng thì hazard unit có thể stall oan: ví dụ `lw x5,…` rồi `lui x6, 0x28`, các bit lệnh ở vị trí rs1 (bit [19:15]) tình cờ bằng 5. Stall thừa không làm sai kết quả, chỉ tốn chu kỳ |
| 5 | Vì sao quyết định nhánh ở EX mà không đưa lên ID cho chỉ mất 1 chu kỳ? | Trade-off. Đưa lên ID phải thêm comparator và mạch forwarding ở ID, và nhánh phụ thuộc lệnh ALU ngay trước sẽ phải stall. Ở EX mạch đơn giản, đúng chắc chắn, đổi lại mất 2 chu kỳ mỗi lần nhảy. Đây là hướng mở rộng ghi trong báo cáo |
| 6 | EBREAK đang ở ID, còn lệnh ở EX là BEQ nhảy. Chuyện gì xảy ra? | Redirect thắng Stall: PC nhận địa chỉ đích, IF/ID và ID/EX bị flush. EBREAK nằm trên nhánh sai nên bị xóa, CPU không dừng. Đúng ngữ nghĩa chương trình |

### Quyền Đức Công hỏi Hà

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | Giải mã tay lệnh `0xFCB50CE3` (đặt ở địa chỉ 0x28). | B-type, opcode 1100011, funct3 = 000 → `beq`. rs1 = x10 (a0), rs2 = x11 (a1), offset = −40 → `beq a0, a1, 0x00` (nhảy về địa chỉ 0) |
| 2 | Vì sao immediate của S-type bị tách đôi thành bit [31:25] và [11:7]? | Để rs1 và rs2 nằm đúng vị trí cố định như mọi định dạng khác, giúp đọc Register File song song với giải mã. S-type không có rd, nên chỗ của rd ([11:7]) dùng để chứa 5 bit thấp của immediate |
| 3 | Khi load-use, vì sao IF/ID phải giữ (EN = 0) chứ không flush? | Lệnh trong IF/ID là lệnh đúng đường, chỉ cần chờ 1 chu kỳ. Flush thì nó biến mất và chương trình mất một lệnh |
| 4 | Có khi nào LoadUse và Redirect cùng bật một lúc không? | Không. LoadUse cần lệnh ở EX là load. Redirect cần lệnh ở EX là branch hoặc jump. Một lệnh không thể là cả hai. Mạch vẫn đặt ưu tiên Redirect để an toàn và dễ chứng minh |
| 5 | AUIPC tính `PC + imm`. Trong pipeline đó là PC nào? Lấy từ đâu? | PC của chính lệnh AUIPC, mang theo qua IF/ID → ID/EX (`E_pc`). Không phải PC hiện tại ở tầng IF, lúc đó đã đi trước 2 lệnh. Đây là lý do thanh ghi pipeline phải mang theo `pc` |
| 6 | Mã hóa ALUCtrl = {bit30, funct3} có nhược điểm gì nếu sau này thêm lệnh nhân MUL? | MUL dùng funct7 = 0000001 với funct3 = 000, trùng mã với ADD. Phải mở rộng ALUCtrl thêm một bit (hoặc thêm một kênh riêng cho khối nhân) và sửa ALUControl để đọc funct7 |

## Pha 2 · Hà kiểm tra Đức Anh và Công

Câu lẻ hỏi Đức Anh, câu chẵn hỏi Công. Lượt sau đổi lại.

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | Opcode nằm ở những bit nào? Vì sao phải đọc opcode trước các trường khác? | Bit [6:0]. Opcode quyết định lệnh thuộc định dạng nào (R/I/S/B/U/J), từ đó mới biết các bit còn lại cắt thế nào |
| 2 | Giải mã tay `0x00500513`. | opcode 0010011 (OP-IMM), rd = x10 (a0), funct3 = 000, rs1 = x0, imm = 5 → `addi a0, x0, 5` |
| 3 | Lệnh `sw t1, 8(t0)` cần RegWrite, MemWrite, BSel, ImmSel bằng bao nhiêu? | RegWrite = 0 (không ghi thanh ghi), MemWrite = 1, BSel = 1 (cộng immediate), ImmSel = S. ALU tính `t0 + 8` làm địa chỉ |
| 4 | Immediate 12 bit `0xFFF` sau khi sign-extend thành gì? Bằng bao nhiêu? | `0xFFFFFFFF` = −1. Bit 11 bằng 1 nên chép 1 sang toàn bộ 20 bit cao |
| 5 | Khi nào PC nhận địa chỉ nhảy thay vì PC+4? | Khi `PCSel = Taken OR Jal OR Jalr` bằng 1. Taken = 1 khi lệnh là branch và điều kiện so sánh đúng |
| 6 | Vẽ sơ đồ thời gian `lw x5, 0(x1)` rồi `add x6, x5, x7`. Lệnh `add` vào EX ở chu kỳ mấy? | `lw`: IF1 ID2 EX3 MEM4 WB5. `add`: IF2 ID3 **ID4** (stall, bubble vào EX ở chu kỳ 4) EX5. Chu kỳ 5 lấy x5 từ MEM/WB |
| 7 | BEQ nhảy mất mấy chu kỳ? Vì sao đúng con số đó? | 2 chu kỳ. Branch được quyết định ở EX, lúc đó 2 lệnh phía sau đã được nạp (ở IF và ID) theo PC+4, phải xóa cả hai |

# Phiên 2 — Nguyễn Đức Anh trình bày: Execute, Data hazard

## Dàn ý trình bày

- Nhị phân, hex, bù 2; có dấu và không dấu (SLT/SLTU, SRA/SRL, BLT/BLTU)
- ALU: tính song song mọi phép rồi dùng MUX chọn; ALUCtrl = {bit30, funct3}; shamt = B[4:0]
- Mạch tổ hợp và tuần tự, cạnh lên clock, Enable
- Register File: decoder ghi, 2 MUX đọc, x0 là hằng 0
- BranchUnit: 2 comparator, funct3[0] đảo kết quả
- Pipeline: RAW hazard, ForwardUnit (01/10, rd ≠ 0, ưu tiên EX/MEM), WB→ID bypass. Demo forwarding trên Pipeline Monitor

**Đức Anh tự ôn trước buổi** (phải trả lời trôi chảy được):

- `0xFFFFFFFF < 0x00000001` với SLT thì sao, với SLTU thì sao?
- Vì sao đọc Register File là tổ hợp còn ghi phải chờ cạnh clock?
- x0 được hiện thực thế nào?
- Điều kiện forwarding là gì? Vì sao kiểm tra `rd ≠ 0`? Vì sao EX/MEM ưu tiên hơn MEM/WB?
- Vì sao bypass WB→ID không đặt luôn trong RegisterFile?

## Pha 1 · Người nghe phản biện Đức Anh

### Bùi Phạm Sơn Hà hỏi Đức Anh

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | ALU của nhóm dùng Adder và Subtractor riêng. Phần cứng thật dùng chung một bộ cộng cho cả hai thế nào? | `A − B = A + (~B) + 1`: XOR từng bit của B với tín hiệu `alt` (alt = 1 thì đảo B), và đưa `alt` vào carry-in. Một bộ cộng làm được cả ADD lẫn SUB |
| 2 | `sll t0, t1, t2` với t2 = 35 cho kết quả gì? Vì sao? | Dịch trái 3 bit. RV32I chỉ dùng 5 bit thấp của toán hạng dịch (`B[4:0]`), 35 = 100011₂, nên 5 bit thấp là 00011 = 3 |
| 3 | Nếu để trống đầu vào 0 của MUX đọc Register File (không nối hằng 0) thì chuyện gì xảy ra? | Đọc x0 ra giá trị floating (X, dây xanh dương). Mọi lệnh dùng x0 sai theo: `li`, `mv`, `j`, `beqz`… vốn đều là lệnh thật đọc x0 |
| 4 | `lw x5, 0(x1)` rồi ngay sau là `add x6, x5, x7`. Forwarding có cứu được không? Khối nào xử lý? | Không. Dữ liệu load chỉ có ở cuối tầng MEM, trong khi `add` cần nó ở đầu EX cùng chu kỳ. HazardUnit stall 1 chu kỳ (chèn bubble), sau đó ForwardUnit lấy dữ liệu từ MEM/WB (FwdA = 10) |
| 5 | `addi x5,x0,1` · `addi x5,x0,2` · `add x6,x5,x5`. Khi `add` ở EX, FwdA bằng bao nhiêu? Vì sao? | FwdA = 01: lấy từ EX/MEM, tức là lệnh gần nhất (x5 = 2). MEM/WB cũng khớp nhưng chứa giá trị cũ hơn (1), nên EX/MEM phải được ưu tiên |
| 6 | BranchUnit so sánh `rs1d` lấy thẳng từ ID/EX, hay giá trị sau MUX forwarding? Nếu dùng giá trị chưa forward thì lỗi gì? | Giá trị sau forwarding (`E_fa`, `E_fb`). Nếu không, `addi x5,x5,-1` rồi ngay sau `bnez x5, loop` sẽ so sánh giá trị x5 cũ, vòng lặp chạy sai số lần |

### Quyền Đức Công hỏi Đức Anh

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | Nếu không có Comparator, làm SLT (có dấu) từ bộ trừ thế nào? | Tính `A − B`. `A < B` (có dấu) = bit dấu của hiệu XOR cờ tràn (overflow). Chỉ nhìn bit dấu là sai khi phép trừ bị tràn, ví dụ `0x80000000 − 1` |
| 2 | Register File có 2 cổng đọc nhưng chỉ 1 cổng ghi. Vì sao đủ? | Mỗi lệnh RV32I đọc tối đa 2 thanh ghi và ghi tối đa 1. Trong pipeline, mỗi chu kỳ chỉ có một lệnh ở WB nên chỉ cần một cổng ghi |
| 3 | Lệnh ở MEM là `jal ra, f`, lệnh ở EX đọc `ra`. Forward giá trị gì? Có đúng không? | Forward `exres` = PC+4 của lệnh JAL, đúng là giá trị JAL ghi vào `ra`. Đúng nhờ exres đã chọn PC+4 cho JAL/JALR ngay từ tầng EX |
| 4 | Lệnh ở MEM là `lw x5`, lệnh ở EX đọc x5. ForwardUnit sẽ chọn 01 và lấy **địa chỉ** chứ không phải dữ liệu. Vì sao chuyện này không bao giờ xảy ra? | Vì HazardUnit đã stall 1 chu kỳ khi phát hiện load-use. Lúc lệnh phụ thuộc tới EX thì `lw` đã ở WB, và forward lấy dữ liệu từ MEM/WB. Hai khối phối hợp với nhau |
| 5 | `add x0, x5, x6` rồi ngay sau là `add x7, x0, x0`. x7 bằng bao nhiêu? Nếu ForwardUnit thiếu điều kiện `rd ≠ 0` thì x7 bằng bao nhiêu? | Đúng là x7 = 0. Thiếu điều kiện thì x0 bị forward thành `x5 + x6`, nên x7 = 2·(x5 + x6). Sai đặc tả "x0 luôn bằng 0" |
| 6 | Đường găng (critical path) của CPU đơn chu kỳ đi qua những khối nào trong mảng của Đức Anh? Khối nào chậm nhất? | MUX đọc Register File → MUX ASel/BSel → ALU, rồi ALU còn đi tiếp tới RAM. Trong ALU, bộ cộng 32 bit là chậm nhất (chuỗi nhớ lan truyền qua 32 bit) |

## Pha 2 · Đức Anh kiểm tra Hà và Công

Câu lẻ hỏi Hà, câu chẵn hỏi Công. Lượt sau đổi lại.

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | `0x80000000` hiểu là số có dấu bằng bao nhiêu? Hiểu là không dấu? | Có dấu: −2³¹ = −2 147 483 648. Không dấu: 2³¹ = 2 147 483 648 |
| 2 | `−8 >> 1` theo SRA và theo SRL cho kết quả gì (viết hex)? | SRA: `0xFFFFFFFC` = −4 (chép bit dấu). SRL: `0x7FFFFFFC` (chèn 0 bên trái) |
| 3 | ALU biết làm ADD hay SUB nhờ tín hiệu nào? Tín hiệu đó lấy từ đâu trong lệnh? | `alt` = ALUCtrl[3], lấy từ bit 30 của lệnh (qua ALUControl). funct3 = 000 cho cả ADD lẫn SUB |
| 4 | Ghi Register File: cái gì chọn thanh ghi nào được ghi? Ghi xảy ra lúc nào? | Decoder 5→32 biến WA (rd) thành one-hot, có Enable = WE (RegWrite). Ghi xảy ra ở cạnh lên clock, chỉ thanh ghi có EN = 1 |
| 5 | RAW hazard là gì? Cho một ví dụ hai lệnh. | Read After Write: lệnh sau đọc thanh ghi mà lệnh trước chưa kịp ghi. Ví dụ `addi x1, x0, 5` rồi ngay sau `add x2, x1, x1` |
| 6 | FwdA = 10 nghĩa là gì? | Toán hạng A lấy từ MEM/WB (W_data), tức là kết quả của lệnh đứng trước 2 lệnh |
| 7 | `addi x1,x0,1` · `addi x2,x0,2` · `add x3,x1,x2`. Khi `add` ở EX, FwdA và FwdB bằng bao nhiêu? | x2 vừa tính ở lệnh ngay trước, đang ở EX/MEM → FwdB = 01. x1 ở lệnh trước 2 lệnh, đang ở MEM/WB → FwdA = 10 |

# Phiên 3 — Quyền Đức Công trình bày: Memory, Pipeline, Kiểm thử

## Dàn ý trình bày

- Địa chỉ byte, little-endian, word address = `Addr[13:2]`, byte offset `Addr[1:0]`
- LoadUnit (dịch + extend), StoreUnit (read-modify-write) và byte-enable trong phần cứng thật
- Bản đồ bộ nhớ và memory-mapped I/O: UART (TTY + Keyboard), GPIO (LED 7 đoạn, LED, công tắc DIP). Demo `t11_io.s`
- 4 thanh ghi pipeline: chứa gì, vì sao tín hiệu điều khiển đi theo lệnh, stall bằng EN, flush đồng bộ bằng MUX nạp 0, bit valid
- Kiểm thử: test vector, golden model, run_tests, fuzz, bản NoHazard fail mọi test
- CPI: công thức `N + 4 + loaduse + 2·taken`, bảng số đo; vì sao pipeline vẫn nhanh hơn dù CPI > 1

**Công tự ôn trước buổi** (phải trả lời trôi chảy được):

- `sb` byte 0xAB vào offset 2 của word 0x11223344 cho ra gì? Mạch làm thế nào?
- Vì sao IMEM lấy `PC[11:2]`?
- Thanh ghi ID/EX chứa gì? Vì sao tín hiệu điều khiển phải đi theo lệnh qua từng tầng?
- Vì sao flush bằng MUX nạp 0 mà không dùng chân Clear của Register?
- Làm sao biết bộ test đủ mạnh? (Gợi ý: bản NoHazard fail mọi test.)

## Pha 1 · Người nghe phản biện Công

### Bùi Phạm Sơn Hà hỏi Công

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | Trong pipeline, lệnh `sw` ghi RAM ở tầng nào, vào thời điểm nào? Lệnh `lw` đọc RAM lúc nào? | Cả hai ở tầng MEM. `sw` ghi ở cạnh lên **cuối** chu kỳ MEM (khi RamWE = 1). `lw` đọc tổ hợp (asynchronous read) **trong** chu kỳ MEM, rồi dữ liệu được chốt vào MEM/WB ở cạnh lên |
| 2 | `lw t0, 2(x0)` (địa chỉ không chia hết cho 4) thì CPU làm gì? | Không hỗ trợ truy cập lệch. RAM đọc word ở địa chỉ 0, LoadUnit dịch phải 16 bit, kết quả không đúng đặc tả. Golden model báo lỗi. Đây là hạn chế ghi trong báo cáo (phần cứng thật sẽ sinh exception) |
| 3 | Vì sao ID/EX cần trường `MemRead` nhưng EX/MEM thì không có? | `ID_EX.MemRead` dùng để phát hiện load-use (HazardUnit cần biết lệnh ở EX có phải load không). Từ MEM trở đi RAM luôn đọc (OE = 1), chỉ cần `MemToReg` để chọn dữ liệu ghi lại |
| 4 | `exres` là gì? Vì sao một trường dùng được cho cả địa chỉ bộ nhớ, giá trị forward và giá trị ghi lại? | `exres = (JAL/JALR) ? PC+4 : kết quả ALU`. Load/store không bao giờ là JAL/JALR, nên với chúng exres chính là địa chỉ. Với lệnh khác, exres chính là giá trị sẽ ghi vào rd, nên forward từ EX/MEM luôn đúng (trừ load, đã có stall lo) |
| 5 | Công thức `cycles = N + 4 + loaduse + 2·taken`: số 4 ở đâu ra? | Thời gian lấp đầy pipeline. Lệnh cuối (EBREAK) được nạp ở chu kỳ N, cần thêm 4 cạnh clock nữa để đi qua ID, EX, MEM tới WB, lúc đó `halt` mới bật |
| 6 | Mạch được so với golden model. Nếu golden model cũng sai giống mạch thì sao? Nhóm giảm rủi ro này thế nào? | Rủi ro có thật. Giảm bằng cách: assembler được đối chiếu mã máy với `llvm-mc` (400 lệnh khớp 100%); ISS viết độc lập theo đặc tả, không dựa vào mạch; từng module còn có test vector riêng. Có thể đối chiếu thêm với RARS hoặc Spike |
| 7 | CPU biết bàn phím vừa có ký tự bằng cách nào? Có dùng ngắt không? | Không có ngắt. Phần mềm hỏi vòng (polling): đọc UART_STATUS (`0xF0000008`) lặp lại cho tới khi bit 0 = 1, rồi mới đọc UART_RXDATA. Muốn dùng ngắt phải có CSR và cơ chế trap, là một mục nâng cao khác |

### Nguyễn Đức Anh hỏi Công

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | Vì sao RAM phải đặt *Asynchronous read*? Nếu để đọc đồng bộ thì CPU đơn chu kỳ sai thế nào? | Đọc đồng bộ thì dữ liệu chỉ ra sau cạnh clock, khi lệnh `lw` đã kết thúc. Thanh ghi đích nhận dữ liệu cũ hoặc của lệnh khác. CPU đơn chu kỳ cần cả đường đi từ PC tới ghi lại là tổ hợp trong một chu kỳ |
| 2 | `sb` hoạt động thế nào khi RAM chỉ ghi được cả word 32 bit? Phần cứng thật làm khác ra sao? | Read-modify-write: đọc word cũ, `New = (Old AND ~M) OR ((WData << sh) AND M)`, rồi ghi cả word. Phần cứng thật dùng tín hiệu byte-enable (4 bit) để RAM chỉ ghi đúng byte cần ghi |
| 3 | Khi load-use, IF/ID được giữ (EN = 0) nhưng ID/EX lại bị flush. Vì sao không giữ luôn ID/EX? | Giữ ID/EX thì lệnh `lw` đang ở EX cũng đứng yên và không bao giờ tới MEM để lấy dữ liệu. Phải cho `lw` đi tiếp và chèn một bubble vào sau nó, còn lệnh phụ thuộc chờ ở ID |
| 4 | Bộ đếm `instret` làm sao không đếm bubble? | Mỗi lệnh mang bit `valid` qua các thanh ghi pipeline. Flush nạp toàn 0 nên bubble có valid = 0. `instret` chỉ tăng khi `MEM_WB.valid = 1` |
| 5 | Vì sao flush bằng MUX nạp 0 mà không dùng chân R (clear) của Register? | Chân clear của Register trong Logisim là bất đồng bộ: bật là xóa ngay giữa chu kỳ, kể cả trước khi tầng sau kịp dùng giá trị. MUX nạp 0 vào D thì việc xóa xảy ra đúng ở cạnh lên, đồng bộ với cả pipeline |
| 6 | Fuzz test sinh chương trình ngẫu nhiên. Làm sao chắc chắn chương trình luôn dừng? | Nhánh ngẫu nhiên chỉ nhảy tới trước. Vòng lặp nào cũng có bộ đếm riêng (x16). Gọi hàm dùng thanh ghi link riêng (x18) mà phần lệnh ngẫu nhiên không ghi đè. Thêm nữa, golden model báo lỗi nếu chạy quá 200 000 lệnh |
| 7 | Vì sao tín hiệu lấy ký tự khỏi Keyboard (`KbdRE`) phải AND với `MemRead`, và vì sao EX/MEM phải mang trường `MemRead`? | Đọc RXDATA có **tác dụng phụ**: ký tự bị lấy khỏi hàng đợi. Nếu không AND với MemRead, một lệnh `add` tình cờ tính ra 0xF0000004 cũng làm mất ký tự. Việc này chỉ được làm ở tầng MEM, nơi lệnh chắc chắn được thực thi (flush chỉ xóa IF/ID và ID/EX). Vì vậy tầng MEM phải biết MemRead, tức EX/MEM phải mang trường này |

## Pha 2 · Công kiểm tra Hà và Đức Anh

Câu lẻ hỏi Hà, câu chẵn hỏi Đức Anh. Lượt sau đổi lại.

| # | Câu hỏi | Đáp án mong đợi |
|---|---|---|
| 1 | Địa chỉ byte `0x00000108` nằm ở ô (word) số mấy của RAM, byte thứ mấy trong ô? | Ô số 0x108 >> 2 = 0x42 (66). Offset `Addr[1:0]` = 0, tức byte 0 |
| 2 | Word `0x11223344` đặt ở địa chỉ 0. `lbu t0, 1(x0)` cho ra gì? | `0x00000033`. Little-endian: byte 0 = 44, byte 1 = 33, byte 2 = 22, byte 3 = 11 |
| 3 | Byte `0x80` được nạp bằng `lb` và bằng `lbu` thì khác nhau thế nào? | `lb`: sign-extend → `0xFFFFFF80` (−128). `lbu`: zero-extend → `0x00000080` (128) |
| 4 | Thanh ghi pipeline dùng để làm gì? Kể tên 4 thanh ghi. | Cắt đường tổ hợp dài thành 5 đoạn và giữ toàn bộ thông tin của một lệnh giữa hai tầng. IF/ID, ID/EX, EX/MEM, MEM/WB |
| 5 | Stall và flush khác nhau thế nào trên thanh ghi pipeline? | Stall: EN = 0, giữ nguyên giá trị (lệnh đứng chờ). Flush: nạp toàn 0, biến lệnh thành bubble (lệnh bị xóa) |
| 6 | CPI là gì? Pipeline lý tưởng có CPI bằng bao nhiêu? Vì sao CPU của nhóm đo được 1.3–1.6? | Số chu kỳ trung bình cho một lệnh. Lý tưởng = 1. Thực tế cao hơn vì mỗi load-use mất 1 chu kỳ và mỗi lần nhảy mất 2 chu kỳ |
| 7 | Muốn in một ký tự ra TTY, và muốn hiện số 0x1234 lên LED 7 đoạn, thì chương trình viết gì? | `li s1, 0xF0000000` · `li t0, 72` · `sb t0, 0(s1)` in chữ H. `li t1, 0x1234` · `sw t1, 0x10(s1)` ghi vào GPIO_OUT |

# Bảo vệ thử (T7 7/11)

1. **Dẫn lệnh qua CPU** (mỗi người 5 phút, nói tên và giá trị từng tín hiệu): Hà dẫn `beq` nhảy, Đức Anh dẫn `add` phụ thuộc lệnh trước (có forwarding), Công dẫn `sw` ngay sau `lw` cùng thanh ghi. Ai cũng phải dẫn được `lw` qua CPU đơn chu kỳ.
2. **Hỏi ngẫu nhiên**: rút ngẫu nhiên câu bất kỳ trong file này, kể cả câu thuộc mảng người khác. Ưu tiên các câu từng bị chấm "Chưa" ở buổi T5.
3. Câu nào cả nhóm vẫn không trả lời được thì ghi lại và tra `LO_TRINH` cùng nhau trước CN 8/11.
