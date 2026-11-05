# CLAUDE.md

Bài tập lớn môn Kiến trúc máy tính tiên tiến: CPU RISC-V RV32I trên Logisim-evolution 4.1.0, ba bản
`circ/RV32I_SingleCycle.circ`, `circ/RV32I_Pipeline.circ` (forwarding, WB→ID bypass, load-use stall,
flush khi branch/jump) và `circ/extra/RV32I_Pipeline_NoHazard.circ` (không forwarding/stall, chạy đúng nhờ
assembler chèn `nop`). Người dùng viết tiếng Việt thân mật; trả lời bằng tiếng Việt.

`README.md` và `docs/LO_TRINH.md` là nguồn chính về đặc tả, cách chạy, trạng thái test.

## Viết tài liệu

Trước mọi thao tác viết hoặc sửa văn bản (báo cáo LaTeX, README, docs, ghi chú, commit/PR dài), load skill
`writing-docs-viktor` và làm đúng theo nó; chạy checklist của nó trước khi giao. Không áp dụng cho code hay prompt.
Báo cáo LaTeX: dùng thêm `academic-latex-writer` (nội dung) và `latex-project-editor` (sửa .tex/.bib, lỗi compile).

## Quy tắc

- **Không bịa số liệu.** Số chu kỳ, `instret`, CPI, PASS/FAIL chỉ lấy từ lần chạy thật
  (`tools/run_tests.py`, `tools/compare.py`, `tools/rvsim.py`). Chưa chạy lại sau khi sửa mạch thì không khẳng
  định kết quả. Thiếu số liệu thì ghi `TODO_MEASURE`, không điền giá trị đoán.
- **Không bịa trích dẫn.** Mọi tài liệu tham khảo (spec RISC-V, Patterson & Hennessy, Logisim) phải kiểm chứng
  được; chưa kiểm thì ghi `TODO_CITE`.
- Logisim không mô phỏng trễ cổng: mọi con số ps/ns/speedup theo thời gian là giả định trễ tầng
  (IF 200, ID 100, EX 200, MEM 200, WB 100 ps, thanh ghi pipeline 20 ps) và phải ghi là giả định.
- Tên khối, tín hiệu trong văn bản phải trùng với file `.circ` (`ForwardUnit`, `HazardUnit`, `IDBypass`,
  `FwdA`, `FwdB`, `Redirect`, `LoadUse`...). Không mô tả thứ mạch không có (cache, ngắt, CSR, dự đoán nhánh động).
- Sửa mạch: ưu tiên sửa qua `generator/` rồi sinh lại `.circ`; sau đó chạy lại test cả ba bản.
  Không đụng các file `circ/.*.autosave` (thuộc phiên Logisim đang mở của người dùng).
- `build/` bị gitignore, sinh lại được bằng `tools/rvasm.py`.
- Windows: subprocess gửi stdin dạng bytes (text mode đổi `\n` thành `\r\n`); timeout phải kill cả cây tiến trình
  (`taskkill /F /T`) vì `java` có thể là launcher.
- Chỉ commit khi người dùng yêu cầu.

## Lệnh

```bash
python tools/rvasm.py programs/demo.s -o build/demo [--nohazard] [--circ <file.circ>]
python tools/run_tests.py circ/RV32I_SingleCycle.circ
python tools/run_tests.py circ/RV32I_Pipeline.circ --programs programs/fuzz
python tools/run_tests.py circ/extra/RV32I_Pipeline_NoHazard.circ --nohazard
python tools/compare.py [programs/t06_hazard.s]
```

Cần `LOGISIM_JAR` trỏ tới `logisim-evolution-4.1.0-all.jar` (Java 21). LaTeX: TinyTeX
(`pdflatex`/`xelatex`/`latexmk`, có `vntex`, `babel-vietnamese`, `texfot`, `chktex`, `latexdiff`).

## Cấu trúc

- `circ/` file Logisim · `generator/` sinh `.circ` bằng Python · `programs/` chương trình test (.s)
- `tools/` assembler, golden model, runner, so sánh · `tests/vectors/` test vector từng module
- `docs/` lộ trình, trang so sánh, `img/` ảnh mạch · `.claude/skills/` skill viết báo cáo
