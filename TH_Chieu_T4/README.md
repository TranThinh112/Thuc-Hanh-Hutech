# Thực Hành An Toàn Mạng & Giám Sát An Ninh Thông Tin (TH_Chieu_T4)

Kho lưu trữ toàn văn mã nguồn, cấu hình hệ thống và các báo cáo thực hành chuyên sâu môn **Thực hành An toàn Mạng / Giám sát và Ứng cứu Sự cố An toàn Thông tin (Network Security & SIEM/SOC)** - Ca học: **Chiều Thứ 4** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Lớp:** 23DATA1
* **Chuyên ngành:** An toàn Thông tin - Khoa Công nghệ Thông tin
* **Thành viên nhóm (Bài thực hành Buổi 1):**
  * Trịnh Thành Đông (MSSV: 2387700372)
  * Trần Tăng Trường Thịnh (MSSV: 2387701939)
  * Hoàng Xuân Đạt (MSSV: 2387700013)
* **Nền tảng công nghệ & Công cụ:**
  * Hệ điều hành: Ubuntu Server 22.04 LTS, Kali Linux, Windows Host (VMware Workstation Lab).
  * Công cụ giám sát & phân tích gói tin: Python 3, Tshark (Wireshark CLI), Iptables Firewall.
  * Nền tảng SIEM & Phân tích sự cố: Splunk Enterprise, Splunk Universal Forwarder, SPL (Search Processing Language).
  * Công cụ tấn công kiểm thử: Nmap, Scapy, Ping / ICMP generator, SSH Brute-force simulator.

---

## Danh Mục Các Bài Thực Hành Chi Tiết

```
TH_Chieu_T4/
│
├── Buoi_1_13_5/                   # Buổi 1 (13/05): Hệ thống ngăn chặn xâm nhập lai ghép (Hybrid IPS)
│   ├── Buoi1.py                   # Mã nguồn Python điều khiển Tshark & IPTables thời gian thực
│   └── Buoi_1_BaoCao.docx         # Báo cáo thực nghiệm, giải thích giải thuật và kiểm thử
│
├── Buoi_5_10_6/                   # Buổi 5 (10/06): Triển khai Splunk SIEM & Giám sát hệ thống
│   └── TruongThinh_1939_Lab_5.docx # Báo cáo kết nối Forwarder, Syslog, FIM và Cấu hình Alert
│
├── Buoi_6_16_6/                   # Buổi 6 (16/06): Thiết kế SIEM Dashboard & Phân tích Drilldown
│   └── Trường Thịnh 2387701939.docx # Báo cáo Lab 3: Interactive Drilldown, Panels, Visualizations
│
└── README.md                      # Tài liệu tổng quan mô tả môn học và chi tiết các bài lab
```

---

## Chi Tiết Kỹ Thuật Từng Bài Lab

### 1. Buổi 1 (13/05/2026): Xây Dựng Hệ Thống Hybrid IPS Bắt Gói Tin Thời Gian Thực Với Python, Tshark & IPTables

#### Mục tiêu & Mô hình thử nghiệm
Thiết kế và triển khai một giải pháp **Intrusion Prevention System (IPS)** hoạt động tại thời gian thực (realtime) có khả năng tự động phân tích hành vi lưu lượng mạng ở Tầng 3 (Network Layer) và Tầng 4 (Transport Layer) theo mô hình OSI, phát hiện tấn công và tự động kích hoạt luật chặn trên tường lửa Linux kernel (IPTables).

* **Mô hình mạng phòng lab (VMware Network):**
  * **IPS Server (Ubuntu Server):** IP `192.168.88.168` (Interface `ens33`) - Chạy daemon phát hiện xâm nhập viết bằng Python kết hợp Tshark.
  * **Attacker 1 (Windows Host):** IP `192.168.88.123` - Tạo lưu lượng tấn công ICMP Ping Flood dồn dập (Layer 3).
  * **Attacker 2 (Kali Linux):** IP `192.168.88.103` - Chạy Nmap quét cổng TCP SYN/Connect Scan (Layer 4).

#### Cấu trúc và Thuật toán của `Buoi1.py`
1. **Thu thập gói tin liên tục (Realtime Packet Sniffing):**
   * Sử dụng `subprocess.Popen` thực thi Tshark nền với tùy chọn trường xuất định dạng ống dẫn (Pipe):
     ```bash
     tshark -l -i ens33 -Y ip -T fields -E separator=| \
            -e ip.src -e icmp.type -e tcp.flags.syn -e tcp.flags.ack -e tcp.dstport
     ```
   * Dùng cơ chế `select.select([process.stdout], [], [], 1)` để đọc luồng chuẩn non-blocking, tránh nghẽn CPU.
   * Tích hợp cơ chế tự phục hồi: nếu tiến trình Tshark gặp lỗi hoặc bị ngắt, script tự động khởi động lại Tshark.

