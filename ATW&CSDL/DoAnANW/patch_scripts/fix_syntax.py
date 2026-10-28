with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    code = f.read()

# Replace multi-line strings inside alert() or strings
# In JS, double-quoted string with literal unescaped newlines is a SyntaxError.
code = code.replace(
    'alert("TRUY CẬP BỊ TỪ CHỐI!\n\nTài khoản của bạn (" + (currentUser?.name || "Khách") + " - " + (currentUser?.role || "USER") + ") chỉ có quyền mua sắm tại Cửa Hàng TMĐT.\nChỉ tài khoản Quản Trị Viên (ADMIN) mới có quyền truy cập Trang Quản Trị!");',
    'alert("TRUY CẬP BỊ TỪ CHỐI!\\n\\nTài khoản của bạn (" + (currentUser?.name || "Khách") + " - " + (currentUser?.role || "USER") + ") chỉ có quyền mua sắm tại Cửa Hàng TMĐT.\\nChỉ tài khoản Quản Trị Viên (ADMIN) mới có quyền truy cập Trang Quản Trị!");'
)

# Also check for alert(`Đăng nhập thành công!\nTài khoản: ${currentUser.name}\nSố điện thoại: ${currentUser.phone}\nQuyền: ${currentUser.role}`);
# template literals are allowed, but regular strings with actual newlines are not.

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Saved.")
