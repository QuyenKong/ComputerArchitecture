# Kịch bản thuyết trình CPU RISC-V RV32I

Bản đã thay số liệu, sinh từ kich_ban.src.md. Lời thoại giống speaker notes trong RV32I_ThuyetTrinh.pptx.


Thứ tự: Hà (slide 1–10), Công (slide 11–16), Đức Anh (slide 17–24), cả nhóm (slide 25). Mỗi người khoảng 10 phút.
Dòng bắt đầu bằng [DEMO] là thao tác trên Logisim hoặc terminal, không đọc thành tiếng.

## Slide 1 · CPU RISC-V RV32I
Người nói: Hà · 0:00–0:30

Em chào thầy và các bạn. Nhóm em gồm Quyền Đức Công, Bùi Phạm Sơn Hà và Nguyễn Đức Anh. Đề tài của nhóm là thiết kế
CPU RISC-V RV32I trên Logisim-evolution, gồm một bản đơn chu kỳ và một bản pipeline 5 tầng có xử lý hazard.

Bài trình bày có ba phần, mỗi người khoảng 10 phút: em trình bày kiến trúc và các module, Công trình bày CPU đơn chu kỳ
và kiểm thử, Đức Anh trình bày pipeline, hazard và kết quả.

## Slide 2 · Đề bài và sản phẩm
Người nói: Hà · 0:30–1:45

Đề bài yêu cầu một máy tính 32 bit theo tập lệnh RV32I: dữ liệu, lệnh, thanh ghi và PC đều 32 bit, có 32 thanh ghi.
Phải có hai phiên bản, đơn chu kỳ và pipeline 5 tầng, trong đó pipeline xử lý đúng data hazard và control hazard cơ
bản. Chương trình chạy từ lệnh nạp vào bộ nhớ lệnh, không được chỉnh tay thanh ghi.

Nhóm em làm ba file mạch. SingleCycle là CPU đơn chu kỳ. Pipeline là bản nộp chính, có forwarding, bypass từ WB về
ID, stall khi load-use và flush khi nhảy. NoHazard là cùng pipeline nhưng bỏ forwarding và stall, chỉ chạy đúng khi
assembler chèn nop; nhóm giữ bản này để đo phần cứng xử lý hazard đem lại bao nhiêu.

Bốn con số ở dưới: CPU hiện thực 37 lệnh RV32I. 13 circuit có test vector, bản pipeline đạt 4014/4014. 12 chương trình
test và 25 chương trình sinh ngẫu nhiên đều PASS trên bản đơn chu kỳ, bản pipeline, và trên bản NoHazard khi chèn
nop. Theo giả định trễ, pipeline nhanh hơn đơn chu kỳ 2.29 lần.

## Slide 3 · Tập lệnh RV32I và định dạng lệnh
Người nói: Hà · 1:45–3:00

RV32I có 32 thanh ghi x0 đến x31. x0 luôn đọc ra 0 và mọi lệnh ghi vào x0 bị bỏ qua, nên phần cứng chỉ cần 31 thanh ghi
thật. Bảng bên trái là sáu định dạng lệnh. Các trường rd, funct3, rs1, rs2 luôn nằm cùng vị trí, nhờ vậy register file
đọc rs1, rs2 song song với việc giải mã. Bit dấu của immediate luôn là bit 31, nên mở rộng dấu bắt đầu được ngay.

Mỗi lệnh dài 4 byte nên PC tăng 4. ROM và RAM của Logisim lưu mỗi ô một word, nên chỉ số ô là địa chỉ bỏ hai bit thấp:
IMEM dùng PC bit 11 đến 2, DMEM dùng địa chỉ bit 13 đến 2.

Bên phải là 37 lệnh nhóm hiện thực: 10 lệnh R, 9 lệnh I số học, 5 lệnh load, 3 lệnh store, 6 lệnh rẽ nhánh, cùng JAL,
JALR, LUI và AUIPC. FENCE được giải mã thành NOP. Cách này đúng với CPU của nhóm vì chỉ có một luồng thực thi, không có
cache, và mọi truy cập RAM hay I/O diễn ra theo đúng thứ tự chương trình. ECALL và EBREAK được quy ước là lệnh dừng để
bộ test có điểm kết thúc. Các lệnh CSR thuộc phần mở rộng Zicsr, không nằm trong RV32I base, nhóm không hiện thực.

