# Hướng dẫn demo CPU đơn chu kỳ trên Logisim

Demo trực tiếp trên `circ/RV32I_SingleCycle.circ`, gồm hai phần:

- Phần A: chạy `demo.s` (đã nạp sẵn trong ROM) để thầy thấy CPU chạy trọn một chương trình có vòng lặp, load/store và I/O.
- Phần B: theo dõi đúng lệnh trên slide 13, `lw t4, 8(sp)` (mã máy `0x00812E83`), qua từng khối trong một chu kỳ.

Phần C (nếu thầy hỏi về kiểm thử) là lệnh chạy bộ test tự động trên terminal.

Mọi giá trị ghi trong file này lấy từ lần chạy ngày 13/11/2026: `tools/rvsim.py` cho giá trị mong đợi, và
`tools/run_tests.py` trên Logisim cho kết quả PASS, kể cả với chương trình `demo/lw_demo.s`.

## Chuẩn bị trước giờ demo

1. Sinh file ảnh ROM cho phần B (chỉ cần làm một lần, file nằm trong `build/`):

   ```powershell
   cd D:\hust-master\KienTrucMayTienTien\Project
   python tools/rvasm.py demo/lw_demo.s -o build/lw_demo
   ```

   Kết quả là `build/lw_demo.text.hex`, gồm 6 lệnh:

   | PC | Mã máy | Lệnh | Tác dụng |
   |---|---|---|---|
   | 0x00 | 01000113 | `addi sp, zero, 0x10` | sp = 0x10 |
   | 0x04 | 123452b7 | `lui t0, 0x12345` | t0 = 0x12345000 |
   | 0x08 | 67828293 | `addi t0, t0, 0x678` | t0 = 0x12345678 |
   | 0x0C | 00512423 | `sw t0, 8(sp)` | M[0x18] = 0x12345678 |
   | 0x10 | 00812e83 | `lw t4, 8(sp)` | t4 = M[sp + 8] = 0x12345678 |
   | 0x14 | 00100073 | `ebreak` | halt |

   Ba lệnh đầu đặt sp = 0x10 và nạp 0x12345678 vào t0, lệnh `sw` ghi giá trị này vào RAM, để khi tới `lw` thì
   giá trị đọc ra khác 0 và dễ nhận ra.

   File hex chỉ chứa cột "Mã máy" (6 số, mỗi số là một ô ROM, ô 0 ứng với PC 0x00, ô 4 ứng với PC 0x10). Muốn
   xem đủ địa chỉ, mã máy và lệnh thì mở `build/lw_demo.lst`. File `build/lw_demo.data.hex` chỉ có một word 0 vì
   chương trình không có đoạn `.data`; phần B không cần nạp file này.

2. Mở Logisim-evolution 4.1.0, File → Open → `circ/RV32I_SingleCycle.circ`.
3. Vào Simulate → Tick Frequency. Chọn 8 Hz nếu vừa chạy vừa thuyết minh Phần A (RAM, a0, TTY đổi đủ chậm để chỉ
   tay), chọn 64 Hz nếu chỉ cần chạy nhanh tới kết quả. Tập trước ở nhà để biết từng đoạn chạy mất bao lâu ở tần
   số đã chọn. Ở mức 1 Hz, `demo.s` chạy 188 chu kỳ sẽ mất vài phút.
4. Chỉnh mức zoom (ô phần trăm ở góc dưới trái cửa sổ) sao cho thấy được cả ROM IMEM, Register File, ALU và RAM DMEM.
   Khi cần đọc số nhỏ thì phóng to vào đúng khối đó.

## Bản đồ màn hình: nhìn vào đâu

Mạch chia năm cột theo nhãn ở đầu: FETCH, DECODE / REGISTER READ, EXECUTE, MEMORY, WRITE BACK.

| Vị trí | Thành phần | Xem gì |
|---|---|---|
| Cột FETCH, bên trái | Thanh ghi `PC` | Địa chỉ lệnh đang chạy |
| Cột FETCH | ROM `IMEM` (ROM 1K x 32) và probe vàng `instr` bên phải ROM | Mã máy lệnh hiện tại |
| Cột DECODE, phía trên | `Control` (khối màu be) và các tunnel bên phải nó | RegWrite, ASel, BSel, ALUOp, MemRead, MemWrite, WBSel, Halt |
| Cột DECODE, giữa | `Register File` (khối xanh lá) | 32 dòng có nhãn `x0 zero`, `x1_ra`… `x31_t6`: cột trái x0 đến x15, cột phải x16 đến x31; ví dụ `x2_sp` dòng 3 cột trái, `x10_a0` dòng 11 cột trái, `x29_t4` dòng 14 cột phải |
| Cột DECODE, dưới | `ImmGen` | Immediate |
| Cột EXECUTE | `ALU` (hình thang xanh) và probe vàng `ALU_result` | Kết quả ALU, với load/store là địa chỉ |
| Cột EXECUTE, dưới | `Branch` | Taken khi rẽ nhánh |
| Cột MEMORY | `AddrDec`, `Store`, RAM `DMEM` (RAM 4K x 32), `I/O Ctrl` | Nội dung RAM, mỗi dòng 2 word, số đầu dòng là chỉ số word |
| Cột WRITE BACK | `Load`, MUX WBSel, probe vàng `WB_data` | Giá trị sẽ ghi vào rd |
| Góc dưới phải | TTY (UART), 4 LED 7 đoạn, 8 LED | Kết quả I/O của `demo.s` |
| Hàng dưới cùng | Chân `halt`, `cycles`, `instret`, `pc`, `gpio` | Bộ đếm hiệu năng, số hiển thị dạng hex |

Dây 1 bit: xanh lá sáng là 1, xanh lá đậm là 0. Dây nhiều bit (ALUOp, BSel, WBSel) không đọc được qua màu; chọn công cụ
Poke (bàn tay trên thanh công cụ) rồi bấm vào dây để Logisim hiện giá trị. Nên thử thao tác này trước ở nhà.

Phím tắt: Ctrl+R reset, Ctrl+T chạy nửa chu kỳ (một lần bấm là một cạnh clock), Ctrl+K bật hoặc tắt clock tự chạy.

## Phần A: chạy demo.s

Mục tiêu: cho thầy thấy CPU chạy trọn một chương trình nạp sẵn trong ROM, có tính toán, vòng lặp, load/store và
I/O, và mỗi lệnh xong trong một chu kỳ. Cách trình bày giống Phần B: thao tác, giá trị đúng, lời nói (đoạn `>`).

Kịch bản rút gọn để thuyết trình trong 3 phút nằm ở `demo/KICH_BAN_DEMO_S_3PHUT.md`. Các mục dưới đây là bản đầy đủ
để học trước và để tra khi thầy hỏi sâu.

### Kiến thức nền trước khi demo

Đọc hết mục này trước khi tập. Mỗi khái niệm có ghi nó nằm ở đâu trên màn hình.

#### 1. Máy tính trong mạch gồm những gì

| Thành phần | Là gì | Trên màn hình |
|---|---|---|
| CPU | Phần đọc lệnh, giải mã, tính toán, quyết định lệnh tiếp theo | Toàn bộ 5 cột FETCH → WRITE BACK |
| Bộ nhớ lệnh | Chứa chương trình (mã máy), CPU chỉ đọc | ROM `IMEM`, khối "ROM 1K x 32" ở cột FETCH: 1024 ô, mỗi ô 32 bit |
| Bộ nhớ dữ liệu | Chứa dữ liệu chương trình đọc/ghi | RAM `DMEM`, khối "RAM 4K x 32" ở cột MEMORY: 4096 ô, mỗi ô 32 bit |
| Thiết bị vào/ra (I/O) | Màn hình chữ, bàn phím, đèn, công tắc | Góc dưới phải: TTY, Keyboard, 4 LED 7 đoạn, 8 LED, 8 DIP switch |

