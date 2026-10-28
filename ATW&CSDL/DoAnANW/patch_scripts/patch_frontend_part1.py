# Python script to update python_app/static/index.html
import re

with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Navigation Header
old_header_search = '<button onclick="toggleCartModal()"'
new_header_elements = """<!-- User Profile & Auth Capsule -->
                <div id="user-auth-capsule" class="flex items-center space-x-2 bg-slate-800/90 border border-slate-700 px-3 py-1.5 rounded-xl text-xs">
                    <div class="w-7 h-7 rounded-full bg-blue-600/30 border border-blue-500/50 flex items-center justify-center text-blue-400 font-bold">
                        <i class="fa-solid fa-user"></i>
                    </div>
                    <div class="leading-tight">
                        <div class="flex items-center space-x-1.5">
                            <span id="nav-user-name" class="font-bold text-white">Thịnh</span>
                            <span id="nav-user-role" class="text-[10px] px-1.5 py-0.2 rounded font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">USER</span>
                        </div>
                        <span id="nav-user-phone" class="text-[10px] text-slate-400 font-mono">0972445090</span>
                    </div>
                    <button onclick="openTokenModal()" title="Xem Access Token & Refresh Token JWT" class="ml-1 p-1.5 bg-slate-700/80 hover:bg-slate-700 text-yellow-400 rounded-lg text-xs transition">
                        <i class="fa-solid fa-key"></i>
                    </button>
                    <button onclick="openLoginModal()" title="Đổi tài khoản đăng nhập" class="p-1.5 bg-slate-700/80 hover:bg-slate-700 text-slate-300 rounded-lg text-xs transition">
                        <i class="fa-solid fa-right-left"></i>
                    </button>
                    <button onclick="logout()" title="Đăng xuất" class="p-1.5 bg-slate-700/80 hover:bg-red-900/60 text-red-400 rounded-lg text-xs transition">
                        <i class="fa-solid fa-arrow-right-from-bracket"></i>
                    </button>
                </div>

                <button onclick="toggleCartModal()" """

if "user-auth-capsule" not in html:
    html = html.replace(old_header_search, new_header_elements, 1)

# Ensure Admin button has id="nav-admin-btn" and Storefront button exists
old_admin_btn = '<button onclick="showView(\'admin\')"'
new_admin_btn = """<button id="nav-store-btn" onclick="showView('store')" class="hidden bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs px-3.5 py-2 rounded-lg transition border border-slate-700">
                    <i class="fa-solid fa-store mr-1.5 text-blue-400"></i> Xem Cửa Hàng
                </button>
                <button id="nav-admin-btn" onclick="showView('admin')" """

if "nav-admin-btn" not in html:
    html = html.replace(old_admin_btn, new_admin_btn, 1)