2. **Phát hiện tấn công quét cổng (Port Scan Detection - Layer 4):**
   * Sử dụng cấu trúc hàng đợi hai đầu có thời gian trượt (`collections.deque`) với cửa sổ theo dõi `WINDOW = 10` giây.
   * Ghi nhận tập hợp các cổng đích (`tcp.dstport`) riêng biệt mà một IP nguồn cố gắng gửi gói tin đến.
   * Khi số lượng cổng được quét đạt từ 8 cổng trở lên trong 10 giây (`PORTSCAN_THRESHOLD = 8`), hệ thống kết luận hành vi quét cổng bằng Nmap:
     * Kích hoạt gọi lệnh: `iptables -A INPUT -s <IP> -j DROP`.
     * Khóa IP trong thời gian `PORTSCAN_BLOCK_TIME = 10` giây.
     * Làm rỗng bộ đếm của IP đó để giải phóng bộ nhớ.

3. **Phát hiện tấn công Ping dồn dập (High-rate ICMP Flood - Layer 3):**
   * Giám sát các gói tin ICMP Echo Request (`icmp.type == "8"`).
   * Đếm số lượt ping nhận được trong cửa sổ 10 giây.
   * Nếu vượt ngưỡng 10 gói tin ping trong 10 giây (`PING_THRESHOLD = 10`), hệ thống xác định tấn công DoS ICMP Flood:
     * Khóa IP bằng luật: `iptables -A INPUT -s <IP> -j DROP`.
     * Áp dụng thời gian phạt cách ly: `HIGH_RATE_BLOCK_TIME = 20` giây.

4. **Cơ chế phòng thủ an toàn & Tự động gỡ chặn (Auto Unblock):**
   * **Danh sách Whitelist:** Thiết lập sẵn `127.0.0.1` và IP của chính server `192.168.88.168` để không bao giờ bị khóa nhầm.
   * **Vòng lặp giải phóng (`unblock_expired`):** Định kỳ kiểm tra mốc thời gian của từng IP trong `blocked_ips`. Khi `now - start_time >= duration`, hệ thống gọi `iptables -D INPUT -s <IP> -j DROP` để mở lại kết nối, tránh tràn bảng luật firewall.

#### Kết quả thực nghiệm
* Attacker Windows gửi ping liên tục -> Đến gói thứ 10, hệ thống in cảnh báo `[TRIGGER] HIGH_RATE ICMP` và `[BLOCKED] 192.168.88.123 for 20s`, kết nối phía Windows chuyển sang `Request timed out`. Sau 20 giây xuất hiện thông báo `[UNBLOCKED]` và ping thành công trở lại.
* Attacker Kali Linux chạy `nmap -sS -p 1-100 192.168.88.168` -> Sau 8 cổng thử nghiệm, hệ thống in `[TRIGGER] PORT_SCAN DETECTED`, toàn bộ các cổng còn lại của Nmap bị trạng thái `filtered/drop`.

---

### 2. Buổi 5 (10/06/2026): Triển Khai Hệ Thống Giám Sát Nhật Ký Tập Trung Và Cảnh Báo An Ninh Với Splunk SIEM

#### Mục tiêu bài thực hành
Xây dựng giải pháp giám sát an ninh mạng trung tâm (Security Operation Center - SOC mini) bằng **Splunk Enterprise**, cấu hình thu thập dữ liệu nhật ký phân tán từ máy trạm Linux Forwarder, phân tích các chỉ số an toàn hệ thống và thiết lập quy tắc cảnh báo (Alert) khi phát hiện tấn công.

#### Các bước triển khai & Câu lệnh SPL (Search Processing Language)
1. **Kết nối nguồn nhật ký từ Client (Data Inputs Configuration):**
   * Triển khai máy chủ Splunk lắng nghe dữ liệu thu thập qua cổng TCP `9997`.
   * Cấu hình chuyển tiếp toàn bộ nhật ký hệ điều hành máy trạm Ubuntu (`/var/log/syslog`, `/var/log/auth.log`) về Splunk Indexer chính.
   * Kiểm tra tính sẵn sàng của máy Client trên giao diện Splunk:
     ```spl
     index=main host="trthinh1112-VMware-Virtual-Platform"
     ```

2. **Giám sát tính toàn vẹn của tệp tin (File Integrity Monitoring - FIM):**
   * Theo dõi các thay đổi trái phép đối với các tệp tin cấu hình hoặc tệp mã nguồn quan trọng trên máy chủ:
     ```spl
     index=main "file modified"
     ```
   * Phân tích thời gian, đường dẫn file và tiến trình đã thực hiện chỉnh sửa file.

3. **Giám sát lỗi hệ thống (System Error Auditing):**
   * Lọc và thống kê toàn bộ các sự kiện mang mức độ lỗi (`error`) trong file `syslog` trong vòng 24 giờ qua:
     ```spl
     index=main source="/var/log/syslog" error earliest=-24h
     ```

