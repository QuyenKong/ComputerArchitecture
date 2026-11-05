# RV32I CPU trên Logisim-evolution: Single-cycle và Pipeline 5 tầng

Bài tập lớn môn Kiến trúc máy tính tiên tiến: máy tính 32-bit kiến trúc tập lệnh **RISC-V RV32I**. Có hai phiên bản:

| File | Mô tả |
|---|---|
| `circ/RV32I_SingleCycle.circ` | CPU đơn chu kỳ |
| `circ/RV32I_Pipeline.circ` | CPU pipeline IF→ID→EX→MEM→WB: forwarding, WB→ID bypass, stall load-use, flush khi branch/jump (predict not-taken) |
| `circ/extra/RV32I_Pipeline_NoHazard.circ` | Pipeline cố ý **không** có forwarding và load-use stall. Chạy đúng khi assembler chèn `nop` (`rvasm.py --nohazard`, `run_tests.py --nohazard`); ROM đã nạp sẵn `demo.s` có chèn `nop` |

So sánh 3 bản (số chu kỳ, giản đồ từng chu kỳ): `python tools/compare.py [programs/t06_hazard.s]`. Trang giải thích: `docs/SO_SANH.html`.

**Báo cáo kỹ thuật (LaTeX):** `latex/report.tex`, bản PDF `latex/report.pdf`. Dựng lại: `python latex/scripts/gen_results.py` rồi `cd latex && latexmk -pdf report.tex`.

**Hướng dẫn chi tiết và lộ trình tự xây dựng:** [`docs/LO_TRINH.md`](docs/LO_TRINH.md) (bản HTML: `docs/LO_TRINH.html`).

## Đặc tả

- Data 32 bit, lệnh 32 bit, 32 thanh ghi × 32 bit (x0 = 0), PC 32 bit.
- Toàn bộ RV32I base: ADD SUB AND OR XOR SLT SLTU SLL SRL SRA · ADDI ANDI ORI XORI SLTI SLTIU SLLI SRLI SRAI · LW LH LB LHU LBU · SW SH SB · BEQ BNE BLT BGE BLTU BGEU · JAL JALR · LUI AUIPC. ECALL/EBREAK = HALT.
- IMEM: ROM 1K × 32. DMEM: RAM 16 KiB.
- **GPIO/UART (memory-mapped I/O)**: `0xF0000000` UART TX (TTY), `0xF0000004` UART RX (Keyboard), `0xF0000008` UART STATUS, `0xF0000010` GPIO_OUT (4 LED 7 đoạn + 8 LED), `0xF0000014` GPIO_IN (8 công tắc DIP).
- Bộ đếm hiệu năng `cycles`, `instret` để tính CPI.

## Mở và chạy (GUI)

1. Cài **Logisim-evolution 4.1.0** (cần Java 21).
2. File → Open → `circ/RV32I_SingleCycle.circ` (hoặc `RV32I_Pipeline.circ`).
3. **Ctrl+K** để clock tự chạy (chỉnh tốc độ ở Simulate → Tick Frequency). **Ctrl+T** chạy từng nửa chu kỳ. **Ctrl+R** reset.
4. Chương trình demo (`programs/demo.s`) đã nạp sẵn trong ROM. Kết quả: TTY in `Hello RISC-V!`, `a0 = 0xE8`, LED 7 đoạn hiện `00E8`, 8 LED sáng, sau đó `halt = 1`. Muốn thử bàn phím: nạp `build/t11_io.text.hex`, Ctrl+K, click vào khối Keyboard rồi gõ. CPU in lại chữ hoa ra TTY, Enter để kết thúc.
5. Quan sát: 32 thanh ghi hiện ngay trên khối **Register File**. RAM xem trực tiếp trên khối `DMEM`. Pipeline có **Pipeline Monitor** ở góc dưới: PC và lệnh ở từng tầng, cùng `Stall`, `LoadUse`, `Redirect`, `FwdA`, `FwdB`.

## Nạp chương trình mới

```bash
python3 tools/rvasm.py programs/t08_sort.s -o build/t08_sort
```

Lệnh trên sinh ra `build/t08_sort.text.hex`, `.data.hex` và `.lst`. Trong Logisim: chuột phải ROM **IMEM** → *Load Image…* → chọn `.text.hex`. Nếu chương trình có `.data` khởi tạo thì chuột phải RAM **DMEM** → *Load Image…* → chọn `.data.hex`. Sau đó Ctrl+R và Ctrl+K.

Hoặc nạp thẳng vào file mạch, không cần GUI:

```bash
python3 tools/rvasm.py programs/t08_sort.s -o build/t08_sort --circ circ/RV32I_Pipeline.circ --circ-out build/sort_pipeline.circ
```

`build/` đã có sẵn file hex của mọi chương trình trong `programs/`.

## Chạy test

**Test từng module** (GUI): mở circuit con (ví dụ `ALU`) → Simulate → Test Vector → Load `tests/vectors/ALU.txt`.
Dòng lệnh: `java -jar logisim-evolution-4.1.0-all.jar -w ALU tests/vectors/ALU.txt circ/RV32I_Pipeline.circ` (in `Passed: n, Failed: m`). Lệnh này lỗi khi cạnh file mạch có file `.RV32I_*.circ.autosave` của một phiên Logisim đang mở; khi đó đóng Logisim hoặc chạy trên bản sao của file `.circ`.

**Test toàn CPU** (headless, so với golden model `tools/rvsim.py`: 32 thanh ghi + toàn bộ RAM + TTY + GPIO + số chu kỳ):

```bash
export LOGISIM_JAR=/path/to/logisim-evolution-4.1.0-all.jar
python3 tools/run_tests.py circ/RV32I_SingleCycle.circ
python3 tools/run_tests.py circ/RV32I_Pipeline.circ
python3 tools/run_tests.py circ/RV32I_Pipeline.circ --programs programs/fuzz      # 25 chương trình ngẫu nhiên
python3 tools/fuzz.py 50 programs/fuzz2                                           # sinh thêm
```

Kết quả hiện tại: single-cycle 12/12 + fuzz 25/25; pipeline 12/12 + fuzz 25/25, kể cả số chu kỳ khớp mô hình `N + 4 + loaduse + 2·taken`. Bản NoHazard FAIL đúng như dự kiến. Chương trình có dòng `# STDIN: "..."` (ví dụ `t11_io.s`) sẽ được runner gõ chuỗi đó vào Keyboard.

Bảng đối chiếu từng yêu cầu của đề với phần hiện thực: mục 0.2 trong `docs/LO_TRINH.md`.

## Cấu trúc thư mục

```
circ/        file Logisim (.circ)
programs/    chương trình test (.s); programs/fuzz: chương trình ngẫu nhiên
build/       mã máy đã assemble (.text.hex, .data.hex, .lst)
tests/       test vector từng module
tools/       rvasm.py (assembler), rvsim.py (golden model), run_tests.py, fuzz.py
generator/   mã Python sinh các file .circ (không bắt buộc, xem generator/README.md)
docs/        LO_TRINH.md / .html (lộ trình + giải thích), img/ (ảnh mạch)
```