Lệnh và dữ liệu nằm ở hai bộ nhớ riêng. PC chỉ dùng để đọc ROM. Lệnh `lw`/`sw` chỉ đọc/ghi RAM hoặc I/O, nên địa chỉ
0 của RAM không liên quan tới lệnh ở PC = 0.

#### 2. Chương trình, mã máy và assembler

- Chương trình viết bằng hợp ngữ (file `.s`), ví dụ `add a0, a0, t4`.
- CPU chỉ hiểu mã máy: mỗi lệnh là một số 32 bit, viết thành 8 chữ số hex, ví dụ `01d50533`.
- `tools/rvasm.py` là assembler của nhóm: dịch `.s` thành file `.text.hex`, rồi Load Image nạp file này vào ROM.
- Một số lệnh trong `.s` là lệnh giả, assembler đổi thành lệnh thật. Ví dụ `li sp, 0x3FF0` thành hai lệnh
  `lui sp, 4` + `addi sp, sp, -16`; `mv t0, t1` thành `addi t0, t1, 0`; `bnez t2, fibl` thành `bne t2, x0, fibl`.
  Vì vậy `demo.s` có 53 dòng lệnh nhưng ROM có 57 lệnh (`li sp`, `li s1` và hai lệnh `la` mỗi lệnh thành hai). Muốn đối chiếu từng lệnh thì mở `build/demo.lst`.

#### 3. Số hex

Logisim hiện mọi giá trị dạng hex (cơ số 16): chữ số 0–9 rồi a = 10, b = 11, c = 12, d = 13, e = 14, f = 15. Mỗi chữ
số hex là 4 bit, nên 32 bit là 8 chữ số. Đổi sang thập phân: `e8` = 14 × 16 + 8 = 232; `59` = 5 × 16 + 9 = 89;
`3ff0` = 16368. Các số cần nhớ khi demo: 0x10 = 16, 0x18 = 24, 0x30 = 48, 0xBC = 188, 0xE8 = 232.

#### 4. PC (Program Counter)

PC là thanh ghi 32 bit giữ địa chỉ của lệnh đang chạy, nằm ở cột FETCH bên trái, có nhãn `PC`. Mỗi lệnh dài 4 byte,
nên bình thường PC tăng 4 sau mỗi chu kỳ (0x00, 0x04, 0x08...). Lệnh rẽ nhánh hoặc nhảy (`bne`, `jal`...) có thể đưa
PC tới địa chỉ khác, đó là cách vòng lặp quay lại. ROM đánh số theo ô, ô = PC / 4: PC = 0x1C thì đọc ô 7.

#### 5. Thanh ghi và Register File

Thanh ghi là ô nhớ nhỏ, nhanh, nằm trong CPU. RV32I có 32 thanh ghi, mỗi thanh ghi 32 bit, tên x0 đến x31. Lệnh tính
toán (`add`, `addi`, `sub`...) chỉ làm việc trên thanh ghi. x0 đặc biệt: luôn bằng 0, ghi vào cũng không đổi.

Mỗi thanh ghi còn có tên ABI theo quy ước dùng trong hợp ngữ. Assembler hiểu cả hai tên, `a0` và `x10` là cùng một
thanh ghi:

| Tên ABI | Số thanh ghi | Quy ước dùng |
|---|---|---|
| zero | x0 | luôn bằng 0 |
| ra | x1 | địa chỉ trả về khi gọi hàm |
| sp | x2 | con trỏ ngăn xếp |
| gp, tp | x3, x4 | con trỏ toàn cục, con trỏ luồng (demo không dùng) |
| t0 – t2 | x5 – x7 | biến tạm |
| s0, s1 | x8, x9 | biến cần giữ qua lời gọi hàm |
| a0 – a7 | x10 – x17 | tham số hàm; a0 còn là giá trị trả về |
| s2 – s11 | x18 – x27 | biến cần giữ qua lời gọi hàm |
| t3 – t6 | x28 – x31 | biến tạm |

Trên màn hình, `Register File` là khối màu xanh lá ở giữa cột DECODE / REGISTER READ, tiêu đề "Register File" ở trên.
Bên trong khối hiện giá trị cả 32 thanh ghi, chia hai cột, mỗi cột 16 dòng. Mỗi dòng có nhãn chữ nhỏ bên trái dạng
`số_tênABI` và giá trị 8 chữ số hex bên phải:

```
            Register File
 x0 zero  00000000      x16_a6   00000000
 x1_ra    00000000      x17_a7   00000000
 x2_sp    00003ff0      x18_s2   00000000
 x3_gp    00000000      x19_s3   00000000
 x4_tp    00000000      x20_s4   00000000
 x5_t0    00000090      x21_s5   00000000
 x6_t1    000000e9      x22_s6   00000000
 x7_t2    00000000      x23_s7   00000000
 x8_s0    00000030      x24_s8   00000000
 x9_s1    f0000000      x25_s9   00000000
 x10_a0   000000e8      x26_s10  00000000
 x11_a1   00000000      x27_s11  00000000
 x12_a2   00000000      x28_t3   000000e9
 x13_a3   00000000      x29_t4   00000059
 x14_a4   00000000      x30_t5   000000ff
 x15_a5   00000000      x31_t6   00000000
```

Giá trị trong sơ đồ là lúc `demo.s` chạy xong (lấy từ `rvsim.py`). Vậy "trỏ vào a0" nghĩa là: zoom vào khối Register
File, tìm dòng có nhãn `x10_a0`, tức dòng thứ 11 của cột trái, ngay dưới `x9_s1`. Nhãn dùng chữ cỡ 8 nên phải zoom
khá lớn mới đọc được, nên thử trước ở nhà.

#### 6. Thanh ghi khác RAM thế nào

| | Thanh ghi | RAM `DMEM` |
|---|---|---|
| Ở đâu | trong CPU (`Register File`) | ngoài đường tính toán, cột MEMORY |
| Số ô | 32 | 4096 |
| Gọi bằng | tên thanh ghi trong lệnh (a0, t0...) | địa chỉ byte tính bằng thanh ghi + offset |
| Lệnh dùng | mọi lệnh tính toán | chỉ `lw`/`sw` và các biến thể byte/half (`lb`, `sb`...) |

Kiến trúc kiểu này gọi là load/store: muốn tính trên dữ liệu trong RAM thì phải `lw` vào thanh ghi trước, tính xong
`sw` ra RAM.

Địa chỉ trong lệnh là địa chỉ byte, còn mỗi ô RAM chứa 4 byte, nên ô = địa chỉ / 4 (địa chỉ 0x18 là ô 6). Trên màn
hình, RAM hiện mỗi dòng 2 ô. Số đầu dòng (hex) là số thứ tự của ô đầu dòng, nên các dòng đánh số 000, 002, 004...

#### 7. Bản đồ địa chỉ (memory map)

| Địa chỉ | Thiết bị | Dùng trong demo.s |
|---|---|---|
| 0x0000_0000 – 0x0000_3FFF | RAM 16 KiB (4096 ô) | mảng `fib` ở 0x00 – 0x2F |
| 0xF000_0000 | UART TX: ghi 1 byte là in 1 ký tự lên TTY | in `Hello RISC-V!` |
| 0xF000_0004 | UART RX: đọc ký tự từ Keyboard | không |
| 0xF000_0008 | UART STATUS: bàn phím có ký tự chưa | không |
| 0xF000_0010 | GPIO_OUT: bit 15:0 ra 4 LED 7 đoạn, bit 23:16 ra 8 LED | `00E8` và 8 LED |
| 0xF000_0014 | GPIO_IN: đọc 8 DIP switch | không |

