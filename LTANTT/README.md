# Lập Trình An Toàn Thông Tin (LTANTT)

Kho lưu trữ bài tập, báo cáo thực hành, đồ án và chuyên đề thuyết trình môn **Lập trình An toàn Thông tin** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Lớp:** 23DATA1
* **Ngôn ngữ & Công cụ:** Python 3.x, Flask, Docker, Kali Linux, Nmap, Metasploit Framework, Visual Studio Code.

---

## Danh Mục Học Phần & Cấu Trúc Thư Mục

`	ext
LTANTT/
├── lab1/                              # Lab 1: Lập trình Python căn bản & giải thuật mật mã cơ bản
├── lab2/                              # Lab 2: Lập trình Socket Mạng TCP & Hàm băm bảo mật (MD5/SHA-256)
├── lab 3/                             # Lab 3: Rà quét mạng Nmap & Mô hình săn tìm mối đe dọa với Metasploit
├── Thuyet Trinh/                      # Chuyên đề: Phát hiện đăng nhập bất thường dựa trên hành vi người dùng (UBA)
└── đồ án cuối kỳ LTANTT/              # Đồ án cuối kỳ: CertGuard - Quản lý và kiểm tra chứng thư số SSL/TLS
`

---

## Chi Tiết Các Nội Dung

### 1. lab1 (Lab 1: Lập trình Python căn bản trong An toàn thông tin)
* Các bài tập thực hành Python từ cơ bản đến nâng cao (x02_01.py đến x02_10.py):
  * Xử lý chuỗi, mã hóa ký tự đơn giản (Caesar cipher, mã hóa thay thế).
  * Xử lý cấu trúc dữ liệu: List, Dictionary, Tuple phục vụ lưu trữ thông tin đối tượng.
  * Đọc/ghi tệp tin, chuẩn hóa dữ liệu.
* Báo cáo thực hành chi tiết: Lab 1.docx.

### 2. lab2 (Lab 2: Lập trình Socket Mạng & Hàm Băm Mật Mã)
* 	cp_server.py & 	cp_client.py: Lập trình ứng dụng truyền nhận dữ liệu qua giao thức TCP Socket.
* port_scanner.py: Xây dựng công cụ rà quét cổng mạng (Port Scanner) đa luồng để kiểm tra trạng thái mở/đóng của các dịch vụ mạng.
* hashing_basics.py: Ứng dụng các thuật toán hàm băm bảo mật (MD5, SHA-256) kiểm tra tính toàn vẹn của tệp văn bản (sample.txt).
* Báo cáo thực hành chi tiết: TranTangTruongThinh_2387701939.docx.

### 3. lab 3 (Lab 3: Mô hình hóa & Săn tìm Mối đe dọa Mạng - Threat Hunting)
* **Báo cáo toàn văn:** TranTangTruongThinh_1939_Lab3.docx.
* **Nội dung thực nghiệm:**
  * Thu thập thông tin mạng trên Kali Linux: kiểm tra địa chỉ IP và bảng định tuyến (Routing table).
  * Rà quét dịch vụ mạng bằng Nmap: phát hiện các cổng mở (80/HTTP, 443/HTTPS chạy Apache trên Debian Linux).
  * Khai thác lỗ hổng bảo mật với **Metasploit Framework** (msfconsole): tìm kiếm module khai thác SMB (search smb), thử nghiệm tấn công lỗ hổng MS17-010 (EternalBlue) trên máy mục tiêu và đánh giá khả năng tạo phiên Meterpreter.

### 4. Thuyet Trinh (Báo Cáo Chuyên Đề: Phát Hiện Đăng Nhập Bất Thường Dựa Trên Hành Vi Người Dùng)
* **Tài liệu:** Slide thuyết trình (.pptx, .pdf) và video kịch bản thực nghiệm (demo.mp4).
* **Trọng tâm đề tài:** Ứng dụng mô hình phân tích hành vi người dùng (UBA/UEBA), chấm điểm rủi ro phiên đăng nhập (IP, thiết bị, thời gian) và cơ chế xác thực tương thích (Adaptive Authentication) phòng chống tấn công dò mật khẩu và chiếm quyền tài khoản.

### 5. đồ án cuối kỳ LTANTT (Đề Tài Cuối Kỳ: CertGuard - Quản Lý & Kiểm Tra Chứng Thư Số SSL/TLS)
* **Mã nguồn:** Hệ thống kiểm tra & giám sát SSL/TLS tự động viết bằng Python/Flask (certguard/) đi kèm cụm Web Server mô phỏng các kịch bản lỗi SSL trên Docker (certguard-webservers/).
* **Tài liệu:** Báo cáo toàn văn (.docx, .pdf), Slide thuyết trình (.pptx), Phân công công việc và Video báo cáo demo hoàn chỉnh.
