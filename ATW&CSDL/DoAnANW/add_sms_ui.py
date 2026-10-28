# Script to add SMS Inbox and Floating Notifications to index.html and app.js

with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add SMS Inbox Button in Header
old_cart_btn = '<button onclick="toggleCartModal()"'
new_sms_header_btn = """<button onclick="openSmsInboxModal()" class="relative bg-slate-800 hover:bg-slate-700 px-3 py-2 rounded-lg text-slate-200 border border-slate-700 transition flex items-center space-x-1.5" title="Mở Hộp Thư Tin Nhắn SMS Của Điện Thoại">
                    <i class="fa-solid fa-comment-sms text-blue-400 text-sm"></i>
                    <span class="text-xs font-semibold hidden md:inline">Tin Nhắn SMS</span>
                    <span id="sms-unread-badge" class="bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.2 rounded-full">0</span>
                </button>
                <button onclick="toggleCartModal()" """

if "openSmsInboxModal()" not in html:
    html = html.replace(old_cart_btn, new_sms_header_btn, 1)

# 2. Add Floating Phone Widget, iOS Toast and Smartphone Modal before </body>
sms_ui_components = """
    <!-- ================================================================= -->
    <!-- FLOATING QUICK ACCESS BUTTON FOR SMARTPHONE SMS -->
    <!-- ================================================================= -->
    <div class="fixed bottom-6 right-6 z-40">
        <button onclick="openSmsInboxModal()" class="flex items-center space-x-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold px-4 py-3 rounded-full shadow-2xl border border-blue-400/40 transition transform hover:scale-105 shadow-blue-500/30">
            <i class="fa-solid fa-mobile-screen-button text-lg text-white"></i>
            <span class="text-xs font-semibold">Xem Hộp Thư SMS</span>
            <span id="sms-floating-count" class="bg-red-500 text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">...</span>
        </button>
    </div>

    <!-- ================================================================= -->
    <!-- FLOATING PUSH NOTIFICATION TOAST (IOS/ANDROID STYLE) -->
    <!-- ================================================================= -->
    <div id="ios-sms-toast" class="fixed top-5 left-1/2 -translate-x-1/2 z-50 hidden transition-all duration-300 max-w-md w-full px-4">
        <div class="glass-card bg-slate-900/95 border border-blue-500/60 rounded-2xl p-4 shadow-2xl flex items-start space-x-3 backdrop-blur-xl">
            <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white text-lg flex-shrink-0 shadow-lg shadow-blue-600/40">
                <i class="fa-solid fa-comment-sms"></i>
            </div>
            <div class="flex-1 text-xs">
                <div class="flex justify-between items-center text-slate-400 text-[10px] pb-1">
                    <span class="font-bold text-white uppercase tracking-wider">TIN NHẮN SMS MỚI TỪ SECURE-PAY</span>
                    <span>Vừa xong</span>
                </div>
                <div class="font-semibold text-blue-300 font-mono text-[11px]" id="toast-phone">0972445090</div>
                <p class="text-slate-200 mt-1 leading-relaxed" id="toast-content"></p>
            </div>
            <button onclick="closeSmsToast()" class="text-slate-400 hover:text-white text-sm"><i class="fa-solid fa-xmark"></i></button>
        </div>
    </div>

    <!-- ================================================================= -->
    <!-- SMARTPHONE SMS INBOX MODAL (SIMULATING A REAL SMARTPHONE) -->
    <!-- ================================================================= -->
    <div id="sms-inbox-modal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="glass-card bg-slate-900 w-full max-w-sm rounded-[36px] border-4 border-slate-700 shadow-2xl overflow-hidden flex flex-col h-[650px] relative">
            <!-- Phone Speaker & Notch -->
            <div class="h-7 bg-slate-950 flex items-center justify-between px-6 pt-1">
                <span class="text-[10px] text-slate-300 font-bold" id="phone-clock">14:30</span>
                <div class="w-16 h-3 bg-slate-800 rounded-full"></div>
                <div class="flex items-center space-x-1 text-[10px] text-slate-300">
                    <i class="fa-solid fa-signal"></i>
                    <i class="fa-solid fa-wifi"></i>
                    <i class="fa-solid fa-battery-full"></i>
                </div>
            </div>

            <!-- Phone Top Header -->
            <div class="bg-slate-950/95 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                <div class="flex items-center space-x-2.5">
                    <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold shadow">
                        SP
                    </div>
                    <div>
                        <h4 class="text-xs font-bold text-white">SECURE-PAY BRANDNAME</h4>
                        <p class="text-[10px] text-blue-400 font-mono font-semibold" id="phone-inbox-owner">SĐT: 0972445090</p>
                    </div>
                </div>
                <button onclick="closeSmsInboxModal()" class="w-7 h-7 rounded-full bg-slate-800 flex items-center justify-center text-slate-300 hover:text-white text-xs">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <!-- Phone Messages Scrollable Body -->
            <div id="phone-sms-list" class="flex-1 p-3 overflow-y-auto space-y-3 bg-slate-900/90 text-xs">
                <p class="text-center text-slate-500 py-6">Đang tải tin nhắn SMS...</p>
            </div>

            <!-- Phone Home Indicator Bar -->
            <div class="h-5 bg-slate-950 flex items-center justify-center">
                <div class="w-28 h-1 bg-slate-600 rounded-full"></div>
            </div>
        </div>
    </div>
"""

if "sms-inbox-modal" not in html:
    html = html.replace("</body>", sms_ui_components + "\n</body>", 1)

with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated with SMS Inbox and Floating widgets!")