Khối `AddrDec` ở cột MEMORY nhìn 4 bit cao của địa chỉ: bằng F thì là I/O (IsIO = 1), còn lại là RAM.

#### 8. Clock, chu kỳ và các bộ đếm

- Clock là tín hiệu đổi 0/1 liên tục. Một chu kỳ là từ cạnh lên này tới cạnh lên tiếp theo. Ctrl+T đổi clock một nửa
  chu kỳ, nên hai lần bấm là một chu kỳ. Ctrl+K cho clock tự chạy hoặc dừng.
- Chỉ ba khối có trí nhớ là `PC`, `Register File` và RAM `DMEM`, và chúng chỉ đổi giá trị ở cạnh lên. Các khối khác
  tính tức thì theo đầu vào (xem thêm "Đọc trước: single cycle chạy thế nào" ở Phần B).
- Hàng dưới cùng có các chân ra:
  - `cycles`: số chu kỳ đã chạy;
  - `instret`: số lệnh đã hoàn thành;
  - `pc`: bản sao PC;
  - `halt`: bằng 1 khi CPU dừng;
  - `gpio`: giá trị GPIO_OUT.
- CPI = cycles / instret. CPU đơn chu kỳ luôn có CPI = 1.

#### 9. Các loại lệnh gặp trong demo.s

| Lệnh | Làm gì | Ví dụ trong demo.s |
|---|---|---|
| `addi rd, rs1, imm` | rd = rs1 + hằng số | `addi s0, s0, 4` |
| `add rd, rs1, rs2` | rd = rs1 + rs2 | `add t3, t0, t1` |
| `lui rd, imm` | rd = imm << 12 (nạp 20 bit cao) | `lui s1, 0xF0000` để có 0xF0000000 |
| `sw rs2, off(rs1)` | ghi 4 byte của rs2 vào địa chỉ rs1 + off | `sw t0, 0(s0)` |
| `sb rs2, off(rs1)` | ghi 1 byte thấp của rs2 | `sb t5, 0(s1)` in một ký tự |
| `lw rd, off(rs1)` | đọc 4 byte từ địa chỉ rs1 + off vào rd | `lw t4, 0(s0)` |
| `bne rs1, rs2, nhãn` | nếu rs1 ≠ rs2 thì nhảy tới nhãn | `bnez t2, fibl` = `bne t2, x0, fibl` |
| `ebreak` | dừng CPU (Halt = 1) | lệnh cuối |

#### 10. Công cụ và ký hiệu của Logisim cần biết

- Tunnel là nhãn tên đặt ở đầu dây, ví dụ `instr`, `alu`, `pc4`. Hai tunnel cùng tên coi như được nối với nhau, dù
  không có dây vẽ giữa chúng. Vì vậy nhiều khối nhìn như không nối gì: dây của chúng đi qua tunnel.
- Probe là ô vàng hiện sẵn giá trị một dây, ví dụ `instr`, `ALU_result`, `WB_data`.
- Màu dây: dây 1 bit xanh lá sáng là 1, xanh lá đậm là 0. Dây nhiều bit không đọc được qua màu.
- Công cụ Poke (bàn tay): bấm vào dây để xem giá trị. Công cụ Select (mũi tên): chọn khối, xem thuộc tính ở góc dưới
  trái. Dùng Select trước khi bấm Ctrl+T.
- Phím tắt: Ctrl+R reset, Ctrl+T nửa chu kỳ, Ctrl+K bật/tắt clock tự chạy.

### Đọc trước: demo.s làm gì

`demo.s` có 57 lệnh trong ROM, chạy 188 lệnh (có vòng lặp) rồi dừng ở `ebreak`. Chương trình chia năm đoạn. Nhìn
thanh ghi `PC` là biết CPU đang ở đoạn nào:

| Đoạn | PC | Việc làm | Khi đoạn kết thúc | Thấy gì trên màn hình |
|---|---|---|---|---|
| 1. Khởi tạo | 0x00 – 0x18 | sp = 0x3FF0, s0 = 0 (địa chỉ mảng `fib`), t0 = 0, t1 = 1, t2 = 12 | `cycles` = 7 | các thanh ghi trên nhận giá trị |
| 2. Vòng Fibonacci | 0x1C – 0x34 | 12 vòng, mỗi vòng 7 lệnh: ghi F(n) vào RAM, tính số tiếp theo | PC ra 0x38, `cycles` = 0x5B (91) | RAM ô 0 đến ô 11 lần lượt có số |
| 3. Vòng tính tổng | 0x38 – 0x58 | đọc lại 12 ô RAM, cộng dồn vào a0 | PC ra 0x5C, `cycles` = 0x9B (155) | x10 (a0) tăng dần tới e8 |
| 4. In chuỗi | 0x5C – 0xD0 | 14 cặp `li t5, mã ASCII` + `sb t5, 0(s1)` | PC ra 0xD4, `cycles` = 0xB9 (185) | TTY hiện từng chữ `Hello RISC-V!` |
| 5. GPIO và dừng | 0xD4 – 0xE0 | ghi a0 ra 4 LED 7 đoạn, bật 8 LED, `ebreak` | `cycles` = `instret` = 0xBC (188) | `00E8`, 8 LED sáng, `halt` = 1 |

Các thanh ghi `demo.s` dùng, tìm theo nhãn trong khối `Register File` (xem sơ đồ ở mục 5 phần kiến thức nền):

| Nhãn trên màn hình | Vị trí | Vai trò trong demo.s | Giá trị cuối |
|---|---|---|---|
| `x2_sp` | cột trái, dòng 3 | con trỏ ngăn xếp, chỉ khởi tạo | 00003ff0 |
| `x5_t0`, `x6_t1` | cột trái, dòng 6, 7 | hai số Fibonacci liên tiếp F(n), F(n+1) | 00000090, 000000e9 |
| `x7_t2` | cột trái, dòng 8 | bộ đếm vòng lặp, từ 12 (0xc) về 0 | 00000000 |
| `x8_s0` | cột trái, dòng 9 | địa chỉ ô RAM đang ghi/đọc, mỗi vòng +4 | 00000030 |
| `x9_s1` | cột trái, dòng 10 | địa chỉ I/O 0xF0000000 | f0000000 |
| `x10_a0` | cột trái, dòng 11 | tổng cộng dồn | 000000e8 |
| `x28_t3` | cột phải, dòng 13 | F(n) + F(n+1) tạm thời | 000000e9 |
| `x29_t4` | cột phải, dòng 14 | số vừa đọc từ RAM ở vòng tính tổng | 00000059 |
| `x30_t5` | cột phải, dòng 15 | mã ASCII của ký tự sắp in | 000000ff |

### Đọc trước: dãy Fibonacci vào RAM bằng cách nào

Không ai nhập dãy số vào RAM. Chương trình tự tính bằng lệnh `add` và tự ghi bằng lệnh `sw`, đi qua đúng đường dữ
liệu đã giải thích ở Phần B (lệnh `sw t0, 8(sp)` của `lw_demo`):

```
fibl:   sw   t0, 0(s0)      # ghi F(n) vào RAM ở địa chỉ s0
        add  t3, t0, t1     # t3 = F(n) + F(n+1) = F(n+2)
        mv   t0, t1         # dời cửa sổ: t0 = F(n+1)
        mv   t1, t3         #             t1 = F(n+2)
        addi s0, s0, 4      # địa chỉ word tiếp theo
        addi t2, t2, -1     # còn bao nhiêu số
        bnez t2, fibl       # chưa đủ 12 số thì quay lại
```

