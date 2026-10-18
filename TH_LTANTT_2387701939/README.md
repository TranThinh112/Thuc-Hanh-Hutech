# Thực Hành Lập Trình An Toàn Thông Tin (TH_LTANTT)

Thư mục lưu trữ bài làm và mã nguồn thực hành môn **Lập trình An toàn Thông tin** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Chuyên ngành:** An toàn Thông tin

---

## Mục Tiêu & Nội Dung Môn Học
Học phần trang bị kiến thức lập trình chuyên sâu phục vụ lĩnh vực bảo mật và an toàn thông tin:
1. **Lập trình Mạng Căn bản & Bảo mật:**
   * Lập trình Socket TCP/UDP Client - Server bằng ngôn ngữ Python.
   * Xây dựng công cụ dò quét cổng mạng (Port Scanner), nhận diện dịch vụ và banner grabbing.
2. **Mật Mã Học Ứng Dụng (Cryptography):**
   * Các hàm băm một chiều (MD5, SHA-256, SHA-512) và kiểm tra tính toàn vẹn thông điệp.
   * Mã hóa đối xứng (AES, DES, Caesar, Vigenère).
   * Mã hóa bất đối xứng (RSA, trao đổi khóa Diffie-Hellman, chữ ký số).
3. **Phân Tích Lưu Lượng & An Toàn Ứng Dụng:**
   * Đánh chặn gói tin, kiểm tra tính bảo mật của các giao thức truyền tải dữ liệu.
   * Lập trình phòng thủ và xử lý ngoại lệ trong môi trường mạng không tin cậy.

---

## Cấu Trúc Thư Mục
* `Buoi 4_14_10_26/`: Thư mục bài tập thực hành buổi 4 (ngày 14/10/2026).
* Các thư mục bài tập tiếp theo sẽ được cập nhật tương ứng theo tiến độ học tập trên lớp.

---

## Môi Trường & Công Cụ Yêu Cầu
* **Ngôn ngữ:** Python 3.10+
* **IDE / Trình soạn thảo:** Visual Studio Code / PyCharm.
* **Các thư viện Python thông dụng:**
  ```bash
  pip install pycryptodome cryptography requests scapy
  ```