## Slide 4 · Sơ đồ khối và quyết định thiết kế
Người nói: Hà · 3:00–4:15

Hàng trên là sơ đồ khối theo năm bước: PC và IMEM để nạp lệnh, Control, ImmGen và RegisterFile để giải mã, ALU và
BranchUnit để thực thi, DMEM cùng LoadUnit, StoreUnit, I/O để truy cập bộ nhớ, và MUX ghi lại vào rd. 11 circuit con
này dùng chung cho cả hai CPU; pipeline thêm 4 thanh ghi pipeline và 3 khối xử lý hazard.

Năm quyết định thiết kế chính. Một, kiến trúc Harvard: ROM lệnh và RAM dữ liệu tách riêng nên nạp lệnh và load, store
không tranh nhau một cổng bộ nhớ. Hai, ALU tính luôn địa chỉ đích: với branch và JAL đầu vào A là PC, với JALR là rs1,
nên không cần bộ cộng PC cộng immediate riêng. Ba, lệnh toàn 0 là NOP vì decoder chỉ bật khi hai bit thấp của opcode
bằng 11; pipeline flush một tầng chỉ cần nạp 0. Bốn, SB và SH làm bằng đọc, sửa, ghi cả word, vì RAM của Logisim chỉ
có byte enable khi đọc đồng bộ. Năm, UART và GPIO là vài địa chỉ đặc biệt, CPU dùng chính lw, sw để điều khiển.

## Slide 5 · Phần 1: Thiết kế các module
Người nói: Hà · 4:15–4:25

Em bắt đầu phần 1: các module. Hai CPU có tổng cộng 18 circuit con, 11 circuit dùng chung và 7 circuit chỉ có ở
pipeline.

## Slide 6 · 18 circuit con và test vector
Người nói: Hà · 4:25–5:25

Đây là 18 circuit đó. Màu đỏ nhạt là nhóm giải mã: Control, ImmGen, ALUControl. Màu cam là nhóm thực thi:
RegisterFile, ALU, BranchUnit. Màu xám là bộ nhớ, vào ra và bộ đếm. Các ô đỏ đậm là 7 circuit chỉ có ở pipeline:
ForwardUnit, HazardUnit, IDBypass và 4 thanh ghi pipeline; phần đó Đức Anh sẽ trình bày.

Dòng nhỏ dưới mỗi ô là kết quả test vector, ví dụ ALU đạt 250 trên 250. Có 13 circuit có file test vector: tổng
2914/2914 trên bản đơn chu kỳ và 4014/4014 trên bản pipeline. Giá trị mong đợi sinh từ mô hình Python, chạy bằng tùy chọn
-w của Logisim. PerfCounters và 4 thanh ghi pipeline không có vector riêng; chúng được kiểm tra qua các chương trình
chạy trên toàn CPU.

## Slide 7 · ALU và ALUControl
Người nói: Hà · 5:25–6:40

ALU nhận hai toán hạng A, B 32 bit và mã ALUCtrl 4 bit. Trong mạch, mười phép tính chạy song song: bộ cộng, bộ trừ,
hai bộ so sánh có dấu và không dấu, ba cổng logic, ba bộ dịch. MUX 8 vào chọn kết quả theo ba bit thấp của ALUCtrl,
chính là funct3; hai MUX 2 vào theo bit 3 chọn giữa ADD và SUB, giữa SRL và SRA. Lượng dịch chỉ lấy 5 bit thấp của B,
đúng đặc tả.

Bảng nhỏ là mã ALUCtrl. Có một bẫy: với lệnh I như addi, bit 30 thuộc immediate, lệnh addi x1, x1, -1024 có bit 30
bằng 1. Nếu lấy bit 30 cho mọi lệnh thì addi số âm bị tính thành phép trừ. Vì vậy ALUControl chỉ lấy bit 30 khi lệnh
là R hoặc là SRAI. Chương trình t01_alu.s có ca kiểm tra đúng lỗi này.

## Slide 8 · Control và ImmGen
Người nói: Hà · 6:40–8:00