Ở lệnh `sw t0, 0(s0)` của vòng thứ n (đếm từ 0):

- Register File đọc rs1 = s0 = 4n và rs2 = t0 = F(n).
- ALU tính s0 + 0 = 4n. `AddrDec` ra WordAddr = n, IsIO = 0, RamWE = 1.
- Khối `Store` đưa t0 ra dây `stnew`, đi vào chân dữ liệu của RAM.
- Ở cạnh lên, RAM ghi F(n) vào ô n.

Mảng `fib` bắt đầu ở địa chỉ 0, nên 12 số nằm ở ô 0 đến ô 11. RAM hiện mỗi dòng 2 word, số đầu dòng là chỉ số word
của ô đầu dòng:

| Dòng RAM | Ô | Giá trị (hex) | Thập phân |
|---|---|---|---|
| 000 | 0, 1 | 0, 1 | 0, 1 |
| 002 | 2, 3 | 1, 2 | 1, 2 |
| 004 | 4, 5 | 3, 5 | 3, 5 |
| 006 | 6, 7 | 8, d | 8, 13 |
| 008 | 8, 9 | 15, 22 | 21, 34 |
| 00a | 10, 11 | 37, 59 | 55, 89 |

### Đọc trước: a0 là gì, vì sao bằng 0xE8

a0 là thanh ghi x10. Tên a0 (argument 0) lấy từ quy ước gọi hàm của RISC-V: a0 chứa tham số đầu tiên và giá trị trả
về của hàm. `demo.s` dùng a0 làm biến tổng:

```
suml:   lw   t4, 0(s0)      # đọc lại F(n) từ RAM ô n
        add  a0, a0, t4     # cộng dồn
        addi s0, s0, 4
        addi t2, t2, -1
        bnez t2, suml
```

a0 sau mỗi vòng: 0, 1, 2, 4, 7, c, 14, 21, 36, 58, 8f, e8 (hex). Kết quả 0+1+1+2+3+5+8+13+21+34+55+89 = 232, và
232 = 14 × 16 + 8 = 0xE8. Vòng này đọc ngược từ RAM nên nó kiểm tra luôn lệnh `lw`: nếu vòng Fibonacci ghi sai một ô
thì tổng sẽ khác 0xE8.

### Đọc trước: TTY và GPIO nhận dữ liệu qua đâu

CPU không có lệnh "in" riêng. TTY (khung màn hình chữ ở góc dưới phải, có chữ "UART TX: TTY (0xF0000000)") được nối
như một ô nhớ đặc biệt ở địa chỉ 0xF0000000. Cách này gọi là memory-mapped I/O. Ghi một byte bằng `sb` vào địa chỉ
đó là in ra một ký tự.

Đường đi của lệnh `sb t5, 0(s1)`, với s1 = 0xF0000000 và t5 là mã ASCII, ví dụ 72 = 'H':

- ALU tính địa chỉ 0xF0000000.
- `AddrDec` thấy Addr[31:28] = F nên ra IsIO = 1. RamWE = MemWrite AND NOT IsIO = 0, nên RAM không bị ghi.
- `I/O Ctrl` chọn thanh ghi I/O theo Addr[4:2] = 0, tức UART TX. Nó bật TxWE = 1 và đưa 7 bit thấp của dữ liệu ra
  TxData.
- Ở cạnh lên, TTY nhận ký tự và hiện lên màn hình.

GPIO cũng làm theo cách đó:

- `sw a0, 0x10(s1)` ghi 0x000000E8 vào thanh ghi `GPIO_OUT` (địa chỉ 0xF0000010) nằm trong `I/O Ctrl`. Bit 15:0 nối
  ra 4 LED 7 đoạn, hiện `00E8`.
- `sb t5, 0x12(s1)` với t5 = 0xFF ghi vào byte 2 của `GPIO_OUT`, tức bit 23:16, nối ra 8 LED.
- Khối `Store` chỉ thay byte 2 và giữ nguyên ba byte còn lại, đọc lại từ `GPIO_OUT` qua MUX "IsIO ? I/O : RAM". Vì
  vậy chân `gpio` cuối cùng là 00ff00e8.

### A1. Giới thiệu mạch

Thao tác: zoom ra cho thấy cả mạch. Trỏ chuột lần lượt qua 5 nhãn cột FETCH, DECODE / REGISTER READ, EXECUTE, MEMORY,
WRITE BACK, rồi chỉ `PC`, ROM `IMEM` (ROM 1K x 32), `Register File`, `ALU`, RAM `DMEM` (RAM 4K x 32), khu I/O ở góc
dưới phải.

> "Đây là CPU đơn chu kỳ RV32I của nhóm em. PC 32 bit, ROM lệnh 1K word, 32 thanh ghi 32 bit, RAM dữ liệu 4K word.
> Mạch xếp thành 5 cột theo 5 bước IF, ID, EX, MEM, WB, nhưng giữa các cột không có thanh ghi, nên mỗi lệnh đi hết 5
> bước trong một chu kỳ clock. Góc dưới phải là khu I/O: màn hình chữ TTY, bàn phím, 4 LED 7 đoạn và 8 LED, CPU truy
> cập chúng qua địa chỉ 0xF000_0000 trở lên."

### A2. Reset

Thao tác: Ctrl+R. Chỉ lần lượt: `PC` = 00000000, probe `instr` = 00004137, `Register File` toàn 0, RAM toàn 0, TTY
trống, LED 7 đoạn `0000`, 8 LED tắt, chân `cycles` = 00000000.

> "Chương trình demo.s đã được assembler của nhóm dịch và nạp sẵn vào ROM lệnh. Sau reset, PC bằng 0, mọi thanh ghi
> và RAM bằng 0. Em không sửa tay giá trị nào, mọi thứ thay đổi sau đây đều do lệnh trong ROM. Lệnh đầu tiên
> 0x00004137 là `lui sp, 4`, phần đầu của lệnh giả `li sp, 0x3FF0`."

### A3. Đoạn khởi tạo (bấm từng bước)

Đoạn này chỉ có 7 lệnh. Để clock tự chạy thì nó xong trong khoảng một giây, không kịp chỉ, nên đi từng lệnh bằng
Ctrl+T. Mỗi lệnh cần hai lần bấm, tổng cộng 14 lần.

Thao tác: zoom sao cho thấy cùng lúc thanh ghi `PC`, probe `instr` (cột FETCH), khối `Register File` (đọc được nhãn)
và probe `WB_data` (cột WRITE BACK). Với mỗi lệnh, làm ba việc:

1. Trước khi bấm, đọc probe `instr` và `PC` để biết lệnh đang chạy. Đọc probe `WB_data` để biết giá trị sắp ghi.
2. Bấm Ctrl+T tới khi `PC` đổi.
3. Trỏ vào dòng thanh ghi vừa nhận giá trị trong `Register File`.

| PC | `instr` | Lệnh thật | Thuộc lệnh trong demo.s | Dòng thay đổi sau cạnh lên | Giá trị mới |
|---|---|---|---|---|---|
| 00 | 00004137 | `lui sp, 4` | `li sp, 0x3FF0` | `x2_sp` (cột trái, dòng 3) | 00004000 |
| 04 | ff010113 | `addi sp, sp, -16` | `li sp, 0x3FF0` | `x2_sp` | 00003ff0 |
| 08 | 00000437 | `lui s0, 0` | `la s0, fib` | `x8_s0` (cột trái, dòng 9) | 00000000, không đổi |
| 0c | 00040413 | `addi s0, s0, 0` | `la s0, fib` | `x8_s0` | 00000000, không đổi |
| 10 | 00000293 | `addi t0, x0, 0` | `li t0, 0` | `x5_t0` (cột trái, dòng 6) | 00000000, không đổi |
| 14 | 00100313 | `addi t1, x0, 1` | `li t1, 1` | `x6_t1` (cột trái, dòng 7) | 00000001 |
| 18 | 00c00393 | `addi t2, x0, 12` | `li t2, 12` | `x7_t2` (cột trái, dòng 8) | 0000000c |

