sms_js_code = """
// =========================================================================
// SMARTPHONE SMS INBOX & FLOATING NOTIFICATIONS
// =========================================================================

async function loadSmsInbox() {
    try {
        const phone = currentUser?.phone || "0972445090";
        const url = `/api/user/sms-notifications?phone=${phone}`;
        const headers = {};
        if (accessToken) headers["Authorization"] = "Bearer " + accessToken;

        const res = await fetch(url, { headers });
        const list = await res.json();

        // Update badge counts
        const unreadCount = list.length;
        const badge1 = document.getElementById("sms-unread-badge");
        const badge2 = document.getElementById("sms-floating-count");
        if (badge1) badge1.innerText = unreadCount;
        if (badge2) badge2.innerText = unreadCount;

        const ownerEl = document.getElementById("phone-inbox-owner");
        if (ownerEl) ownerEl.innerText = `SĐT: ${phone} (${currentUser?.name || 'Khách hàng'})`;

        const clockEl = document.getElementById("phone-clock");
        if (clockEl) clockEl.innerText = new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });

        const phoneList = document.getElementById("phone-sms-list");
        if (!phoneList) return;

        if (list.length === 0) {
            phoneList.innerHTML = `
                <div class="text-center py-10 space-y-2 text-slate-500">
                    <i class="fa-regular fa-comment-dots text-3xl"></i>
                    <p class="text-xs">Chưa có tin nhắn SMS nào gửi đến số ${phone}.</p>
                </div>
            `;
            return;
        }

        phoneList.innerHTML = list.map(s => {
            const isSuccess = (s.messageType === "ORDER_SUCCESS");
            return `
                <div class="space-y-1">
                    <div class="text-center text-[10px] text-slate-500 font-mono">${s.createdAt}</div>
                    <div class="p-3 rounded-2xl text-xs font-sans leading-relaxed border shadow-md ${isSuccess ? 'bg-emerald-950/80 border-emerald-700/80 text-emerald-100' : 'bg-red-950/80 border-red-700/80 text-red-200'}">
                        <div class="flex items-center space-x-1.5 pb-1 font-bold ${isSuccess ? 'text-emerald-400' : 'text-red-400'} text-[11px]">
                            <i class="${isSuccess ? 'fa-solid fa-circle-check' : 'fa-solid fa-triangle-exclamation'}"></i>
                            <span>${isSuccess ? 'XÁC NHẬN ĐƠN HÀNG THÀNH CÔNG' : 'CẢNH BÁO AN TOÀN THANH TOÁN'}</span>
                        </div>
                        <p class="mt-0.5 leading-relaxed">${s.content}</p>
                    </div>
                </div>
            `;
        }).join("");
    } catch (e) {
        console.warn("Failed to load SMS inbox", e);
    }
}

function openSmsInboxModal() {
    loadSmsInbox();
    document.getElementById("sms-inbox-modal")?.classList.remove("hidden");
}

function closeSmsInboxModal() {
    document.getElementById("sms-inbox-modal")?.classList.add("hidden");
}

let smsToastTimer = null;
function showSmsToast(phone, content) {
    const toast = document.getElementById("ios-sms-toast");
    const phoneEl = document.getElementById("toast-phone");
    const contentEl = document.getElementById("toast-content");
    if (!toast) return;

    if (phoneEl) phoneEl.innerText = `Gửi đến: ${phone}`;
    if (contentEl) contentEl.innerText = content;

    toast.classList.remove("hidden");
    toast.classList.add("animate-bounce");
    setTimeout(() => toast.classList.remove("animate-bounce"), 1000);

    if (smsToastTimer) clearTimeout(smsToastTimer);
    smsToastTimer = setTimeout(() => {
        closeSmsToast();
    }, 9000);
}

function closeSmsToast() {
    document.getElementById("ios-sms-toast")?.classList.add("hidden");
}
"""

with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    app_text = f.read()

if "openSmsInboxModal" not in app_text:
    app_text += "\n" + sms_js_code

    # Also hook into showPaymentResult to trigger showSmsToast and loadSmsInbox
    hook_target = "showPaymentResult(data);"
    hook_replacement = """showPaymentResult(data);
        if (data.smsNotification && data.smsNotification.content) {
            showSmsToast(data.smsNotification.phone || "0972445090", data.smsNotification.content);
        }
        loadSmsInbox();"""
    app_text = app_text.replace(hook_target, hook_replacement, 1)

    # Also hook into initAuth to load inbox on startup
    hook_init = "updateAuthUI();"
    hook_init_rep = "updateAuthUI();\n    loadSmsInbox();"
    app_text = app_text.replace(hook_init, hook_init_rep, 1)

    with open("python_app/static/app.js", "w", encoding="utf-8") as f:
        f.write(app_text)
    print("app.js updated with SMS Inbox and Toast triggers successfully!")
else:
    print("SMS JS already present in app.js")
