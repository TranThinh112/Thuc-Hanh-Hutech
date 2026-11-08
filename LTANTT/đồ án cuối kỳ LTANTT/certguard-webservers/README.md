# CertGuard Web Servers – Các web server demo (1 laptop + Docker)

7 web server Nginx thật, mỗi server dùng một chứng thư / cấu hình TLS khác nhau,
làm đối tượng để CertGuard kiểm tra và chấm điểm.

## Mô hình

```
                         LAPTOP (Windows/Linux/macOS)
 ┌──────────────────────────────────────────────────────────────────────┐
 │  CertGuard (Flask) :5000  ──TLS handshake thật──►  Docker:            │
 │        │                                         web-good       :8443 │
 │        │                                         web-expiring   :8444 │
 │        │                                         web-expired    :8445 │
 │        │                                         web-selfsigned :8446 │
 │        │                                         web-wronghost  :8447 │
 │        │                                         web-incomplete :8448 │
 │        │                                         web-weak       :8449 │
 │        └──TLS thật──► Internet: google.com, github.com, *.badssl.com  │
 └──────────────────────────────────────────────────────────────────────┘
```

Chứng thư được cấp bởi CA nội bộ giả lập **CertGuard Internal Root CA → CertGuard Internal Issuing CA**.

## Cài đặt (làm 1 lần)

1. Cài **Docker Desktop** và **Python 3.10+**.
2. Sinh chứng thư:
   ```
   pip install cryptography
   python gen_certs.py
   ```
3. Khai báo tên miền. Mở file hosts với quyền admin
   (Windows: `C:\Windows\System32\drivers\etc\hosts`, Linux/macOS: `/etc/hosts`) và thêm:
   ```
   127.0.0.1 good.certguard.webservers expiring.certguard.webservers expired.certguard.webservers
   127.0.0.1 selfsigned.certguard.webservers wronghost.certguard.webservers incomplete.certguard.webservers weak.certguard.webservers
   ```
4. Chạy các web server:
   ```
   docker compose up -d
   ```
5. Kiểm tra: mở `https://good.certguard.webservers:8443` trên trình duyệt.
6. Trong CertGuard, vào **Cài đặt → Root CA tin cậy bổ sung**, tải lên `certs/ca/root.pem`.

## Bảng kịch bản kiểm thử

| Máy chủ | Cổng | Tình trạng thật trên máy chủ | Kết quả openssl | CertGuard |
|---|---|---|---|---|
| good | 8443 | Chứng thư hợp lệ, cấu hình chuẩn Mozilla | `0 (ok)` | Hợp lệ, A+ |
| expiring | 8444 | Còn 5 ngày | `0 (ok)` | Cảnh báo sắp hết hạn |
| expired | 8445 | Đã hết hạn | `10 (certificate has expired)` | Lỗi, F |
| selfsigned | 8446 | Tự ký | `18 (self-signed certificate)` | Lỗi, F |
| wronghost | 8447 | Cấp cho `khac.certguard.webservers` | `62 (hostname mismatch)` | Lỗi, F |
| incomplete | 8448 | Không gửi chứng thư trung gian | `21 (unable to verify the first certificate)` | Cảnh báo, B |
| weak | 8449 | RSA 1024, TLS 1.0/1.1, cipher yếu, không HSTS | `0 (ok)` nhưng khóa 1024 bit | Cảnh báo, C |

Chạy `bash verify_servers.sh` (Git Bash/WSL trên Windows) để in lại kết quả openssl độc lập.

## Lệnh hay dùng

| Việc | Lệnh |
|---|---|
| Bật | `docker compose up -d` |
| Tắt | `docker compose down` |
| Khởi động lại sau khi đổi chứng thư/cấu hình | `docker compose restart` |
| Xem lỗi 1 server | `docker logs web-weak` |
| Sinh lại chứng thư, đổi số ngày còn lại | `python gen_certs.py --expiring-days 2` rồi `docker compose restart` |
| Tắt 1 server để thử "mất kết nối" | `docker stop web-good` |