Ba lệnh ở PC 08, 0c, 10 ghi giá trị 0 vào thanh ghi vốn đã bằng 0 sau reset, nên trên màn hình không thấy gì đổi.
Khi tới mấy lệnh này, chỉ vào `WB_data` = 00000000 và nói lệnh vẫn ghi, chỉ là ghi số 0.

Lời nói theo từng chỗ chỉ:

> (chỉ `instr` = 00004137, rồi `x2_sp` đổi thành 00004000, rồi 00003ff0) "Hai lệnh đầu là lệnh giả `li sp, 0x3FF0`.
> Assembler tách nó thành `lui` nạp 20 bit cao, được 0x4000, rồi `addi` trừ 16, được 0x3FF0. sp là con trỏ ngăn xếp,
> đặt ở đỉnh RAM."
>
> (chỉ `x8_s0` và `WB_data` = 0) "Lệnh `la s0, fib` nạp địa chỉ mảng fib vào s0. Mảng nằm ở đầu RAM nên địa chỉ là 0.
> s0 sẽ là con trỏ tới ô RAM đang ghi."
>
> (chỉ `x5_t0`, rồi `x6_t1` đổi thành 1) "t0 bằng 0 và t1 bằng 1 là hai số Fibonacci đầu tiên, F(0) và F(1)."
>
> (chỉ `x7_t2` đổi thành c) "t2 bằng 12, viết hex là c, là số phần tử cần tính. Mỗi vòng lặp sẽ trừ t2 đi 1."

Sau lệnh thứ 7, `PC` = 0000001c: CPU đã tới đầu vòng lặp `fibl`.

### A3b. Vòng Fibonacci

Thao tác: Ctrl+K cho clock tự chạy (8 Hz). Chuyển sang RAM `DMEM`, chỉ từng ô khi có số mới. Thỉnh thoảng chỉ `PC`
đang quay vòng trong khoảng 0x1C đến 0x34, và dòng `x8_s0` tăng 4 sau mỗi vòng.

> "Bây giờ CPU vào vòng lặp. Thầy nhìn PC chạy từ 0x1C tới 0x34 rồi nhảy về 0x1C, đó là lệnh `bnez` rẽ nhánh. Mỗi vòng,
> lệnh `sw` ghi t0 vào ô RAM có địa chỉ s0, rồi s0 tăng 4 để sang ô tiếp theo. Dãy Fibonacci hiện dần trong RAM: 0, 1,
> 1, 2, 3, 5, 8, 0xD..."

Nên làm thêm nếu có thời gian: dừng ở một lệnh `sw` để chỉ đường ghi. Ctrl+K để dừng clock, rồi bấm Ctrl+T tới khi
`PC` = 0000001c. Dùng Poke xem các dây: `rs1d` = s0, `rs2d` = t0, `ALU_result` = s0, `WordAddr` = s0 / 4,
`RamWE` = 1, `stnew` = t0. Bấm thêm một cạnh lên để thấy ô RAM tương ứng nhận giá trị. Ctrl+K để chạy tiếp.

> "Em dừng ở lệnh `sw`. Địa chỉ s0 qua ALU rồi tới bộ giải mã địa chỉ, ra số thứ tự ô RAM và RamWE bằng 1. Giá trị
> t0 qua khối Store tới chân dữ liệu của RAM. Tới cạnh lên clock thì RAM ghi, đây ô này vừa nhận số mới."

### A4. Vòng tính tổng

Thao tác: khi `PC` ra khỏi khoảng 0x1C – 0x34 (RAM đã có đủ 12 số, dòng 00a là `37 59`), zoom vào `Register File`,
trỏ vào dòng nhãn `x10_a0` (cột trái, dòng 11, ngay dưới `x9_s1`) và dòng nhãn `x29_t4` (cột phải, dòng 14). Chỉ a0 tăng dần: 1, 2, 4, 7, c, 14, 21, 36, 58, 8f, e8.

> "Đủ 12 số thì vòng lặp thoát. Đoạn tiếp theo đọc lại từng ô RAM bằng lệnh `lw` vào t4 rồi cộng dồn vào a0. a0 là
> thanh ghi x10, theo quy ước RISC-V dùng cho tham số và giá trị trả về, ở đây em dùng làm biến tổng. Tổng 12 số
> Fibonacci đầu là 232, tức 0xE8. Vì a0 lấy dữ liệu đọc lại từ RAM, đúng 0xE8 nghĩa là cả `sw` lẫn `lw` đều chạy đúng."

### A5. In chuỗi ra TTY

Thao tác: khi `PC` qua 0x5C, trỏ vào TTY. Chỉ từng chữ hiện ra. Có thể chỉ thêm dòng `x30_t5` (cột phải, dòng 15) đổi theo
mã ASCII (Register File hiện hex: 00000048 = 72 = 'H', 00000065 = 101 = 'e'...) và x9 (s1) = f0000000.

> "Bây giờ CPU in chuỗi ra TTY. CPU không có lệnh in riêng: TTY được gắn vào địa chỉ 0xF0000000. Mỗi cặp lệnh nạp
> mã ASCII vào t5 rồi `sb` ghi byte đó vào địa chỉ 0xF0000000. Bộ giải mã địa chỉ thấy 4 bit cao bằng F nên chuyển lệnh
> ghi sang khối I/O thay cho RAM, RAM không bị ghi. Khối I/O bật tín hiệu ghi của TTY và ký tự hiện lên màn hình."

Nếu thầy muốn xem chi tiết: Ctrl+K dừng, Ctrl+T tới một lệnh `sb t5, 0(s1)` (PC 0x68, 0x70, 0x78... tức các địa chỉ
chia hết cho 8 từ 0x68 đến 0xD0). Poke `IsIO` = 1, `RamWE` = 0, và dây `IO_txwe` cạnh TTY = 1. Bấm một
cạnh lên, TTY hiện thêm một chữ.

### A6. GPIO và dừng

Thao tác: trỏ vào 4 LED 7 đoạn (`00E8`) và 8 LED (sáng hết), có chữ "GPIO_OUT (0xF0000010): [15:0] hex, [23:16] LED"
phía trên. Đợi chân `halt` = 1, Ctrl+K tắt clock. Chỉ `PC` đứng ở 000000e0.

> "Lệnh `sw a0, 0x10(s1)` ghi tổng ra thanh ghi GPIO ở 0xF0000010, 16 bit thấp nối ra 4 LED 7 đoạn nên hiện 00E8.
> Lệnh `sb` tiếp theo ghi 0xFF vào byte 2 của thanh ghi đó, nối ra 8 LED nên sáng hết. Cuối cùng là `ebreak`: Control
> bật Halt, PC dừng ở 0xE0."

### A7. Kiểm tra kết quả cùng thầy

