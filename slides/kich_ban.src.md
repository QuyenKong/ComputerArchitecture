# Kịch bản thuyết trình CPU RISC-V RV32I

Nguồn của speaker notes trong `RV32I_ThuyetTrinh.pptx`. Tên trong ngoặc nhọn được `build_slides.py` thay bằng số
liệu trong `latex/generated/numbers.tex`; bản đã thay số để đọc và in là `KICH_BAN.md`.

Thứ tự: Hà (slide 1–8), Công (slide 9–13), Đức Anh (slide 14–19), cả nhóm (slide 20). Mỗi người khoảng 10 phút.
Dòng bắt đầu bằng [DEMO] là thao tác trên Logisim, không đọc thành tiếng.

## Slide 1 · CPU RISC-V RV32I
Người nói: Hà · 0:00–0:30

Em chào thầy và các bạn. Nhóm em gồm Quyền Đức Công, Bùi Phạm Sơn Hà và Nguyễn Đức Anh. Đề tài của nhóm là thiết kế
CPU RISC-V RV32I trên Logisim-evolution, gồm một bản đơn chu kỳ và một bản pipeline 5 tầng có xử lý hazard.

Bài trình bày chia làm ba phần, mỗi người khoảng 10 phút. Em trình bày 11 module dùng chung, Công trình bày CPU đơn
chu kỳ, và Đức Anh trình bày pipeline.

## Slide 2 · Đề bài và sản phẩm
Người nói: Hà · 0:30–2:00

Đề bài yêu cầu một máy tính 32 bit theo tập lệnh RV32I: 32 thanh ghi 32 bit, chương trình chạy từ lệnh nạp vào bộ nhớ
lệnh, không được sửa tay giá trị thanh ghi. Phải có hai phiên bản: đơn chu kỳ, và pipeline 5 tầng xử lý được data
hazard và control hazard.

Nhóm em làm ba file mạch. File SingleCycle là CPU đơn chu kỳ, mỗi lệnh xong trong một chu kỳ. File Pipeline là bản
nộp chính, có forwarding, bypass từ WB về ID, stall khi load-use và flush khi nhảy. File thứ ba là NoHazard: cùng
pipeline nhưng bỏ forwarding và stall, chỉ chạy đúng khi assembler chèn lệnh nop. Nhóm giữ bản này để đo xem phần
cứng xử lý hazard nhanh hơn bao nhiêu.

Bên phải là bốn con số chính. CPU hỗ trợ 37 lệnh RV32I, gồm cả các lệnh tùy chọn như LB, SH, BLT. Có 13 module có
test vector, bản pipeline đạt {vecPL} vector. 12 chương trình test và 25 chương trình sinh ngẫu nhiên đều PASS trên
bản đơn chu kỳ, bản pipeline, và trên bản NoHazard khi assembler chèn nop. Theo giả định trễ, pipeline nhanh hơn đơn
chu kỳ {resSpeedPL} lần. Các con số này lấy từ lần chạy test ngày 5/11.

## Slide 3 · Phần 1: 11 module dùng chung
Người nói: Hà · 2:00–2:15

Em bắt đầu phần 1. Cả hai CPU dùng chung 11 circuit con. Mỗi circuit có tên chân cố định và một file test vector
riêng, nên nhóm kiểm từng khối trước rồi mới ghép thành CPU.

## Slide 4 · 11 circuit con và test vector
Người nói: Hà · 2:15–3:15

Đây là 11 circuit đó, chia theo màu. Màu đỏ nhạt là nhóm giải mã: Control, ImmGen, ALUControl. Màu cam là nhóm thực
thi: RegisterFile, ALU, BranchUnit. Màu xám là bộ nhớ và vào ra: AddrDecode, LoadUnit, StoreUnit, IOController. Cuối
cùng là PerfCounters, đếm số chu kỳ và số lệnh.

Dòng nhỏ dưới mỗi ô là kết quả test vector, ví dụ ALU đạt 250 trên 250. Các vector chạy bằng tùy chọn -w của Logisim,
giá trị mong đợi sinh từ mô hình Python. PerfCounters không có vector riêng vì lần chạy chương trình nào cũng so bộ
đếm của nó với golden model.

Ô đỏ đậm là ba khối chỉ có ở pipeline: ForwardUnit, HazardUnit, IDBypass. Phần đó Đức Anh sẽ trình bày.

## Slide 5 · ALU và ALUControl
Người nói: Hà · 3:15–4:45

