---
title: "Phân công nhóm — CPU RISC-V RV32I"
subtitle: "Bùi Phạm Sơn Hà · Nguyễn Đức Anh · Quyền Đức Công — hạn nộp CN 8/11"
---

# 1. Vai trò

Cả nhóm dùng **bản tham chiếu làm khung chạy được ngay từ đầu**. Mỗi người tự dựng lại các module cốt lõi trong mảng của mình, thay khối đó vào khung và chạy test để chứng minh mạch đúng. Các module lặp lại hoặc ít giá trị học (4 thanh ghi pipeline, bộ đếm, khối I/O) thì giữ bản tham chiếu, chỉ cần giải thích được. Mỗi mảng gồm **cả phần đơn chu kỳ lẫn phần pipeline**, để khi bảo vệ không ai bị hổng nguyên một nửa.

| | **Bùi Phạm Sơn Hà** | **Nguyễn Đức Anh** | **Quyền Đức Công** |
|---|---|---|---|
| **Mảng** | Fetch, Decode, Control hazard | Execute, Data hazard | Memory, Pipeline, Kiểm thử · ghép mạch và biên tập báo cáo |
| **Tự dựng lại** | `ImmGen`, `Control`, `HazardUnit` | `ALU`, `RegisterFile`, `ForwardUnit` | `AddrDecode`, `LoadUnit`, `StoreUnit` |
| **Dựng thêm nếu còn thời gian** | `ALUControl` | `BranchUnit` | `IF_ID` |
| **Dùng bản tham chiếu, phải giải thích được** | PC, next-PC, IMEM | MUX ASel/BSel, `IDBypass` | 4 thanh ghi pipeline, RAM, `IOController` (UART + GPIO), PerfCounters |

Hà và Đức Anh có thể đổi vai cho nhau. Ai vững logic số hơn (cổng, MUX, số bù 2) thì nhận mảng **Execute**.

# 2. Bùi Phạm Sơn Hà — Fetch, Decode, Control hazard

## 2.1 Đầu việc và tiêu chí hoàn thành

| Đầu việc | Việc cần làm | Coi là hoàn thành khi |
|---|---|---|
| **Nắm ISA** | Đọc phần 1–2 và phase 3–4 của `LO_TRINH`. Học 6 định dạng lệnh và bảng opcode | Giải mã tay được một lệnh bất kỳ (ví dụ `0xFCB50CE3`) mà không nhìn tài liệu |
| **ImmGen** | Dựng lại trong file riêng `HA.circ`, đúng tên chân `Instr`, `ImmSel` → `Imm` | `ImmGen.txt` pass 300/300 |
| **Control** | Dựng lại theo kiểu decoder 5→32 + cổng OR. Tự điền bảng tín hiệu điều khiển 10 nhóm lệnh trước khi vẽ | `Control.txt` pass 400/400 · CPU đơn chu kỳ dùng khối này chạy `run_tests.py` 12/12 |
| **HazardUnit** | Dựng lại: phát hiện load-use, tạo PCWrite, IFID_Write, IFID_Flush, IDEX_Flush. Vẽ tay sơ đồ thời gian một lần load-use và một lần BEQ nhảy | `HazardUnit.txt` pass · sơ đồ vẽ tay khớp với Pipeline Monitor khi chạy `t06_hazard.s` |
| **Fetch / next-PC** | Không cần vẽ lại. Đọc hiểu PC, PC+4, `target = ALU & ~1`, MUX next-PC trong bản tham chiếu | Giải thích được vì sao cần `& ~1` và khi nào PC nhận target |
| **Báo cáo** | Viết: ISA và tập lệnh, Control Unit, ImmGen, control hazard + load-use (4–5 trang) + cheat sheet 1 trang | Công nhận bài, không phải sửa nội dung kỹ thuật |
| **Demo** | Quay phần giải mã lệnh, flush khi nhảy, stall khi load-use | Có đoạn video 1,5–2 phút |

## 2.2 Cần truyền đạt lại cho Đức Anh và Công

**Ý chính phải truyền đạt**

