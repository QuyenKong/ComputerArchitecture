# Kịch bản 3 phút: chạy demo.s trên CPU đơn chu kỳ

Mục tiêu của 3 phút này là cho thầy thấy hai điều: CPU chạy đúng một chương trình thật, và mình hiểu vì sao mỗi lệnh
xong trong đúng một chu kỳ. Mỗi đoạn dưới đây có: nhìn/chỉ vào đâu, nói gì, và vì sao giá trị như vậy (để trả lời nếu
thầy hỏi, không cần nói ra).

Chi tiết và kiến thức nền nằm trong `HUONG_DAN_DEMO_SC.md`, Phần A.

## Chuẩn bị (trước khi lên)

- Mở `circ/RV32I_SingleCycle.circ`. ROM phải là `demo.s`: sau Ctrl+R, probe `instr` = `00004137`. Nếu không phải thì
  nạp lại `build/demo.text.hex` vào ROM `IMEM`.
- Simulate → Tick Frequency = 4 Hz. Tập trước một lần. Nếu chương trình chạy xong trước khi nói hết đoạn 3–5 thì cứ
  nói tiếp, các giá trị vẫn nằm trên màn hình.
- Zoom sao cho thấy cùng lúc: `PC`, probe `instr`, `Register File` (đọc được nhãn `x10_a0`), RAM `DMEM`, probe
  `WB_data`, TTY và LED ở góc dưới phải, các chân `cycles`, `instret` ở hàng dưới cùng.

## Đoạn 1 (0:00 – 0:25): mạch là gì

Nhìn/chỉ: lướt chuột qua 5 nhãn cột FETCH → WRITE BACK. Chỉ `PC`, ROM `IMEM`, `Register File`, `ALU`, RAM `DMEM`.
Bấm Ctrl+R.

> "Đây là CPU đơn chu kỳ RV32I. Mạch xếp theo 5 bước: lấy lệnh, giải mã và đọc thanh ghi, tính ALU, truy cập bộ nhớ,
> ghi kết quả. Giữa các bước không có thanh ghi ngăn, nên một lệnh đi hết 5 bước trong một chu kỳ clock. Chương trình
> demo.s đã được assembler của nhóm dịch và nạp vào ROM. Sau reset, PC bằng 0, thanh ghi và RAM đều bằng 0, em không
> sửa tay giá trị nào."

Vì sao: chỉ có 3 thứ có trí nhớ là `PC`, `Register File` và RAM, và cả ba chỉ đổi giá trị ở cạnh lên clock. Các khối
còn lại là mạch tổ hợp, tính xong ngay khi đầu vào đổi.

## Đoạn 2 (0:25 – 1:00): một lệnh, một chu kỳ

Đây là đoạn thể hiện hiểu single cycle, nên làm chậm.

Nhìn/chỉ:

1. Chỉ `PC` = 00000000 và probe `instr` = 00004137.
2. Chỉ probe `WB_data` = 00004000, rồi dòng `x2_sp` trong `Register File` vẫn là 00000000.
3. Bấm Ctrl+T tới khi `PC` đổi. Chỉ `PC` = 00000004 và `x2_sp` = 00004000.
4. Chỉ `WB_data` = 00003ff0, bấm Ctrl+T tới khi PC = 00000008. Chỉ `x2_sp` = 00003ff0.

> "Lệnh đầu tiên là `lui sp, 4`. Ngay khi PC bằng 0, cả đường dữ liệu đã tính xong: kết quả 0x4000 có sẵn ở WB_data.
> Nhưng thanh ghi sp vẫn bằng 0, vì Register File chỉ ghi ở cạnh lên. Em bấm một cạnh lên: sp nhận 0x4000 và PC tăng
> lên 4 cùng lúc. Lệnh tiếp theo `addi sp, sp, -16` cũng vậy: sp thành 0x3FF0. Hai lệnh này là lệnh giả `li sp, 0x3FF0`
> do assembler tách ra. Mỗi lệnh một chu kỳ, PC tăng 4 vì mỗi lệnh dài 4 byte."

Vì sao: `lui sp, 4` nạp 4 vào 20 bit cao, tức 4 << 12 = 0x4000. `addi` cộng −16 nên 0x4000 − 0x10 = 0x3FF0, là đỉnh
vùng RAM 16 KiB làm con trỏ ngăn xếp.

## Đoạn 3 (1:00 – 1:40): vòng Fibonacci ghi vào RAM

Nhìn/chỉ: bấm Ctrl+K cho clock tự chạy. Chỉ `PC` quay vòng từ 0x1C tới 0x34 rồi về 0x1C. Chỉ dòng `x8_s0` tăng
0, 4, 8, c... Chỉ RAM `DMEM` hiện dần số mới.

> "CPU vào vòng lặp: PC chạy từ 0x1C tới 0x34 rồi lệnh `bne` đưa nó về 0x1C. Mỗi vòng 7 lệnh, 7 chu kỳ. Lệnh `sw`
> ghi số Fibonacci hiện tại trong t0 vào RAM tại địa chỉ s0. ALU tính địa chỉ, bộ giải mã địa chỉ chia 4 để ra số ô,
> RAM ghi ở cạnh lên. Sau đó s0 tăng 4 để sang ô tiếp theo, vì mỗi ô RAM chứa 4 byte. Dãy hiện trong RAM: 0, 1, 1, 2, 3,
> 5, 8, 0xD..., tới 0x59 là 89."