| Chỗ nhìn | Giá trị đúng | Ý nghĩa |
|---|---|---|
| TTY | `Hello RISC-V!` | 14 lệnh `sb` ra UART đúng thứ tự |
| RAM dòng 000 đến 00a | 0, 1, 1, 2, 3, 5, 8, d, 15, 22, 37, 59 | vòng Fibonacci và lệnh `sw` |
| x10 (a0) | 000000e8 | vòng tính tổng và lệnh `lw` |
| LED 7 đoạn | `00E8` | GPIO_OUT[15:0] |
| 8 LED | sáng hết | GPIO_OUT[23:16] = 0xFF |
| Chân `gpio` | 00ff00e8 | giá trị đầy đủ của GPIO_OUT |
| x2 (sp), x8 (s0), x9 (s1) | 00003ff0, 00000030, f0000000 | s0 = 12 × 4 sau 12 vòng |
| `PC`, chân `halt` | 000000e0, 1 | dừng ở `ebreak` |
| Chân `cycles` và `instret` | 000000bc (188), bằng nhau | CPI = 1 |

> "Kết quả khớp hết: dãy Fibonacci trong RAM, tổng 0xE8 trong a0 và trên LED, chuỗi trên TTY. Bộ đếm cycles và instret
> đều bằng 188, tức 188 lệnh trong 188 chu kỳ, CPI bằng 1, đúng tính chất CPU đơn chu kỳ."

### Nếu thầy hỏi (Phần A)

| Câu hỏi | Trả lời |
|---|---|
| Sao t0 cuối cùng là 0x90 (144), không phải 0x59? | Mỗi vòng tính trước số tiếp theo. Sau vòng thứ 12, t0 = F(12) = 144 và t1 = F(13) = 233 (0xE9), nhưng chỉ F(0) đến F(11) được ghi vào RAM. |
| sp = 0x3FF0 để làm gì? | Đặt con trỏ ngăn xếp ở đỉnh RAM 16 KiB theo thói quen. demo.s không gọi hàm nên không dùng tới; `t09_recursion.s` mới dùng ngăn xếp. |
| Sao in chuỗi không làm hỏng RAM? | Địa chỉ 0xF0000000 có 4 bit cao bằng F, `AddrDec` cho IsIO = 1 nên RamWE = 0, chỉ khối I/O được ghi. |
| Chạy `run_tests.py` ra demo.s 220 chu kỳ, sao trên màn hình 188? | Runner nối thêm đoạn code dump thanh ghi ra RAM để so sánh (32 lệnh). Chạy trong GUI thì không có đoạn đó; mô hình tham chiếu `rvsim.py` cũng ra 188. |
| Ctrl+R có xóa RAM không? | Có. Reset đưa PC, thanh ghi, RAM và TTY về 0, nên chạy lại lần nào cũng ra cùng kết quả. |

## Phần B: lệnh lw t4, 8(sp) trong một chu kỳ

Mục tiêu: cho thầy thấy một lệnh đi qua đủ IF, ID, EX, MEM, WB trong cùng một chu kỳ clock. Mỗi bước dưới đây có
ba phần: thao tác trên màn hình (zoom tới đâu, trỏ chuột vào đâu, Poke dây nào), giá trị đúng phải thấy, và lời nói
gợi ý (đoạn trích dẫn `>`). Lời nói không cần đọc thuộc, nói theo cách của mình miễn đủ ý.

Tên dây trong các bảng là tên tunnel trong mạch (`instr`, `rs1d`, `imm`, `alu`, `memword`, `loaddata`, `wbdata`,
`pc4`, `PCSel`...). Muốn xem giá trị một dây nhiều bit: chọn công cụ Poke (bàn tay), bấm vào dây đó, Logisim hiện
giá trị. Xem xong chuyển lại công cụ Select (mũi tên) trước khi bấm Ctrl+T.

Poke hiện một giá trị theo ba cách: nhị phân, thập phân và số thực. Ví dụ dây `pc4` hiện
`0000 0000 0000 0000 0000 0000 0001 0100 / 20 / 2.8e-44`, tức 0x14 = 20. Số thực (2.8e-44) là Logisim đọc 32 bit như
float, bỏ qua. Đổi sang hex bằng cách nhóm 4 bit từ phải sang: `0001 0100` = 0x14.

### Đọc trước: single cycle chạy thế nào

Cả mạch chỉ có ba phần tử nhớ: thanh ghi `PC`, `Register File` và RAM `DMEM`. Cả ba chỉ đổi giá trị ở cạnh lên clock.
Mọi khối còn lại (ROM đọc, `Control`, `ImmGen`, `ALU`, `AddrDec`, `Load`, các MUX) là mạch tổ hợp: đầu vào đổi thì đầu
ra đổi ngay. Logisim không mô phỏng trễ cổng, nên khi `PC` nhận giá trị mới thì cả chuỗi IF → ID → EX → MEM → WB tính
xong tức thì.

Năm cột FETCH, DECODE, EXECUTE, MEMORY, WRITE BACK chỉ là cách sắp khối. Giữa các cột không có thanh ghi như IF/ID,
ID/EX, EX/MEM, MEM/WB của bản pipeline. Vì vậy khi dừng ở PC = 0x10, cả năm cột cùng hiện giá trị của lệnh `lw`, chỉ
riêng việc ghi t4 phải đợi cạnh lên kế tiếp.

Trong single cycle mọi khối đều tính với mọi lệnh. Tín hiệu điều khiển (select của các MUX, RegWrite, RamWE) quyết
định kết quả nào được dùng và có được ghi vào phần tử nhớ hay không.

### B1. Nạp chương trình

Thao tác:

1. Chuột phải vào ROM `IMEM` → Load Image… → chọn `build/lw_demo.text.hex`.
2. Ctrl+R. Trỏ chuột vào `PC` = 00000000, rồi probe `instr` = 01000113.

Không lưu file .circ sau khi nạp (xem mục "Trả mạch về như cũ").

> "Để xem riêng một lệnh, em nạp vào ROM lệnh một chương trình ngắn 6 lệnh. Lệnh cần xem là `lw t4, 8(sp)` ở địa chỉ
> 0x10, đúng lệnh trên slide 13. Ba lệnh đầu đặt sp bằng 0x10 và nạp 0x12345678 vào t0, lệnh `sw` ghi giá trị đó vào
> RAM ở địa chỉ 0x18. Như vậy tới lệnh `lw`, giá trị đọc ra là 0x12345678, khác 0 nên dễ nhận ra."

### B2. Chạy tới lệnh lw

Thao tác: zoom vừa đủ thấy `PC`, `Register File` và RAM `DMEM`. Bấm Ctrl+T từng lần, nhìn `PC`. Mỗi lần PC đổi là
một lệnh vừa xong:

| PC sau cạnh lên | Lệnh vừa xong | Thay đổi nhìn thấy |
|---|---|---|
| 00000004 | `addi sp, zero, 0x10` | x2 (sp) = 00000010 |
| 00000008 | `lui t0, 0x12345` | x5 (t0) = 12345000 |
| 0000000c | `addi t0, t0, 0x678` | x5 (t0) = 12345678 |
| 00000010 | `sw t0, 8(sp)` | RAM dòng 006, cột đầu = 12345678 |

> (trong lúc bấm) "Mỗi lần PC đổi là một lệnh xong, mỗi lệnh đúng một chu kỳ. Đây sp thành 0x10, đây t0 thành
> 0x12345678, đây lệnh sw ghi vào RAM ô số 6."

Dừng ngay khi PC = 00000010. Trạng thái lúc này:

| Ở đâu | Giá trị | Do lệnh nào |
|---|---|---|
| x2 (sp), dòng 3 cột trái của Register File | 00000010 | `addi sp, zero, 0x10` |
| x5 (t0) | 12345678 | `lui` + `addi` |
| RAM dòng 006, cột đầu | 12345678 | `sw t0, 8(sp)` |
| x29 (t4), dòng 14 cột phải | 00000000 | chưa ai ghi |

> "Bây giờ PC bằng 0x10, CPU đang ở giữa chu kỳ của lệnh `lw`. Mạch tổ hợp đã tính xong hết, chỉ còn chờ cạnh lên
> để ghi kết quả. Em đi qua từng khối từ trái sang phải, không bấm thêm gì."

