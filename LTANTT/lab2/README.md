# LAB 2: GIAO TIẾP MẠNG VÀ MÃ HÓA VỚI HASHING TRONG PYTHON

Hệ thống mã nguồn và tài liệu hướng dẫn thực hành thuộc bài Lab 2 bao gồm hai nội dung chính:
1. **2.3 Giao tiếp mạng bằng Python** (Socket TCP Client/Server, Port Scanner).
2. **2.4 Mã hóa với Hashing trong Python** (Băm chuỗi, so sánh hash, tính toàn vẹn tệp, so sánh thuật toán MD5/SHA-1/SHA-256, Salting).

---

## 📁 Cấu trúc thư mục

`	ext
lab2/
├── tcp_client.py       # Chương trình TCP Client kết nối và gửi/nhận dữ liệu
├── tcp_server.py       # Chương trình TCP Server lắng nghe kết nối tại 127.0.0.1:8080
├── port_scanner.py     # Trình quét các cổng mạng trên IP đích
├── hashing_basics.py   # Chương trình thực thi đầy đủ các bài tập băm (SHA-256, MD5, SHA-1, Salting)
├── sample.txt          # Tệp văn bản mẫu dùng để kiểm tra băm tính toàn vẹn tệp
└── README.md           # Hướng dẫn chạy và giải đáp chi tiết các câu hỏi phản tư
`

---

## 🚀 Hướng dẫn chạy chương trình

### 1. Thử nghiệm TCP Client & Server (	cp_server.py và 	cp_client.py)
Mở 2 cửa sổ Terminal tại thư mục lab2:

- **Cửa sổ 1 (Khởi động Server):**
  `ash
  python tcp_server.py
  `
  *Kết quả xuất ra:* Server đang lắng nghe tại 127.0.0.1:8080

- **Cửa sổ 2 (Khởi động Client):**
  `ash
  python tcp_client.py
  `
  *Kết quả xuất ra:*
  `	ext
  Đã kết nối tới 127.0.0.1 tại cổng 8080
  Phản hồi từ Server: Hello, Client!
  `
  *Đồng thời bên phía Server sẽ nhận được:*
  `	ext
  Kết nối từ ('127.0.0.1', <port_ngau_nhien>)
  Đã nhận: Hello, Server!
  `

---

### 2. Thử nghiệm Trình quét cổng (port_scanner.py)
Chạy câu lệnh:
`ash
python port_scanner.py
`
- Nếu Server 	cp_server.py đang bật, kết quả sẽ cho thấy cổng 8080 ở trạng thái **đang mở** (Cổng 8080 đang mở), các cổng khác đóng.

---

### 3. Thử nghiệm Mã hóa với Hashing (hashing_basics.py)
Chạy câu lệnh:
`ash
python hashing_basics.py
`
Chương trình sẽ thực thi tuần tự 5 phần từ các hình ảnh bài lab:
1. **Phần 1: Hashing cơ bản (SHA-256)**
2. **Phần 2: So sánh hash**
3. **Phần 3: Kiểm tra tính toàn vẹn tệp (sample.txt)**
4. **Phần 4: Khám phá các thuật toán hashing khác (MD5, SHA-1)**
5. **Phần 5: Triển khai tiện ích băm mật khẩu có Salting**

---

## 🧠 TRẢ LỜI CÁC CÂU HỎI PHẢN TƯ (REFLECTION)

### 2.3 Giao tiếp mạng bằng Python

#### 1. Sự khác biệt giữa TCP và UDP trong lập trình socket là gì?
- **TCP (Transmission Control Protocol):** Là giao thức hướng kết nối (connection-oriented). Yêu cầu bắt tay 3 bước (3-way handshake) trước khi truyền dữ liệu. Đảm bảo dữ liệu đến nơi tin cậy, đúng thứ tự và không bị mất gói (nhờ cơ chế ACK và retransmission). Thích hợp cho Web (HTTP/HTTPS), SSH, FTP, Email.
- **UDP (User Datagram Protocol):** Là giao thức không hướng kết nối (connectionless). Gửi dữ liệu trực tiếp mà không cần thiết lập kết nối trước, không đảm bảo thứ tự hay độ tin cậy. Đổi lại, UDP có tốc độ nhanh và độ trễ rất thấp. Thích hợp cho Stream Video/Audio, Game online, DNS, VoIP.

#### 2. Làm thế nào để bảo mật giao tiếp client-server và tránh truy cập trái phép?
- **Mã hóa kênh truyền:** Sử dụng SSL/TLS (HTTPS, WSS) để mã hóa toàn bộ dữ liệu lưu thông trên đường truyền, tránh bị nghe lén (Sniffing) hoặc tấn công Man-in-the-Middle (MitM).
- **Xác thực & Phân quyền (Authentication & Authorization):** Yêu cầu Client xác thực bằng Token (JWT, OAuth2) hoặc chứng chỉ số client (mTLS) trước khi thực hiện các yêu cầu.
- **Tường lửa & Giới hạn truy cập (Firewall / Rate Limiting):** Sử dụng IP Whitelisting, Rate Limiting để ngăn chặn tấn công từ chối dịch vụ (DDoS) và brute-force.
- **Kiểm tra dữ liệu đầu vào (Input Validation):** Sanitize toàn bộ dữ liệu nhận được từ Client để tránh các lỗ hổng Injection (Command Injection, Buffer Overflow).