1. Mọi lệnh dài 32 bit. opcode, rd, funct3, rs1, rs2 luôn nằm ở **vị trí cố định**, nhờ vậy phần cứng đọc thanh ghi song song với giải mã.
2. Vì sao bit immediate của B/J bị "xáo trộn": để bit dấu luôn là bit 31 và các mảnh nằm cùng chỗ giữa các định dạng, nên ImmGen chỉ là nối dây + MUX.
3. Control = **bảng chân lý vẽ thành mạch**: decoder biến opcode thành một đường cho mỗi nhóm lệnh, mỗi tín hiệu là OR của các nhóm cần nó. Lệnh `0x00000000` là NOP an toàn vì decoder chỉ bật khi `opcode[1:0] = 11`.
4. Bẫy ADDI và bit 30: chỉ SRAI mới dùng bit 30 làm "alt".
5. **Control hazard**: đoán "không nhảy", quyết định ở EX, nhảy thì xóa 2 lệnh đã nạp sai, mất 2 chu kỳ.
6. **Load-use**: forwarding không cứu được, phải chờ 1 chu kỳ. Khi đó PC giữ, IF/ID giữ, ID/EX nạp bubble. Redirect được ưu tiên hơn Stall.

**Demo phải cho người nghe xem**
- Chạy `RV32I_SingleCycle.circ` từng nửa chu kỳ (Ctrl+T) với lệnh `addi a0, x0, 5`, chỉ từng tín hiệu ra của Control.
- Chạy `RV32I_Pipeline.circ` tới một lần BEQ nhảy: `E_Redirect = 1`, hai lệnh phía sau thành `00000000`.
- Chạy tới một lần load-use: `Stall = 1`, lệnh phụ thuộc đứng yên ở ID một chu kỳ.

**Sau buổi, người nghe phải tự làm được**
- Giải mã tay `0x00500513` ra `addi a0, x0, 5`.
- Nói đúng RegWrite, MemWrite, BSel, ImmSel của lệnh `sw`.
- Vẽ sơ đồ thời gian `lw` rồi `add` phụ thuộc, chỉ ra chu kỳ bị stall.

# 3. Nguyễn Đức Anh — Execute, Data hazard

## 3.1 Đầu việc và tiêu chí hoàn thành

| Đầu việc | Việc cần làm | Coi là hoàn thành khi |
|---|---|---|
| **Nắm nền số học** | Đọc phần 1 và phase 1–2 của `LO_TRINH`: nhị phân, hex, bù 2, có dấu và không dấu, tổ hợp và tuần tự, cạnh lên clock | Tự giải thích được SLT khác SLTU, SRA khác SRL bằng ví dụ số cụ thể |
| **ALU** | Dựng lại trong file riêng `DUCANH.circ`: tính song song 10 phép rồi dùng MUX chọn theo `ALUCtrl = {bit30, funct3}` | `ALU.txt` pass 250/250 |
| **RegisterFile** | Dựng lại: 31 thanh ghi, decoder ghi, 2 MUX đọc, x0 là hằng 0 | `RegisterFile.txt` pass 400/400 · CPU đơn chu kỳ dùng khối này chạy `run_tests.py` 12/12 |
| **ForwardUnit** | Dựng lại: so `rd` của EX/MEM và MEM/WB với `rs1`, `rs2`, điều kiện `rd ≠ 0`, ưu tiên EX/MEM | `ForwardUnit.txt` pass · CPU pipeline dùng khối này chạy 12/12 + fuzz 25/25 |
| **IDBypass, MUX ASel/BSel** | Không cần vẽ lại. Đọc hiểu trong bản tham chiếu | Giải thích được vì sao bypass WB→ID không đặt trong RegisterFile |
| **Báo cáo** | Viết: nền số học, ALU, Register File, Branch Unit, data hazard và forwarding (4–5 trang) + cheat sheet 1 trang | Công nhận bài, không phải sửa nội dung kỹ thuật |
| **Demo** | Quay phần forwarding trên Pipeline Monitor | Có đoạn video 1,5–2 phút |

## 3.2 Cần truyền đạt lại cho Hà và Công

**Ý chính phải truyền đạt**

1. Vì sao máy tính dùng bit và hex. Bù 2 cho phép cộng/trừ dùng chung mạch. Chỉ so sánh, dịch phải và mở rộng mới phải phân biệt có dấu hay không dấu.
2. **Mô hình register → mạch tổ hợp → register**: trong một chu kỳ mọi thứ "tính", ở cạnh lên mọi register chụp cùng lúc. Không bao giờ đưa clock qua cổng logic, muốn dừng thì dùng Enable.
3. ALU không "chạy if-else": mọi phép tính cùng lúc, MUX chọn kết quả. ALUCtrl trùng với funct3 nên ALUControl gần như chỉ là nối dây.
4. Register File: đọc là tổ hợp (chỉ là MUX), ghi phải chờ cạnh clock. x0 không phải thanh ghi mà là hằng 0 ở đầu vào MUX.
5. **Data hazard (RAW)** và forwarding: lấy kết quả từ EX/MEM (FwdA = 01) hoặc MEM/WB (FwdA = 10). Phải kiểm tra `rd ≠ 0`, EX/MEM được ưu tiên vì mới hơn.
6. WB→ID bypass thay cho "ghi nửa đầu, đọc nửa sau chu kỳ" trong sách.