### B3. IF (cột FETCH)

Đường đi: `PC` → bộ tách `PC[11:2]` → ROM `IMEM` → dây `instr`.

Thao tác: zoom vào cột FETCH. Trỏ chuột lần lượt: thanh ghi `PC` → bộ tách có chữ "PC[11:2] (word index)" → ROM
`IMEM` → probe vàng `instr` bên phải ROM. Cuối cùng xem `pc4`:

- Bộ cộng nằm ngay phía trên ROM `IMEM`, có chữ nhỏ "PC + 4" ở trên. Đầu vào trái phía trên là dây từ `PC` đi lên,
  đầu vào trái phía dưới là hằng số 4 (`0x00000004`), đầu ra bên phải là một đoạn dây ngắn nối vào tunnel `pc4`.
- Bộ cộng không có probe, nên chọn công cụ Poke rồi bấm vào đoạn dây ngắn giữa đầu ra bộ cộng và tunnel `pc4`. Logisim
  hiện 0x00000014.
- Có thể chỉ thêm MUX có chữ "next PC" bên trái `PC`: PCSel = 0 nên dây từ MUX vào chân D của `PC` cũng mang
  0x00000014. Đây là giá trị PC sẽ nhận ở cạnh lên.

| Chỗ nhìn | Giá trị đúng |
|---|---|
| `PC` | 00000010 |
| `PC[11:2]` (địa chỉ ROM) | 004 (0x10 / 4) |
| probe `instr` | 00812e83 |
| `pc4` | 00000014 |

> "Bước IF. PC đang là 0x10. ROM lệnh đánh địa chỉ theo word, nên mạch lấy PC bit 11 đến 2, tức 0x10 chia 4 bằng 4.
> ROM trả về ô số 4 là 0x00812E83, đúng mã máy trên slide. Song song, bộ cộng phía trên tính sẵn PC + 4 bằng 0x14,
> là địa chỉ lệnh tiếp theo. PC chưa nhận 0x14 ngay, phải đợi cạnh lên clock."

### B4. ID (cột DECODE / REGISTER READ)

Dây `instr` đi cùng lúc vào ba khối: `Control`, `Register File` (qua các trường rs1, rs2, rd) và `ImmGen`.

Tách mã máy (giống slide 13):

```
0000 0000 1000 | 0001 0 | 010 | 1110 1 | 000 0011
 imm[11:0]=8   | rs1=2  | f3  | rd=29  | opcode = LOAD
```

Thao tác:

1. Trỏ vào khối `Control` (màu be, phía trên). Chỉ các dây 1 bit bên phải: RegWrite và MemRead sáng, MemWrite,
   Branch, Jal, Jalr, Halt tối.
2. Chọn Poke, bấm lần lượt các dây ASel, BSel, ALUOp, ImmSel, WBSel.
3. Trỏ xuống `Register File` (khối xanh lá): chỉ x2 (dòng 3 cột trái) = 00000010, rồi x29 (dòng 14 cột phải) =
   00000000. Poke dây ra RD1 (tunnel `rs1d`).
4. Trỏ xuống `ImmGen` phía dưới, Poke dây ra (tunnel `imm`).

| Khối | Tín hiệu | Giá trị đúng | Ý nghĩa |
|---|---|---|---|
| `Control` | RegWrite | 1 | lệnh có ghi rd |
| | MemRead / MemWrite | 1 / 0 | đọc bộ nhớ, không ghi |
| | ASel | 00 | ALU lấy A = rs1 |
| | BSel | 1 | ALU lấy B = immediate |
| | ALUOp | 00 | phép cộng |
| | ImmSel | 000 | immediate kiểu I |
| | WBSel | 01 | ghi về dữ liệu đọc từ bộ nhớ |
| | Branch, Jal, Jalr, Halt | 0 | không nhảy, không dừng |
| `Register File` | `rs1d` (RA1 = 2) | 00000010 | giá trị sp |
| | x29 | 00000000 | chưa ghi |
| `ImmGen` | `imm` | 00000008 | instr[31:20] mở rộng dấu |

> "Bước ID. Dây instr đi cùng lúc vào ba khối: Control, Register File và ImmGen. Tách mã máy theo slide: imm bằng 8,
> rs1 là x2 tức sp, funct3 bằng 010 là LW, rd là x29 tức t4, opcode 0000011 là nhóm LOAD."
>
> "Control nhìn opcode LOAD và bật: RegWrite bằng 1 vì lệnh có ghi thanh ghi, MemRead bằng 1, MemWrite bằng 0. BSel
> bằng 1 để ALU lấy immediate thay cho rs2, ALUOp bằng 00 là phép cộng, WBSel bằng 01 để ghi về dữ liệu đọc từ bộ
> nhớ."
>
> "Register File đọc rs1 là x2, ra 0x10. ImmGen cắt bit 31 đến 20 rồi mở rộng dấu, ra 8. Còn x29 vẫn bằng 0, vì
> thanh ghi chỉ được ghi ở cạnh lên clock, cuối chu kỳ."

### B5. EX (cột EXECUTE)

Thao tác:

1. Trỏ vào MUX có chữ "ASel: 0 rs1, 1 PC, 2 zero", rồi MUX có chữ "BSel: 0 rs2, 1 imm".
2. Trỏ vào khối `ALUControl` phía trên, Poke dây ALUCtrl.
3. Trỏ vào `ALU` (hình thang) và probe vàng `ALU_result`.
4. Trỏ xuống khối `Branch` và cổng OR có chữ "PCSel = Taken | Jal | Jalr", Poke dây PCSel.

| Khối | Vào | Ra (giá trị đúng) |
|---|---|---|
| MUX ASel | ASel = 0 | A = `rs1d` = 00000010 |
| MUX BSel | BSel = 1 | B = `imm` = 00000008 |
| `ALUControl` | ALUOp = 00, funct3 = 010 | ALUCtrl = 0000 (ADD) |
| `ALU` | 0x10 + 0x8 | probe `ALU_result` = 00000018 |
| `Branch` | Branch = 0 | Taken = 0 |
| cổng OR | Taken, Jal, Jalr đều 0 | PCSel = 0, MUX "next PC" ở cột FETCH chọn `pc4` |

> "Bước EX. MUX A chọn rs1 bằng 0x10. MUX B chọn imm bằng 8 vì BSel bằng 1. ALU Control thấy ALUOp bằng 00 nên ra mã
> cộng, không cần nhìn funct3. ALU tính 0x10 cộng 8 bằng 0x18. Với lệnh load, kết quả ALU là địa chỉ bộ nhớ chứ chưa
> phải dữ liệu."
>
> "Phía dưới là phần chọn PC tiếp theo. Đây không phải lệnh nhảy nên Branch, Jal, Jalr đều bằng 0, PCSel bằng 0, MUX
> next PC chọn PC + 4."

### B6. MEM (cột MEMORY)

Thao tác:

1. Trỏ vào khối `AddrDec`, Poke lần lượt các dây ra IsIO, WordAddr, Off, RamWE.
2. Zoom vào RAM `DMEM` (khối duy nhất có chữ "RAM 4K x 32" trong cột MEMORY), chỉ dòng 006, cột đầu.
3. Trỏ vào MUX có chữ "IsIO ? I/O : RAM" (cạnh khối `I/O Ctrl`), Poke dây ra (tunnel `memword`).
4. Trỏ sang khối `Load` (đầu cột WRITE BACK trên màn hình, nhưng về chức năng thuộc bước MEM), Poke dây ra
   (tunnel `loaddata`).

