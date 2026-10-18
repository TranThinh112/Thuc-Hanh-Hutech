# Lập Trình An Toàn Thông Tin (LTANTT)

Kho lưu trữ bài tập và báo cáo thực hành môn **Lập trình An toàn Thông tin** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Ngôn ngữ & Công cụ:** Python 3.x, Kali Linux, Nmap, Metasploit Framework, Visual Studio Code.

---

## Nội Dung Các Bài Thực Hành (Labs)

### 1. `lab1` (Lab 1: Lập trình Python căn bản trong An toàn thông tin)
* Các bài tập thực hành Python từ cơ bản đến nâng cao (`ex02_01.py` đến `ex02_10.py`):
  * Xử lý chuỗi, mã hóa ký tự đơn giản (Caesar cipher, mã hóa thay thế).
  * Xử lý cấu trúc dữ liệu: List, Dictionary, Tuple phục vụ lưu trữ thông tin đối tượng.
  * Đọc/ghi tệp tin, chuẩn hóa dữ liệu.
* Báo cáo thực hành chi tiết: `Lab 1.docx`.

### 2. `lab2` (Lab 2: Lập trình Socket Mạng & Hàm Băm Mật Mã)
* `tcp_server.py` & `tcp_client.py`: Lập trình ứng dụng truyền nhận dữ liệu qua giao thức TCP Socket.
* `port_scanner.py`: Xây dựng công cụ rà quét cổng mạng (Port Scanner) đa luồng để kiểm tra trạng thái mở/đóng của các dịch vụ mạng.
* `hashing_basics.py`: Ứng dụng các thuật toán hàm băm bảo mật (MD5, SHA-256) kiểm tra tính toàn vẹn của tệp văn bản (`sample.txt`).
* Báo cáo thực hành chi tiết: `TranTangTruongThinh_2387701939.docx`.

### 3. `lab 3` (Lab 3: Mô hình hóa & Săn tìm Mối đe dọa Mạng - Threat Hunting)
* **Báo cáo toàn văn:** `TranTangTruongThinh_1939_Lab3.docx`.
* **Nội dung thực nghiệm:**
  * Thu thập thông tin mạng trên Kali Linux: kiểm tra địa chỉ IP và bảng định tuyến (Routing table).
  * Rà quét dịch vụ mạng bằng Nmap: phát hiện các cổng mở (80/HTTP, 443/HTTPS chạy Apache trên Debian Linux).
  * Khai thác lỗ hổng bảo mật với **Metasploit Framework** (`msfconsole`): tìm kiếm module khai thác SMB (`search smb`), thử nghiệm tấn công lỗ hổng MS17-010 (EternalBlue) trên máy mục tiêu và đánh giá khả năng tạo phiên Meterpreter.
