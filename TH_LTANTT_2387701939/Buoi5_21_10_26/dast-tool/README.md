# ⚡ DAST Tool - Dynamic Application Security Testing cho Python

Bộ công cụ kiểm thử bảo mật động (DAST) chạy trong thời gian thực, cung cấp khả năng giám sát tài nguyên tiến trình, phát hiện rò rỉ bộ nhớ, thống kê lưu lượng mạng, kiểm tra hành vi độc hại qua Sandbox cô lập và cung cấp RESTful API qua Flask.

---

## 📌 Các Tính Năng Chính

1. **Giám sát Tiến trình (Runtime Monitor):** Đo lường mức độ sử dụng CPU, RAM và danh sách tập tin đang mở (open file descriptors) của một tiến trình hệ thống theo PID thông qua psutil.
2. **Phân tích Rò rỉ Bộ nhớ (Memory Leak Analyzer):** Theo dõi số lượng đối tượng không thể thu hồi qua Garbage Collection (gc.garbage) và phát hiện hiện tượng tràn số nguyên.
3. **Phân tích Lưu lượng Mạng (Network Traffic Analyzer):** Đo đạc dung lượng gói tin gửi/nhận (bytes sent/received) trên toàn bộ các card mạng hệ thống.
4. **Kiểm tra Hành vi Độc hại (Security Behavior Checker):** Nhận diện các lệnh thực thi nguy hiểm cấp hệ thống như os.system, subprocess, val, xec.
5. **Môi trường Cách ly (Virtual Sandbox):** Chạy thử nghiệm các câu lệnh shell trong môi trường thư mục tạm cô lập an toàn, tự động dọn dẹp sau khi thực thi.
6. **RESTful Web API (Flask Server):** Cung cấp các endpoint HTTP JSON cho phép tích hợp vào các hệ thống giám sát tập trung.

---

## 📁 Cấu Trúc Thư Mục

`	ext
dast-tool/
├── __init__.py
├── runtime_monitor.py          # Module giám sát tài nguyên CPU, RAM, open files
├── memory_analyzer.py          # Module phân tích bộ nhớ và Garbage Collection
├── network_traffic_analyzer.py # Module đo lưu lượng mạng mạng vào/ra
├── security_behavior_checker.py# Module nhận diện các lệnh nguy hiểm
├── virtual_sandbox.py          # Môi trường chạy cách ly tạm thời
├── main.py                     # CLI thực thi kiểm thử độc lập
├── app.py                      # Flask RESTful API Server
├── tests/
│   ├── test_runtime_monitor.py
│   ├── test_memory_analyzer.py
│   ├── test_network_traffic_analyzer.py
│   ├── test_security_behavior_checker.py
│   └── test_virtual_sandbox.py
├── requirements.txt            # Thư viện phụ thuộc: psutil, Flask
└── README.md
`

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Cài đặt thư viện phụ thuộc

`ash
cd dast-tool
pip install -r requirements.txt
`

### 2. Chạy bộ kiểm thử tự động (Unit Tests)

`ash
python -m unittest discover tests
`
*Kết quả:* Chạy thành công toàn bộ 5/5 test cases.

### 3. Chạy script kiểm thử trực tiếp qua CLI

`ash
python main.py
`

### 4. Khởi động Web API Server

`ash
python app.py
`
Máy chủ API sẽ lắng nghe tại cổng mặc định http://127.0.0.1:5000/.

**Các API Endpoint chính:**
- GET /api/monitor?pid=<PID>: Lấy thông số CPU, RAM, file descriptor của tiến trình.
- GET /api/memory: Kiểm tra trạng thái rò rỉ bộ nhớ qua GC.
- GET /api/network: Thống kê lưu lượng mạng vào/ra.
- POST /api/check-behavior: Gửi đoạn mã Python để phân tích các hàm nguy hiểm.
- POST /api/sandbox: Chạy lệnh trong sandbox cô lập an toàn.