**Demo phải cho người nghe xem**
- Mở `ALU`, đổi A, B, ALUCtrl bằng Poke tool, cho thấy SLT và SLTU ra khác nhau với `0xFFFFFFFF` và `1`.
- Chạy `RV32I_SingleCycle.circ`, chỉ thanh ghi đổi giá trị ngay trên khối Register File sau cạnh lên.
- Chạy `RV32I_Pipeline.circ` với chuỗi lệnh phụ thuộc, chỉ `FwdA`/`FwdB` bật đúng chu kỳ.
- Chạy bản `RV32I_Pipeline_NoHazard.circ` cùng chuỗi đó để thấy kết quả sai.

**Sau buổi, người nghe phải tự làm được**
- Đổi qua lại giữa nhị phân và hex, tính `−8` dịch phải theo SRA và SRL.
- Giải thích được ghi Register File xảy ra lúc nào và thanh ghi nào được ghi.
- Với `addi x1,x0,1` · `addi x2,x0,2` · `add x3,x1,x2`, nói đúng FwdA và FwdB khi `add` ở EX.

# 4. Quyền Đức Công — Memory, Pipeline, Kiểm thử, Tích hợp

## 4.1 Đầu việc và tiêu chí hoàn thành

| Đầu việc | Việc cần làm | Coi là hoàn thành khi |
|---|---|---|
| **Hạ tầng nhóm** | Tạo repo chung, đưa project lên, chia sẻ link `LO_TRINH`, trang phân công và trang câu hỏi. Chạy được `run_tests.py` trên máy mình | Cả 3 file CPU báo ALL PASSED trên máy Công · hai bạn kia mở được Logisim và chạy demo |
| **AddrDecode, LoadUnit, StoreUnit** | Dựng lại trong file riêng `CONG.circ` | 3 file test vector tương ứng pass 100% |
| **Ghép single-cycle** | Nạp `HA.circ`, `DUCANH.circ`, `CONG.circ` bằng *Load Library*, thay các khối tự dựng vào CPU đơn chu kỳ | `run_tests.py` 12/12 trên CPU dùng khối của cả nhóm |
| **Ghép pipeline** | Thay HazardUnit, ForwardUnit tự dựng vào CPU pipeline. Hiểu 4 thanh ghi pipeline. Chạy bản NoHazard để có ví dụ lỗi | `run_tests.py` 12/12 + fuzz 25/25, số chu kỳ khớp mô hình |
| **Đo đạc** | Lập bảng CPI (single-cycle với pipeline), đếm load-use và số lần nhảy, chụp ảnh mạch cho báo cáo | Có bảng số liệu và bộ ảnh |
| **Báo cáo** | Viết: bộ nhớ và I/O, thanh ghi pipeline, kiểm thử, CPI, hạn chế, mở đầu, kết luận (3–4 trang). Ghép và biên tập toàn bộ (10–20 trang). Viết README nộp bài | Báo cáo hoàn chỉnh, thống nhất giọng văn và thuật ngữ |
| **Nộp bài** | Chạy lại toàn bộ test trên máy của Hà hoặc Đức Anh, đóng gói source + video + báo cáo | Nộp trước hạn ít nhất 3 tiếng |

## 4.2 Cần truyền đạt lại cho Hà và Đức Anh

**Ý chính phải truyền đạt**

