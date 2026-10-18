# 🎓 TỔNG HỢP CÁC BÀI THỰC HÀNH & ĐỒ ÁN - HUTECH

Kho lưu trữ toàn diện mã nguồn, tài liệu hướng dẫn, đề tài đồ án và báo cáo thực hành các môn học chuyên ngành **An toàn Thông tin / Công nghệ Thông tin** tại **Trường Đại học Công nghệ TP.HCM (HUTECH)**.

---

## 👨‍🎓 Thông tin sinh viên
* **Họ và tên:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Lớp:** 23DATA1
* **Khoa:** Công nghệ Thông tin
* **Chuyên ngành:** An toàn Thông tin

---

## 📂 Danh Mục Học Phần & Cấu Trúc Repository

```text
Thuc-Hanh-Hutech/
│
├── 📁 DoAnVM_1112/                 # Tổng hợp Đồ án Chuyên ngành, Đồ án Cơ sở & Đồ án Linux
│   ├── 📁 DoAnChuyenNganh/         # Đề cương: Tích hợp AI vào SIEM phát hiện đe dọa từ EDR
│   ├── 📁 DoAnCoSo/                # Đề tài Nhóm 8: Bảo mật mạng doanh nghiệp với pfSense Firewall (Báo cáo, Slide, Video demo)
│   └── 📁 DoanLinux/               # Đề tài: Giám sát mạng bằng Cacti & SNMP trên Linux (Báo cáo, Slide, Video demo)
│
├── 📁 Lap_Trinh Web/               # Học phần Lập trình Web (ASP.NET Core MVC & Cloud Deployment)
│   ├── 📁 Web_buoi2_20_4 -> Buoi8  # Các bài tập tuần: Bootstrap, MVC Architecture, Task CRUD, EF Core, Identity & Phân quyền
│   ├── 📁 Web_buoi7_5_6_Giua_Ky    # Bài thi kiểm tra giữa kỳ tích hợp hoàn chỉnh
│   ├── 📁 Thuyet_Trinh/            # Chuyên đề thuyết trình: Hướng dẫn Deploy dự án ASP.NET Core lên Railway Cloud
│   └── 📄 HDKN.txt                 # Cẩm nang lệnh EF Core Migrations & CLI
│
├── 📁 LTANTT/                      # Lập trình An toàn Thông tin (Python & Network Security)
│   ├── 📁 lab1/                    # Lab 1: Lập trình Python cơ bản, xử lý chuỗi và mã hóa thay thế
│   ├── 📁 lab2/                    # Lab 2: TCP Socket Client-Server, Port Scanner và Hàm băm MD5/SHA-256
│   └── 📁 lab 3/                   # Lab 3: Mô hình hóa & Săn tìm mối đe dọa (Kali Linux, Nmap, Metasploit SMB MS17-010)
│
├── 📁 TH_AnToanWeb&CSDL/           # Thực hành An toàn Web & Cơ sở dữ liệu
│   ├── 📄 BÀI 1.pdf                # Lab 1: Làm quen WebGoat và bắt gói tin với Burp Suite Proxy
│   ├── 📄 Bài 2.pdf                # Lab 2: Bảo mật Session, HTTPS/TLS và phòng chống Bot với reCAPTCHA
│   ├── 📄 TranTangTruongThinh_2387701939_Lab3.pdf   # Lab 3: Khai thác & Phòng chống Command Injection và SQL Injection
│   └── 📄 TranTangTruongThinh_2387701939_Lab4.docx  # Lab 4: Khai thác lỗ hổng PHP (File Upload, LFI) và tấn công XSS
│
├── 📁 TH_Chieu_T4/                 # Thực hành An toàn Mạng & Giám sát An ninh Thông tin (SIEM / SOC)
│   ├── 📁 Buoi_1_13_5/             # Buổi 1: Hệ thống Hybrid IPS thời gian thực bằng Python + Tshark + IPTables
│   ├── 📁 Buoi_5_10_6/             # Buổi 5: Triển khai Splunk SIEM Enterprise, Universal Forwarder, Syslog, FIM & Alert
│   └── 📁 Buoi_6_16_6/             # Buổi 6: Thiết kế SOC Dashboard, Visualizations (Pie/Column) & Interactive Drilldown
│
└── 📁 TH_Lap_Trinh_Web/            # Thực hành Lập trình Web (Mã nguồn thực hành trên lớp)
│   ├── 📁 TH1-16_5                 # TH1: Thiết kế giao diện Web Responsive với HTML5/CSS3 & Bootstrap
│   ├── 📁 TH2                      # TH2: Mô hình MVC với Repository Pattern, CRUD Mock Data & File Upload
│   ├── 📁 TH4-6_6                  # TH4: Kết nối SQL Server với EF Core Code-First Migrations & Phân hệ Admin Area
│   ├── 📁 TH5-14_6                 # TH5: Xây dựng Giỏ hàng (Shopping Cart) lưu trữ ISession & Quy trình Checkout
│   └── 📁 TH6-20_6                 # TH6: Xây dựng dịch vụ RESTful Web API (GET, POST, PUT, DELETE)
│
```

---

## 🛠️ Công Nghệ & Nền Tảng Sử Dụng

| Lĩnh vực | Công cụ & Công nghệ |
| :--- | :--- |
| **Lập trình Web & Backend** | C# (.NET 8), ASP.NET Core MVC, Entity Framework Core, RESTful Web API, SQL Server LocalDB/Express |
| **Frontend & Giao diện** | HTML5, CSS3, JavaScript, Bootstrap 5, Font Awesome |
| **An toàn Thông tin & SOC** | Splunk Enterprise SIEM, Splunk Universal Forwarder, SPL, Tshark (Wireshark CLI), Linux IPTables |
| **Kiểm thử Xâm nhập & Đánh giá**| Kali Linux, Nmap, Metasploit Framework, Burp Suite Proxy, OWASP WebGoat |
| **Mạng & Tường lửa** | pfSense Firewall (WAN / LAN / DMZ, NAT, Rule filtering), VMware Workstation VMnet |
| **Giám sát Mạng** | Cacti Network Monitoring, SNMP Daemon (`snmpd`), MariaDB, Apache LAMP Stack |
| **Lập trình An toàn Mạng** | Python 3, Socket TCP/UDP, PyCryptodome, Hashlib, Requests |
| **Cloud & DevOps** | Railway Cloud Platform, Git, GitHub |

---

## 📌 Hướng Dẫn Clone & Khởi Chạy
Để tải toàn bộ tài liệu và mã nguồn về máy cục bộ:
```bash
git clone https://github.com/TranThinh112/Thuc-Hanh-Hutech.git
cd Thuc-Hanh-Hutech
```

---
*© 2026 Trần Tăng Trường Thịnh - HUTECH. Mọi tài liệu và mã nguồn phục vụ mục đích học tập và nghiên cứu khoa học.*
