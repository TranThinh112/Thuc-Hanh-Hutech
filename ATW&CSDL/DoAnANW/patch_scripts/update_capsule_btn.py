with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_capsule = """                <div id="user-auth-capsule" class="flex items-center space-x-2 bg-slate-800/90 border border-slate-700 px-3 py-1.5 rounded-xl text-xs">
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
                </div>"""

new_capsule = """                <!-- User Profile & Auth Capsule with Explicit Action Buttons -->
                <div id="user-auth-capsule" class="flex items-center space-x-2 bg-slate-800/90 border border-slate-700 p-1.5 pl-3 rounded-xl text-xs">
                    <div class="flex items-center space-x-2 cursor-pointer hover:opacity-80 transition" onclick="openLoginModal()" title="Bấm vào để đổi tài khoản đăng nhập">
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
                    </div>
                    <button onclick="openLoginModal()" title="Mở bảng Đăng Nhập / Đổi Tài Khoản" class="px-2.5 py-1.5 bg-blue-600/80 hover:bg-blue-600 text-white rounded-lg text-xs font-semibold transition flex items-center space-x-1 shadow">
                        <i class="fa-solid fa-right-to-bracket text-xs"></i>
                        <span>Đổi Tài Khoản</span>
                    </button>
                    <button onclick="openTokenModal()" title="Xem Access Token & Refresh Token JWT" class="p-1.5 bg-slate-700/80 hover:bg-slate-700 text-yellow-400 rounded-lg text-xs transition" title="Token JWT">
                        <i class="fa-solid fa-key"></i>
                    </button>
                    <button onclick="logout()" title="Đăng xuất" class="p-1.5 bg-slate-700/80 hover:bg-red-900/60 text-red-400 rounded-lg text-xs transition">
                        <i class="fa-solid fa-arrow-right-from-bracket"></i>
                    </button>
                </div>"""

if old_capsule in html:
    html = html.replace(old_capsule, new_capsule)
    html = html.replace('/static/app.js?v=2.3', '/static/app.js?v=2.4')
    with open("python_app/static/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Capsule updated with prominent 'Đổi Tài Khoản' button!")
else:
    print("Target not found, checking...")
