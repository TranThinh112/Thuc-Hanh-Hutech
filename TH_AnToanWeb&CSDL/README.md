# Thực Hành An Toàn Web & Cơ Sở Dữ Liệu

Thư mục lưu trữ các báo cáo bài tập thực hành (Lab Reports) môn học **An toàn Web và Cơ sở dữ liệu** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Môi trường & Công cụ thực hành:** Kali Linux, Windows Server / Desktop, OWASP WebGoat, Burp Suite, Wireshark, SQLMap, cURL, Python 3, iptables, iptstate, Apache/PHP/MySQL.

---

## Chi Tiết Các Bài Thực Hành (Labs)

### 1. `BÀI 1.pdf`: Công Cụ WebGoat & Burp Suite
* **Nội dung chính:**
  * Giới thiệu nền tảng kiểm thử bảo mật ứng dụng WebGoat do OWASP phát triển.
  * Cài đặt và thiết lập proxy trung gian với Burp Suite:
    * Cấu hình Network Proxy trên trình duyệt trỏ về Burp Suite (`127.0.0.1:8080`).
    * Sử dụng tính năng **Intercept** để bắt giữ, phân tích cấu trúc HTTP Request/Response và chỉnh sửa tham số trước khi gửi đến máy chủ.
  * Nhập môn phương pháp kiểm thử xâm nhập (Penetration Testing) ứng dụng Web.

### 2. `Bài 2.pdf`: Sessions, HTTPS & reCAPTCHA
* **Nội dung chính:**
  * **HTTPS & SSL/TLS:** Thiết lập chứng chỉ số, mã hóa kênh truyền bảo vệ tính bảo mật và toàn vẹn của dữ liệu giữa máy trạm và máy chủ.
  * **Session Management:** Cơ chế lưu trữ và quản lý phiên làm việc người dùng qua Cookie / Session ID; phân tích các nguy cơ tấn công như Session Hijacking (chiếm quyền điều khiển phiên) và Session Fixation.
  * **Chống Tấn Công Tự Động:** Tích hợp cơ chế reCAPTCHA để phòng chống tấn công dò mật khẩu (Brute-force) và từ chối dịch vụ tầng ứng dụng (Application DoS).
  * Thực nghiệm kết nối và phân tích lưu lượng giữa máy trạm mục tiêu và máy kiểm thử Kali Linux.

### 3. `TranTangTruongThinh_2387701939_Lab3.pdf`: Command Injection & SQL Injection
* **Nội dung chính:**
  * **OS Command Injection (Chèn lệnh hệ điều hành):**
    * Cơ chế phát sinh lỗ hổng khi ứng dụng truyền trực tiếp chuỗi nhập liệu người dùng vào các hàm thực thi hệ thống (`system()`, `exec()`, `shell_exec()`).
    * Khai thác qua các ký tự nối lệnh (`&&`, `;`, `|`) để đọc tệp hệ thống và thực thi shell tùy ý.
  * **SQL Injection (SQLi - Chèn truy vấn cơ sở dữ liệu):**
    * Khai thác câu truy vấn SQL không được tham số hóa để vượt qua xác thực đăng nhập (Authentication Bypass: `' OR 1=1 --`).
    * Trích xuất thông tin người dùng, mật khẩu đã băm từ cơ sở dữ liệu.
  * **Biện pháp phòng ngừa:** Sử dụng Prepared Statements (Parameterized Queries), ORM và kiểm duyệt dữ liệu đầu vào (Input Validation & Whitelisting).

### 4. `TranTangTruongThinh_2387701939_Lab4.pdf`: Xác Minh, Khai Thác Lỗ Hổng PHP & XSS
* **Nội dung chính:**
  * **Khai thác lỗ hổng ứng dụng PHP:**
    * Lỗ hổng tải lên tệp tin không kiểm soát (Unrestricted File Upload) để tải Web Shell lên máy chủ.
    * Lỗ hổng nhúng file cục bộ/từ xa (Local/Remote File Inclusion - LFI/RFI).
  * **Cross-Site Scripting (XSS - Chèn mã kịch bản độc hại):**
    * Phân tích các dạng tấn công XSS: Reflected XSS, Stored XSS và DOM-based XSS.
    * Khai thác chèn mã JavaScript đánh cắp Cookie phiên (`document.cookie`) và chuyển hướng độc hại.
  * **Biện pháp phòng ngừa:** Mã hóa đầu ra (Contextual Output Encoding), cấu hình cờ `HttpOnly`, `Secure` cho Cookie và áp dụng Content Security Policy (CSP).

### 5. `TranTangTruongThinh_2387701939_Lab5.pdf`: Khai Thác Lỗ Hổng CSRF
* **Nội dung chính:**
  * **Cơ chế tấn công Cross-Site Request Forgery (CSRF):** Lợi dụng quyền xác thực của người dùng trên trình duyệt để ép buộc thực thi các yêu cầu trái phép.
  * **Thực nghiệm tấn công:**
    * Bắt gói tin HTTP chứa cookie phiên của nạn nhân bằng Wireshark.
    * Tái lập yêu cầu (Replay Request) qua công cụ cURL (`-H "Cookie: AUTH=..."`) để chiếm phiên làm việc mà không cần mật khẩu.
    * Khai thác kịch bản CSRF trên môi trường thực hành AttackDirect.
  * **Biện pháp phòng ngừa:** Sử dụng Anti-CSRF Token ngẫu nhiên cho mỗi phiên/biểu mẫu, cấu hình thuộc tính `SameSite` (Strict/Lax) cho Cookie và kiểm tra trường `Origin` / `Referer`.

### 6. `Lab 6 26_10_26/`: Bảo Vệ Máy Chủ và Tự Động Hóa Các Yêu Cầu Web
* **Thư mục:** `Lab 6 26_10_26/` (gồm báo cáo `TranTangTruongThinh_2387701939_Lab6.pdf`, `TranTangTruongThinh_2387701939_Lab6.docx`).
* **Nội dung chính:**
  * **Phần 1 - Bảo vệ máy chủ bằng Firewall (`iptables` & `iptstate`):**
    * Thiết lập mô hình 2 máy ảo Linux (Máy A - Server và Máy B - Client/Attacker).
    * Khởi tạo chuỗi quy tắc tường lửa tùy biến (`LAB06_IN`), kiểm soát gói tin TCP/UDP theo trạng thái kết nối và cờ TCP (`SYN`, `ACK`, `FIN`, `RST`).
    * Theo dõi bảng trạng thái kết nối thời gian thực qua công cụ `iptstate` khi thiết lập phiên Netcat (`nc`).
  * **Phần 2 - Tự động hóa kiểm thử Web bằng Python:**
    * Bắt và phân tích cấu trúc HTTP POST request (`/blind2.php`) trên DevTools Network tab của trình duyệt.
    * Lập trình script Python (`urllib.request`) tự động gửi payload kiểm tra lỗ hổng **Time-Based Blind Command Injection**.
    * Đo đạc thời gian phản hồi (`time.perf_counter()`), đối chiếu độ trễ và kết quả phản hồi giữa trình duyệt và script Python.
