# BÀI THỰC HÀNH 9: ĐÁNH GIÁ AN TOÀN THÔNG TIN ỨNG DỤNG WEB

Dự án thực hành đánh giá an toàn thông tin (Security Assessment / Penetration Testing) cho ứng dụng web theo chuẩn **OWASP Top 10**, bao gồm môi trường lab mục tiêu, kịch bản khai thác tự động (PoC), bộ ảnh chụp bằng chứng và báo cáo hoàn chỉnh định dạng Word (`.docx`).

---

## 📁 Cấu Trúc Thư Mục

```text
Bai 9/
├── app/
│   ├── server.js              # Mã nguồn ứng dụng web lab mục tiêu (Node.js + Express + SQLite)
│   ├── test_poc.py            # Kịch bản Python tự động kiểm thử và khai thác PoC
│   ├── package.json           # Danh sách thư viện phụ thuộc của ứng dụng
│   └── package-lock.json
│
├── screenshots/               # Bộ ảnh chụp minh chứng khai thác (Proof of Concept)
│   ├── 01_trang_chu.png       # Giao diện chính của ứng dụng
│   ├── 02_sqli_login_input.png # Chèn payload SQLi vào form Login
│   ├── 03_sqli_login_success.png # Bypass đăng nhập thành công vào tài khoản Admin
│   ├── 04_sqli_union_leak.png # Khai thác UNION SQLi trích xuất toàn bộ Database
│   ├── 05_reflected_xss.png   # Kích hoạt mã độc Reflected XSS
│   ├── 06_stored_xss_list.png # Mã độc Stored XSS lưu vĩnh viễn trong CSDL
│   ├── 07_idor_profile_id2.png# Khai thác IDOR xem hồ sơ người dùng khác
│   ├── 08_admin_403_forbidden.png # Trang Admin từ chối truy cập thường (403)
│   └── 09_admin_bypass_header.png # Leo thang đặc quyền Admin qua HTTP Header
│
├── reports/
│   └── BAO_CAO_DANH_GIA_AN_TOAN_THONG_TIN.md # Bản thảo báo cáo dạng Markdown
│
├── Bai 9.docx                 # BÁO CÁO CHÍNH THỨC (Word hoàn chỉnh kèm đầy đủ hình ảnh)
├── HUONG_DAN_THUC_HANH.md     # Hướng dẫn chi tiết các bước thực hành với Burp Suite
├── capture.py                 # Script tự động chụp màn hình giao diện bằng Playwright
├── make_docx.py               # Script tự động định dạng và xuất báo cáo Word
└── README.md                  # Tài liệu hướng dẫn tổng quan dự án
```

---

## 🎯 Mục Tiêu Đánh Giá

1. **Thực hành quy trình kiểm thử xâm nhập (Penetration Testing):** Từ bước trinh sát (Reconnaissance), thu thập thông tin tham số đến khai thác điểm yếu.
2. **Phát hiện các lỗ hổng phổ biến theo OWASP:**
   - **SQL Injection (SQLi):** Bypass Authentication và UNION-based Data Disclosure.
   - **Cross-Site Scripting (XSS):** Reflected XSS trên URL và Stored XSS trong database.
   - **Broken Access Control (IDOR):** Xem trái phép thông tin cá nhân của tài khoản khác qua tham số `?id=`.
   - **Privilege Escalation:** Vượt cơ chế kiểm tra quyền truy cập vào bảng quản trị `/admin`.
   - **Broken Authentication / Insecure Session:** Lộ plaintext password, thiếu cờ cookie an toàn (`HttpOnly`, `Secure`, `SameSite`).
3. **Đề xuất biện pháp phòng vệ & khắc phục:** Áp dụng Prepared Statements, HTML Entity Encoding, Role-Based Access Control (RBAC), Hashing mật khẩu bằng Bcrypt/Argon2.

---

## 🚀 Hướng Dẫn Cài Đặt & Vận Hành

### 1. Yêu cầu hệ thống
- **Node.js** (v18 trở lên)
- **Python** (v3.10 trở lên)
- **Trình duyệt web** (Google Chrome, Microsoft Edge, Firefox)
- *(Tùy chọn)* **Burp Suite Community Edition** hoặc **OWASP ZAP**

### 2. Khởi chạy Ứng dụng Web Lab
Mở PowerShell tại thư mục dự án và thực hiện:
```powershell
cd "C:\Users\Admin\Downloads\Bai 9\app"
node server.js
```
Ứng dụng sẽ hoạt động tại địa chỉ: **`http://localhost:3000`**

### 3. Chạy Kịch bản Kiểm thử Tự động (PoC)
Mở một cửa sổ Terminal khác:
```powershell
cd "C:\Users\Admin\Downloads\Bai 9\app"
$env:PYTHONIOENCODING="utf-8"
python test_poc.py
```
Toàn bộ quy trình kiểm thử 5 loại lỗ hổng sẽ được thực thi tự động và hiển thị kết quả xác nhận.

---

## 🛠️ Hướng Dẫn Kiểm Thử Thủ Công Nhanh

| Chức năng | URL kiểm thử | Payload / Thao tác | Hiện tượng xác nhận lỗ hổng |
|---|---|---|---|
| **SQLi Login** | `/login` | `username`: `admin' --`<br>`password`: bất kỳ | Đăng nhập thẳng vào tài khoản `admin` không cần mật khẩu |
| **SQLi UNION** | `/products` | `' UNION SELECT id, username, password, role FROM users --` | Bảng sản phẩm lộ toàn bộ mật khẩu tài khoản hệ thống |
| **Reflected XSS** | `/products` | `<script>alert('Reflected-XSS')</script>` | Trình duyệt thực thi script trực tiếp trên kết quả tìm kiếm |
| **Stored XSS** | `/feedback` | Nội dung: `<script>alert(document.cookie)</script>` | Script được lưu vào CSDL và tự chạy mỗi khi xem phản hồi |
| **IDOR** | `/profile` | Đổi `?id=1`, `?id=2`, `?id=3` | Xem được toàn bộ thông tin nhạy cảm của người dùng khác |
| **Bypass Admin** | `/admin` | Thêm Header: `X-Role-Override: admin` | Vượt qua mã chặn 403, mở toàn quyền quản trị hệ thống |

---

## 📄 Báo Cáo Kết Quả Thực Hành

File nộp bài chính thức đã được định dạng chuẩn chỉnh tại:
👉 **`Bai 9.docx`**

- Có bảng tổng hợp phân loại rủi ro theo CVSS v3.1 và danh mục OWASP.
- Đã chèn đầy đủ **9 ảnh chụp thực tế** từng bước khai thác.
- Cung cấp mã nguồn minh họa nguyên nhân lỗi và đoạn code sửa chữa tương ứng.

---
*Dự án phục vụ mục đích học tập và nghiên cứu an toàn thông tin.*