ALU nhận hai toán hạng A, B 32 bit và mã ALUCtrl 4 bit. Trong mạch, mười phép tính chạy song song: bộ cộng, bộ trừ,
hai bộ so sánh có dấu và không dấu, ba cổng logic, ba bộ dịch. Sau đó MUX 8 vào chọn kết quả theo funct3. Tức là ALU
không chạy kiểu if-else, mà tính hết rồi chọn.

Nhóm chọn mã ALUCtrl bằng bit 30 của lệnh ghép với funct3. Ba bit thấp chính là funct3, bit 3 phân biệt ADD với SUB
và SRL với SRA, như bảng nhỏ bên phải. Nhờ vậy khối ALUControl gần như chỉ là nối dây.

Có một bẫy ở đây. Với lệnh I như addi, bit 30 thuộc về immediate: lệnh addi x1, x1, -1024 có bit 30 bằng 1. Nếu lấy
bit 30 cho mọi lệnh thì addi số âm bị tính thành phép trừ. Vì vậy bit 3 chỉ lấy bit 30 khi lệnh là R hoặc là SRAI.
Chương trình t01_alu.s có ca kiểm tra đúng lỗi này.

[DEMO nếu còn thời gian] Mở circuit ALU, dùng Poke đặt A = 0xFFFFFFFF, B = 1. SLT ra 1 vì có dấu thì A là -1, còn
SLTU ra 0.

## Slide 6 · Control và ImmGen
Người nói: Hà · 4:45–6:15

Khối Control nhận lệnh 32 bit và sinh mọi tín hiệu điều khiển. Nhóm dựng nó như một bảng chân lý vẽ thành mạch.
Decoder 5 sang 32 theo opcode bit 6 đến 2 tạo ra một đường cho mỗi nhóm lệnh. Mỗi tín hiệu điều khiển là OR của các
nhóm cần nó, ví dụ RegWrite bằng OP hoặc OP-IMM hoặc LOAD hoặc JAL, JALR, LUI, AUIPC. Bảng bên phải là đúng bảng chân
lý trong mạch.

Một chi tiết quan trọng: decoder chỉ bật khi hai bit thấp của opcode bằng 11. Lệnh toàn số 0 vì thế cho mọi tín hiệu
bằng 0, tức là NOP. Phần pipeline tận dụng điều này: muốn xóa một lệnh chỉ cần nạp 0 vào thanh ghi pipeline.

ImmGen tách lệnh thành 8 mảnh bit có vị trí cố định, ghép lại theo 5 định dạng I, S, B, U, J, mở rộng dấu, rồi chọn
bằng MUX theo ImmSel. RISC-V xáo bit immediate của B và J để bit dấu luôn ở bit 31 và các mảnh nằm cùng chỗ giữa các
định dạng, nên ImmGen chủ yếu là nối dây.

Control còn sinh UseRs1, UseRs2, cho biết lệnh có thật sự đọc rs1, rs2 hay không. Đức Anh sẽ nói vì sao cần hai tín
hiệu này.

## Slide 7 · RegisterFile và BranchUnit
Người nói: Hà · 6:15–7:45

RegisterFile có 31 thanh ghi thật, x1 đến x31. x0 không phải thanh ghi: đầu vào số 0 của MUX đọc nối thẳng hằng 0,
nên đọc x0 luôn ra 0 và ghi vào x0 không có tác dụng. Có hai cổng đọc tổ hợp và một cổng ghi đồng bộ. Khi ghi,
decoder 5 sang 32 chỉ bật enable của đúng thanh ghi rd, và thanh ghi đó chụp giá trị ở cạnh lên clock.

Nhóm cố ý không bypass bên trong RegisterFile. Ở CPU đơn chu kỳ, lệnh addi x1, x1, 1 có rd trùng rs1. Nếu có bypass
bên trong thì đường từ ALU sang cổng ghi, sang cổng đọc rồi quay lại ALU thành một vòng tổ hợp, và mạch dao động.
Pipeline cần bypass thì dùng khối IDBypass đặt bên ngoài.

BranchUnit tách riêng vì ALU đang bận tính địa chỉ đích PC cộng immediate. Nó có hai bộ so sánh, không dấu và có dấu.
MUX chọn theo funct3 bit 2 và 1: bằng nhau, nhỏ hơn có dấu, hay nhỏ hơn không dấu. RISC-V mã hóa BNE, BGE, BGEU là
phủ định của BEQ, BLT, BLTU, nên chỉ cần XOR với funct3 bit 0, rồi AND với tín hiệu Branch để ra Taken.