Control nhận lệnh 32 bit và sinh mọi tín hiệu điều khiển. Decoder 5 sang 32 theo opcode bit 6 đến 2 tạo một đường cho
mỗi nhóm lệnh, enable bằng opcode bit 1 AND bit 0. Mỗi tín hiệu điều khiển là OR của các nhóm cần nó. Bảng bên trái là
đúng bảng chân lý trong mạch. Lệnh toàn số 0 cho mọi tín hiệu bằng 0, tức là NOP. Control còn sinh UseRs1, UseRs2 cho
biết lệnh có thật sự đọc rs1, rs2 không, để pipeline không stall oan khi trường rs1 của LUI hay JAL tình cờ trùng rd
của một lệnh load.

ImmGen tách lệnh thành 8 mảnh bit có vị trí cố định, ghép theo 5 định dạng, mở rộng dấu rồi chọn bằng MUX theo
ImmSel. Offset của B và J là bội của 2 nên đặc tả không mã hóa bit 0, ImmGen nối hằng 0 vào đó. Bit 1 vẫn được mã hóa
vì đặc tả chọn đơn vị 2 byte để dùng chung với phần mở rộng C, có lệnh nén dài 2 byte.

## Slide 9 · RegisterFile và BranchUnit
Người nói: Hà · 8:00–9:05

RegisterFile có 31 thanh ghi thật, x1 đến x31. Đầu vào số 0 của MUX đọc nối thẳng hằng 0, nên đọc x0 luôn ra 0. Có hai
cổng đọc tổ hợp và một cổng ghi đồng bộ: decoder 5 sang 32 chỉ bật enable của đúng thanh ghi rd ở cạnh lên.

Nhóm cố ý không bypass bên trong RegisterFile. Ở CPU đơn chu kỳ, lệnh addi x1, x1, 1 có rd trùng rs1; nếu có bypass
bên trong thì đường ALU sang cổng ghi, sang cổng đọc rồi quay về ALU thành vòng tổ hợp và mạch dao động. Pipeline dùng
khối IDBypass đặt bên ngoài.

BranchUnit có hai bộ so sánh, không dấu và có dấu. MUX chọn theo funct3 bit 2 và 1: bằng nhau, nhỏ hơn có dấu, hay
nhỏ hơn không dấu. RISC-V mã hóa BNE, BGE, BGEU là phủ định của BEQ, BLT, BLTU, nên chỉ cần XOR với funct3 bit 0, rồi
AND với Branch để ra Taken.

## Slide 10 · Bộ nhớ, I/O và bộ đếm
Người nói: Hà · 9:05–10:30

Bảng bên trái là bản đồ bộ nhớ: ROM lệnh 1024 lệnh, RAM dữ liệu 16 KiB, vùng 0x700 dùng cho bộ test lưu x1 đến x31, và
từ 0xF000_0000 là các thanh ghi của UART và GPIO.

AddrDecode tách địa chỉ thành chỉ số word, offset trong word, và cờ IsIO khi 4 bit cao bằng F. LoadUnit dịch word đọc
được sang phải offset nhân 8 bit rồi mở rộng dấu hoặc mở rộng 0 theo funct3. StoreUnit làm đọc, sửa, ghi: mặt nạ M là
mask dịch trái offset nhân 8, word mới giữ các byte ngoài M của word cũ và lấy byte mới trong M. Ví dụ ở khung đỏ: sb
0xAB vào offset 2 của word 0x11223344 cho M bằng 0x00FF0000 và word mới 0x11AB3344.

IOController có một chi tiết: đọc RXDATA lấy ký tự ra khỏi hàng đợi bàn phím, nên tín hiệu đọc phải AND với MemRead.
Nếu không, một lệnh add tình cờ ra kết quả 0xF0000004 cũng làm mất ký tự. PerfCounters đếm cycles khi CPU chưa halt và
instret khi có lệnh hoàn thành, bubble không được đếm.

Phần của em đến đây. Mời Công trình bày CPU đơn chu kỳ.

## Slide 11 · Phần 2: CPU đơn chu kỳ và kiểm thử
Người nói: Công · 0:00–0:15

Em là Công, em trình bày phần 2: ghép các module thành CPU đơn chu kỳ, theo một lệnh lw đi qua mạch, cách chọn PC kế
tiếp và đường găng, rồi cách nhóm kiểm thử cả ba bản mạch.

## Slide 12 · Datapath đơn chu kỳ
Người nói: Công · 0:15–2:00

