# generator/ — sinh file .circ bằng Python

Các file `.circ` trong `circ/` **không vẽ tay**. Chúng được sinh ra từ mã Python ở đây. Như vậy layout nhất quán, và có thể kiểm tra tự động.

| File | Vai trò |
|---|---|
| `lgen.py` | Thư viện nhỏ: đặt linh kiện, nối dây, tunnel, vẽ appearance của sub-circuit, phát hiện lỗi nối dây (chạm chữ T, chập dây) |
| `modules.py` | Toàn bộ khối: ALU, Control, RegisterFile, ImmGen, Load/Store, Forward, Hazard, thanh ghi pipeline… |
| `cpu_single.py`, `cpu_pipeline.py` | Mạch top-level |
| `build_all.py` | `python3 build_all.py ../circ` sinh lại cả 3 file |
| `refmodels.py`, `mkvec.py` | Mô hình tham chiếu và sinh test vector cho từng module |
| `geometry.json` | Cache vị trí chân của linh kiện Logisim, lấy từ chính Logisim qua `inspect/Inspect.java` |

Chỉ khi thêm loại linh kiện hoặc thuộc tính mới thì mới cần Java helper:
`export LOGISIM_JAR=...; cd inspect && javac -cp $LOGISIM_JAR Inspect.java`.
`Inspect.java` còn có lệnh `lint` (tìm chân hở, tunnel lẻ, xung đột độ rộng) và `render` (xuất ảnh PNG từng mạch).
