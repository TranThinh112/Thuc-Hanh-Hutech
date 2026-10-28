with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the multi-line broken strings with proper template literals or clean strings
old_snippet = '''    const confirmLock = confirm(
        "🚨 BẠN ĐANG KÍCH HOẠT CHẾ ĐỘ ĐÓNG BĂNG TÀI KHOẢN KHẨN CẤP!

" +
        "• Toàn bộ tính năng mua hàng & thanh toán sẽ bị TẠM KHÓA TRONG 30 PHÚT.
" +
        "• Kẻ gian sẽ lập tức bị cô lập và không thể rút tiền hay tạo đơn mới.

" +
        "Bạn có chắc chắn muốn tiến hành bảo vệ tài khoản ngay lúc này?"
    );'''

new_snippet = '''    const confirmLock = confirm(
        "🚨 BẠN ĐANG KÍCH HOẠT CHẾ ĐỘ ĐÓNG BĂNG TÀI KHOẢN KHẨN CẤP!\\n\\n" +
        "• Toàn bộ tính năng mua hàng & thanh toán sẽ bị TẠM KHÓA TRONG 30 PHÚT.\\n" +
        "• Kẻ gian sẽ lập tức bị cô lập và không thể rút tiền hay tạo đơn mới.\\n\\n" +
        "Bạn có chắc chắn muốn tiến hành bảo vệ tài khoản ngay lúc này?"
    );'''

if old_snippet in text:
    text = text.replace(old_snippet, new_snippet)
    with open('python_app/static/app.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed snippet successfully!")
else:
    print("Exact snippet not matched, inspecting lines...")
