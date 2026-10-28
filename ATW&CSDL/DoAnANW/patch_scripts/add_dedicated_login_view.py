# Script to add dedicated Login Page view to index.html and update header

with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Header to include dedicated Login Button when not logged in
old_auth_markup = """                <!-- User Profile & Auth Capsule with Explicit Action Buttons -->
                <div id="user-auth-capsule" class="flex items-center space-x-2 bg-slate-800/90 border border-slate-700 p-1.5 pl-3 rounded-xl text-xs">"""

new_auth_markup = """                <!-- Login Button for Guest Browsing -->
                <button id="nav-login-btn" onclick="showView('login')" class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold text-xs px-4 py-2 rounded-xl transition shadow flex items-center space-x-1.5 border border-blue-400/30">
                    <i class="fa-solid fa-right-to-bracket text-xs"></i>
                    <span>Đăng Nhập</span>
                </button>

                <!-- User Profile & Auth Capsule when Logged in -->
                <div id="user-auth-capsule" class="hidden flex items-center space-x-2 bg-slate-800/90 border border-slate-700 p-1.5 pl-3 rounded-xl text-xs">"""

if old_auth_markup in html:
    html = html.replace(old_auth_markup, new_auth_markup)

# 2. Add VIEW 3: Dedicated Login View inside <main> right after VIEW 2
view_login_html = """
        <!-- ================================================================= -->
        <!-- VIEW 3: DEDICATED LOGIN PAGE (TRANG ĐĂNG NHẬP RIÊNG BIỆT) -->
        <!-- ================================================================= -->
        <div id="view-login" class="hidden max-w-lg mx-auto py-4 space-y-4">
            <!-- Back button to Storefront -->
            <button onclick="showView('store')" class="text-xs text-slate-400 hover:text-white flex items-center space-x-1.5 transition">
                <i class="fa-solid fa-arrow-left"></i>
                <span>Quay lại Cửa Hàng (Tiếp tục lướt xem sản phẩm)</span>
            </button>

            <!-- Main Login Card -->
            <div class="glass-card bg-slate-900 rounded-3xl border border-slate-700/80 shadow-2xl p-7 space-y-6">
                <!-- Header of Login Card -->
                <div class="text-center space-y-2">
                    <div class="w-14 h-14 mx-auto rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 border border-blue-400/40 flex items-center justify-center text-white text-2xl shadow-lg shadow-blue-600/30">
                        <i class="fa-solid fa-lock"></i>
                    </div>
                    <h2 class="text-xl font-extrabold text-white tracking-wide">Đăng Nhập Khách Hàng</h2>
                    <p class="text-xs text-slate-400">Đăng nhập tài khoản để đặt hàng & kích hoạt động cơ AI phát hiện gian lận thanh toán</p>
                </div>

                <!-- Alert box when redirected from checkout -->
                <div id="login-checkout-alert" class="hidden p-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-center space-x-2">
                    <i class="fa-solid fa-triangle-exclamation text-amber-400 text-sm flex-shrink-0"></i>
                    <span><strong>Lưu ý:</strong> Quý khách cần đăng nhập tài khoản để tiến hành thanh toán đơn hàng an toàn.</span>
                </div>

                <!-- Manual Login Form (Name & Password) -->
                <form onsubmit="handleDedicatedLogin(event)" class="space-y-4 text-xs">
                    <div>
                        <label class="block text-slate-300 font-semibold mb-1.5 flex items-center justify-between">
                            <span><i class="fa-solid fa-user text-blue-400 mr-1.5"></i>Tên Đăng Nhập hoặc Số Điện Thoại</span>
                            <span class="text-[10px] text-slate-400 font-normal">thinh / 0972445090</span>
                        </label>
                        <input id="dedicated-login-username" type="text" placeholder="Nhập tên đăng nhập hoặc số điện thoại..." required class="w-full bg-slate-950 border border-slate-700 p-3 rounded-xl text-white text-sm focus:outline-none focus:border-blue-500 font-mono transition">
                    </div>

                    <div>
                        <label class="block text-slate-300 font-semibold mb-1.5 flex items-center justify-between">
                            <span><i class="fa-solid fa-key text-blue-400 mr-1.5"></i>Mật Khẩu</span>
                            <span class="text-[10px] text-slate-400 font-normal">Mặc định: 123</span>
                        </label>
                        <input id="dedicated-login-password" type="password" value="123" placeholder="Nhập mật khẩu..." required class="w-full bg-slate-950 border border-slate-700 p-3 rounded-xl text-white text-sm focus:outline-none focus:border-blue-500 font-mono transition">
                    </div>

                    <div id="dedicated-login-error" class="hidden text-red-400 text-xs bg-red-950/60 border border-red-800/60 p-2.5 rounded-xl flex items-center space-x-2">
                        <i class="fa-solid fa-circle-exclamation text-red-400"></i>
                        <span id="dedicated-login-error-text"></span>
                    </div>

                    <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 font-bold py-3.5 rounded-xl text-white text-sm transition shadow-lg shadow-blue-600/30 flex items-center justify-center space-x-2">
                        <i class="fa-solid fa-right-to-bracket"></i>
                        <span>Đăng Nhập Vào Hệ Thống</span>
                    </button>
                </form>

                <!-- 1-Click Quick Demo Login Section -->
                <div class="pt-4 border-t border-slate-800 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-bold text-blue-400 uppercase tracking-wider flex items-center">
                            <i class="fa-solid fa-bolt mr-1.5 text-yellow-400"></i>Đăng Nhập Nhanh 1 Chạm (Demo):
                        </span>
                        <span class="text-[10px] text-slate-500">Mật khẩu: 123</span>
                    </div>

                    <div class="grid grid-cols-2 gap-2.5">
                        <button type="button" onclick="quickLoginDedicated('thinh')" class="p-3 rounded-xl bg-slate-800/80 hover:bg-blue-950/60 border border-slate-700 hover:border-blue-500 text-left transition group">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-white group-hover:text-blue-300">Thịnh</span>
                                <span class="text-[9px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-bold">USER</span>
                            </div>
                            <div class="text-[11px] text-slate-400 font-mono mt-1">SĐT: 0972445090</div>
                        </button>

                        <button type="button" onclick="quickLoginDedicated('dat')" class="p-3 rounded-xl bg-slate-800/80 hover:bg-blue-950/60 border border-slate-700 hover:border-blue-500 text-left transition group">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-white group-hover:text-blue-300">Đạt</span>
                                <span class="text-[9px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-bold">USER</span>
                            </div>
                            <div class="text-[11px] text-slate-400 font-mono mt-1">SĐT: 0981234567</div>
                        </button>

                        <button type="button" onclick="quickLoginDedicated('dong')" class="p-3 rounded-xl bg-slate-800/80 hover:bg-blue-950/60 border border-slate-700 hover:border-blue-500 text-left transition group">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-white group-hover:text-blue-300">Đông</span>
                                <span class="text-[9px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-bold">USER</span>
                            </div>
                            <div class="text-[11px] text-slate-400 font-mono mt-1">SĐT: 0977654321</div>
                        </button>

                        <button type="button" onclick="quickLoginDedicated('admin')" class="p-3 rounded-xl bg-gradient-to-r from-purple-950/50 to-blue-950/50 hover:from-purple-900/60 hover:to-blue-900/60 border border-purple-600/50 text-left transition group">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-xs text-purple-300">Quản Trị Viên</span>
                                <span class="text-[9px] bg-purple-500/30 text-purple-300 px-1.5 py-0.2 rounded font-bold">ADMIN</span>
                            </div>
                            <div class="text-[11px] text-slate-400 font-mono mt-1">admin (Toàn quyền)</div>
                        </button>
                    </div>
                </div>
            </div>
        </div>
"""

old_main_end = """        </div>
    </main>"""

# Find where view-admin ends in <main>
idx_view_admin = html.find('id="view-admin"')
if idx_view_admin > 0 and 'id="view-login"' not in html:
    # Insert before </main>
    idx_main_close = html.find('</main>')
    html = html[:idx_main_close] + view_login_html + "\n    " + html[idx_main_close:]

html = html.replace('/static/app.js?v=2.4', '/static/app.js?v=2.5')
html = html.replace('/static/app.js?v=2.3', '/static/app.js?v=2.5')

with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated with dedicated Login view and navigation!")