# 2. Add Login Modal and Token Modal before </body>
login_modals_html = """
    <!-- ================================================================= -->
    <!-- AUTHENTICATION & LOGIN MODAL -->
    <!-- ================================================================= -->
    <div id="login-modal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="glass-card bg-slate-900 w-full max-w-md rounded-2xl border border-slate-700 shadow-2xl p-6 space-y-5">
            <div class="flex justify-between items-center pb-3 border-b border-slate-800">
                <div class="flex items-center space-x-2.5">
                    <div class="w-9 h-9 rounded-xl bg-blue-600/30 border border-blue-500/40 flex items-center justify-center text-blue-400 text-lg">
                        <i class="fa-solid fa-shield-halved"></i>
                    </div>
                    <div>
                        <h3 class="text-base font-bold text-white">Đăng Nhập Hệ Thống</h3>
                        <p class="text-[11px] text-slate-400">Website TMĐT & AI Phát Hiện Gian Lận</p>
                    </div>
                </div>
                <button onclick="closeLoginModal()" class="text-slate-400 hover:text-white text-sm"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>

            <!-- Quick 1-Click Demo Login -->
            <div class="space-y-2">
                <label class="block text-[11px] font-semibold text-blue-400 uppercase tracking-wider">
                    <i class="fa-solid fa-bolt mr-1"></i>Chọn nhanh tài khoản mẫu (1-Click Login):
                </label>
                <div class="grid grid-cols-2 gap-2">
                    <button type="button" onclick="quickLogin('thinh')" class="p-2.5 rounded-xl bg-slate-800/90 hover:bg-blue-950/60 border border-slate-700 hover:border-blue-500 text-left transition group">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-xs text-white group-hover:text-blue-300">Thịnh</span>
                            <span class="text-[9px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-bold">USER</span>
                        </div>
                        <div class="text-[10px] text-slate-400 font-mono mt-0.5">0972445090</div>
                    </button>
                    <button type="button" onclick="quickLogin('dat')" class="p-2.5 rounded-xl bg-slate-800/90 hover:bg-blue-950/60 border border-slate-700 hover:border-blue-500 text-left transition group">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-xs text-white group-hover:text-blue-300">Đạt</span>
                            <span class="text-[9px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-bold">USER</span>
                        </div>
                        <div class="text-[10px] text-slate-400 font-mono mt-0.5">0981234567</div>
                    </button>
                    <button type="button" onclick="quickLogin('dong')" class="p-2.5 rounded-xl bg-slate-800/90 hover:bg-blue-950/60 border border-slate-700 hover:border-blue-500 text-left transition group">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-xs text-white group-hover:text-blue-300">Đông</span>
                            <span class="text-[9px] bg-emerald-500/20 text-emerald-400 px-1.5 py-0.2 rounded font-bold">USER</span>
                        </div>
                        <div class="text-[10px] text-slate-400 font-mono mt-0.5">0977654321</div>
                    </button>
                    <button type="button" onclick="quickLogin('admin')" class="p-2.5 rounded-xl bg-gradient-to-r from-purple-950/50 to-blue-950/50 hover:from-purple-900/60 hover:to-blue-900/60 border border-purple-600/50 text-left transition group">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-xs text-purple-300">Quản Trị Viên</span>
                            <span class="text-[9px] bg-purple-500/30 text-purple-300 px-1.5 py-0.2 rounded font-bold">ADMIN</span>
                        </div>
                        <div class="text-[10px] text-slate-400 font-mono mt-0.5">admin (Toàn quyền)</div>
                    </button>
                </div>
            </div>

            <div class="relative flex py-1 items-center">
                <div class="flex-grow border-t border-slate-800"></div>
                <span class="flex-shrink mx-3 text-[10px] text-slate-500 uppercase">Hoặc đăng nhập thủ công</span>
                <div class="flex-grow border-t border-slate-800"></div>
            </div>

            <!-- Manual Form -->
            <form onsubmit="handleManualLogin(event)" class="space-y-3 text-xs">
                <div>
                    <label class="block text-slate-300 mb-1">Tên đăng nhập hoặc Số điện thoại</label>
                    <input id="login-username" type="text" placeholder="thinh / 0972445090 / admin" required class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-white focus:outline-none focus:border-blue-500">
                </div>
                <div>
                    <label class="block text-slate-300 mb-1">Mật khẩu (mặc định: 123)</label>
                    <input id="login-password" type="password" value="123" required class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-white focus:outline-none focus:border-blue-500">
                </div>
                <div id="login-error" class="hidden text-red-400 text-[11px] bg-red-950/50 border border-red-800/50 p-2 rounded-lg"></div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 font-bold py-2.5 rounded-xl text-white text-xs transition shadow-lg">
                    <i class="fa-solid fa-right-to-bracket mr-1.5"></i>Đăng Nhập
                </button>
            </form>
        </div>
    </div>

    <!-- ================================================================= -->
    <!-- JWT TOKEN DETAILS VIEWER MODAL -->
    <!-- ================================================================= -->
    <div id="token-modal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="glass-card bg-slate-900 w-full max-w-xl rounded-2xl border border-slate-700 shadow-2xl p-6 space-y-4">
            <div class="flex justify-between items-center pb-3 border-b border-slate-800">
                <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-key text-yellow-400 text-lg"></i>
                    <div>
                        <h3 class="text-base font-bold text-white">Chứng Thực Danh Tính Hai Lớp (JWT Tokens)</h3>
                        <p class="text-[11px] text-slate-400">Access Token (24h) & Refresh Token (7 ngày)</p>
                    </div>
                </div>
                <button onclick="closeTokenModal()" class="text-slate-400 hover:text-white"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>
            <div class="space-y-3 text-xs">
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <span class="font-bold text-blue-400">1. Access Token (Bearer Token):</span>
                        <span class="text-[10px] text-slate-400">Dùng gửi Header Authorization</span>
                    </div>
                    <textarea id="modal-access-token" readonly rows="3" class="w-full bg-slate-950 border border-slate-800 font-mono text-[10px] text-slate-300 p-2.5 rounded-lg select-all"></textarea>
                </div>
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <span class="font-bold text-purple-400">2. Refresh Token:</span>
                        <span class="text-[10px] text-slate-400">Dùng cấp mới Access Token khi hết hạn</span>
                    </div>
                    <textarea id="modal-refresh-token" readonly rows="3" class="w-full bg-slate-950 border border-slate-800 font-mono text-[10px] text-slate-300 p-2.5 rounded-lg select-all"></textarea>
                </div>
                <div class="flex items-center justify-between pt-2 border-t border-slate-800">
                    <span class="text-[11px] text-slate-400">Kiểm thử API cấp mới token:</span>
                    <button onclick="testRefreshToken()" class="px-3 py-1.5 bg-purple-700 hover:bg-purple-600 text-white rounded-lg text-xs font-semibold transition">
                        <i class="fa-solid fa-arrows-rotate mr-1"></i>Thử Refresh Token Ngay
                    </button>
                </div>
            </div>
        </div>
    </div>
"""

if "login-modal" not in html:
    html = html.replace("</body>", login_modals_html + "\n</body>", 1)

with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html part 1 (Header, Login Modal, Token Modal) patched successfully!")