1. Bộ nhớ đánh địa chỉ **theo byte**, little-endian. Mỗi ô RAM là một word, nên ô = `Addr[13:2]` và byte trong ô = `Addr[1:0]`. Cùng lý do đó IMEM lấy `PC[11:2]` và PC tăng 4.
2. LB/LH dịch byte về vị trí thấp rồi sign-extend, LBU/LHU zero-extend. SB/SH làm bằng **read-modify-write**, còn phần cứng thật dùng byte-enable.
3. Bản đồ bộ nhớ và **memory-mapped I/O** (phần nâng cao GPIO/UART): thiết bị ngoại vi chỉ là vài địa chỉ. `sb` vào `0xF0000000` in ký tự, `lw` từ `0xF0000004` đọc phím, `sw` vào `0xF0000010` bật đèn. Đọc RXDATA có tác dụng phụ (lấy ký tự khỏi hàng đợi), nên chỉ được bật khi `MemRead = 1` và ở tầng MEM.
4. **Thanh ghi pipeline** cắt đường dài thành 5 đoạn. Mỗi thanh ghi mang theo dữ liệu lẫn **tín hiệu điều khiển** của lệnh. Stall = giữ (EN = 0). Flush = nạp 0 bằng MUX, đồng bộ, không dùng chân Clear.
5. **Kiểm chứng**: test vector cho từng module, golden model để so cả CPU (thanh ghi, RAM, TTY, số chu kỳ), fuzz test. Bản NoHazard fail mọi test chứng minh bộ test bắt được lỗi.
6. **CPI** và công thức `N + 4 + loaduse + 2·taken`. Vì sao CPI > 1 mà pipeline vẫn nhanh hơn: chu kỳ clock ngắn hơn nhiều.

**Demo phải cho người nghe xem**
- Mở `DMEM` trong lúc chạy `t05_mem.s`, chỉ từng byte bị `sb` và `sh` ghi đè.
- Mở thanh ghi `ID_EX`, chỉ các trường đi theo lệnh và lúc một bubble (toàn 0) đi qua.
- Chạy `run_tests.py` trên terminal: ALL PASSED với bản đúng, FAIL với bản NoHazard.
- Chạy `t11_io.s`: click vào Keyboard gõ chữ, TTY in lại chữ hoa. LED 7 đoạn hiện số ký tự đã gõ.

**Sau buổi, người nghe phải tự làm được**
- Tính ô RAM và byte offset của một địa chỉ bất kỳ, đọc đúng một byte theo little-endian.
- Phân biệt stall và flush trên thanh ghi pipeline.
- Tự chạy `rvasm.py` để nạp một chương trình vào ROM và chạy `run_tests.py` trên máy mình.

# 5. Mốc của cả nhóm

| Mốc | Hạn | Tiêu chí |
|---|---|---|
| Kickoff: chốt vai, chốt tên pin, cài Logisim 4.1.0 + Java 21 | T7 31/10 | Cả 3 người chạy được demo trên máy mình |
| Single-cycle dùng khối tự dựng | T3 3/11 | `run_tests.py` 12/12 |
| Pipeline dùng khối tự dựng | T4 4/11 | 12/12 + fuzz 25/25, số chu kỳ khớp |
| Chia sẻ kiến thức: 3 phiên trình bày + phản biện | T5 5/11 | Theo file **Bộ câu hỏi trình bày và phản biện** (`CAU_HOI`) |
| Hà và Đức Anh nộp phần báo cáo cho Công | T6 6/11 | Đủ trang, đủ cheat sheet |
| Video demo + bảo vệ thử | T7 7/11 | Ai cũng dẫn được một lệnh `lw` qua cả CPU |
| Nộp bài | CN 8/11 | Trước hạn ít nhất 3 tiếng |

**Nếu bị trễ:** bỏ module "nếu còn thời gian" trước. Vẫn trễ thì bỏ module thứ ba của mỗi người (HazardUnit / ForwardUnit / StoreUnit) và dùng bản tham chiếu thay vào. **Không bỏ** buổi chia sẻ kiến thức và buổi bảo vệ thử, vì thầy hỏi "vì sao" chứ không hỏi "ai vẽ".

# 6. Luật kỹ thuật

- **Không đổi tên circuit, tên pin, độ rộng pin** so với bản tham chiếu. Nhờ vậy test vector chạy được trên mạch tự vẽ, và thay khối chỉ là xóa cũ, kéo mới.
- **Mỗi người một file `.circ` riêng** (`HA.circ`, `DUCANH.circ`, `CONG.circ`). Chỉ Công sửa file CPU chính, nạp file của hai người kia bằng *Project → Load Library → Logisim Library…*. File `.circ` là XML, hai người cùng sửa một file sẽ ghi đè nhau và Git không merge được.
- **"Xong" một module** nghĩa là test vector pass 100%, và người làm giải thích lại được cho người khác mà không cần nhìn tài liệu.