4. **Giả lập tấn công & Thiết lập cảnh báo tự động (Security Alerting):**
   * Thử nghiệm tấn công xâm nhập bằng SSH với mật khẩu không hợp lệ.
   * Đẩy sự kiện tấn công an ninh mẫu vào luồng log với định danh `"ATTACK DETECTED"`.
   * **Cấu hình Alert trên Splunk:**
     * **Search criteria:** `index=main "ATTACK DETECTED"`
     * **Trigger condition:** Số lượng kết quả trả về `> 0` trong chu kỳ kiểm tra 5 phút hoặc Realtime.
     * **Alert Action:** Kích hoạt cảnh báo mức độ nghiêm trọng (Severity: High), lưu vào danh sách `Triggered Alerts` và gửi thông báo tới người quản trị SOC.

---

### 3. Buổi 6 (16/06/2026): Thiết Kế Bảng Điều Khiển An Ninh Mạng (SIEM Dashboard) & Kỹ Thuật Tương Tác Drilldown

#### Mục tiêu bài thực hành
Nâng cao kỹ năng phân tích và điều tra sự cố của chuyên viên SOC thông qua việc trực quan hóa luồng dữ liệu bảo mật thành các **Dashboard**, Panel đa dạng (Pie Chart, Column Chart, Single Value) và thiết lập tính năng **Drilldown** cho phép nhấp vào biểu đồ để chuyển tiếp ngay sang trang điều tra chuyên sâu.

#### Nội dung các Task thực hiện trong Báo cáo Lab 3
1. **Task 1: Cấu hình tương tác Drilldown (Interactive Drilldown):**
   * Kích hoạt chế độ `Edit Drilldown` trên các biểu đồ tròn và biểu đồ cột trên Dashboard.
   * Chọn hành động: `Link to Search` (Liên kết trực tiếp tới giao diện Search & Reporting).
   * Thiết lập câu lệnh tìm kiếm tự động nhận giá trị mà người dùng vừa nhấp chuột (`$click.value$` / `$click.name$`).
   * Kết quả: Khi chuyên viên SOC nhấp vào một lát cắt trên biểu đồ (ví dụ một mã lỗi hoặc một IP khả nghi), một tab tìm kiếm mới sẽ mở ra với toàn bộ sự kiện chi tiết của mục đó.

2. **Task 2: Thiết kế các Panel trực quan hóa (Data Visualization Panels):**
   * Xây dựng Dashboard an ninh mang tiêu đề: *"TruongThinh 2387701939 - Báo cáo an ninh mạng"*.
   * **Panel Biểu đồ tròn (Pie Chart):** Thống kê tỷ lệ phân bố sự kiện theo từng loại dịch vụ, phương thức xác thực hoặc tỷ lệ lỗi.
   * **Panel Biểu đồ cột (Column Chart):** Biểu diễn mật độ các cuộc tấn công hoặc số lượng sự kiện theo mốc thời gian (`timechart`).

3. **Task 3: Phân tích thống kê dữ liệu chuyên sâu với SPL:**
   * Sử dụng các lệnh thống kê mạnh mẽ:
     * `stats count by <field>`: Nhóm và đếm số lần xuất hiện của các trường quan trọng (EventCode, User, Host).
     * `timechart span=1h count by host`: Theo dõi số lượng sự kiện theo từng giờ của máy trạm.
     * `top limit=10 src_ip`: Liệt kê 10 địa chỉ IP phát sinh nhiều sự kiện nhất.
   * Tích hợp bảng thống kê chi tiết (`Statistics Table`) đặt song song với biểu đồ trực quan.

4. **Task 4: Tối ưu giao diện & Bộ lọc động (Dashboard Form Inputs):**
   * Tích hợp thành phần chọn khoảng thời gian (`Time Range Picker Input`) áp dụng đồng bộ cho toàn bộ panel trên Dashboard.
   * Tinh chỉnh mã nguồn XML (`Dashboard Source XML`) để tùy biến bố cục hiển thị linh hoạt, tối ưu hiệu năng tải dữ liệu cho các trung tâm giám sát an ninh mạng chuyên nghiệp.

---

## Ý Nghĩa Thực Tiễn Của Học Phần
Học phần trang bị cho sinh viên năng lực thực chiến toàn diện:
1. **Phòng thủ chủ động ở tầng mạng (Host-based / Network-based IPS):** Tự xây dựng phần mềm phát hiện bất thường từ luồng gói tin thực tế bằng Tshark và chặn tự động bằng IPTables trên Linux.
2. **Quản trị an ninh tập trung (SIEM):** Nắm vững quy trình cấu hình thu thập, lập chỉ mục và phân tích nhật ký bằng giải pháp SIEM Splunk tiêu chuẩn ngành.
3. **Vận hành trung tâm SOC:** Xây dựng Dashboard trực quan, thiết lập luật Alert phát hiện tấn công và kỹ thuật Drilldown phục vụ phản ứng sự cố nhanh chóng.