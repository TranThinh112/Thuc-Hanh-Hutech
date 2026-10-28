with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Upgrade Checkout Modal Form
old_form_marker = '<form id="checkout-form" onsubmit="submitPayment(event)" class="space-y-4 text-xs">'
new_form_content = """<form id="checkout-form" onsubmit="submitPayment(event)" class="space-y-4 text-xs">
                <!-- Customer Information Section -->
                <div class="p-3 bg-slate-800/90 rounded-xl border border-slate-700/80 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="font-bold text-white"><i class="fa-solid fa-address-card mr-1.5 text-blue-400"></i>Thông Tin Khách Hàng & Giao Hàng</span>
                        <span id="chk-user-badge" class="text-[10px] bg-blue-500/20 text-blue-300 border border-blue-500/30 px-2 py-0.5 rounded font-mono">Tự động nhận diện</span>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block text-slate-300 mb-1">Họ và tên người nhận</label>
                            <input id="chk-cust-name" type="text" value="Thịnh" required class="w-full bg-slate-900 border border-slate-700 p-2 rounded text-white focus:outline-none focus:border-blue-500">
                        </div>
                        <div>
                            <label class="block text-slate-300 mb-1">Số điện thoại nhận tin nhắn SMS</label>
                            <input id="chk-cust-phone" type="text" value="0972445090" required class="w-full bg-slate-900 border border-slate-700 p-2 rounded text-white font-mono focus:outline-none focus:border-blue-500">
                        </div>
                    </div>
                    <div>
                        <label class="block text-slate-300 mb-1">Địa chỉ nhận hàng</label>
                        <input id="chk-cust-address" type="text" value="Số 15 Cầu Giấy, Hà Nội" required class="w-full bg-slate-900 border border-slate-700 p-2 rounded text-white focus:outline-none focus:border-blue-500">
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-slate-300 font-medium mb-1">Số tiền giao dịch (VND)</label>
                        <input id="chk-amount" type="number" readonly class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-emerald-400 font-bold text-sm">
                    </div>
                    <div>
                        <label class="block text-slate-300 font-medium mb-1">Phương thức thanh toán</label>
                        <select id="chk-pm" class="w-full bg-slate-800 border border-slate-700 p-2.5 rounded-lg text-white">
                            <option value="VISA">Thẻ Quốc Tế VISA Credit</option>
                            <option value="MASTERCARD">Thẻ MasterCard</option>
                            <option value="MOMO">Ví Điện Tử MoMo</option>
                            <option value="COD">Thanh Toán Khi Nhận Hàng (COD)</option>
                        </select>
                    </div>
                </div>

                <!-- Accordion for Fraud Simulation Override (Hidden by default for realistic UX) -->
                <div class="border border-slate-700/80 rounded-xl overflow-hidden bg-slate-800/40">
                    <button type="button" onclick="toggleSimAccordion()" class="w-full px-3 py-2.5 flex items-center justify-between text-left bg-slate-800/80 hover:bg-slate-800 transition text-slate-300 font-semibold text-xs">
                        <span class="flex items-center text-amber-400">
                            <i class="fa-solid fa-flask mr-2 text-amber-400"></i>Tùy chọn giả lập IP & Thiết bị (Dành cho Thử nghiệm & Demo Gian Lận)
                        </span>
                        <i id="sim-acc-icon" class="fa-solid fa-chevron-down text-slate-400 text-xs transition-transform"></i>
                    </button>
                    <div id="sim-acc-body" class="hidden p-3 space-y-3 bg-slate-900/70 border-t border-slate-800">
                        <p class="text-[11px] text-slate-400">
                            💡 <em>Trong môi trường thực tế, IP và Thiết bị được hệ thống tự động băm (hash) và nhận diện ngầm. Các ô dưới đây dùng để bạn chủ động đổi IP/Thiết bị nhằm kích hoạt các kịch bản AI phát hiện gian lận.</em>
                        </p>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                            <div>
                                <label class="block text-slate-400 mb-1">Địa chỉ IP</label>
                                <input id="chk-ip" type="text" value="113.161.44.12" class="w-full bg-slate-950 border border-slate-700 p-2 rounded text-slate-200 font-mono text-[11px]">
                            </div>
                            <div>
                                <label class="block text-slate-400 mb-1">Mã Thiết Bị (Device ID)</label>
                                <input id="chk-device" type="text" value="device_thinh_iphone" class="w-full bg-slate-950 border border-slate-700 p-2 rounded text-slate-200 font-mono text-[11px]">
                            </div>
                            <div>
                                <label class="block text-slate-400 mb-1">Thành Phố / Quốc Gia</label>
                                <input id="chk-city" type="text" value="Hà Nội" class="w-full bg-slate-950 border border-slate-700 p-2 rounded text-slate-200 text-[11px]">
                            </div>
                        </div>
                        <div class="flex flex-wrap items-center gap-2 pt-1">
                            <span class="text-[10px] text-slate-400 font-semibold">Chọn nhanh kịch bản:</span>
                            <button type="button" onclick="setPreset('legit')" class="px-2.5 py-1 bg-emerald-950/70 hover:bg-emerald-900 border border-emerald-600/60 text-emerald-300 rounded text-[11px]">
                                <i class="fa-solid fa-check mr-1"></i>Hợp Lệ (Hà Nội, IP Quen)
                            </button>
                            <button type="button" onclick="setPreset('ato')" class="px-2.5 py-1 bg-red-950/70 hover:bg-red-900 border border-red-600/60 text-red-300 rounded text-[11px]">
                                <i class="fa-solid fa-skull mr-1"></i>Chiếm Đoạt (Tokyo, IP Hacker Tor)
                            </button>
                            <button type="button" onclick="setPreset('travel')" class="px-2.5 py-1 bg-purple-950/70 hover:bg-purple-900 border border-purple-600/60 text-purple-300 rounded text-[11px]">
                                <i class="fa-solid fa-plane mr-1"></i>Di Chuyển Bất Khả Thi (London)
                            </button>
                        </div>
                    </div>
                </div>
"""

