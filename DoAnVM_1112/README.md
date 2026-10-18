# Tổng Hợp Đồ Án Chuyên Ngành, Đồ Án Cơ Sở & Đồ Án Linux

Thư mục lưu trữ các đề tài đồ án chuyên ngành, đồ án cơ sở và đồ án môn học hệ điều hành Linux thuộc chương trình đào tạo ngành **An toàn Thông tin / Công nghệ Thông tin** - Trường Đại học Công nghệ TP.HCM (HUTECH).

---

## Danh Sách Đồ Án & Nội Dung

### 1. Đồ Án Chuyên Ngành (`DoAnChuyenNganh`)
* **Tên đề tài:** *Nghiên cứu tích hợp Trí tuệ nhân tạo (AI) vào hệ thống SIEM nhằm nâng cao khả năng phát hiện mối đe dọa từ dữ liệu EDR*
* **Chuyên ngành:** An toàn thông tin
* **Tài liệu gồm có:**
  * `Đề Cương ĐỒ ÁN CHUYÊN NGÀNH.docx`: Bản đề cương chi tiết trình bày tính cấp thiết, mục tiêu, đối tượng nghiên cứu, phương pháp ứng dụng học máy / trí tuệ nhân tạo (Machine Learning/AI) vào hệ thống SIEM (Security Information and Event Management) để phân tích log và phát hiện hành vi tấn công từ dữ liệu EDR (Endpoint Detection and Response).

---

### 2. Đồ Án Cơ Sở (`DoAnCoSo`)
* **Tên đề tài:** *Thiết kế và đánh giá hệ thống bảo mật mạng doanh nghiệp sử dụng Firewall (pfSense)* (Nhóm 8)
* **Giảng viên hướng dẫn:** TS. Văn Thiên Hoàng
* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh cùng nhóm sinh viên
* **Tài liệu & Sản phẩm bàn giao:**
  * `BaoCaoDoAnCoSo_Nhom_8.docx` & `BaoCaoDoAnCoSo_Nhom_8.pdf`: Báo cáo toàn văn đồ án cơ sở.
  * `Slide_Nhom8_TruongThinh.pdf`: Slide báo cáo thuyết trình trước hội đồng.
  * `Demo_DACS (1).mp4`: Video clip quay lại quá trình vận hành, cấu hình và thử nghiệm hệ thống.
  * `HDSD.docx`: Hướng dẫn cấu hình card mạng ảo (VMnet) và hệ thống pfSense:
    * `VMnet0`: Kết nối Internet (WAN).
    * `VMnet1`: Mạng nội bộ văn phòng (LAN).
    * `VMnet2`: Phân vùng máy chủ dịch vụ (DMZ).
    * Cấu hình tường lửa (Firewall Rules), Outbound NAT và kiểm tra các cổng (Port forwarding/testing).
  * `Phieu mat truoc.jpg` & `Phieu mat sau.jpg`: Phiếu đánh giá chấm điểm đồ án cơ sở.

---

### 3. Đồ Án Linux (`DoanLinux`)
* **Tên đề tài:** *Xây dựng hệ thống giám sát mạng bằng Cacti trên nền tảng Linux*
* **Giảng viên hướng dẫn:** ThS. Nguyễn Hoàng Nam
* **Sinh viên thực hiện:** Hoàng Xuân Đạt (MSSV: 2387700013)
* **Tài liệu & Sản phẩm bàn giao:**
  * `HoangXuanDat_2387700013/BaoCao_Cacti.docx`: Báo cáo học phần chi tiết về giải pháp giám sát lưu lượng mạng bằng Cacti.
  * `HoangXuanDat_2387700013/SlideCacti.pdf`: Slide trình bày báo cáo.
  * `HoangXuanDat_2387700013/demoCacti.mp4`: Video demo thực tế hệ thống Cacti thu thập số liệu qua SNMP.
  * `HuongDanCaiDat_CACTI.docx`: Tài liệu hướng dẫn từng bước cài đặt và vận hành Cacti trên Linux (CentOS / Ubuntu):
    * Cài đặt LAMP Stack: Apache Web Server, MariaDB/MySQL, PHP.
    * Khởi động và kích hoạt `snmpd` (Simple Network Management Protocol).
    * Cấu hình mở cổng tường lửa `firewall-cmd --add-port=161/udp`.

---

## Yêu Cầu Môi Trường & Công Cụ
* **Môi trường ảo hóa:** VMware Workstation / VirtualBox.
* **Hệ điều hành:** Linux CentOS, Ubuntu, pfSense Firewall OS.
* **Phần mềm giám sát & an ninh:** pfSense, Cacti, SNMP Daemon, SIEM platform.