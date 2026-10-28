# Đồ Án Linux: Hệ Thống Giám Sát Mạng Doanh Nghiệp Với Cacti & SNMP

* **Đề tài:** Triển khai giải pháp giám sát lưu lượng mạng và trạng thái máy chủ Linux sử dụng Cacti và giao thức SNMP.
* **Môi trường:** Ubuntu Server / CentOS Linux, MariaDB, Apache, PHP, Net-SNMP, RRDtool.

---

## 📌 Chức Năng Chính
1. **Thu thập chỉ số hiệu năng:** CPU, RAM, Disk I/O, Traffic Network qua giao thức SNMPv2c/SNMPv3.
2. **Trực quan hóa đồ thị (RRDtool):** Tự động vẽ biểu đồ lưu lượng mạng theo thời gian thực (5 phút / 30 phút / ngày / tuần).
3. **Cảnh báo ngưỡng:** Tự động kích hoạt thông báo khi lưu lượng băng thông hoặc tải hệ thống vượt ngưỡng định mức.

---

## 🖼️ Hình Ảnh Giao Diện Dashboard Cacti

![Dashboard Cacti](HoangXuanDat_2387700013/images/img_BaoCao_Cacti_1.png)
*Giao diện đăng nhập và quản trị máy chủ giám sát Cacti*

![Đồ Thị Băng Thông](HoangXuanDat_2387700013/images/img_BaoCao_Cacti_10.png)
*Biểu đồ lưu lượng mạng SNMP thu thập theo thời gian thực*