## Slide 8 · Bộ nhớ, I/O và bộ đếm
Người nói: Hà · 7:45–9:45

Nhóm cuối là bộ nhớ và vào ra. Bảng bên trái là bản đồ bộ nhớ. Bộ nhớ lệnh là ROM 1024 lệnh, bộ nhớ dữ liệu là RAM
16 KiB. Logisim lưu mỗi ô một word nên chỉ số ô là địa chỉ bỏ hai bit thấp. Từ 0xF000_0000 trở lên là các thanh ghi
vào ra của UART và GPIO.

AddrDecode tách địa chỉ thành chỉ số word, offset trong word, và cờ IsIO khi 4 bit cao bằng F. LoadUnit dịch word đọc
được sang phải offset nhân 8 bit, rồi mở rộng dấu hoặc mở rộng 0 theo funct3.

StoreUnit phức tạp hơn. RAM của Logisim chỉ có byte enable khi đọc đồng bộ, không dùng được cho CPU đơn chu kỳ. Nên
nhóm làm theo kiểu đọc, sửa, ghi: đọc word cũ, dùng mặt nạ thay đúng byte hoặc halfword, rồi ghi cả word. Ví dụ ở
khung đỏ: sb 0xAB vào offset 2 của word 0x11223344 cho mặt nạ 0x00FF0000 và word mới 0x11AB3344.

IOController dùng chính lw, sw để điều khiển UART và GPIO. Có một lỗi nhóm đã gặp: đọc RXDATA sẽ lấy ký tự ra khỏi
hàng đợi bàn phím, nên tín hiệu đọc phải AND với MemRead. Nếu không, một lệnh add tình cờ ra kết quả 0xF0000004 cũng
làm mất ký tự. Cuối cùng, PerfCounters đếm cycles và instret để tính CPI.

Phần của em đến đây. Mời Công trình bày cách ghép 11 khối này thành CPU đơn chu kỳ.

## Slide 9 · Phần 2: CPU đơn chu kỳ
Người nói: Công · 0:00–0:15

Em là Công, em trình bày phần 2: CPU đơn chu kỳ. Em sẽ đi qua datapath, theo một lệnh lw chạy trong mạch, rồi nói về
cách chọn PC kế tiếp, đường găng và cách nhóm kiểm thử.

## Slide 10 · Datapath đơn chu kỳ
Người nói: Công · 0:15–2:30

Đây là mạch top-level của CPU đơn chu kỳ trong Logisim. Toàn bộ đường từ thanh ghi PC qua các module tới register
file và RAM là mạch tổ hợp. Ở mỗi cạnh lên clock, PC, thanh ghi đích và RAM cập nhật cùng lúc, nên mỗi lệnh xong
trong đúng một chu kỳ.

Một lệnh đi qua năm bước như cột bên phải. IF: PC đưa vào IMEM lấy lệnh, song song bộ cộng tính PC + 4. ID: Control
sinh tín hiệu, RegisterFile đọc rs1 và rs2, ImmGen tạo immediate. EX: ALU tính, đầu vào A là rs1, PC hoặc 0, đầu vào B
là rs2 hoặc immediate; BranchUnit so sánh. MEM: địa chỉ là kết quả ALU, StoreUnit ghép dữ liệu ghi, LoadUnit tách dữ
liệu đọc. WB: MUX WBSel chọn kết quả ALU, dữ liệu load hoặc PC + 4 để ghi vào rd.

Em gọi tên năm bước giống pipeline, nhưng ở bản này chúng xảy ra trong cùng một chu kỳ.

[DEMO] Mở RV32I_SingleCycle.circ, bấm Ctrl+K cho clock chạy. Chương trình demo.s đã nạp sẵn trong ROM. Chỉ vào
RegisterFile thấy thanh ghi thay đổi, TTY in Hello RISC-V!, LED 7 đoạn hiện 00E8 là tổng 12 số Fibonacci, chân halt
lên 1 khi chạy xong.

## Slide 11 · Ví dụ: lw t4, 8(sp) trong một chu kỳ
Người nói: Công · 2:30–4:30

Để rõ hơn, em theo một lệnh cụ thể: lw t4, 8(sp), mã máy 0x00812E83. Tách trường như hàng trên: 12 bit immediate
bằng 8, rs1 là x2 tức sp, funct3 bằng 010 nghĩa là load cả word, rd là x29 tức t4, và opcode 0000011 là nhóm LOAD.