#### 3. Cần cân nhắc điều gì về đạo đức khi chạy trình quét cổng trên một mạng?
- **Quyền hạn & Sự cho phép:** Chỉ quét các hệ thống/mạng mà bạn sở hữu hoặc đã được sự cho phép bằng văn bản từ chủ sở hữu. Quét cổng trái phép trên hệ thống của người khác có thể bị coi là hành vi tấn công mạng và vi phạm pháp luật.
- **Ảnh hưởng hệ thống (Service Disruption):** Việc gửi lượng lớn gói tin thăm dò (port scanning) có thể làm quá tải firewall, gây nghẽn mạng hoặc crash các dịch vụ nhạy cảm trên máy đích.
- **Cảnh báo an ninh:** Hoạt động quét cổng sẽ kích hoạt hệ thống cảnh báo (IDS/IPS), có thể làm phiền đội ngũ quản trị an ninh mạng nếu không thông báo trước.

---

### 2.4 Mã hóa với Hashing trong Python

#### 1. Tại sao hashing là một chiều (không thể đảo ngược)?
- Hàm băm là hàm toán học ánh xạ dữ liệu đầu vào có độ dài tùy ý thành chuỗi đầu ra có độ dài cố định.
- Trong quá trình băm, thông tin bị nén và làm biến mất các cấu trúc gốc (mất mát thông tin toán học một chiều). Không có thuật toán giải nén hay giải mã ngược nào có thể khôi phục lại dữ liệu ban đầu từ giá trị hash.

#### 2. Hash thay đổi thế nào khi dữ liệu đầu vào bị thay đổi?
- Hàm băm an toàn sở hữu **Hiệu ứng Tuyết lở (Avalanche Effect)**: Chỉ cần thay đổi 1 ký tự hoặc 1 bit duy nhất ở đầu vào, giá trị hash đầu ra sẽ thay đổi hoàn toàn và ngẫu nhiên (thay đổi hơn 50% các bit đầu ra).

#### 3. Cách quy trình so sánh hash được sử dụng trong hệ thống để xác minh mật khẩu lưu trữ?
- Hệ thống **không bao giờ lưu mật khẩu ở dạng rõ (plain-text)** trong cơ sở dữ liệu.
- Khi người dùng đăng ký, hệ thống băm mật khẩu và lưu chuỗi hash.
- Khi người dùng đăng nhập, hệ thống băm mật khẩu vừa nhập rồi so sánh chuỗi hash mới này với chuỗi hash đã lưu trong DB. Nếu 2 chuỗi hash trùng khớp (erify_hash == True), đăng nhập thành công.

#### 4. Tại sao hashing hữu ích để xác minh tính toàn vẹn tệp và áp dụng phát hiện malware như thế nào?
- **Xác minh toàn vẹn tệp:** Khi tải tệp về, người dùng băm tệp và so sánh với giá trị hash do nhà phát hành cung cấp. Nếu giá trị hash khớp, tệp chưa bị lỗi hay bị can thiệp.
- **Phát hiện Malware:** Các hệ thống an ninh (như VirusTotal, Antivirus) lưu trữ danh sách hash của các tệp mã độc đã biết. Khi phát hiện tệp mới, hệ thống băm tệp và tra cứu hash. Nếu hash nằm trong danh sách đen, tệp đó lập tức bị cảnh báo là malware.

#### 5. So sánh độ dài đầu ra của MD5, SHA-1, SHA-256 và lý do SHA-256 được ưa chuộng hơn?
- **MD5:** Đầu ra 128 bit (32 ký tự Hex).
- **SHA-1:** Đầu ra 160 bit (40 ký tự Hex).
- **SHA-256:** Đầu ra 256 bit (64 ký tự Hex).
- **Lý do SHA-256 được ưa chuộng:** MD5 và SHA-1 hiện nay đã bị phá vỡ về mặt lý thuyết lẫn thực tiễn (dễ bị tấn công xung đột hash - Collision Attack). SHA-256 cung cấp không gian khóa cực lớn (2^256), chống va chạm cực tốt và an toàn trước các kỹ thuật tấn công hiện tại.

#### 6. Salting cải thiện bảo mật mật khẩu băm như thế nào? Điều gì xảy ra nếu hai đầu vào giống hệt được băm với hai salt khác nhau?
- **Salting** là kỹ thuật thêm một chuỗi ngẫu nhiên (salt) vào mật khẩu trước khi băm.
- **Cải thiện bảo mật:** Chống lại tấn công Bảng Cầu Vồng (Rainbow Table) và Tấn công Từ Điển (Dictionary Attack). Chuỗi salt làm cho chuỗi hash trở nên duy nhất.
- **Kết quả:** Ngay cả khi 2 người dùng đặt mật khẩu giống hệt nhau (ví dụ 123456), nhờ 2 chuỗi salt ngẫu nhiên khác nhau, giá trị băm lưu trữ của 2 người dùng sẽ hoàn toàn khác nhau.