Đây là mạch top-level của CPU đơn chu kỳ. Toàn bộ đường từ thanh ghi PC qua các module tới register file và RAM là
mạch tổ hợp. Ở mỗi cạnh lên clock, PC, thanh ghi đích và RAM cập nhật cùng lúc, nên mỗi lệnh xong trong một chu kỳ.

Một lệnh đi qua năm bước như cột bên phải. IF: PC vào IMEM lấy lệnh, song song bộ cộng tính PC + 4. ID: Control sinh
tín hiệu, RegisterFile đọc rs1, rs2, ImmGen tạo immediate. EX: đầu vào A của ALU là rs1, PC hoặc 0, đầu vào B là rs2
hoặc immediate; BranchUnit so sánh. MEM: StoreUnit ghép dữ liệu ghi, LoadUnit tách dữ liệu đọc. WB: MUX WBSel chọn
kết quả ALU, dữ liệu load hoặc PC + 4 để ghi vào rd. Ở bản này năm bước xảy ra trong cùng một chu kỳ.

[DEMO] Mở RV32I_SingleCycle.circ, bấm Ctrl+K. demo.s đã nạp sẵn trong ROM. Chỉ RegisterFile, TTY in Hello RISC-V!,
LED 7 đoạn hiện 00E8 là tổng 12 số Fibonacci, 8 LED sáng.

## Slide 13 · Ví dụ: lw t4, 8(sp) trong một chu kỳ
Người nói: Công · 2:00–3:45

Em theo một lệnh cụ thể: lw t4, 8(sp), mã máy 0x00812E83. Tách trường như hàng trên: immediate bằng 8, rs1 là x2 tức
sp, funct3 bằng 010 là load cả word, rd là x29 tức t4, opcode 0000011 là nhóm LOAD.

Control bật nhóm LOAD: RegWrite bằng 1, BSel chọn immediate, MemRead bằng 1, WBSel bằng 1 chọn dữ liệu bộ nhớ. ALU cộng
sp với 8 ra địa chỉ. AddrDecode thấy IsIO bằng 0 nên đọc RAM. LoadUnit lấy cả word theo funct3. Đến cạnh lên clock, t4
nhận giá trị và PC nhận PC + 4.

Lệnh load đi qua nhiều khối nhất, nên chính nó quyết định chu kỳ clock dài bao nhiêu.

[DEMO tùy chọn] Ctrl+T chạy từng nửa chu kỳ tới một lệnh lw trong demo.s, chỉ các tín hiệu ra của Control.

## Slide 14 · Next-PC, halt và đường găng
Người nói: Công · 3:45–5:30

PC kế tiếp: PCSel bằng Taken hoặc Jal hoặc Jalr. Nếu PCSel bằng 1, PC nhận kết quả ALU AND 0xFFFFFFFE. Đặc tả JALR yêu
cầu xóa bit 0 của đích nhảy, còn với branch và JAL bit này vốn bằng 0, nên một mạch dùng chung cho cả ba lệnh. Thanh
ghi PC có enable bằng NOT Halt: gặp EBREAK, CPU giữ nguyên trạng thái và chân halt lên 1.

Nhược điểm của đơn chu kỳ: CPI bằng 1 nhưng chu kỳ phải đủ dài cho lệnh chậm nhất là load. Logisim không mô phỏng trễ
cổng, nên nhóm dùng giả định trễ theo Patterson và Hennessy: nạp lệnh 200, đọc thanh ghi 100, ALU 200, bộ nhớ dữ liệu
200, ghi thanh ghi 100 pico giây, tổng 800 ps. Lệnh add không dùng RAM vẫn phải chờ hết 800 ps. Đây
là con số giả định để so sánh, không phải số đo trên mạch.

## Slide 15 · Kiểm thử hai mức: module và toàn CPU
Người nói: Công · 5:30–7:45

Nhóm kiểm thử ở hai mức. Mức module là test vector như Hà đã nói, bảng bên phải là kết quả từng module trên hai bản.
Mức toàn CPU dùng toolchain Python ở hàng trên. rvasm.py dịch assembly ra mã máy và ghi thẳng vào ROM trong file .circ.
run_tests.py chạy Logisim không giao diện rồi so với rvsim.py, một trình mô phỏng mức lệnh viết độc lập, không dùng gì
từ file mạch.