Control bật nhóm LOAD và cho RegWrite bằng 1, BSel chọn immediate, MemRead bằng 1, WBSel chọn dữ liệu bộ nhớ. ALU
cộng sp với 8 ra địa chỉ. AddrDecode thấy địa chỉ không thuộc vùng I/O nên đọc RAM. LoadUnit chọn cả word theo
funct3. MUX ghi lại chọn dữ liệu bộ nhớ. Đến cạnh lên clock, t4 nhận giá trị và PC nhận PC + 4.

Lệnh load đi qua nhiều khối nhất: ROM, register file, ALU, RAM, LoadUnit. Nên chính nó quyết định chu kỳ clock dài
bao nhiêu, em nói ở slide sau.

[DEMO tùy chọn] Bấm Ctrl+T chạy từng nửa chu kỳ tới một lệnh lw trong demo.s, chỉ các tín hiệu ra của Control.

## Slide 12 · Next-PC, halt và đường găng
Người nói: Công · 4:30–6:30

Bên trái là cách chọn PC kế tiếp. PCSel bằng Taken hoặc Jal hoặc Jalr. Nếu PCSel bằng 1 thì PC nhận kết quả ALU AND
với 0xFFFFFFFE. Với branch và JAL, đầu vào A của ALU là PC; với JALR là rs1. Đặc tả JALR yêu cầu xóa bit 0 của đích
nhảy, còn với branch và JAL bit này vốn bằng 0. Nên một mạch dùng chung cho cả ba lệnh, không cần bộ cộng PC + imm
riêng.

Thanh ghi PC có enable bằng NOT Halt. Gặp lệnh EBREAK, CPU giữ nguyên trạng thái và chân halt lên 1, để bộ test biết
chương trình đã xong.

Bên phải và thanh phía dưới là nhược điểm của đơn chu kỳ. CPI luôn bằng 1, nhưng chu kỳ phải đủ dài cho lệnh chậm
nhất là load. Logisim không mô phỏng trễ cổng, nên nhóm dùng giả định trễ theo sách Patterson và Hennessy: nạp lệnh
200, đọc thanh ghi 100, ALU 200, bộ nhớ dữ liệu 200, ghi thanh ghi 100 pico giây, tổng {resTSingle} ps. Lệnh add không
dùng RAM vẫn phải chờ hết {resTSingle} ps. Đây là con số giả định để so sánh, không phải đo trên mạch. Phần 3 sẽ cắt
đường này thành 5 đoạn.

## Slide 13 · Kiểm thử tự động và kết quả bản đơn chu kỳ
Người nói: Công · 6:30–9:30

Cuối cùng là cách nhóm kiểm thử, áp dụng cho cả ba bản mạch. Nhóm tự viết toolchain bằng Python. rvasm.py dịch
assembly ra mã máy và ghi thẳng vào ROM trong file .circ, đúng phần công cụ từ assembly ra mã máy mà đề khuyến khích.
run_tests.py chạy Logisim không giao diện rồi so kết quả với rvsim.py, một trình mô phỏng mức lệnh viết độc lập,
không dùng gì từ file mạch.

Thứ được so gồm 31 thanh ghi, toàn bộ 16 KiB RAM, chuỗi in ra TTY, giá trị GPIO, và cả hai bộ đếm cycles, instret. Vì
so cả số chu kỳ, bộ test bắt được lỗi về thời gian mà kết quả cuối vẫn đúng, ví dụ stall thừa một chu kỳ.

Kết quả trên bản đơn chu kỳ: 12 trên 12 chương trình test và 25 trên 25 chương trình ngẫu nhiên đều PASS, {vecSC}
test vector đạt. CPI bằng 1: tổng {resTotSC} lệnh chạy đúng {resTotSC} chu kỳ. Riêng demo.s có {resDemoN} lệnh và
chạy {resDemoN} chu kỳ.

[DEMO] Mở terminal, chạy python tools/run_tests.py circ/RV32I_SingleCycle.circ, chờ dòng ALL PASSED.

Phần của em đến đây. Mời Đức Anh trình bày pipeline.

## Slide 14 · Phần 3: Pipeline 5 tầng và hazard
Người nói: Đức Anh · 0:00–0:15

Em là Đức Anh, em trình bày phần 3: pipeline 5 tầng. Em sẽ nói cách chia datapath, các loại hazard nhóm xử lý, và
kết quả so sánh ba phiên bản.

## Slide 15 · Datapath pipeline 5 tầng
Người nói: Đức Anh · 0:15–2:00

