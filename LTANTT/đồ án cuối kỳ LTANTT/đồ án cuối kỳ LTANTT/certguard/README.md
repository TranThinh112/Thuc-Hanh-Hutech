# CertGuard – Hệ thống quản lý và kiểm tra chứng thư số SSL/TLS

## Chức năng

| Nhóm | Chức năng |
|---|---|
| Kiểm tra | Bắt tay TLS thật, lấy chuỗi chứng thư, kiểm tra thời hạn, tên miền (SAN), chuỗi tin cậy, khóa yếu, thuật toán ký yếu, TLS 1.0/1.1, cipher yếu, Forward Secrecy, HSTS, thu hồi (OCSP/CRL), chấm điểm A+…F |
| Giám sát | Danh sách máy chủ, quét định kỳ, lịch sử quét, phát hiện chứng thư bị thay đổi |
| Cảnh báo | Telegram / Email khi hết hạn, sắp hết hạn, lỗi chuỗi, sai tên miền, mất kết nối… |
| Công cụ | Kiểm tra nhanh 1 tên miền, phân tích file .pem/.crt |
| Bảo mật | Mật khẩu băm scrypt, khóa tài khoản sau 5 lần sai, CSRF token, phân quyền admin/user, chống SSRF (cả với URL OCSP/CRL trong chứng thư), chống DNS rebinding, chống SQL Injection (truy vấn tham số), chống XSS (auto-escape + CSP), nhật ký kiểm toán, bí mật đặt trong `.env` |

## Cài đặt và chạy (Windows)

Mở thư mục `certguard` trong VS Code, mở Terminal (Ctrl + `):

```
pip install -r requirements.txt
python manage.py create-admin
python app.py
```

Mở trình duyệt: **http://127.0.0.1:5000** và đăng nhập bằng tài khoản vừa tạo.

## Kết nối với các web server demo

1. Bật các web server: trong thư mục `certguard-webservers` chạy `docker compose up -d`.
2. Vào **Cài đặt → Root CA tin cậy bổ sung**, tải lên file `certguard-webservers/certs/ca/root.pem`.
   (Giống như doanh nghiệp tin CA nội bộ của mình. Nếu bỏ qua bước này, mọi web server demo sẽ bị báo "Root CA không tin cậy".)
3. Danh sách cho phép mặc định đã có `*.certguard.webservers`, nên các web server demo (trỏ về 127.0.0.1) được phép quét.
4. Ở trang Tổng quan, thêm lần lượt:

```
good.certguard.webservers:8443
expiring.certguard.webservers:8444
expired.certguard.webservers:8445
selfsigned.certguard.webservers:8446
wronghost.certguard.webservers:8447
incomplete.certguard.webservers:8448
weak.certguard.webservers:8449
```

Kết quả mong đợi (đã kiểm thử):

| Máy chủ | Trạng thái | Điểm | Phát hiện chính |
|---|---|---|---|
| good | Hợp lệ | A+ | Không có |
| expiring | Cảnh báo | A+ | Còn 5 ngày |
| expired | Lỗi | F | Đã hết hạn |
| selfsigned | Lỗi | F | Tự ký |
| wronghost | Lỗi | F | Sai tên miền |
| incomplete | Cảnh báo | B | Thiếu chứng thư trung gian |
| weak | Cảnh báo | C | RSA 1024, TLS 1.0/1.1, cipher yếu, không PFS, không HSTS |

Thêm cả site thật: `google.com`, `github.com`, `expired.badssl.com`, `self-signed.badssl.com`, `wrong.host.badssl.com`, `revoked.badssl.com`.

## Cảnh báo Telegram

Sao chép `.env.example` thành `.env`, điền token và chat id theo hướng dẫn trong file, khởi động lại `python app.py`, rồi vào **Cài đặt → Gửi tin nhắn thử**.

## Lệnh quản trị

| Lệnh | Tác dụng |
|---|---|
| `python manage.py create-admin` | Tạo tài khoản admin |
| `python manage.py reset-db` | Xóa sạch CSDL (dùng trước khi quay video để bắt đầu từ trống) |
| `python manage.py stats` | Đếm số bản ghi trong từng bảng |
| `python scanner.py good.certguard.webservers:8443` | Quét từ dòng lệnh, in kết quả JSON |

## Cấu trúc mã nguồn

```
certguard/
├── app.py           Web app Flask: định tuyến, phân quyền, lập lịch quét
├── scanner.py       Lõi kiểm tra TLS/X.509 (phần quan trọng nhất của đề tài)
├── monitor.py       Quét domain, lưu kết quả, phát hiện thay đổi, gửi cảnh báo
├── security.py      Băm mật khẩu, khóa tài khoản, CSRF, phân quyền, audit log, header bảo mật
├── notifier.py      Gửi Telegram / Email
├── db.py            Lược đồ và truy cập CSDL SQLite
├── manage.py        Công cụ dòng lệnh
├── templates/       Giao diện (Jinja2)
├── static/          CSS, JS
├── trusted_roots/   Root CA tin cậy bổ sung
└── instance/        CSDL + secret key (tự sinh, không nộp kèm)
```

## Quy tắc chấm điểm

Bắt đầu từ A+, mỗi lỗi giới hạn điểm tối đa:

| Lỗi | Điểm tối đa |
|---|---|
| Hết hạn / chưa hiệu lực / tự ký / Root không tin cậy / sai tên miền / bị thu hồi / ký bằng SHA-1, MD5 | F |
| Khóa RSA < 2048 bit, chấp nhận cipher yếu | C |
| Thiếu chuỗi trung gian, còn bật TLS 1.0/1.1, không có Forward Secrecy | B |
| Không có HSTS | A |

Sắp hết hạn không làm giảm điểm (cấu hình vẫn tốt), nhưng chuyển trạng thái sang **Cảnh báo** và gửi thông báo.