Thứ được so gồm 31 thanh ghi x1 đến x31, toàn bộ 16 KiB RAM, chuỗi in ra TTY, GPIO_OUT và cả hai bộ đếm cycles,
instret. Vì so cả số chu kỳ, bộ test bắt được lỗi thời gian mà kết quả cuối vẫn đúng, ví dụ stall thừa hay flush
thiếu.

Có 12 chương trình: demo.s, năm chương trình phủ từng nhóm lệnh, t06_hazard.s gom các ca forwarding, load-use và ghi
x0, ba chương trình thực tế hơn là Fibonacci, sắp xếp nổi bọt và đệ quy, và hai chương trình UART, GPIO. Thêm 25
chương trình sinh ngẫu nhiên, mỗi chương trình 189 đến 231 lệnh, có nhiều phụ thuộc gần để kích hoạt
forwarding và stall.

[DEMO] Chạy python tools/run_tests.py circ/RV32I_SingleCycle.circ, chờ dòng ALL PASSED.

## Slide 16 · Kết quả kiểm thử
Người nói: Công · 7:45–9:45

Bảng là kết quả chạy lại ngày 05/11/2026. Bản đơn chu kỳ và bản pipeline đều PASS 12 trên 12 chương trình và 25 trên
25 chương trình fuzz. Bản NoHazard chạy chương trình bình thường thì không chương trình nào PASS; khi assembler chèn nop
thì PASS hết. Test vector: 2914/2914 trên bản đơn chu kỳ, 4014/4014 trên bản pipeline.

Ở mọi lần PASS, số chu kỳ Logisim đếm khớp đúng với golden model, trừ t11_io.s vì thời điểm ký tự bàn phím đến phụ
thuộc Logisim. Bản đơn chu kỳ có CPI bằng 1: tổng 5993 lệnh chạy đúng 5993 chu kỳ.

Vì sao NoHazard sai: ngay ở demo.s, thanh ghi sp ra 0xFFFFFFF0 thay vì 0x00003FF0, vì lệnh addi sp, sp, -16 đọc sp trước
khi lệnh lui sp, 4 kịp ghi. Đó chính là data hazard mà phần cứng của bản pipeline xử lý.

Phần của em đến đây. Mời Đức Anh trình bày pipeline.

## Slide 17 · Phần 3: Pipeline 5 tầng và hazard
Người nói: Đức Anh · 0:00–0:15

Em là Đức Anh, em trình bày phần 3: cách chia datapath thành năm tầng, ba loại hazard và cách nhóm xử lý, bản NoHazard,
và kết quả so sánh ba phiên bản.

## Slide 18 · Năm tầng và thanh ghi pipeline
Người nói: Đức Anh · 0:15–1:45

Pipeline cắt đường tổ hợp của bản đơn chu kỳ thành năm đoạn và đặt thanh ghi pipeline giữa hai đoạn liên tiếp. Chu kỳ
clock chỉ cần đủ cho tầng chậm nhất cộng thời gian thanh ghi: theo giả định là 200 cộng 20 bằng 220 ps. Nếu CPI
vẫn bằng 1, tăng tốc lý tưởng là 3.64 lần.

Bảng dưới là các trường của bốn thanh ghi pipeline. Tín hiệu điều khiển sinh một lần ở ID rồi đi theo lệnh. Mỗi trường
là một MUX và một Register: EN bằng 0 thì giữ giá trị để stall, FLUSH bằng 1 thì nạp toàn 0 và lệnh thành bubble. Trường
exres là PC + 4 với JAL, JALR và kết quả ALU với lệnh khác. Trường instr của IF/ID là đầu vào của Control và ImmGen; pc
của ID/EX vào MUX ASel cho BRANCH, JAL, AUIPC; pc4 vào MUX chọn exres. Các trường pc, instr ở EX/MEM và MEM/WB chỉ để
hiển thị trên Pipeline Monitor.

[DEMO] Mở RV32I_Pipeline.circ, chỉ Pipeline Monitor ở góc dưới.

## Slide 19 · Ba loại hazard; forwarding và bypass WB→ID
Người nói: Đức Anh · 1:45–3:45