| Chỗ nhìn | Giá trị đúng | Vì sao |
|---|---|---|
| IsIO | 0 | Addr[31:28] = 0, không phải F, nên là RAM |
| WordAddr | 006 | Addr[13:2] = 0x18 / 4 |
| Off | 00 | Addr[1:0], đọc từ đầu word |
| RamWE | 0 | MemWrite = 0 |
| RAM dòng 006 | 12345678 | lệnh `sw` đã ghi |
| `memword` | 12345678 | IsIO = 0 nên MUX chọn RAM |
| `loaddata` | 12345678 | funct3 = 010 (LW), lấy cả word |

> "Bước MEM. Địa chỉ 0x18 vào bộ giải mã địa chỉ. 4 bit cao bằng 0, không phải F, nên IsIO bằng 0: đây là RAM, không
> phải vùng I/O. Địa chỉ word bằng 0x18 chia 4 bằng 6, byte offset bằng 0. MemWrite bằng 0 nên RamWE bằng 0, RAM không
> bị ghi."
>
> "RAM đọc ô số 6, ra 0x12345678, đúng giá trị lệnh sw đã ghi lúc nãy. Khối Load thấy funct3 bằng 010 là LW nên lấy
> nguyên word. Nếu là LB hay LH thì khối này mới cắt byte và mở rộng dấu."

### B7. WB (cột WRITE BACK)

Thao tác:

1. Trỏ vào MUX có chữ "WBSel: 0 ALU, 1 Mem, 2 PC+4". Poke ba dây vào: `alu`, `loaddata`, `pc4`.
2. Trỏ vào probe vàng `WB_data`.
3. Kéo màn hình về `Register File`, chỉ cổng WD (tunnel `wbdata`), cổng WA và WE.

| Ngõ MUX | Dây | Giá trị |
|---|---|---|
| 0 | `alu` | 00000018 |
| 1 (được chọn) | `loaddata` | 12345678 |
| 2 | `pc4` | 00000014 |
| ra | probe `WB_data` | 12345678 |

> "Bước WB. MUX này có ba ngõ vào và cả ba đều đang có giá trị: kết quả ALU 0x18, dữ liệu bộ nhớ 0x12345678 và PC + 4
> bằng 0x14. WBSel bằng 01 nên chọn dữ liệu bộ nhớ, WB_data bằng 0x12345678. Giá trị này quay về cổng ghi của Register
> File, địa chỉ ghi là 29, RegWrite bằng 1."
>
> "Đến đây cả năm bước đã tính xong, nhưng t4 vẫn bằng 0. Nó chỉ được ghi khi có cạnh lên clock."

Nếu Control sai và WBSel = 0 thì `WB_data` sẽ là 00000018. Vì 0x18 và 0x12345678 khác hẳn nhau nên nhìn là biết
MUX chọn đúng ngõ.

### B8. Cạnh lên clock: lệnh hoàn thành

Thao tác: zoom ra cho thấy cùng lúc `PC`, probe `instr` và x29 trong `Register File`. Đặt chuột cạnh x29 rồi bấm
Ctrl+T cho tới khi PC đổi (một hoặc hai lần, tùy clock đang ở mức nào).

| Phần tử nhớ | Nhận từ | Giá trị mới |
|---|---|---|
| x29 (t4) | `wbdata` (WE = 1, WA = 29) | 12345678 |
| `PC` | MUX next PC, đang chọn `pc4` | 00000014 |
| RAM `DMEM` | không đổi, RamWE = 0 | |

Ngay sau cạnh lên, PC mới chạy lại cả chuỗi tổ hợp cho lệnh kế tiếp: probe `instr` = 00100073 (`ebreak`), Control bật
Halt, chân `halt` = 1, PCEn = !Halt = 0.

> "Em bấm một cạnh lên. t4 nhận 0x12345678 và PC lên 0x14, hai việc xảy ra ở cùng một cạnh. Lệnh lw xong trong đúng
> một chu kỳ. Lệnh này đi qua nhiều khối nhất: ROM, Register File, ALU, RAM, rồi quay về Register File, nên nó quyết
> định độ dài chu kỳ clock của CPU đơn chu kỳ."

Bấm Ctrl+T thêm vài lần: PC đứng ở 00000014. Chỉ vào chân `cycles` và `instret` ở hàng dưới cùng, cả hai dừng ở
00000005.

> "Lệnh tiếp theo là ebreak, Control bật Halt nên PC bị khóa ở 0x14. Bộ đếm cycles và instret cùng dừng ở 5: năm lệnh
> trong năm chu kỳ, CPI bằng 1."

### Nếu thầy hỏi

| Câu hỏi | Trả lời |
|---|---|
| Dây `rs2d` đang có giá trị, lệnh lw có dùng rs2 không? | Không. Bit 24:20 luôn nối vào cổng RA2 nên Register File vẫn đọc x8 (= 0), nhưng BSel = 1 nên MUX B lấy imm và bỏ rs2. |
| Dây `target` (= 00000018) để làm gì? | Là địa chỉ nhảy cho branch/JAL/JALR (ALU & ~1). PCSel = 0 nên MUX next PC không chọn nó. |
| Khối `Store` cũng có đầu ra, RAM có bị ghi không? | Không. RamWE = MemWrite AND (không phải I/O) = 0, nên RAM bỏ qua dữ liệu trên dây `stnew`. |
| Tại sao t4 không đổi ngay khi `WB_data` đã có giá trị? | Register File là phần tử nhớ, chỉ ghi ở cạnh lên clock. Nhờ vậy rs1 đọc trong chu kỳ này không bị đổi giữa chừng. |
| Single cycle khác pipeline ở đâu trên mạch? | Bản pipeline có thanh ghi IF/ID, ID/EX, EX/MEM, MEM/WB chia đường dữ liệu thành 5 tầng, mỗi tầng chứa một lệnh khác nhau. Ở bản này không có, cả 5 bước của một lệnh nằm trong một chu kỳ. |

## Phần C: chạy bộ test tự động (tùy chọn)

Mở PowerShell:

```powershell
cd D:\hust-master\KienTrucMayTienTien\Project
$env:LOGISIM_JAR = "C:\Program Files\logisim-evolution\app\logisim-evolution-4.1.0-all.jar"
python tools/run_tests.py circ/RV32I_SingleCycle.circ
```

Lệnh này chạy 12 chương trình trong `programs/` trên Logisim không giao diện và so thanh ghi, RAM, TTY với `rvsim.py`.
Lần chạy ngày 14/11/2026 cho 12/12 PASS, dòng cuối `ALL PASSED`, mất khoảng 17 giây. Mọi dòng có `CPI=1.00`.
Cùng ngày, 25 chương trình `programs/fuzz` cũng `ALL PASSED`, và test vector của 10 module (Control, RegisterFile,
ImmGen, ALUControl, ALU, BranchUnit, AddrDecode, StoreUnit, LoadUnit, IOController) đều `Failed: 0`.

Nếu mọi dòng báo FAIL với "no RAM dump" thì là do chưa đặt `$env:LOGISIM_JAR` trong cửa sổ PowerShell đó.

## Trả mạch về như cũ

Load Image chỉ đổi ROM trong phiên Logisim đang mở. Có hai cách để ROM quay lại `demo.s`:

- Đóng Logisim, khi được hỏi lưu thay đổi thì chọn không lưu.
- Hoặc chuột phải ROM `IMEM` → Load Image… → chọn `build/demo.text.hex` (sinh bằng
  `python tools/rvasm.py programs/demo.s -o build/demo`).

Không lưu file .circ khi ROM đang chứa `lw_demo`, nếu không lần mở sau sẽ mất chương trình `demo.s` nạp sẵn.
