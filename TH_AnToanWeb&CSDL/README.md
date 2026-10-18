# Thực Hành An Toàn Web & Cơ Sở Dữ Liệu

Thư mục lưu trữ các báo cáo bài tập thực hành (Lab Reports) môn học **An toàn Web và Cơ sở dữ liệu** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Môi trường & Công cụ thực hành:** Kali Linux, Windows Server / Desktop, OWASP WebGoat, Burp Suite, Wireshark, SQLMap, Apache/PHP/MySQL.

---

## Chi Tiết Các Bài Thực Hành (Labs)

### 1. `BÀI 1.pdf`: Công Cụ WebGoat & Burp Suite
* **Nội dung chính:**
  * Giới thiệu nền tảng ứng dụng kiểm thử bảo mật WebGoat do OWASP phát triển.
  * Cài đặt và thiết lập proxy trung gian với Burp Suite:
    * Cấu hình Network Proxy trên trình duyệt trỏ về Burp Suite (`127.0.0.1:8080`).
    * Sử dụng tính năng **Intercept** để bắt giữ (sniff), phân tích cấu trúc HTTP Request/Response và chỉnh sửa tham số trước khi gửi đến máy chủ.
  * Nhập môn phương pháp kiểm thử xâm nhập (Penetration Testing) ứng dụng Web.

### 2. `Bài 2.pdf`: Sessions, HTTPS & reCAPTCHA
* **Nội dung chính:**
  * **HTTPS & SSL/TLS:** Thiết lập chứng chỉ số, mã hóa kênh truyền bảo vệ tính bảo mật và toàn vẹn của dữ liệu truyền tải giữa máy trạm và máy chủ.
  * **Session Management:** Cơ chế lưu trữ và quản lý phiên làm việc người dùng qua Cookie / Session ID; phân tích các nguy cơ tấn công như Session Hijacking (chiếm quyền điều khiển phiên) và Session Fixation.
  * **Chống Tấn Công Tự Động:** Tích hợp cơ chế reCAPTCHA để phòng chống tấn công dò mật khẩu (Brute-force) và từ chối dịch vụ tầng ứng dụng (Application DoS).
  * Thực nghiệm kết nối và phân tích lưu lượng giữa máy trạm mục tiêu và máy kiểm thử Kali Linux.

### 3. `TranTangTruongThinh_2387701939_Lab3.pdf`: Command Injection & SQL Injection
* **Nội dung chính:**
  * **OS Command Injection (Chèn lệnh hệ thống):**
    * Cơ chế xuất hiện lỗ hổng khi ứng dụng truyền trực tiếp chuỗi nhập liệu của người dùng vào các hàm gọi thực thi hệ điều hành (`system()`, `exec()`, `shell_exec()`).
    * Khai thác qua các ký tự nối lệnh (`&&`, `;`, `|`) để đọc file hệ thống, thực thi shell tùy ý.
  * **SQL Injection (SQLi - Chèn truy vấn cơ sở dữ liệu):**
    * Khai thác câu truy vấn SQL không được tham số hóa để vượt qua màn hình đăng nhập (Authentication Bypass: `' OR 1=1 --`).
    * Trích xuất thông tin người dùng, mật khẩu đã băm từ cơ sở dữ liệu.
  * **Biện pháp phòng ngừa:**
    * Sử dụng Prepared Statements (Parameterized Queries) và ORM.
    * Xác thực và kiểm duyệt chặt chẽ dữ liệu đầu vào (Input Validation & Whitelisting).

### 4. `TranTangTruongThinh_2387701939_Lab4.pdf`: Xác Minh, Khai Thác Lỗ Hổng PHP & XSS
* **Nội dung chính:**
  * **Khai thác lỗ hổng ứng dụng PHP:**
    * Tìm kiếm và khai thác lỗ hổng tải lên tệp tin không kiểm soát (Unrestricted File Upload) để tải Web Shell lên máy chủ.
    * Lỗ hổng nhúng file cục bộ/từ xa (Local/Remote File Inclusion - LFI/RFI).
  * **Cross-Site Scripting (XSS - Chèn mã kịch bản độc hại):**
    * Phân tích các dạng tấn công XSS: Reflected XSS, Stored XSS và DOM-based XSS.
    * Kịch bản chèn mã JavaScript đánh cắp Cookie phiên người dùng (`document.cookie`) và chuyển hướng người dùng đến trang giả mạo.
  * **Biện pháp phòng ngừa:**
    * Mã hóa dữ liệu đầu ra phù hợp ngữ cảnh (Contextual Output Encoding: HTML, JavaScript, URL encoding).
    * Bật cờ `HttpOnly` và `Secure` cho Session Cookie.
    * Cấu hình Content Security Policy (CSP).