Pipeline có ba loại hazard. Structural hazard không xảy ra vì bộ nhớ lệnh và dữ liệu tách riêng, register file có hai
cổng đọc và một cổng ghi. Data hazard xử lý bằng forwarding và bypass, riêng load-use phải stall. Control hazard xử lý
bằng đoán không nhảy và flush.

Lệnh cách 1 hoặc 2 vị trí: kết quả đã nằm ở EX/MEM hoặc MEM/WB, chỉ chưa ghi vào register file. ForwardUnit so rs1, rs2
của lệnh ở EX với rd của lệnh ở MEM và WB. FwdA bằng 01 là lấy từ EX/MEM, bằng 10 là lấy từ MEM/WB. Điều kiện rd khác 0
để không forward vào x0, và EX/MEM được ưu tiên vì giá trị mới nhất thuộc lệnh gần hơn. Không mất chu kỳ nào.

Lệnh cách 3 vị trí: lệnh ở WB ghi register file ở cạnh lên cuối chu kỳ, còn lệnh ở ID đọc ngay trong chu kỳ đó nên
nhận giá trị cũ. IDBypass đặt sau cổng đọc, thấy rd của WB trùng thì đưa thẳng dữ liệu WB vào ID. Cách này tương đương
quy ước ghi nửa đầu, đọc nửa sau chu kỳ trong sách, và giữ RegisterFile dùng được cho bản đơn chu kỳ.

## Slide 20 · Load-use, control hazard và HazardUnit
Người nói: Đức Anh · 3:45–5:45

Load-use: dữ liệu load chỉ có ở cuối tầng MEM, còn lệnh ngay sau cần nó ở đầu tầng EX, nên forwarding không kịp.
HazardUnit phát hiện theo công thức trong khung đỏ, giữ PC và IF/ID, chèn một bubble vào ID/EX. Chu kỳ sau, lệnh phụ
thuộc lên EX và nhận dữ liệu qua forwarding từ MEM/WB. Mất 1 chu kỳ.

Control hazard: pipeline luôn nạp PC + 4. Lệnh nhảy quyết định ở EX; nếu nhảy, Redirect bằng 1, PC nhận địa chỉ đích,
hai lệnh nạp sai ở IF/ID và ID/EX bị flush, mất 2 chu kỳ. Nếu cùng lúc có stall và redirect thì redirect thắng vì lệnh
đang chờ nằm trên nhánh sai. EBREAK ở ID làm Stall bằng 1, CPU dừng khi EBREAK tới WB.

Khung xám là các phương trình của HazardUnit. Từ các cơ chế trên, số chu kỳ của pipeline bằng số lệnh cộng 4 chu kỳ
lấp đầy, cộng số lần load-use, cộng 2 nhân số lần nhảy. Bộ test so con số này với Logisim trên mọi chương trình.

[DEMO] Chạy t06_hazard.s từng chu kỳ: Stall bằng 1 ở lần load-use, E_Redirect bằng 1 ở lệnh beq và hai lệnh sau thành
00000000.

## Slide 21 · Bản NoHazard và giản đồ pipeline của t06_hazard.s
Người nói: Đức Anh · 5:45–7:15

Bản NoHazard khác bản pipeline ở hai chỗ: chân chọn MUX forwarding nối hằng 0, và đầu vào E_MemRead của HazardUnit nối
0; flush khi nhảy và IDBypass vẫn giữ. Để nó chạy đúng, assembler chèn nop: lệnh đọc rd của lệnh ngay trước được chèn 2
nop, đọc rd của lệnh trước đó 2 vị trí được chèn 1 nop, sau đó IDBypass lo phần còn lại. Bộ đếm khoảng cách chỉ đặt lại
sau jal và jalr, vì lệnh tới bằng một lần nhảy luôn có 2 bubble phía trước. Nhãn thì không được đặt lại, vì lệnh ở nhãn
còn tới được bằng cách chạy tiếp từ lệnh liền trước.

Hai giản đồ là cùng bảy lệnh của t06_hazard.s, sinh tự động từ golden model. Trên pipeline, ba lệnh dùng ngay kết quả
lw mỗi lệnh chờ 1 chu kỳ, ô đỏ là chu kỳ đứng ở ID; lệnh beq nhảy nên hai lệnh xám bị flush. Bảy lệnh chiếm 14 chu kỳ.
Trên NoHazard, mỗi phụ thuộc gần phải chờ bằng nop, kể cả phụ thuộc mà pipeline forward được, nên cùng đoạn chiếm 17 chu
kỳ.

