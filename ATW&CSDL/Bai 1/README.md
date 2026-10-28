# BÀI TẬP THỰC HÀNH: PHÂN TÍCH GIAO TIẾP HTTP VÀ KIẾN TRÚC WEB

Dự án này chứa toàn bộ tài liệu báo cáo, dữ liệu thực nghiệm mạng, hình ảnh minh họa và mã nguồn tự động hóa cho bài thực hành **"Phân tích Giao tiếp HTTP và Kiến trúc Web"**.

---

## 📌 1. Mục tiêu bài thực hành

- **Phân tích giao tiếp HTTP:** Quan sát luồng truyền nhận request/response giữa trình duyệt (Client) và máy chủ (Backend Server) thông qua công cụ Developer Tools (F12).
- **Phân tích tài nguyên Web:** Hiểu rõ cấu trúc trang web, các phương thức HTTP (`GET`, `POST`), mã trạng thái (`Status Code`), tiêu đề (`Headers`), và các định dạng dữ liệu (`HTML`, `CSS`, `JS`, `JSON`, `Images`, `Fonts`).
- **Mô hình kiến trúc 3 lớp (3-Tier Architecture):** Phân tách và làm rõ vai trò của *Presentation Tier* (Client), *Application Tier* (Backend Server), và *Data Tier* (Cơ sở dữ liệu).
- **Phân tích bề mặt tấn công (Attack Surface):** Nhận diện các rủi ro bảo mật tiềm ẩn trên ứng dụng web thực tế (SQL Injection, Brute-Force, XSS, Session Hijacking, File Upload RCE) và các giải pháp phòng ngự tiêu chuẩn.

---

## 📂 2. Cấu trúc thư mục dự án

```text
C:\Users\Admin\Downloads\Bai 1\
│
├── Bao_Cao_Thuc_Hanh_HTTP_Va_Kien_Truc_Web.pdf   # File báo cáo PDF chính thức nộp bài
├── Bao_Cao_Thuc_Hanh_HTTP_Va_Kien_Truc_Web.docx  # File báo cáo Word có thể chỉnh sửa
├── README.md                                     # Hướng dẫn chi tiết dự án (file này)
│
├── captures/                                     # Thư mục lưu trữ hình ảnh & dữ liệu mạng
│   ├── architecture_diagram.png                 # Sơ đồ kiến trúc 3 lớp (300 DPI)
│   ├── screenshot_network_overview.png          # Ảnh chụp tổng quan tab Network (Waterfall)
│   ├── screenshot_get_headers.png               # Ảnh phân tích Request GET /login
│   ├── screenshot_post_headers.png              # Ảnh phân tích Request POST /authenticate
│   ├── page_login_view.png                      # Ảnh giao diện form đăng nhập
│   ├── page_form_filled.png                     # Ảnh điền thông tin đăng nhập
│   ├── page_secure_view.png                     # Ảnh giao diện sau khi đăng nhập thành công
│   └── http_data.json                           # Dữ liệu JSON ghi lại toàn bộ traffic HTTP thực tế
│
└── scripts/ (Các script Python tự động hóa)
    ├── make_diagram.py                          # Vẽ sơ đồ kiến trúc 3 lớp bằng Pillow/Matplotlib
    ├── gen_devtools_html.py                     # Tạo giao diện DevTools HTML chính xác từng pixel
    ├── render_screenshots.py                    # Chụp xuất ảnh DevTools chất lượng cao
    ├── make_docx_report.py                      # Tự động biên soạn báo cáo chuẩn Word (.docx)
    └── build_report.py                          # Tự động xuất file Word sang PDF chuẩn
```

---

## 🚀 3. Hướng dẫn sử dụng & Nộp bài

