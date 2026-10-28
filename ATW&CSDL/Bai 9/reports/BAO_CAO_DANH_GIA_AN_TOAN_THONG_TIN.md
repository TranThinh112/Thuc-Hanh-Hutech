# BÁO CÁO ĐÁNH GIÁ AN TOÀN THÔNG TIN ỨNG DỤNG WEB
**Môn học:** An Toàn Thông Tin / An Ninh Mạng  
**Bài thực hành:** Đánh giá an toàn thông tin cho ứng dụng web  
**Mục tiêu kiểm thử:** Ứng dụng mẫu `SecureApp Vulnerable Lab` (http://localhost:3000)  
**Thời gian thực hiện:** Tháng 10/2026  
**Phương pháp tiếp cận:** Blackbox / Graybox Testing kết hợp Thủ công (Manual) & Công cụ Proxy (Burp Suite, OWASP ZAP)

---

## 1. TỔNG QUAN VÀ PHẠM VI ĐÁNH GIÁ (SCOPE)

### 1.1. Mục tiêu
- Khảo sát bề mặt tấn công của ứng dụng web.
- Xác định các điểm yếu theo chuẩn quốc tế **OWASP Top 10**.
- Đưa ra bằng chứng khai thác (Proof of Concept - PoC) và đánh giá mức độ ảnh hưởng.
- Đề xuất giải pháp khắc phục triệt để bằng mã nguồn và cấu hình máy chủ.

### 1.2. Phạm vi kiểm thử (Scope)
| URL / Endpoint | Phương thức HTTP | Chức năng | Tham số / Input |
|---|---|---|---|
| `/login` | GET / POST | Đăng nhập tài khoản | `username`, `password` |
| `/products` | GET | Tìm kiếm sản phẩm | `q` |
| `/feedback` | GET / POST | Góp ý phản hồi | `author`, `content` |
| `/profile` | GET | Xem hồ sơ người dùng | `id` |
| `/admin` | GET | Trang quản trị hệ thống | Headers (`X-Role-Override`) |

---

## 2. TỔNG HỢP KẾT QUẢ ĐÁNH GIÁ (EXECUTIVE SUMMARY)

| Mã lỗ hổng | Tên lỗ hổng bảo mật | Mức độ nghiêm trọng | Trạng thái xác nhận | Chuẩn OWASP |
|---|---|---|---|---|
| **VULN-01** | SQL Injection (Authentication Bypass & UNION-based) | **CRITICAL (Nghiêm trọng)** | Đã khai thác thành công | OWASP A03:2021 - Injection |
| **VULN-02** | Stored & Reflected Cross-Site Scripting (XSS) | **HIGH (Cao)** | Đã khai thác thành công | OWASP A03:2021 - Injection |
| **VULN-03** | Broken Access Control (IDOR - Lộ thông tin cá nhân) | **HIGH (Cao)** | Đã khai thác thành công | OWASP A01:2021 - Broken Access Control |
| **VULN-04** | Broken Access Control (Bypass quyền Admin bằng Header) | **CRITICAL (Nghiêm trọng)** | Đã khai thác thành công | OWASP A01:2021 - Broken Access Control |
| **VULN-05** | Broken Authentication & Session Management (Lộ Plaintext Password & Missing Cookie Flags) | **MEDIUM (Trung bình)** | Đã khai thác thành công | OWASP A07:2021 - Identification & Auth Failures |

---

## 3. CHI TIẾT CÁC LỖ HỔNG VÀ BẰNG CHỨNG KHAI THÁC (FINDINGS & POC)

### 3.1. VULN-01: SQL Injection (SQLi)
- **Mức độ rủi ro:** **CRITICAL** (CVSS v3.1: 9.8)
- **Vị trí phát hiện:**
  1. Endpoint `/login` (Tham số `username`).
  2. Endpoint `/products` (Tham số `q`).

#### A. Khai thác vượt qua xác thực (Authentication Bypass):
- **Phân tích nguyên nhân:** Câu lệnh SQL được tạo bằng cách nối chuỗi trực tiếp:
  ```javascript
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  ```
- **Payload sử dụng:** `admin' --` hoặc `' OR 1=1 --`
- **Request mẫu:**
  ```http
  POST /login HTTP/1.1
  Host: localhost:3000
  Content-Type: application/x-www-form-urlencoded

  username=admin%27+--&password=any
  ```
- **Kết quả:** Truy vấn trở thành `SELECT * FROM users WHERE username = 'admin' -- ...`. Kẻ tấn công đăng nhập thành công vào tài khoản Quản trị viên (`admin`) mà không cần mật khẩu.

#### B. Khai thác trích xuất toàn bộ cơ sở dữ liệu (UNION-based SQLi):
- **Payload sử dụng trên thanh tìm kiếm:**
  ```text
  ' UNION SELECT id, username, password, role FROM users --
  ```
- **Request mẫu:**
  ```http
  GET /products?q='%20UNION%20SELECT%20id,%20username,%20password,%20role%20FROM%20users%20-- HTTP/1.1
  Host: localhost:3000
  ```
- **Kết quả thu được:** Hệ thống trả về toàn bộ danh sách tài khoản, bao gồm mật khẩu dạng plaintext (`admin123`, `password123`).

#### Giải pháp khắc phục:
Sử dụng **Parameterized Queries (Prepared Statements)**:
```javascript
// Khắc phục trên /login
const stmt = db.prepare('SELECT * FROM users WHERE username = ? AND password = ?');
const user = stmt.get(username, hashedPassword);

// Khắc phục trên /products
const stmt = db.prepare('SELECT id, name, price, description FROM products WHERE name LIKE ?');
const items = stmt.all(`%${q}%`);
```

---

### 3.2. VULN-02: Cross-Site Scripting (XSS)
- **Mức độ rủi ro:** **HIGH** (CVSS v3.1: 8.2)
- **Phân loại:**
  1. **Reflected XSS:** Tại chức năng tìm kiếm `/products?q=...`
  2. **Stored XSS (Persistent):** Tại chức năng gửi góp ý `/feedback`

#### A. Khai thác Reflected XSS:
- **Request:**
  ```http
  GET /products?q=<script>alert('Reflected-XSS')</script> HTTP/1.1
  Host: localhost:3000
  ```
- **Kết quả:** Ứng dụng in trực tiếp giá trị tham số `q` vào tài liệu HTML mà không qua xử lý. Trình duyệt thực thi đoạn mã script độc hại.

#### B. Khai thác Stored XSS:
- **Request:**
  ```http
  POST /feedback HTTP/1.1
  Host: localhost:3000
  Content-Type: application/x-www-form-urlencoded

  author=Hacker&content=<script>alert(document.cookie)</script>
  ```
- **Kết quả:** Script độc hại được lưu trực tiếp vào database. Bất kỳ người dùng hoặc quản trị viên nào truy cập trang `/feedback` đều bị kích hoạt mã độc, dẫn tới việc bị đánh cắp Cookie phiên làm việc hoặc giả mạo thao tác (Session Hijacking).

#### Giải pháp khắc phục:
1. **HTML Entity Encoding:** Mã hóa mọi dữ liệu đầu vào trước khi in ra HTML (chuyển đổi `<` thành `&lt;`, `>` thành `&gt;`, `"` thành `&quot;`, `&` thành `&amp;`).
2. **Cấu hình Content Security Policy (CSP):**
   ```http
   Content-Security-Policy: default-src 'self'; script-src 'self';
   ```

---

### 3.3. VULN-03: Insecure Direct Object Reference (IDOR)
- **Mức độ rủi ro:** **HIGH** (CVSS v3.1: 7.5)
- **Vị trí phát hiện:** Endpoint `/profile?id={user_id}`

#### Bằng chứng khai thác:
- Kẻ tấn công không cần đăng nhập, chỉ cần duyệt URL bằng cách thay đổi giá trị `id`:
  - `http://localhost:3000/profile?id=1` -> Đọc toàn bộ hồ sơ bí mật của Admin.
  - `http://localhost:3000/profile?id=2` -> Đọc hồ sơ của John Doe.
  - `http://localhost:3000/profile?id=3` -> Đọc hồ sơ của Jane Smith.
- **Nguyên nhân:** Ứng dụng tin tưởng trực tiếp tham số người dùng truyền lên mà không kiểm tra xem phiên hiện tại có quyền sở hữu tài nguyên hay không.

#### Giải pháp khắc phục:
Kiểm tra phiên đăng nhập và quyền truy cập trước khi trả về dữ liệu:
```javascript
app.get('/profile', (req, res) => {
  if (!req.user) {
    return res.status(401).redirect('/login');
  }
  // Chỉ cho phép xem hồ sơ của chính mình hoặc phải có role admin
  const requestedId = parseInt(req.query.id);
  if (req.user.id !== requestedId && req.user.role !== 'admin') {
    return res.status(403).send("Bạn không có quyền xem hồ sơ này!");
  }
  // Tiếp tục xử lý...
});
```

---

### 3.4. VULN-04: Broken Access Control & Privilege Escalation
- **Mức độ rủi ro:** **CRITICAL** (CVSS v3.1: 9.1)
- **Vị trí phát hiện:** Endpoint `/admin`

#### Bằng chứng khai thác:
1. Người dùng thông thường hoặc khách vãng lai truy cập `/admin` nhận mã phản hồi `403 Forbidden`.
2. Khi kẻ tấn công chèn thêm HTTP Header tuỳ biến `X-Role-Override: admin` vào request thông qua Burp Suite:
   ```http
   GET /admin HTTP/1.1
   Host: localhost:3000
   X-Role-Override: admin
   ```
3. Máy chủ lập tức cấp quyền truy cập đầy đủ vào trang Admin và hiển thị toàn bộ mật khẩu người dùng trong cơ sở dữ liệu.

#### Giải pháp khắc phục:
- Không bao giờ dựa vào các header từ client gửi lên để xác định vai trò.
- Quyền hạn (Role / Permission) bắt buộc phải được lưu trữ phía Server trong Database hoặc Session đã ký số an toàn (JWT có Secret Key vững chắc).

---

### 3.5. VULN-05: Broken Authentication & Insecure Session Cookie
- **Mức độ rủi ro:** **MEDIUM** (CVSS v3.1: 6.5)
- **Phân tích:**
  1. Cookie `auth_token` được sinh ra theo quy tắc tĩnh (`session_{username}_token_...`), kẻ tấn công có thể dễ dàng đoán trước token của người khác.
  2. Mật khẩu lưu trữ trong database ở dạng thô (**Plaintext**), không qua băm (Hashing) như `bcrypt` hay `Argon2`.
  3. Header thiết lập cookie thiếu các cờ bảo mật quan trọng:
     - Thiếu `HttpOnly`: Cho phép mã JavaScript (qua XSS) đánh cắp cookie.
     - Thiếu `Secure`: Cookie truyền qua HTTP thường, dễ bị bắt lén (Sniffing).
     - Thiếu `SameSite=Strict/Lax`: Dễ bị tấn công CSRF.

#### Giải pháp khắc phục:
1. Băm mật khẩu bằng thư viện `bcrypt`:
   ```javascript
   const bcrypt = require('bcrypt');
   const hashedPassword = await bcrypt.hash(password, 12);
   ```
2. Sinh Session ID ngẫu nhiên bằng `crypto.randomBytes(32).toString('hex')`.
3. Thiết lập cookie với đầy đủ cờ bảo mật:
   ```javascript
   res.cookie('auth_token', token, {
     httpOnly: true,
     secure: true, // bật khi chạy HTTPS
     sameSite: 'strict',
     maxAge: 3600000 // 1 giờ
   });
   ```

---

## 4. KẾ HOẠCH VÀ KHUYẾN NGHỊ TỔNG THỂ (REMEDIATION ROADMAP)

1. **Ngắn hạn (Ngay lập tức):**
   - Áp dụng Prepared Statements cho toàn bộ câu lệnh SQL.
   - Thêm bộ lọc HTML Entity Encoding tại các view template.
   - Bổ sung cờ `HttpOnly` cho Cookie xác thực.

2. **Trung hạn:**
   - Loại bỏ toàn bộ logic kiểm tra quyền dựa trên Client Header.
   - Thiết kế phân quyền RBAC (Role-Based Access Control) chặt chẽ tại tầng Backend.
   - Triển khai thuật toán băm mật khẩu chuẩn công nghiệp (Argon2id hoặc Bcrypt).

3. **Dài hạn:**
   - Đưa việc kiểm thử bảo mật (SAST/DAST) vào quy trình CI/CD.
   - Cấu hình tường lửa ứng dụng web (WAF) và áp dụng chính sách CSP.

---
**Người thực hiện đánh giá:** Chuyên viên An Toàn Thông Tin  
**Kết luận:** Ứng dụng đã được ghi nhận toàn diện các lỗ hổng thực tế theo chuẩn OWASP và sẵn sàng cho công tác vá lỗi (Patching).