Vì sao:

- Mảng `fib` bắt đầu ở địa chỉ 0, nên số thứ n nằm ở địa chỉ 4n, tức ô n.
- 12 số chiếm ô 0 đến ô 11. RAM hiện mỗi dòng 2 ô, nên chúng nằm ở dòng 000 đến 00a.
- Các số là F(0) đến F(11) = 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89. Viết hex: 0, 1, 1, 2, 3, 5, 8, d, 15, 22, 37, 59.

## Đoạn 4 (1:40 – 2:10): đọc lại RAM, cộng vào a0

Nhìn/chỉ: khi PC rời khoảng 0x1C – 0x34, chỉ dòng `x10_a0` (cột trái, dòng 11) tăng dần, và dòng `x29_t4` (cột
phải, dòng 14) đổi theo từng số đọc ra.

> "Vòng thứ hai đọc lại từng ô RAM bằng lệnh `lw` vào t4, rồi cộng dồn vào a0. a0 là thanh ghi x10, theo quy ước dùng
> cho giá trị trả về. Tổng 12 số là 232, tức 0xE8. Vì a0 cộng từ dữ liệu đọc lại trong RAM, ra đúng 0xE8 nghĩa là cả
> lệnh ghi lẫn lệnh đọc bộ nhớ đều đúng."

Vì sao: 0+1+1+2+3+5+8+13+21+34+55+89 = 232, và 232 = 14 × 16 + 8 = 0xE8. a0 sau từng vòng: 1, 2, 4, 7, c, 14, 21, 36,
58, 8f, e8.

## Đoạn 5 (2:10 – 2:35): in ra TTY và LED

Nhìn/chỉ: TTY ở góc dưới phải hiện từng chữ `Hello RISC-V!`. Sau đó chỉ 4 LED 7 đoạn hiện `00E8` và 8 LED sáng.

> "Phần này là mở rộng GPIO/UART. CPU không có lệnh in riêng: TTY được gắn vào địa chỉ 0xF0000000. Lệnh `sb` ghi mã
> ASCII vào địa chỉ đó. Bộ giải mã địa chỉ thấy 4 bit cao bằng F nên chuyển lệnh ghi sang khối I/O thay vì RAM. Lệnh
> vẫn chạy trong một chu kỳ như mọi lệnh store khác. Cuối cùng chương trình ghi a0 ra thanh ghi GPIO, nên LED hiện
> 00E8."

Vì sao: 72 là 'H', 101 là 'e'... theo bảng ASCII. Ghi vào 0xF0000010 là GPIO_OUT: bit 15:0 nối 4 LED 7 đoạn, bit
23:16 nối 8 LED (`sb 0xFF` vào byte 2).

## Đoạn 6 (2:35 – 3:00): dừng và kết luận

Nhìn/chỉ: chân `halt` = 1, `PC` đứng ở 000000e0. Bấm Ctrl+K tắt clock. Chỉ `cycles` và `instret` cùng bằng 000000bc.

> "Lệnh cuối là `ebreak`, Control bật Halt nên PC dừng ở 0xE0. Hai bộ đếm cycles và instret cùng bằng 0xBC, tức 188:
> 188 lệnh trong 188 chu kỳ, CPI bằng 1. Đó là tính chất của CPU đơn chu kỳ. Cái giá phải trả là chu kỳ clock phải đủ
> dài cho lệnh chậm nhất là `lw`, lệnh đi qua cả ROM, Register File, ALU, RAM rồi quay lại Register File. Phần tiếp
> theo em sẽ đi chi tiết lệnh `lw` đó."

Vì sao 188 lệnh (ROM chỉ có 57 lệnh, nhưng vòng lặp chạy lại nhiều lần):

| Đoạn | Số lệnh chạy |
|---|---|
| khởi tạo | 7 |
| vòng Fibonacci | 12 × 7 = 84 |
| chuẩn bị vòng tổng | 4 |
| vòng tổng | 12 × 5 = 60 |
| in 14 ký tự | 2 + 14 × 2 = 30 |
| GPIO | 3 |
| cộng | 188 (`ebreak` không tính vì CPU dừng ở đó) |

## Nếu thầy ngắt lời hỏi

| Câu hỏi | Trả lời ngắn |
|---|---|
| Sao sp vẫn bằng 0 khi WB_data đã là 0x4000? | Register File là phần tử nhớ, chỉ ghi ở cạnh lên clock. Trước cạnh lên, giá trị mới chỉ nằm trên dây. |
| Sao PC tăng 4 mà không tăng 1? | Địa chỉ tính theo byte, mỗi lệnh 4 byte. ROM lấy PC chia 4 làm số ô. |
| Sao s0 tăng 4? | Mỗi số Fibonacci là một word 4 byte, s0 là địa chỉ byte. |
| In TTY có phải là single cycle không? | TTY là thiết bị ngoại vi tùy chọn. Lệnh `sb` ghi ra TTY vẫn chạy trong một chu kỳ, chỉ khác là ghi vào khối I/O thay vì RAM. |
| Sao run_tests báo 220 chu kỳ? | Runner nối thêm đoạn code dump thanh ghi ra RAM (32 lệnh) để so sánh. Trong GUI là 188, khớp mô hình tham chiếu `rvsim.py`. |