Pipeline cắt đường tổ hợp của bản đơn chu kỳ thành năm đoạn IF, ID, EX, MEM, WB, và đặt một thanh ghi pipeline giữa
hai đoạn liên tiếp. Mỗi chu kỳ có năm lệnh khác nhau ở năm tầng. Chu kỳ clock chỉ cần đủ cho tầng chậm nhất cộng
thời gian của thanh ghi: theo giả định là 200 cộng 20 bằng {resTPipe} ps, so với {resTSingle} ps của bản đơn chu kỳ.
Nếu CPI vẫn bằng 1 thì tăng tốc lý tưởng là {resIdealSpeedup} lần.

Bốn thanh ghi pipeline giữ mọi thứ tầng sau cần về một lệnh: dữ liệu, số hiệu thanh ghi, và tín hiệu điều khiển. Tín
hiệu điều khiển sinh một lần ở ID rồi đi theo lệnh. Mỗi thanh ghi có chân giữ giá trị để stall, và chân flush nạp
toàn 0. Như Hà đã nói, lệnh toàn 0 là NOP, nên flush biến lệnh thành bubble. Flush làm đồng bộ qua MUX vì chân Clear
của Register trong Logisim là bất đồng bộ.

[DEMO] Mở RV32I_Pipeline.circ, chỉ Pipeline Monitor ở góc dưới: nó hiện PC và lệnh ở từng tầng cùng các tín hiệu
Stall, LoadUse, E_Redirect, FwdA, FwdB.

## Slide 16 · Data hazard: forwarding, bypass và stall
Người nói: Đức Anh · 2:00–4:30

Data hazard xảy ra khi lệnh sau cần kết quả của lệnh trước mà lệnh trước chưa ghi vào register file. Nhóm xử lý theo
khoảng cách giữa hai lệnh.

Cách 1 hoặc 2 lệnh, cột trái: kết quả đã nằm ở thanh ghi EX/MEM hoặc MEM/WB, chỉ chưa ghi vào register file.
ForwardUnit so rs1, rs2 của lệnh ở EX với rd của lệnh ở MEM và WB. Trùng với EX/MEM thì FwdA bằng 01, trùng với
MEM/WB thì bằng 10. Điều kiện rd khác 0 để không forward vào x0. EX/MEM được ưu tiên vì khi hai lệnh liên tiếp cùng
ghi một thanh ghi, giá trị mới nhất thuộc lệnh gần hơn. Trường hợp này không mất chu kỳ nào.

Cách 3 lệnh, cột giữa: lệnh ở WB ghi register file ở cạnh lên cuối chu kỳ, nhưng lệnh ở ID đọc ngay trong chu kỳ đó
nên nhận giá trị cũ. IDBypass đặt sau cổng đọc, thấy rd của WB trùng thì đưa thẳng dữ liệu WB vào ID. Cách này tương
đương quy ước ghi nửa đầu, đọc nửa sau chu kỳ trong sách, và giữ RegisterFile dùng được cho bản đơn chu kỳ như Hà đã
giải thích.

Cột phải là load-use: lw rồi dùng ngay kết quả. Dữ liệu load chỉ có ở cuối tầng MEM, còn lệnh sau cần nó ở đầu tầng
EX trong cùng chu kỳ, nên forwarding không kịp. HazardUnit phát hiện theo công thức phía dưới, giữ PC và IF/ID, chèn
một bubble vào ID/EX. Mất 1 chu kỳ. UseRs1, UseRs2 giúp không stall oan, ví dụ lệnh LUI có các bit ở vị trí rs1 tình
cờ trùng rd của lệnh lw ngay trước.

[DEMO] Chạy t06_hazard.s từng chu kỳ, chỉ FwdA đổi giá trị và Stall bằng 1 trên Pipeline Monitor.

## Slide 17 · Control hazard và giản đồ pipeline
Người nói: Đức Anh · 4:30–6:45

Control hazard: pipeline đã nạp thêm hai lệnh sau một lệnh nhảy trước khi biết lệnh đó có nhảy không. Nhóm chọn cách
đơn giản là luôn đoán không nhảy, nạp PC + 4. Lệnh nhảy được quyết định ở tầng EX. Nếu nhảy, Redirect bằng 1, PC nhận
địa chỉ đích, hai lệnh nạp sai ở IF/ID và ID/EX bị flush, mất 2 chu kỳ. Nếu cùng lúc có stall và redirect thì
redirect thắng, vì lệnh đang bị stall nằm trên nhánh sai.