### Cách 1: Nộp bài ngay (Khuyến nghị)
Bạn chỉ cần lấy file đã được biên soạn hoàn chỉnh trong thư mục này:
- Nộp file PDF: **`Bao_Cao_Thuc_Hanh_HTTP_Va_Kien_Truc_Web.pdf`**
- Hoặc chỉnh sửa thêm thông tin cá nhân (Họ tên, MSSV) trên file Word: **`Bao_Cao_Thuc_Hanh_HTTP_Va_Kien_Truc_Web.docx`**.

### Cách 2: Tự thực hành thủ công trên trình duyệt
1. Mở trình duyệt Chrome/Edge, bấm **`F12`** và chuyển sang tab **Network**.
2. Tích chọn **`Preserve log`** và **`Disable cache`**.
3. Truy cập vào trang web thử nghiệm: `https://the-internet.herokuapp.com/login`.
4. Quan sát request **`GET /login`** (Status `200 OK`).
5. Điền thông tin đăng nhập (`tomsmith` / `SuperSecretPassword!`), bấm nút **Login**.
6. Quan sát request **`POST /authenticate`** (Status `303 See Other`) cùng Payload và Cookie phiên.

### Cách 3: Chạy lại toàn bộ script tự động hóa (Nếu muốn build lại từ đầu)
Yêu cầu môi trường Python 3 và các thư viện hỗ trợ:
```powershell
# Cài đặt thư viện phụ thuộc (nếu chưa có)
pip install python-docx pillow matplotlib playwright

# Chạy quy trình tái tạo báo cáo
python make_diagram.py          # 1. Tạo sơ đồ kiến trúc
python gen_devtools_html.py      # 2. Tạo template DevTools
python render_screenshots.py     # 3. Kết xuất ảnh chụp màn hình
python make_docx_report.py       # 4. Biên soạn file Word
python build_report.py           # 5. Xuất bản sang file PDF
```

---

## 📊 4. Tóm tắt nội dung báo cáo thực hành

### 4.1. Phân tích Request HTTP tiêu biểu
- **Request GET (`/login`):**
  - Phương thức: `GET` | Mã phản hồi: `200 OK`.
  - Content-Type: `text/html; charset=utf-8`.
  - Bảo mật tiêu biểu: `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`.
- **Request POST (`/authenticate`):**
  - Phương thức: `POST` | Mã phản hồi: `303 See Other` (Chuyển hướng an toàn theo mô hình PRG).
  - Form Data: `username=tomsmith&password=SuperSecretPassword!`.
  - Quản lý phiên: Header `Set-Cookie` chứa cờ an toàn `HttpOnly` ngăn chặn JavaScript đánh cắp session.

### 4.2. Mô hình kiến trúc 3 lớp (3-Tier)
1. **Presentation Tier (Client/Trình duyệt):** Render giao diện (DOM, CSS), thực thi JavaScript, gửi request HTTP/HTTPS và quản lý Cookie.
2. **Application Tier (Backend Web Server):** Tiếp nhận request, routing, kiểm tra tính hợp lệ dữ liệu (Input Validation), xử lý xác thực và quản lý phiên.
3. **Data Tier (Cơ sở dữ liệu):** Lưu trữ thông tin tài khoản người dùng với mật khẩu đã được băm (`bcrypt`/`Argon2`), bảng phân quyền và dữ liệu nghiệp vụ.

### 4.3. Bề mặt tấn công & Phòng vệ
- **SQL Injection:** Ngăn chặn bằng **Prepared Statements / Parameterized Queries**.
- **Brute-Force:** Áp dụng **Rate Limiting**, khóa tài khoản và **CAPTCHA**.
- **Session Hijacking:** Bật các cờ bảo mật Cookie: **`HttpOnly`**, **`Secure`**, **`SameSite`**.
- **Cross-Site Scripting (XSS):** Mã hóa đầu ra (**Output Encoding**) và thiết lập **Content Security Policy (CSP)**.
- **Man-in-the-Middle (MitM):** Bắt buộc sử dụng giao thức **HTTPS (TLS 1.3)** và bật **HSTS**.