## Slide 22 · Số chu kỳ và CPI trên 12 chương trình
Người nói: Đức Anh · 7:15–8:30

Bảng là số chu kỳ của 12 chương trình trên ba bản. Tổng cộng: đơn chu kỳ 5993, NoHazard 12509, pipeline
9517 chu kỳ. CPI của pipeline trên cả 12 chương trình là 1.59.

CPI cao nhất là 1.67 ở t03_branch.s: chương trình chỉ có 54 lệnh nhưng nhảy 16 lần, nên
32 chu kỳ flush và 4 chu kỳ lấp đầy chiếm tỉ lệ lớn. t09_recursion.s, chương trình dài nhất, có CPI
1.63: 1260 lần nhảy tốn 2520 chu kỳ, gấp hơn 5 lần 464 chu kỳ load-use. Vậy control
hazard là nguồn mất mát lớn nhất. NoHazard có CPI 2.09 tính trên số lệnh gốc, vì phải chạy thêm 3542
lệnh nop, trong khi pipeline chỉ stall 550 chu kỳ.

## Slide 23 · Tăng tốc so với đơn chu kỳ theo giả định trễ
Người nói: Đức Anh · 8:30–9:30

Biểu đồ quy số chu kỳ ra thời gian theo giả định 800 ps cho đơn chu kỳ và 220 ps cho hai bản
pipeline. Tính trên tổng, pipeline nhanh hơn đơn chu kỳ 2.29 lần, NoHazard 1.74 lần, trong khi mức lý
tưởng là 3.64. Với cùng chu kỳ clock, pipeline chạy ít chu kỳ hơn NoHazard 1.31 lần, đó là phần
đóng góp riêng của forwarding và stall bằng phần cứng.

Chưa đạt mức lý tưởng vì hai lý do: CPI lớn hơn 1 do flush và stall, và các tầng không dài bằng nhau, ID và WB chỉ cần
100 ps nhưng vẫn chiếm trọn 220 ps. Thời gian ở đây là giả định; còn số chu kỳ là số chạy thật và đã khớp với
Logisim.

## Slide 24 · Phần mở rộng, hạn chế và hướng phát triển
Người nói: Đức Anh · 9:30–10:30

Ngoài yêu cầu cơ bản, nhóm làm thêm các lệnh tùy chọn, UART và GPIO, forwarding hai nguồn cùng bypass WB về ID, bộ đếm
cycles và instret, Pipeline Monitor, toolchain kiểm thử tự động và bản NoHazard.

Hạn chế lớn nhất là lệnh nhảy quyết định ở EX nên mỗi lần nhảy mất 2 chu kỳ: trên 12 chương trình, flush tốn 2926
chu kỳ, nhiều hơn 550 chu kỳ load-use. CPU chưa có exception, ngắt và CSR nên UART phải hỏi vòng. Truy cập bộ nhớ
lệch không được hỗ trợ, và đích nhảy lệch cũng không bị phát hiện. Vùng I/O chỉ giải mã vài bit địa chỉ nên có địa chỉ
bí danh.

Hướng phát triển xếp theo lợi ích đo được bằng bộ test hiện có. Ưu tiên một là đưa quyết định nhánh lên ID, giảm phạt
từ 2 xuống 1 chu kỳ; trên t09 tiết kiệm tối đa 1260 chu kỳ, trừ các stall mới khi lệnh nhánh phụ thuộc lệnh ngay
trước. Tiếp theo là dự đoán nhánh 2 bit với BTB, phần mở rộng nhân chia, và ngắt cho UART.

Phần trình bày của nhóm em đến đây.

## Slide 25 · Cảm ơn
Người nói: Cả nhóm

Em cảm ơn thầy và các bạn đã lắng nghe. Nhóm em xin nhận câu hỏi.

Câu hỏi về phần nào thì người trình bày phần đó trả lời: Hà phần kiến trúc và module, Công phần đơn chu kỳ và kiểm
thử, Đức Anh phần pipeline và kết quả. Nếu thầy muốn xem demo, nhóm mở Logisim trực tiếp; video dự phòng ở
demo/demo_RV32I_v2.mp4.