# Replace the old form starting portion up to the submit button
form_sub_idx = html.find('<button type="submit" class="w-full bg-gradient-to-r from-blue-600')
if form_sub_idx > 0 and "chk-cust-name" not in html:
    form_start_idx = html.find(old_form_marker)
    html = html[:form_start_idx] + new_form_content + html[form_sub_idx:]

# 2. Upgrade Result Modal with Smartphone SMS Mockup
old_res_modal_start = '<!-- PAYMENT RESULT DIALOG -->'
old_res_modal_end = '<footer class="border-t border-slate-800'
res_start = html.find(old_res_modal_start)
res_end = html.find(old_res_modal_end)

new_res_modal = """<!-- PAYMENT RESULT DIALOG & SMARTPHONE SMS MOCKUP -->
    <div id="result-modal" class="fixed inset-0 z-50 hidden bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="glass-card bg-slate-900 w-full max-w-2xl rounded-2xl border border-slate-700 shadow-2xl p-6 space-y-4 max-h-[95vh] overflow-y-auto">
            <!-- Header Result -->
            <div class="flex items-center space-x-3 pb-3 border-b border-slate-800">
                <div id="res-icon" class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0"></div>
                <div class="flex-1">
                    <h3 id="res-title" class="text-lg font-bold text-white"></h3>
                    <p id="res-subtitle" class="text-xs text-slate-400 mt-0.5"></p>
                </div>
                <button onclick="closeResultModal()" class="text-slate-400 hover:text-white"><i class="fa-solid fa-xmark text-lg"></i></button>
            </div>

            <!-- Detailed Explanation Box for Customer -->
            <div id="res-explanation-box" class="p-3.5 rounded-xl border space-y-2 text-xs">
                <div class="flex justify-between items-center font-bold">
                    <span id="res-status-label" class="flex items-center"></span>
                    <span id="res-score-badge" class="px-2 py-0.5 rounded text-[11px] font-mono"></span>
                </div>
                <p id="res-explanation-text" class="text-slate-200 leading-relaxed"></p>
            </div>

            <!-- Smartphone SMS Notification Mockup -->
            <div class="border border-slate-700/80 rounded-2xl overflow-hidden bg-slate-950 p-4 shadow-xl">
                <div class="flex items-center justify-between text-[11px] text-slate-400 pb-2 border-b border-slate-800">
                    <div class="flex items-center space-x-2">
                        <i class="fa-solid fa-mobile-screen text-blue-400"></i>
                        <span class="font-semibold text-slate-300">Tin nhắn SMS xác thực gửi đến điện thoại</span>
                    </div>
                    <div class="flex items-center space-x-2 font-mono text-[10px]">
                        <span id="sms-phone-target" class="text-blue-400 font-bold">0972445090</span>
                        <span><i class="fa-solid fa-signal mr-1"></i>5G</span>
                    </div>
                </div>

                <!-- Phone SMS Screen Body -->
                <div class="pt-3 space-y-2">
                    <div class="flex items-center space-x-2">
                        <div class="w-7 h-7 rounded-full bg-blue-600/30 border border-blue-500/50 flex items-center justify-center text-blue-400 text-xs">
                            <i class="fa-solid fa-comment-sms"></i>
                        </div>
                        <div>
                            <span class="font-bold text-white text-xs">SECURE-PAY</span>
                            <span class="text-[10px] text-slate-400 ml-1.5 font-mono" id="sms-time">Vừa xong</span>
                        </div>
                    </div>
                    <div id="sms-bubble" class="p-3 rounded-2xl text-xs font-sans leading-relaxed border shadow-md">
                        <!-- SMS Content will be populated here -->
                    </div>
                </div>
            </div>

            <button onclick="closeResultModal()" class="w-full bg-slate-800 hover:bg-slate-700 font-bold py-2.5 rounded-xl text-white text-xs transition">
                Đóng thông báo
            </button>
        </div>
    </div>
"""

if res_start > 0 and res_end > 0:
    html = html[:res_start] + new_res_modal + html[res_end:]

# 3. Upgrade Admin Transactions Audit Table Headers
old_thead_search = '<tbody id="transactions-tbody">'
new_thead_content = """                        <thead>
                            <tr class="border-b border-slate-800 text-slate-400 text-xs">
                                <th class="p-3">Mã GD (ID)</th>
                                <th class="p-3">Tên Khách Hàng & SĐT</th>
                                <th class="p-3">Sản Phẩm & Số Tiền</th>
                                <th class="p-3">Trạng Thái & Rủi Ro</th>
                                <th class="p-3">Lý Do Block / Đánh Giá AI</th>
                                <th class="p-3 text-center">Thao Tác Quản Trị</th>
                            </tr>
                        </thead>
                        <tbody id="transactions-tbody">"""

thead_start = html.find('<thead>\n                            <tr class="border-b border-slate-800 text-slate-400 text-xs">')
if thead_start > 0 and old_thead_search in html:
    tbody_idx = html.find(old_thead_search)
    html = html[:thead_start] + new_thead_content + html[tbody_idx + len(old_thead_search):]

with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html part 2 (Checkout, Result SMS Mockup, Audit Table) patched successfully!")
