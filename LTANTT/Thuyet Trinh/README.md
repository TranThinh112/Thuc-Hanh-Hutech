# Báo Cáo Thuyết Trình: Xây Dựng Hệ Thống Phát Hiện Đăng Nhập Bất Thường Dựa Trên Hành Vi Người Dùng

**Học phần:** Lập Trình An Toàn Thông Tin (LTANTT)  
**Trường Đại học Công nghệ TP.HCM (HUTECH)**  
**Sinh viên thực hiện:** Trần Tăng Trường Thịnh  
**MSSV:** 2387701939  
**Lớp:** 23DATA1  

---

## 📌 Giới Thiệu Chuyên Đề Báo Cáo

Tài liệu và sản phẩm báo cáo chuyên đề nghiên cứu và ứng dụng giải pháp **Phát hiện đăng nhập bất thường dựa trên hành vi người dùng (User Behavior Analytics - UBA / UEBA)** trong hệ thống thông tin.

Mô hình hướng tới việc giám sát liên tục các thông số ngữ cảnh của phiên đăng nhập (vị trí địa lý IP, Fingerprint trình duyệt/thiết bị, tần suất yêu cầu, khung giờ truy cập bất thường), áp dụng cơ chế chấm điểm rủi ro (Risk Scoring Engine) để kích hoạt biện pháp xác thực tăng cường (MFA / Step-up Authentication) hoặc cảnh báo ngăn chặn kịp thời trước các cuộc tấn công như Brute Force, Credential Stuffing và Chiếm đoạt phiên làm việc (Session Hijacking).

---

## 📂 Danh Mục Tài Liệu Trong Thư Mục

`	ext
Thuyet Trinh/
├── Xây dựng hệ thống phát hiện đăng nhập bất thường dựa trên hành vi người dùng.pptx # Slide báo cáo thuyết trình PowerPoint
├── slide.pdf                                                                       # Bản slide thuyết trình định dạng PDF
├── demo.mp4                                                                        # Video ghi hình kịch bản thực nghiệm và demo hệ thống
└── README.md                                                                       # Tài liệu mô tả nội dung thư mục (File này)
`

---

## 🎯 Nội Dung Trọng Tâm Trong Báo Cáo

1. **Tổng quan về rủi ro bảo mật xác thực danh tính:**
   * Các kiểu tấn công phổ biến nhắm vào tài khoản người dùng: Từ điển / Brute-force, lộ lọt thông tin xác thực (Credential Stuffing), tấn công Man-in-the-Middle (MitM).
   * Điểm hạn chế của phương thức xác thực tĩnh truyền thống (chỉ dùng mật khẩu).

2. **Kiến trúc mô hình phát hiện dựa trên hành vi (UBA):**
   * **Thu thập ngữ cảnh (Contextual Data Collection):** Địa chỉ IP, dải mạng, Fingerprinting thiết bị, User-Agent, mốc thời gian truy cập.
   * **Đánh giá rủi ro động (Dynamic Risk Scoring):** Đối chiếu hồ sơ hành vi thông thường (baseline) để tính toán điểm bất thường.
   * **Phản hồi linh hoạt (Adaptive Authentication):** Chấp thuận cho qua, yêu cầu OTP/2FA bổ sung khi nghi ngờ, hoặc khóa tạm thời và cảnh báo quản trị viên khi điểm rủi ro vượt ngưỡng an toàn.

3. **Kịch bản thực nghiệm & Demo (video demo.mp4):**
   * Thử nghiệm mô phỏng người dùng đăng nhập hợp lệ từ môi trường quen thuộc.
   * Mô phỏng đăng nhập từ IP lạ, thiết bị mới hoặc tần suất sai mật khẩu dồn dập.
   * Đánh giá hiệu quả kích hoạt bảo vệ và cơ chế ghi log cảnh báo an ninh.