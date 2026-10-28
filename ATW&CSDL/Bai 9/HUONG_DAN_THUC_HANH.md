# HƯỚNG DẪN THỰC HÀNH TỪNG BƯỚC VỚI BURP SUITE & TRÌNH DUYỆT

## Bước 1: Khởi động Ứng dụng Lab
Ứng dụng web kiểm thử đang chạy tại địa chỉ:
👉 **URL:** `http://localhost:3000`

Nếu muốn khởi động lại bất cứ lúc nào, bạn mở Terminal tại thư mục `Bai 9` và chạy:
```powershell
cd app
node server.js
```

---

## Bước 2: Cấu hình Burp Suite để bắt gói tin (Intercept)

1. Mở **Burp Suite Community Edition**.
2. Chọn **Temporary Project** -> **Use Burp defaults** -> Bấm **Start Burp**.
3. Vào tab **Proxy** -> **Intercept**:
   - Có thể bấm **Open Browser** ngay trong Burp Suite (trình duyệt tích hợp sẵn không cần chỉnh proxy mạng).
   - Truy cập vào địa chỉ: `http://localhost:3000`.

---

## Bước 3: Thực hành khai thác từng lỗ hổng theo hướng dẫn

### 1. Khai thác SQL Injection Bypass Login
- Trên trình duyệt, truy cập `http://localhost:3000/login`.
- Nhập:
  - **Tên đăng nhập:** `admin' --`
  - **Mật khẩu:** Nhập tuỳ ý (ví dụ `123456`).
- Bấm **Đăng nhập**.
- **Kết quả:** Hệ thống lập tức bỏ qua kiểm tra mật khẩu và đăng nhập thẳng vào tài khoản Quản trị viên (`admin`).

### 2. Khai thác SQL Injection UNION-Based (Rút cạn Database)
- Truy cập `http://localhost:3000/products`.
- Nhập vào ô tìm kiếm chuỗi payload:
  ```text
  ' UNION SELECT id, username, password, role FROM users --
  ```
- Bấm **Tìm kiếm**.
- **Kết quả:** Bảng sản phẩm sẽ hiển thị toàn bộ tài khoản và mật khẩu chưa mã hóa của tất cả người dùng trong hệ thống.

### 3. Khai thác Reflected XSS
- Trên ô tìm kiếm của `/products`, nhập:
  ```html
  <script>alert('Ban bi tan cong Reflected XSS!')</script>
  ```
- Bấm **Tìm kiếm**.
- **Kết quả:** Trình duyệt sẽ bật popup cảnh báo mã độc Javascript do ứng dụng in trực tiếp input vào trang mà không qua mã hóa thực thể HTML.

### 4. Khai thác Stored XSS
- Truy cập `http://localhost:3000/feedback`.
- Nhập:
  - **Họ tên:** Hacker
  - **Nội dung:** `<script>alert("Cookie: " + document.cookie)</script>`
- Bấm **Gửi góp ý**.
- **Kết quả:** Đoạn mã script được ghi vào database. Mỗi khi bất kỳ ai tải lại trang Feedback, trình duyệt đều tự động thực thi script và hiển thị Cookie phiên làm việc.

### 5. Khai thác IDOR (Insecure Direct Object Reference)
- Trên thanh địa chỉ trình duyệt, lần lượt thay đổi:
  - `http://localhost:3000/profile?id=1` (Xem thông tin admin)
  - `http://localhost:3000/profile?id=2` (Xem thông tin user john_doe)
  - `http://localhost:3000/profile?id=3` (Xem thông tin user jane_smith)
- **Kết quả:** Bất kỳ ai cũng có thể trích xuất dữ liệu của người khác mà không có rào cản phân quyền.

### 6. Khai thác Broken Access Control (Burp Suite Repeater)
- Mở tab **Repeater** trong Burp Suite.
- Gửi yêu cầu:
  ```http
  GET /admin HTTP/1.1
  Host: localhost:3000
  X-Role-Override: admin
  ```
- Bấm **Send**.
- **Kết quả:** Trả về mã `200 OK` cùng bảng điều khiển quản trị viên và mật khẩu tài khoản hệ thống.