Bảng bên phải là giản đồ của 7 lệnh đầu trong t06_hazard.s trên pipeline, sinh tự động từ golden model. Ô đỏ là chu
kỳ lệnh phải đứng ở ID vì load-use, có 3 lần. Lệnh beq nhảy ở EX nên hai lệnh xám phía sau bị flush. Bảy lệnh chiếm
14 chu kỳ. Trên bản NoHazard, mọi phụ thuộc gần phải chờ bằng nop, nên cùng đoạn này cần 17 chu kỳ.

Từ các cơ chế đó, số chu kỳ của pipeline bằng số lệnh, cộng 4 chu kỳ lấp đầy, cộng số lần load-use, cộng 2 nhân số
lần nhảy. Bộ test so con số này với bộ đếm cycles của Logisim và khớp trên mọi chương trình; riêng t11_io.s không so
số chu kỳ vì thời điểm gõ phím phụ thuộc Logisim.

[DEMO] Chạy tới lệnh beq: E_Redirect bằng 1 và hai lệnh phía sau thành 00000000.

## Slide 18 · Kết quả ba phiên bản trên 12 chương trình
Người nói: Đức Anh · 6:45–8:45

Đây là kết quả trên 12 chương trình test. Tổng số chu kỳ: đơn chu kỳ {resTotSC}, NoHazard {resTotNH}, pipeline
{resTotPL}. CPI của pipeline là {resTotCPI}. Bản NoHazard có CPI {resTotCPINH} vì phải chạy thêm {resTotNOP} lệnh nop.

Biểu đồ là tăng tốc so với đơn chu kỳ theo giả định trễ {resTSingle} ps và {resTPipe} ps. Tính trên tổng, pipeline
nhanh hơn {resSpeedPL} lần, NoHazard chỉ {resSpeedNH} lần, trong khi mức lý tưởng là {resIdealSpeedup}. Với cùng chu
kỳ clock, pipeline chạy ít chu kỳ hơn NoHazard {resSpeedPLNH} lần. Đó là phần đóng góp riêng của forwarding và stall
bằng phần cứng.

Vì sao chưa đạt {resIdealSpeedup}? Thứ nhất, CPI lớn hơn 1. Nhìn số cuối bên phải: flush khi nhảy tốn {flushTot} chu
kỳ, trong khi load-use chỉ {resTotLU}. Riêng t09_recursion.s có {resNineBR} lần nhảy, tốn {resNineFlush} chu kỳ, gấp
hơn 5 lần {resNineLU} chu kỳ load-use. Vậy control hazard là nguồn mất mát lớn nhất. Thứ hai, các tầng không dài bằng
nhau: ID và WB chỉ cần 100 ps nhưng vẫn chiếm trọn {resTPipe} ps.

Em nhắc lại: thời gian là giả định, còn số chu kỳ là số chạy thật và đã khớp với Logisim.

## Slide 19 · Hạn chế và hướng phát triển
Người nói: Đức Anh · 8:45–9:45

Về hạn chế. Lớn nhất là lệnh nhảy quyết định ở EX nên mỗi lần nhảy mất 2 chu kỳ, như vừa thấy. CPU chưa có exception,
ngắt và CSR: ECALL, EBREAK chỉ dùng làm lệnh dừng, UART phải hỏi vòng. Truy cập bộ nhớ lệch chưa được hỗ trợ. Vùng
I/O chỉ giải mã vài bit địa chỉ nên có địa chỉ bí danh. Và mọi so sánh thời gian dựa trên giả định trễ.

Hướng phát triển nhóm xếp theo lợi ích đo được bằng bộ test hiện có. Ưu tiên một là đưa quyết định nhánh lên ID, giảm
phạt từ 2 xuống 1 chu kỳ; trên t09 tiết kiệm tối đa {resNineBR} chu kỳ, trừ đi các stall mới khi lệnh nhánh phụ thuộc
lệnh ngay trước. Tiếp theo là dự đoán nhánh 2 bit với BTB, phần mở rộng nhân chia, và ngắt cho UART.

Phần trình bày của nhóm em đến đây.

## Slide 20 · Cảm ơn
Người nói: Cả nhóm

Em cảm ơn thầy và các bạn đã lắng nghe. Nhóm em xin nhận câu hỏi.

Câu hỏi về phần nào thì người trình bày phần đó trả lời: Hà phần 11 module, Công phần đơn chu kỳ và kiểm thử, Đức Anh
phần pipeline. Nếu thầy muốn xem demo, nhóm mở Logisim trực tiếp; video dự phòng ở demo/demo_RV32I.mp4.
