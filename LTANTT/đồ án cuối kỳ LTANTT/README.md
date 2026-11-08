# Đồ Án Cuối Kỳ LTANTT - CertGuard

**Học phần:** Lập Trình An Toàn Thông Tin (LTANTT)  
**Trường Đại học Công nghệ TP.HCM (HUTECH)**  
**Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
**MSSV:** 2387701939  
**Lớp:** 23DATA1  

---

## 📌 Giới Thiệu Đồ Án

**CertGuard** là hệ thống toàn diện dùng để quản trị, giám sát và kiểm tra tự động trạng thái chứng thư số SSL/TLS của máy chủ Web. Hệ thống hỗ trợ bắt tay TLS trực tiếp, phân tích chuỗi chứng chỉ (Certificate Chain), phát hiện sớm các nguy cơ mất an toàn bảo mật (hết hạn, sai lệch tên miền, thuật toán băm/khóa mã hóa yếu, cấu hình TLS lỗi thời) và gửi cảnh báo thời gian thực qua Telegram hoặc Email.

---

## 📂 Cấu Trúc Thư Mục

`	ext
đồ án cuối kỳ LTANTT/
├── certguard/                                    # Ứng dụng Web Dashboard & Engine kiểm tra SSL/TLS (Flask, SQLite, Python)
│   ├── app.py                                   # Entrypoint ứng dụng Web Flask & API Endpoints
│   ├── scanner.py                               # Engine kiểm tra bắt tay TLS, SAN, Chain, Cipher, OCSP/CRL
│   ├── monitor.py                               # Tiến trình quét nền định kỳ tự động
│   ├── notifier.py                              # Module phát cảnh báo tự động qua Telegram & Email
│   ├── security.py                              # Cơ chế bảo mật: CSRF, băm mật khẩu scrypt, chống SSRF/DNS Rebinding
│   ├── db.py                                    # Quản lý cơ sở dữ liệu SQLite & bảng kiểm toán (Audit logs)
│   ├── manage.py                                # CLI hỗ trợ tạo tài khoản Admin và quản trị hệ thống
│   ├── static/ & templates/                     # Giao diện người dùng Web Dashboard & CSS/JS
│   ├── trusted_roots/                           # Thư mục lưu trữ Root CA tin cậy bổ sung
│   ├── requirements.txt                         # Thư viện phụ thuộc (Flask, cryptography, requests, v.v.)
│   └── README.md                                # Hướng dẫn chi tiết cài đặt và cấu hình CertGuard
│
├── certguard-webservers/                         # Môi trường mô phỏng các Web Server thực tế bằng Docker Compose
│   ├── docker-compose.yml                       # Khởi chạy 7 Web Server Nginx với nhiều kịch bản lỗi SSL khác nhau
│   ├── gen_certs.py                             # Script sinh Root CA, Intermediate CA và các chứng chỉ test
│   ├── nginx/ & html/                           # Cấu hình máy chủ ảo Nginx và trang web đích mô phỏng
│   ├── verify_servers.sh                        # Script shell kiểm tra nhanh kết nối các server ảo
│   └── README.md                                # Hướng dẫn dựng môi trường thử nghiệm Docker
│
├── BaoCao_CertGuard.docx                         # Báo cáo đồ án chi tiết (File Word hoàn chỉnh)
├── PhanCongCongViec.docx                         # Bảng phân công nhiệm vụ đồ án nhóm
├── Thuyết trình CertGuard.pptx                   # Slide báo cáo thuyết trình đồ án trước hội đồng
├── Thuyết trình CertGuard.pptx.pdf               # Slide thuyết trình định dạng PDF
├── Xây dựng hệ thống quản lý và kiểm tra...docx   # Bản báo cáo thuyết minh đề tài toàn văn
├── Xây dựng hệ thống quản lý và kiểm tra...pdf    # Báo cáo thuyết minh định dạng PDF
├── Recording 2026-11-01 190013.mp4               # Video quay màn hình demo hoạt động của hệ thống
└── README.md                                     # Tài liệu tổng quan đồ án (File này)
`

---

## 🚀 Các Tính Năng Nổi Bật

1. **Kiểm Tra & Phân Tích SSL/TLS Tự Động:**
   * Thực hiện bắt tay TLS thời gian thực, bóc tách toàn bộ chứng thư số từ máy chủ đích.
   * Kiểm tra hạn dùng, cảnh báo chứng thư hết hạn hoặc sắp hết hạn.
   * Đối chiếu SAN (Subject Alternative Name), phát hiện lỗi hostname mismatch.
   * Thẩm tra chuỗi tin cậy (Certificate Chain of Trust), kiểm tra Root CA và Intermediate CA.
   * Nhận diện các cấu hình rủi ro: Khóa RSA < 2048-bit, thuật toán ký lỗi thời (MD5, SHA-1), giao thức kém an toàn (SSLv3, TLS 1.0, TLS 1.1).
   * Kiểm tra cơ chế thu hồi chứng thư số thông qua OCSP & CRL.
   * Đánh giá bảo mật và xếp hạng chứng chỉ theo thang điểm chuẩn (A+ đến F).

2. **Giám Sát Định Kỳ & Cảnh Báo Chủ Động:**
   * Cơ chế Worker quét nền theo chu kỳ cài đặt trước.
   * Gửi thông báo tức thời qua Telegram Bot và Email khi phát hiện sự cố chứng chỉ hoặc máy chủ mất kết nối.

3. **Bảo Mật Hệ Thống Nâng Cao:**
   * Cơ chế phòng thủ tấn công SSRF và DNS Rebinding nghiêm ngặt đối với IP nội bộ và URL OCSP/CRL.
   * Băm mật khẩu người dùng chuẩn mã hóa an toàn scrypt, giới hạn đăng nhập sai (Brute-force protection).
   * Hệ thống phân quyền chặt chẽ (Role-Based Access Control) cùng nhật ký kiểm toán (Audit Logs).

---

## 🛠️ Hướng Dẫn Cài Đặt & Chạy Nhanh

### 1. Dựng Môi Trường Web Server Thử Nghiệm (Tùy chọn)
`ash
cd certguard-webservers
docker compose up -d
`

### 2. Cài Đặt Và Khởi Chạy CertGuard
`ash
cd certguard
pip install -r requirements.txt
python manage.py create-admin
python app.py
`
Truy cập giao diện Web Dashboard tại: **http://127.0.0.1:5000**