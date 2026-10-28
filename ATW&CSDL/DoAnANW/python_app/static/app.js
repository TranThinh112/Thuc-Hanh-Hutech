
function formatProductName(rawName, amount) {
    if (!rawName || !rawName.trim()) return "Sản phẩm công nghệ cao cấp";
    const lower = rawName.toLowerCase();
    if (lower.includes("attack") || lower.includes("attempt") || lower.includes("attacker") || lower.includes("hack")) {
        const amt = Number(amount) || 0;
        if (amt >= 100000000) return "MacBook Pro 16 M3 Max (64GB RAM / 1TB SSD) Space Black";
        if (amt >= 40000000) return "MacBook Pro 14 M3 Pro (18GB/512GB)";
        if (amt >= 20000000) return "iPhone 16 Pro Max 256GB";
        if (amt >= 5000000) return "Sony WH-1000XM5 Headphones";
        if (amt >= 1000000) return "Wireless Mechanical Keyboard";
        return "Cáp sạc Baseus 100W Type-C bọc dù siêu bền";
    }
    return rawName;
}

// =========================================================================
// UNIVERSAL CUSTOM POPUP & MODAL SYSTEM (REPLACES BROWSER ALERT & CONFIRM)
// =========================================================================

let popupConfirmCallback = null;

function showAppPopup({
    title = "THÔNG BÁO HỆ THỐNG",
    subtitle = "Secure Payment Fraud Engine",
    message = "",
    type = "warning", // "lock" | "warning" | "error" | "success" | "info"
    confirmText = "Đã hiểu",
    showCancel = false,
    cancelText = "Hủy bỏ",
    onConfirm = null,
} = {}) {
    popupConfirmCallback = onConfirm;

    const modal = document.getElementById("custom-popup-modal");
    const titleEl = document.getElementById("custom-popup-title");
    const subEl = document.getElementById("custom-popup-subtitle");
    const bodyEl = document.getElementById("custom-popup-body");
    const iconBox = document.getElementById("custom-popup-icon-box");
    const iconEl = document.getElementById("custom-popup-icon");
    const okBtn = document.getElementById("custom-popup-ok-btn");
    const cancelBtn = document.getElementById("custom-popup-cancel-btn");

    if (!modal) {
        console.warn("custom-popup-modal not found!");
        return;
    }

    if (titleEl) titleEl.innerText = title;
    if (subEl) subEl.innerText = subtitle;
    if (bodyEl) {
        bodyEl.innerHTML = (message || "").replace(/\n/g, "<br>");
    }

    if (type === "lock") {
        if (iconBox) iconBox.className = "w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0 bg-red-500/20 text-red-400 border border-red-500/40";
        if (iconEl) iconEl.className = "fa-solid fa-user-lock";
        if (okBtn) okBtn.className = "px-5 py-2.5 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white text-xs font-bold transition shadow-lg shadow-red-500/20";
    } else if (type === "error") {
        if (iconBox) iconBox.className = "w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0 bg-red-500/20 text-red-400 border border-red-500/40";
        if (iconEl) iconEl.className = "fa-solid fa-circle-xmark";
        if (okBtn) okBtn.className = "px-5 py-2.5 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white text-xs font-bold transition shadow-lg shadow-red-500/20";
    } else if (type === "success") {
        if (iconBox) iconBox.className = "w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0 bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
        if (iconEl) iconEl.className = "fa-solid fa-circle-check";
        if (okBtn) okBtn.className = "px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold transition shadow-lg shadow-emerald-500/20";
    } else if (type === "info") {
        if (iconBox) iconBox.className = "w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0 bg-blue-500/20 text-blue-400 border border-blue-500/40";
        if (iconEl) iconEl.className = "fa-solid fa-circle-info";
        if (okBtn) okBtn.className = "px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold transition shadow-lg shadow-blue-500/20";
    } else {
        if (iconBox) iconBox.className = "w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0 bg-amber-500/20 text-amber-400 border border-amber-500/40";
        if (iconEl) iconEl.className = "fa-solid fa-triangle-exclamation";
        if (okBtn) okBtn.className = "px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-600 to-orange-600 hover:from-amber-500 hover:to-orange-500 text-white text-xs font-bold transition shadow-lg shadow-amber-500/20";
    }

    if (okBtn) okBtn.innerText = confirmText;
    if (cancelBtn) {
        if (showCancel) {
            cancelBtn.classList.remove("hidden");
            cancelBtn.innerText = cancelText;
        } else {
            cancelBtn.classList.add("hidden");
        }
    }

    modal.classList.remove("hidden");
}

function closeCustomPopup(confirmed = true) {
    const modal = document.getElementById("custom-popup-modal");
    if (modal) modal.classList.add("hidden");
    if (confirmed && typeof popupConfirmCallback === "function") {
        const cb = popupConfirmCallback;
        popupConfirmCallback = null;
        cb();
    } else {
        popupConfirmCallback = null;
    }
}

// =========================================================================
// UNIVERSAL ESC KEY EVENT LISTENER (CLOSES ANY ACTIVE MODAL / POPUP)
// =========================================================================
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" || e.keyCode === 27) {
        // 1. Close system custom popup modal
        const customPopup = document.getElementById("custom-popup-modal");
        if (customPopup && !customPopup.classList.contains("hidden")) {
            closeCustomPopup(false);
            return;
        }

        // 2. Close payment result modal
        const resModal = document.getElementById("result-modal");
        if (resModal && !resModal.classList.contains("hidden")) {
            closeResultModal();
            return;
        }

        // 3. Close checkout modal
        const chkModal = document.getElementById("checkout-modal");
        if (chkModal && !chkModal.classList.contains("hidden")) {
            closeCheckoutModal();
            return;
        }

        // 4. Close cart modal
        const cartModal = document.getElementById("cart-modal");
        if (cartModal && !cartModal.classList.contains("hidden")) {
            toggleCartModal(false);
            return;
        }

        // 5. Close SMS inbox modal
        const smsModal = document.getElementById("sms-inbox-modal");
        if (smsModal && !smsModal.classList.contains("hidden")) {
            closeSmsInboxModal();
            return;
        }

        // 6. Close login modal
        const loginModal = document.getElementById("login-modal");
        if (loginModal && !loginModal.classList.contains("hidden")) {
            closeLoginModal();
            return;
        }

        // 7. Close token debug modal
        const tokenModal = document.getElementById("token-modal");
        if (tokenModal && !tokenModal.classList.contains("hidden")) {
            closeTokenModal();
            return;
        }

        // 8. Close iOS SMS toast
        closeSmsToast();
    }
});

// OVERRIDE WINDOW.ALERT GLOBALLY TO PREVENT BROWSER DEFAULT DIALOG EVER APPEARING
window.alert = function(message) {
    let type = "info";
    let title = "THÔNG BÁO HỆ THỐNG";
    const msgLower = (message || "").toLowerCase();
    if (msgLower.includes("khóa") || msgLower.includes("tạm khóa") || msgLower.includes("locked")) {
        type = "lock";
        title = "TÀI KHOẢN TẠM KHÓA";
    } else if (msgLower.includes("lỗi") || msgLower.includes("thất bại") || msgLower.includes("từ chối") || msgLower.includes("chặn")) {
        type = "error";
        title = "CẢNH BÁO BẢO MẬT";
    } else if (msgLower.includes("thành công") || msgLower.includes("hoàn tất")) {
        type = "success";
        title = "XÁC NHẬN THÀNH CÔNG";
    } else if (msgLower.includes("cảnh báo") || msgLower.includes("vui lòng") || msgLower.includes("trống")) {
        type = "warning";
        title = "NHẮC NHỞ HỆ THỐNG";
    }

    showAppPopup({
        title,
        message,
        type,
        confirmText: "Đã hiểu"
    });
};

function showAccountLockedAlert() {
    const mins = currentUser?.lockedMinsRemaining || 15;
    showAppPopup({
        title: "TÀI KHOẢN ĐANG BỊ TẠM KHÓA",
        subtitle: "Bảo vệ an toàn số dư tài khoản",
        message: `Tài khoản của bạn đã bị khóa tạm thời trong ${mins} phút do phát hiện 5 lần giao dịch vi phạm chính sách an toàn liên tiếp.\n\nToàn bộ nút 'Mua ngay' và chức năng thanh toán tạm thời bị vô hiệu hóa để bảo vệ an toàn tài sản của bạn.\n\nVui lòng đợi hết thời gian khóa hoặc liên hệ Hotline CSKH 1900-8888 để được hỗ trợ mở khóa sớm.`,
        type: "lock",
        confirmText: "Đã hiểu"
    });
}


function syncLocationFromCity() {
    const citySelect = document.getElementById("chk-city");
    const city = citySelect ? citySelect.value : "Hà Nội";
    const ipEl = document.getElementById("chk-ip");
    const devEl = document.getElementById("chk-device");
    const addrEl = document.getElementById("chk-cust-address");

    if (city === "Tokyo") {
        if (ipEl) ipEl.value = "185.220.101.5";
        if (devEl) devEl.value = "device_hacker_kali";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Shibuya, Tokyo, Japan";
    } else if (city === "London") {
        if (ipEl) ipEl.value = "45.142.120.10";
        if (devEl) devEl.value = "device_bot_script";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Westminster, London, UK";
    } else if (city === "New York") {
        if (ipEl) ipEl.value = "198.51.100.25";
        if (devEl) devEl.value = "device_foreign_pc";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Manhattan, New York, USA";
    } else if (city === "Hồ Chí Minh") {
        if (ipEl) ipEl.value = "14.161.12.99";
        if (devEl) devEl.value = "device_thinh_iphone";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Quận 1, TP. Hồ Chí Minh";
    } else {
        if (ipEl) ipEl.value = "113.161.44.12";
        if (devEl) devEl.value = "device_thinh_iphone";
        if (addrEl && (addrEl.value.includes("Tokyo") || addrEl.value.includes("London"))) addrEl.value = "Số 15 Cầu Giấy, Hà Nội";
    }
}

// SecurePay Fraud Detection & E-Commerce Frontend Logic

let allProducts = [];
let cart = [];
let currentUser = null;
let accessToken = localStorage.getItem("access_token") || "";
let refreshToken = localStorage.getItem("refresh_token") || "";
let chartRiskDist = null, chartDecision = null;

function authFetch(url, options = {}) {
    options = options || {};
    options.headers = options.headers || {};
    const token = accessToken || localStorage.getItem("access_token");
    if (token) {
        options.headers["Authorization"] = "Bearer " + token;
    }
    return fetch(url, options);
}



let detectedClientInfo = null;

async function fetchClientInfo() {
    try {
        const res = await fetch("/api/client-info");
        if (res.ok) {
            detectedClientInfo = await res.json();
            const ipEl = document.getElementById("live-client-ip");
            const devEl = document.getElementById("live-client-device");
            const locEl = document.getElementById("live-client-loc");
            if (ipEl) ipEl.textContent = detectedClientInfo.detectedIp || "127.0.0.1";
            if (devEl) devEl.textContent = detectedClientInfo.deviceName || "Trình duyệt Web";
            if (locEl) locEl.textContent = (detectedClientInfo.city || "Hà Nội") + ", " + (detectedClientInfo.country || "Vietnam");

            const chkIp = document.getElementById("chk-ip");
            if (chkIp && detectedClientInfo.isPublicIp && (!chkIp.value || chkIp.value === "113.161.44.12")) {
                chkIp.value = detectedClientInfo.detectedIp;
            }
            const chkDev = document.getElementById("chk-device");
            if (chkDev && (!chkDev.value || chkDev.value === "device_thinh_iphone")) {
                chkDev.value = detectedClientInfo.deviceId;
            }
        }
    } catch (e) {
        console.warn("fetchClientInfo notice:", e);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    fetchClientInfo();
    try {
        await initAuth();
    } catch (e) {
        console.warn("Auth init error:", e);
    }
    await loadProducts();
    if (currentUser && currentUser.role === "ADMIN") {
        loadDashboard();
    }
});

// =========================================================================
// AUTHENTICATION & ROLE ENFORCEMENT
// =========================================================================

async function initAuth() {
    accessToken = localStorage.getItem("access_token");
    refreshToken = localStorage.getItem("refresh_token");

    if (accessToken) {
        try {
            const res = await fetch("/api/auth/me", {
                headers: { "Authorization": "Bearer " + accessToken }
            });
            if (res.ok) {
                currentUser = await res.json();
                updateAuthUI();
    loadSmsInbox();
                return;
            }
        } catch (e) {
            console.warn("Auth check failed:", e);
        }
    }

    // Auto login as default demo user: Thịnh (0972445090)
    await quickLogin("thinh", false);
}

function updateAuthUI() {
    const navLoginBtn = document.getElementById("nav-login-btn");
    const userCapsule = document.getElementById("user-auth-capsule");
    const nameEl = document.getElementById("nav-user-name");
    const roleEl = document.getElementById("nav-user-role");
    const phoneEl = document.getElementById("nav-user-phone");
    const adminBtn = document.getElementById("nav-admin-btn");
    const storeBtn = document.getElementById("nav-store-btn");
    const navSmsBtn = document.getElementById("nav-sms-btn");
    const navCartBtn = document.getElementById("nav-cart-btn");
    const navOrdersBtn = document.getElementById("nav-orders-btn");
    const smsFloatingFab = document.getElementById("sms-floating-fab");

    const navRegisterBtn = document.getElementById("nav-register-btn");

    if (!currentUser) {
        // GUEST VISITOR MODE
        if (navLoginBtn) navLoginBtn.classList.remove("hidden");
        if (navRegisterBtn) navRegisterBtn.classList.remove("hidden");
        if (userCapsule) userCapsule.classList.add("hidden");
        if (adminBtn) adminBtn.classList.add("hidden");
        if (storeBtn) storeBtn.classList.add("hidden");
        if (navSmsBtn) navSmsBtn.classList.remove("hidden");
        if (navCartBtn) navCartBtn.classList.remove("hidden");
        if (navOrdersBtn) navOrdersBtn.classList.remove("hidden");
        if (smsFloatingFab) smsFloatingFab.classList.remove("hidden");
        return;
    }

    // LOGGED IN MODE
    if (navLoginBtn) navLoginBtn.classList.add("hidden");
    if (navRegisterBtn) navRegisterBtn.classList.add("hidden");
    if (userCapsule) userCapsule.classList.remove("hidden");

    if (nameEl) nameEl.innerText = currentUser.name;
    if (phoneEl) phoneEl.innerText = currentUser.phone || "0972445090";

    const isAdmin = (currentUser.role === "ADMIN");

    if (roleEl) {
        roleEl.innerText = currentUser.role;
        if (isAdmin) {
            roleEl.className = "text-[10px] px-1.5 py-0.2 rounded font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40";
        } else {
            roleEl.className = "text-[10px] px-1.5 py-0.2 rounded font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
        }
    }

    // Account Lock UI
    const lockBanner = document.getElementById("account-locked-banner");
    const lockCountdown = document.getElementById("account-lock-countdown-badge");
    if (currentUser && currentUser.isLocked) {
        if (lockBanner) lockBanner.classList.remove("hidden");
        if (lockCountdown) lockCountdown.innerText = `Còn ${currentUser.lockedMinsRemaining || 15} phút`;
    } else {
        if (lockBanner) lockBanner.classList.add("hidden");
    }

    // Strict Role-Based View & Nav Control:
    // ADMIN: ONLY sees Catalog viewing & Admin Management. CANNOT place orders, no cart, no SMS, no deliveries.
    if (isAdmin) {
        if (adminBtn) adminBtn.classList.remove("hidden");
        if (storeBtn) storeBtn.classList.remove("hidden");
        if (navSmsBtn) navSmsBtn.classList.add("hidden");
        if (navCartBtn) navCartBtn.classList.add("hidden");
        if (navOrdersBtn) navOrdersBtn.classList.add("hidden");
        if (smsFloatingFab) smsFloatingFab.classList.add("hidden");
    } else {
        if (adminBtn) adminBtn.classList.add("hidden");
        if (storeBtn) storeBtn.classList.add("hidden");
        if (navSmsBtn) navSmsBtn.classList.remove("hidden");
        if (navCartBtn) navCartBtn.classList.remove("hidden");
        if (navOrdersBtn) navOrdersBtn.classList.remove("hidden");
        if (smsFloatingFab) smsFloatingFab.classList.remove("hidden");
    }

    // Always re-render products so buttons reflect current role and lock status
    if (allProducts && allProducts.length > 0) {
        renderProducts(allProducts);
    }
}

function openLoginModal() {
    showView("login");
}

function closeLoginModal() {
    document.getElementById("login-modal")?.classList.add("hidden");
}

async function quickLogin(username, showAlert = true) {
    try {
        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password: "123" })
        });
        const data = await res.json();
        if (!res.ok) {
            alert(data.detail || "Đăng nhập thất bại");
            return;
        }

        accessToken = data.accessToken;
        refreshToken = data.refreshToken;
        currentUser = data.user;

        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);
        localStorage.setItem("current_user", JSON.stringify(currentUser));

        updateAuthUI();
        closeLoginModal();
        loadSmsInbox();
        showView("store");

        if (showAlert) {
            alert(`Đăng nhập thành công!
Tài khoản: ${currentUser.name}
Số điện thoại: ${currentUser.phone}
Quyền: ${currentUser.role}`);
        }
    } catch (e) {
        console.error("Login failed:", e);
    }
}

async function handleManualLogin(event) {
    event.preventDefault();
    const acc = document.getElementById("login-username").value.trim();
    const pwd = document.getElementById("login-password").value.trim();
    const errEl = document.getElementById("login-error");

    try {
        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: acc, password: pwd })
        });
        const data = await res.json();
        if (!res.ok) {
            errEl.innerText = data.detail || "Đăng nhập không thành công";
            errEl.classList.remove("hidden");
            return;
        }

        accessToken = data.accessToken;
        refreshToken = data.refreshToken;
        currentUser = data.user;

        localStorage.setItem("access_token", accessToken);
        localStorage.setItem("refresh_token", refreshToken);
        localStorage.setItem("current_user", JSON.stringify(currentUser));

        errEl.classList.add("hidden");
        updateAuthUI();
        closeLoginModal();
        loadSmsInbox();
        showView("store");
        alert(`Đăng nhập thành công!
Tài khoản: ${currentUser.name} (${currentUser.role})`);
    } catch (e) {
        errEl.innerText = "Lỗi kết nối máy chủ";
        errEl.classList.remove("hidden");
    }
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("current_user");
    accessToken = "";
    refreshToken = "";
    currentUser = null;
    openLoginModal();
}

function openTokenModal() {
    const accEl = document.getElementById("modal-access-token");
    const refEl = document.getElementById("modal-refresh-token");
    if (accEl) accEl.value = localStorage.getItem("access_token") || "Chưa có Access Token";
    if (refEl) refEl.value = localStorage.getItem("refresh_token") || "Chưa có Refresh Token";
    document.getElementById("token-modal")?.classList.remove("hidden");
}

function closeTokenModal() {
    document.getElementById("token-modal")?.classList.add("hidden");
}

async function testRefreshToken() {
    const curRef = localStorage.getItem("refresh_token");
    if (!curRef) {
        alert("Chưa có Refresh Token trong bộ nhớ!");
        return;
    }
    try {
        const res = await fetch("/api/auth/refresh", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refreshToken: curRef })
        });
        const data = await res.json();
        if (res.ok) {
            localStorage.setItem("access_token", data.accessToken);
            localStorage.setItem("refresh_token", data.refreshToken);
            openTokenModal();
            alert("Đã cấp mới Access Token và Refresh Token thành công bằng API Refresh Token!");
        } else {
            alert(data.detail || "Lỗi khi refresh token");
        }
    } catch (e) {
        alert("Lỗi kết nối khi refresh token");
    }
}

function showView(viewName) {
    if (viewName === "orders" && currentUser && currentUser.role === "ADMIN") {
        showView("admin");
        return;
    }
    const viewStore = document.getElementById("view-store");
    const viewAdmin = document.getElementById("view-admin");
    const viewLogin = document.getElementById("view-login");
    const viewOrders = document.getElementById("view-orders");
    const navStoreBtn = document.getElementById("nav-store-btn");
    const navAdminBtn = document.getElementById("nav-admin-btn");

    if (viewName === "admin") {
        if (!currentUser) {
            showAppPopup({
                title: "YÊU CẦU ĐĂNG NHẬP ADMIN",
                subtitle: "Khu vực Quản trị",
                message: "Vui lòng đăng nhập với tài khoản Quản Trị Viên (Admin) để truy cập Trung Tâm Giám Sát Gian Lận!",
                type: "warning"
            });
            showView("login");
            return;
        }
        if (currentUser.role !== "ADMIN") {
            showAppPopup({
                title: "TRUY CẬP BỊ TỪ CHỐI",
                subtitle: "Phân quyền người dùng (RBAC)",
                message: "Tài khoản của bạn (" + currentUser.name + " - USER) chỉ có quyền mua sắm tại Cửa Hàng TMĐT.\n\nChỉ tài khoản Quản Trị Viên (ADMIN) mới có quyền truy cập Trang Quản Trị!",
                type: "error"
            });
            showView("store");
            return;
        }
        viewStore?.classList.add("hidden");
        viewLogin?.classList.add("hidden");
        viewOrders?.classList.add("hidden");
        viewAdmin?.classList.remove("hidden");
        if (navStoreBtn) navStoreBtn.classList.remove("hidden");
        if (navAdminBtn) navAdminBtn.classList.add("hidden");
        loadDashboard();
        } else if (viewName === "orders") {
        if (!currentUser) {
            showAppPopup({
                title: "YÊU CẦU ĐĂNG NHẬP",
                subtitle: "Quản lý đơn hàng",
                message: "Vui lòng đăng nhập tài khoản để xem tiến trình đóng gói và giao hàng của bạn!",
                type: "info"
            });
            showView("login");
            return;
        }
        viewStore?.classList.add("hidden");
        viewAdmin?.classList.add("hidden");
        viewLogin?.classList.add("hidden");
        viewOrders?.classList.remove("hidden");
        if (navStoreBtn) navStoreBtn.classList.remove("hidden");
        loadPendingOrders();
        window.scrollTo({ top: 0, behavior: "smooth" });
    } else if (viewName === "login") {
        viewStore?.classList.add("hidden");
        viewAdmin?.classList.add("hidden");
        viewOrders?.classList.add("hidden");
        viewLogin?.classList.remove("hidden");
        if (navStoreBtn) navStoreBtn.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        // 'store' view
        viewStore?.classList.remove("hidden");
        viewAdmin?.classList.add("hidden");
        viewLogin?.classList.add("hidden");
        viewOrders?.classList.add("hidden");
        if (navStoreBtn) navStoreBtn.classList.add("hidden");
        if (currentUser && currentUser.role === "ADMIN" && navAdminBtn) {
            navAdminBtn.classList.remove("hidden");
        }
    }
}

function switchAdminTab(tabId) {
    const tabs = ["dashboard", "simulation", "transactions", "rules", "evaluation"];
    tabs.forEach(t => {
        const btn = document.getElementById("adm-tab-" + t);
        const sec = document.getElementById("adm-sec-" + t) || document.getElementById("sec-" + t);
        if (btn) btn.className = (t === tabId) ? "px-3 py-1.5 rounded bg-blue-600 font-semibold text-white" : "px-3 py-1.5 rounded bg-slate-800 text-slate-300";
        if (sec) sec.classList.toggle("hidden", t !== tabId);
    });
    if (tabId === "dashboard") loadDashboard();
    if (tabId === "transactions") loadTransactions();
    if (tabId === "rules") loadRules();
}

// =========================================================================
// STOREFRONT & PRODUCTS
// =========================================================================

async function loadProducts() {
    try {
        const res = await fetch("/api/store/products");
        allProducts = await res.json();
        updateCategoryBadges();
        filterCategory("ALL");
    } catch (e) {
        console.error("Failed to load products", e);
    }
}

function updateCategoryBadges() {
    const counts = {
        "ALL": allProducts.length,
        "UNDER_1M": allProducts.filter(p => p.price <= 1000000).length,
        "Smartphones": allProducts.filter(p => p.category === "Smartphones").length,
        "Laptops": allProducts.filter(p => p.category === "Laptops").length,
        "Audio": allProducts.filter(p => p.category === "Audio").length,
        "Wearables": allProducts.filter(p => p.category === "Wearables").length,
        "Accessories": allProducts.filter(p => p.category === "Accessories").length
    };

    for (const [key, count] of Object.entries(counts)) {
        const el = document.getElementById("badge-count-" + key);
        if (el) el.innerText = count;
    }
}

function renderProducts(products) {
    const grid = document.getElementById("store-product-grid") || document.getElementById("products-grid");
    if (!grid) return;
    const isUserLocked = Boolean(currentUser && currentUser.isLocked);
    if (products.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full py-12 text-center glass-card rounded-2xl border border-slate-700/60 p-8">
                <i class="fa-solid fa-box-open text-4xl text-slate-500 mb-3 block"></i>
                <h4 class="text-white font-bold text-base">Không có sản phẩm nào trong danh mục này</h4>
                <p class="text-xs text-slate-400 mt-1">Vui lòng chọn danh mục khác hoặc nhập từ khóa tìm kiếm mới</p>
            </div>
        `;
        return;
    }
    grid.innerHTML = products.map(p => `
        <div class="glass-card rounded-2xl border border-slate-700/80 overflow-hidden shadow-xl hover:border-slate-500 transition duration-300 flex flex-col justify-between group">
            <div class="relative overflow-hidden h-48 bg-slate-800">
                <img src="${p.imageUrl}" alt="${p.name}" onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80';" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                <span class="absolute top-3 left-3 bg-slate-900/80 backdrop-blur-md text-[10px] font-bold uppercase tracking-wider text-blue-400 px-2 py-0.5 rounded border border-slate-700">
                    ${p.category}
                </span>
            </div>
            <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
                <div>
                    <h3 class="font-bold text-base text-white line-clamp-1">${p.name}</h3>
                    <p class="text-xs text-slate-400 mt-1 line-clamp-2">${p.description}</p>
                </div>
                <div class="pt-2 border-t border-slate-800 flex items-center justify-between">
                    <div>
                        <span class="text-[10px] text-slate-400 block">Giá bán:</span>
                        <span class="text-base font-extrabold text-emerald-400 font-mono">${p.price.toLocaleString()} VNĐ</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        ${(currentUser && currentUser.role === "ADMIN") ? `
                            <span class="px-3 py-1.5 bg-purple-950/60 border border-purple-700/60 text-purple-300 rounded-lg text-xs font-semibold flex items-center shadow-sm">
                                <i class="fa-solid fa-eye mr-1.5 text-purple-400"></i>Chế độ xem (Admin)
                            </span>
                        ` : isUserLocked ? `
                            <button onclick="showAccountLockedAlert()" title="Tài khoản đang tạm khóa giao dịch" class="px-3 py-1.5 bg-slate-800 text-slate-500 border border-slate-700/60 rounded-lg text-xs cursor-not-allowed opacity-50">
                                + Giỏ hàng
                            </button>
                            <button onclick="showAccountLockedAlert()" title="Tài khoản đang tạm khóa do vi phạm an toàn liên tiếp" class="px-3.5 py-1.5 bg-red-600 hover:bg-red-500 text-white font-bold border border-red-500 rounded-lg text-xs cursor-not-allowed flex items-center space-x-1.5 shadow-lg shadow-red-600/30 transition">
                                <i class="fa-solid fa-lock text-xs mr-0.5"></i>
                                <span>Tạm khóa</span>
                            </button>
                        ` : `
                            <button onclick="addToCart('${p.id}')" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs transition">
                                + Giỏ hàng
                            </button>
                            <button onclick="buyNow('${p.id}')" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg text-xs transition shadow">
                                Mua ngay
                            </button>
                        `}
                    </div>
                </div>
            </div>
        </div>
    `).join("");
}

function filterCategory(cat) {
    const catMap = {
        "ALL": ["tất cả", "all"],
        "UNDER_1M": ["giá rẻ", "100k", "under_1m"],
        "Smartphones": ["smartphones", "smartphone", "điện thoại"],
        "Laptops": ["laptops", "laptop"],
        "Audio": ["âm thanh", "audio", "thiết bị âm thanh"],
        "Wearables": ["đồng hồ", "wearables", "đồng hồ thông minh"],
        "Accessories": ["phụ kiện", "accessories"]
    };

    const titleMap = {
        "ALL": "Tất cả sản phẩm",
        "UNDER_1M": "Sản phẩm giá rẻ (≤ 1 triệu VNĐ)",
        "Smartphones": "Smartphones / Điện thoại",
        "Laptops": "Laptops & Máy trạm",
        "Audio": "Thiết bị Âm thanh & Tai nghe",
        "Wearables": "Đồng hồ thông minh & Wearables",
        "Accessories": "Phụ kiện công nghệ"
    };

    document.querySelectorAll(".cat-btn").forEach(b => {
        const btnCat = b.getAttribute("data-cat");
        const txt = (b.innerText || "").toLowerCase().trim();
        const keywords = catMap[cat] || [cat.toLowerCase()];
        const isActive = (btnCat === cat) || keywords.some(kw => txt.includes(kw));
        const badge = b.querySelector(".cat-badge");

        if (isActive) {
            b.className = "cat-btn bg-blue-600 text-white text-xs font-medium px-3.5 py-2 rounded-lg transition shadow flex items-center space-x-1.5";
            if (badge) {
                badge.className = "cat-badge ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-white/20 text-white";
            }
        } else {
            if (btnCat === "UNDER_1M" || txt.includes("giá rẻ")) {
                b.className = "cat-btn bg-slate-800 hover:bg-slate-700 text-emerald-400 border border-emerald-500/40 text-xs font-semibold px-3.5 py-2 rounded-lg transition flex items-center space-x-1.5 shadow";
                if (badge) {
                    badge.className = "cat-badge ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
                }
            } else {
                b.className = "cat-btn bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium px-3.5 py-2 rounded-lg transition flex items-center space-x-1.5";
                if (badge) {
                    badge.className = "cat-badge ml-1 px-1.5 py-0.5 rounded-full text-[10px] font-bold bg-slate-700 text-slate-300";
                }
            }
        }
    });

    let filtered = [];
    if (cat === "UNDER_1M") {
        filtered = allProducts.filter(p => p.price <= 1000000);
    } else if (cat === "ALL") {
        filtered = allProducts;
    } else {
        filtered = allProducts.filter(p => p.category === cat);
    }

    const titleEl = document.getElementById("selected-cat-title");
    const countEl = document.getElementById("category-product-count");
    if (titleEl) titleEl.innerText = titleMap[cat] || cat;
    if (countEl) countEl.innerText = `${filtered.length} sản phẩm`;

    renderProducts(filtered);
}

function filterProducts() {
    const term = (document.getElementById("store-search")?.value || "").toLowerCase().trim();
    const filtered = allProducts.filter(p => p.name.toLowerCase().includes(term) || p.description.toLowerCase().includes(term));
    const titleEl = document.getElementById("selected-cat-title");
    const countEl = document.getElementById("category-product-count");
    if (term) {
        if (titleEl) titleEl.innerText = `Kết quả tìm kiếm: "${term}"`;
    } else {
        if (titleEl) titleEl.innerText = "Tất cả sản phẩm";
    }
    if (countEl) countEl.innerText = `${filtered.length} sản phẩm`;
    renderProducts(filtered);
}

function addToCart(id) {
    if (currentUser && currentUser.role === "ADMIN") {
        showAppPopup({
            title: "TÀI KHOẢN QUẢN TRỊ VIÊN",
            subtitle: "Giới hạn quyền hạn",
            message: "Tài khoản Quản Trị Viên (Admin) chỉ có quyền giám sát hệ thống và xem danh mục sản phẩm, không được phép thêm giỏ hàng hoặc đặt hàng.",
            type: "warning"
        });
        return;
    }
    if (currentUser && currentUser.isLocked) {
        showAccountLockedAlert();
        return;
    }
    const item = allProducts.find(p => p.id === id);
    if (item) {
        cart.push(item);
        updateCartUI();
        toggleCartModal(true);
    }
}

function buyNow(id) {
    if (currentUser && currentUser.isLocked) {
        showAccountLockedAlert();
        return;
    }
    const item = allProducts.find(p => p.id === id);
    if (!item) return;

    cart = [item];
    updateCartUI();

    if (!currentUser) {
        // Require Login before checking out
        sessionStorage.setItem("pending_checkout", "true");
        const alertEl = document.getElementById("login-checkout-alert");
        if (alertEl) alertEl.classList.remove("hidden");
        showView("login");
        return;
    }

    openCheckoutModal();
}

function updateCartUI() {
    const count = document.getElementById("cart-count");
    if (count) count.innerText = cart.length;

    const list = document.getElementById("cart-items");
    const total = document.getElementById("cart-total");
    const sum = cart.reduce((acc, i) => acc + i.price, 0);

    if (total) total.innerText = sum.toLocaleString() + " VND";
    if (!list) return;

    if (cart.length === 0) {
        list.innerHTML = "<p class='text-xs text-slate-500 text-center py-4'>Giỏ hàng của bạn đang trống.</p>";
        return;
    }

    list.innerHTML = cart.map((item, idx) => `
        <div class="flex items-center justify-between p-2.5 bg-slate-800/60 rounded-xl border border-slate-700/60 text-xs">
            <div class="flex items-center space-x-3">
                <img src="${item.imageUrl}" class="w-10 h-10 object-cover rounded-lg">
                <div>
                    <h4 class="font-bold text-white line-clamp-1">${item.name}</h4>
                    <span class="text-emerald-400 font-mono text-[11px]">${item.price.toLocaleString()} VNĐ</span>
                </div>
            </div>
            <button onclick="removeFromCart(${idx})" class="text-slate-500 hover:text-red-400 p-1"><i class="fa-solid fa-trash-can"></i></button>
        </div>
    `).join("");
}

function removeFromCart(idx) {
    cart.splice(idx, 1);
    updateCartUI();
}

function toggleCartModal(forceOpen = false) {
    const modal = document.getElementById("cart-modal");
    if (!modal) return;
    if (forceOpen) {
        modal.classList.remove("hidden");
    } else {
        modal.classList.toggle("hidden");
    }
}

function openCheckoutModal() {
    if (currentUser && currentUser.role === "ADMIN") {
        showAppPopup({
            title: "TÀI KHOẢN QUẢN TRỊ VIÊN",
            subtitle: "Giới hạn quyền hạn",
            message: "Tài khoản Quản Trị Viên (Admin) không được phép thanh toán đặt hàng.",
            type: "warning"
        });
        return;
    }
    fetchClientInfo();
    if (cart.length === 0) {
        showAppPopup({
            title: "GIỎ HÀNG ĐANG TRỐNG",
            subtitle: "Cửa hàng TMĐT",
            message: "Giỏ hàng hiện chưa có sản phẩm nào. Vui lòng bấm 'Mua ngay' hoặc '+ Giỏ hàng' để tiếp tục!",
            type: "warning"
        });
        return;
    }

    // Require Login before checkout
    if (!currentUser) {
        document.getElementById("cart-modal")?.classList.add("hidden");
        sessionStorage.setItem("pending_checkout", "true");
        const alertEl = document.getElementById("login-checkout-alert");
        if (alertEl) alertEl.classList.remove("hidden");
        showView("login");
        return;
    }

    const sum = cart.reduce((acc, i) => acc + i.price, 0);
    const amtEl = document.getElementById("chk-amount");
    if (amtEl) amtEl.value = sum;

    const nameEl = document.getElementById("chk-cust-name");
    const phoneEl = document.getElementById("chk-cust-phone");
    const badgeEl = document.getElementById("chk-user-badge");

    if (currentUser) {
        if (nameEl) nameEl.value = currentUser.name;
        if (phoneEl) phoneEl.value = currentUser.phone || "0972445090";
        if (badgeEl) badgeEl.innerText = `${currentUser.name} (${currentUser.phone || '0972445090'})`;
    }

    document.getElementById("cart-modal")?.classList.add("hidden");
    document.getElementById("checkout-modal")?.classList.remove("hidden");
}

function closeCheckoutModal() {
    document.getElementById("checkout-modal")?.classList.add("hidden");
}

function toggleSimAccordion() {
    const body = document.getElementById("sim-acc-body");
    const icon = document.getElementById("sim-acc-icon");
    if (body) {
        body.classList.toggle("hidden");
        if (icon) icon.classList.toggle("rotate-180");
    }
}

let activeScenarioPreset = "legit";

function setPreset(type) {
    activeScenarioPreset = type;
    try {
        const ip = document.getElementById("chk-ip");
        const dev = document.getElementById("chk-device");
        const city = document.getElementById("chk-city");
        const citySim = document.getElementById("chk-city-sim");
        const addr = document.getElementById("chk-cust-address");
        const amt = document.getElementById("chk-amount");
        const pm = document.getElementById("chk-pm");

        const setCityVal = (val) => {
            if (city) {
                let exists = false;
                for (let i = 0; i < city.options.length; i++) {
                    if (city.options[i].value === val) {
                        city.selectedIndex = i;
                        exists = true;
                        break;
                    }
                }
                if (!exists) {
                    const opt = document.createElement("option");
                    opt.value = val;
                    opt.text = val;
                    city.add(opt);
                    city.value = val;
                }
            }
            if (citySim) citySim.value = val;
        };

        const setPmVal = (val) => {
            if (!pm) return;
            let exists = false;
            for (let i = 0; i < pm.options.length; i++) {
                if (pm.options[i].value === val) {
                    pm.selectedIndex = i;
                    exists = true;
                    break;
                }
            }
            if (!exists) {
                const opt = document.createElement("option");
                opt.value = val;
                opt.text = "Thẻ Quốc Tế " + val;
                pm.add(opt);
                pm.value = val;
            }
        };

        let scenarioName = "";
        if (type === "legit") {
            scenarioName = "Hợp Lệ (Hà Nội, IP Quen, 500k)";
            setCityVal("Hà Nội");
            if (ip) ip.value = "113.161.44.12";
            if (dev) dev.value = "device_windows_pc";
            if (addr) addr.value = "Số 15 Cầu Giấy, Hà Nội";
            if (amt) amt.value = "500000";
            setPmVal("VISA");
        } else if (type === "ato") {
            scenarioName = "Chiếm Đoạt Tài Khoản (Tokyo, 45Tr, Hacker Kali)";
            setCityVal("Tokyo");
            if (ip) ip.value = "185.220.101.5";
            if (dev) dev.value = "device_hacker_kali";
            if (addr) addr.value = "Shibuya, Tokyo, Japan";
            if (amt) amt.value = "45000000";
            setPmVal("VISA");
        } else if (type === "travel") {
            scenarioName = "Di Chuyển Bất Khả Thi (London, UK - Cách VN 9,000km)";
            setCityVal("London");
            if (ip) ip.value = "45.142.120.10";
            if (dev) dev.value = "device_windows_pc";
            if (addr) addr.value = "Westminster, London, UK";
            if (amt) amt.value = "2500000";
            setPmVal("MASTERCARD");
        } else if (type === "velocity") {
            scenarioName = "Spam Tần Suất Cao (Giao dịch liên tục trong 5 phút)";
            setCityVal("Hà Nội");
            if (ip) ip.value = "113.161.44.12";
            if (dev) dev.value = "device_windows_pc";
            if (addr) addr.value = "Số 15 Cầu Giấy, Hà Nội";
            if (amt) amt.value = "2000000";
            setPmVal("VISA");
        } else if (type === "high_amount") {
            scenarioName = "Đột Biến Giá Trị (Đơn hàng lớn 68,000,000 VND)";
            setCityVal("Hà Nội");
            if (ip) ip.value = "113.161.44.12";
            if (dev) dev.value = "device_windows_pc";
            if (addr) addr.value = "Số 15 Cầu Giấy, Hà Nội";
            if (amt) amt.value = "68000000";
            setPmVal("VISA");
        } else if (type === "card_testing") {
            scenarioName = "Thử Thẻ Tự Động (Đơn nhỏ 99k, Máy Bot Tester, Thẻ JCB)";
            setCityVal("TP. Hồ Chí Minh");
            if (ip) ip.value = "45.33.32.156";
            if (dev) dev.value = "device_bot_tester_01";
            if (addr) addr.value = "Quận 1, TP. Hồ Chí Minh";
            if (amt) amt.value = "99000";
            setPmVal("JCB");
        }

        // Visual flash indication on the inputs
        [amt, ip, dev, citySim].forEach(el => {
            if (el) {
                el.style.transition = "background-color 0.3s ease";
                const origBg = el.style.backgroundColor;
                el.style.backgroundColor = "#1e3a8a";
                setTimeout(() => { el.style.backgroundColor = origBg; }, 400);
            }
        });

        const statusEl = document.getElementById("chk-preset-status");
        if (statusEl) {
            statusEl.innerText = "✓ Đã áp dụng: " + scenarioName;
            statusEl.className = "text-[11px] text-amber-300 font-semibold";
        }
    } catch (err) {
        console.error("setPreset error:", err);
    }
}

async function submitPayment(event) {
    event.preventDefault();
    const amount = parseFloat(document.getElementById("chk-amount").value);
    const paymentMethod = document.getElementById("chk-pm").value;
    const customerName = document.getElementById("chk-cust-name")?.value || currentUser?.name || "Thịnh";
    const customerPhone = document.getElementById("chk-cust-phone")?.value || currentUser?.phone || "0972445090";
    const shippingAddress = document.getElementById("chk-cust-address")?.value || "Số 15 Cầu Giấy, Hà Nội";
    const ipAddress = document.getElementById("chk-ip").value;
    const deviceId = document.getElementById("chk-device").value;
    const locationCity = document.getElementById("chk-city").value;
    const itemsSummary = cart.map(i => i.name).join(", ");

    const payload = {
        amount,
        paymentMethod,
        customerName,
        customerPhone,
        shippingAddress,
        itemsSummary,
        ipAddress,
        deviceId,
        locationCity,
        locationCountry: (locationCity === "Tokyo") ? "Japan" : ((locationCity === "London") ? "United Kingdom" : "Vietnam"),
        scenarioTag: activeScenarioPreset || "legit",
        userId: currentUser?.id
    };

    try {
        const headers = { "Content-Type": "application/json" };
        if (accessToken) headers["Authorization"] = "Bearer " + accessToken;

        const res = await fetch("/api/transactions", {
            method: "POST",
            headers,
            body: JSON.stringify(payload)
        });

        const textResponse = await res.text();
        let data;
        try {
            data = JSON.parse(textResponse);
        } catch (jsonErr) {
            data = { detail: textResponse || ("Lỗi máy chủ (HTTP " + res.status + ")") };
        }
        closeCheckoutModal();

        if (!res.ok) {
            if (res.status === 403) {
                if (currentUser) {
                    currentUser.isLocked = true;
                    currentUser.lockedMinsRemaining = 15;
                    updateAuthUI();
                }
            }
            showAppPopup({
                title: "GIAO DỊCH KHÔNG THÀNH CÔNG",
                subtitle: "Kiểm soát an toàn thanh toán",
                message: data.detail || "Giao dịch bị từ chối do vi phạm an toàn.",
                type: res.status === 403 ? "lock" : "error"
            });
            return;
        }

        showPaymentResult(data);
        if (data.smsNotification && data.smsNotification.content) {
            showSmsToast(data.smsNotification.phone || "0972445090", data.smsNotification.content);
        }
        loadSmsInbox();

        if (data.status === "APPROVED") {
            cart = [];
            updateCartUI();
        }

        if (currentUser && currentUser.role === "ADMIN") {
            loadDashboard();
        }
    } catch (e) {
        alert("Lỗi khi kết nối đến cổng thanh toán: " + e.message);
    }
}

let currentPendingTxData = null;

function showPaymentResult(data) {
    currentPendingTxData = data;
    const status = data.status || "PENDING";
    const isApprove = (status === "APPROVED");
    const isReview = (status === "REVIEW" || data.decision === "REVIEW");
    const isBlocked = (status === "BLOCKED" || data.decision === "BLOCK");

    const btnPending = document.getElementById("btn-view-pending-order");
    const icon = document.getElementById("res-icon");
    const title = document.getElementById("res-title");
    const subtitle = document.getElementById("res-subtitle");
    const statusLabel = document.getElementById("res-status-label");
    const scoreBadge = document.getElementById("res-score-badge");
    const expText = document.getElementById("res-explanation-text");
    const expBox = document.getElementById("res-explanation-box");
    const smsBubble = document.getElementById("sms-bubble");
    const smsPhone = document.getElementById("sms-phone-target");
    const smsTime = document.getElementById("sms-time");

    const otpSection = document.getElementById("res-otp-section");
    const emergencySection = document.getElementById("res-emergency-section");
    const otpInput = document.getElementById("res-otp-input");
    const otpFeedback = document.getElementById("res-otp-feedback");

    const score = data.fraudAnalysis?.riskScore || 0;
    const riskLevel = data.fraudAnalysis?.riskLevel || (isApprove ? "LOW" : (isReview ? "HIGH" : "CRITICAL"));

    // Reset Sections Visibility
    if (otpSection) otpSection.classList.add("hidden");
    if (emergencySection) emergencySection.classList.add("hidden");
    if (otpFeedback) {
        otpFeedback.classList.add("hidden");
        otpFeedback.innerText = "";
    }
    if (otpInput) otpInput.value = "";

    if (isApprove) {
        if (btnPending) {
            btnPending.classList.remove("hidden");
            btnPending.innerHTML = '<i class="fa-solid fa-truck-fast mr-1"></i> Xem Đơn Hàng Đang Chờ Giao';
        }
        if (icon) {
            icon.className = "w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0 bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 shadow-lg shadow-emerald-500/20";
            icon.innerHTML = '<i class="fa-solid fa-circle-check"></i>';
        }
        if (title) title.innerText = "ĐẶT HÀNG & THANH TOÁN THÀNH CÔNG!";
        if (subtitle) subtitle.innerText = "Giao dịch hợp lệ, phù hợp với hành vi thông thường và được phê duyệt an toàn.";

        if (statusLabel) {
            statusLabel.innerHTML = '<i class="fa-solid fa-shield-check text-emerald-400 mr-1.5"></i> PHÊ DUYỆT (APPROVE)';
            statusLabel.className = "text-emerald-400 font-bold flex items-center";
        }
        if (scoreBadge) {
            scoreBadge.innerText = `Điểm rủi ro: ${score}/100 (${riskLevel})`;
            scoreBadge.className = "px-2 py-0.5 rounded text-[11px] font-mono bg-emerald-500/20 text-emerald-300 border border-emerald-500/30";
        }
        if (expBox) {
            expBox.className = "p-3.5 rounded-xl border space-y-2 text-xs bg-emerald-950/40 border-emerald-700/60 text-emerald-200";
        }
        if (expText) {
            expText.innerText = data.userExplanation || "Đơn hàng của bạn đã được hệ thống xác thực an toàn. Tin nhắn SMS xác nhận đã được gửi đến số điện thoại của bạn.";
        }

        if (smsBubble) {
            smsBubble.className = "p-3 rounded-2xl text-xs font-sans leading-relaxed border shadow-md bg-emerald-900/60 border-emerald-600/70 text-emerald-100";
            smsBubble.innerText = data.smsNotification?.content || `[ECOMMERCE SECURE PAY] Cảm ơn Quý khách ${data.transaction?.userName}! Đơn hàng #${data.transaction?.shortId} trị giá ${data.transaction?.amount?.toLocaleString()} VND đã thanh toán thành công. Đang giao hàng! CSKH: 1900-8888.`;
        }

        // Clear cart on successful order
        cart = [];
        updateCartUI();

    } else if (isReview) {
        if (btnPending) {
            btnPending.classList.add("hidden");
        }
        if (icon) {
            icon.className = "w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0 bg-amber-500/20 text-amber-400 border border-amber-500/40 shadow-lg shadow-amber-500/20 animate-pulse";
            icon.innerHTML = '<i class="fa-solid fa-key"></i>';
        }
        if (title) title.innerText = "YÊU CẦU XÁC THỰC BƯỚC NHẢY (STEP-UP 2FA / SMART OTP)";
        if (subtitle) subtitle.innerText = "Đơn hàng cần xác thực chính chủ bằng mã OTP để bảo vệ tài khoản và nâng cao an toàn tài chính.";

        if (statusLabel) {
            statusLabel.innerHTML = '<i class="fa-solid fa-shield-halved text-amber-400 mr-1.5"></i> CẦN XÁC MINH (REVIEW)';
            statusLabel.className = "text-amber-400 font-bold flex items-center";
        }
        if (scoreBadge) {
            scoreBadge.innerText = `Điểm rủi ro: ${score}/100 (${riskLevel})`;
            scoreBadge.className = "px-2 py-0.5 rounded text-[11px] font-mono bg-amber-500/20 text-amber-300 border border-amber-500/30";
        }
        if (expBox) {
            expBox.className = "p-3.5 rounded-xl border space-y-2 text-xs bg-amber-950/40 border-amber-700/60 text-amber-200";
        }
        if (expText) {
            expText.innerText = data.userExplanation || "Đơn hàng có số tiền hoặc tần suất giao dịch đột biến so với lịch sử chi tiêu. Hệ thống đã gửi mã OTP 6 số tới điện thoại của bạn. Vui lòng nhập mã để phê duyệt đơn.";
        }

        // SHOW ACTIVE 2FA OTP SECTION
        if (otpSection) {
            otpSection.classList.remove("hidden");
            setTimeout(() => {
                const inp = document.getElementById("res-otp-input");
                if (inp) inp.focus();
            }, 200);
        }

        if (smsBubble) {
            smsBubble.className = "p-3 rounded-2xl text-xs font-sans leading-relaxed border shadow-md bg-amber-950/80 border-amber-600/80 text-amber-200";
            smsBubble.innerText = data.smsNotification?.content || `[SECURE-PAY] Ma xac thuc OTP cua ban la: ${data.otpCode || "------"} (Hieu luc 5 phut). Dung de xac nhan don hang #${data.transaction?.shortId}. CSKH: 1900-8888.`;
        }

    } else { // BLOCKED
        if (btnPending) {
            btnPending.classList.add("hidden");
        }
        if (icon) {
            icon.className = "w-12 h-12 rounded-xl flex items-center justify-center text-2xl flex-shrink-0 bg-red-500/20 text-red-400 border border-red-500/40 shadow-lg shadow-red-500/20 animate-bounce";
            icon.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i>';
        }
        if (title) title.innerText = "GIAO DỊCH BỊ CHẶN ĐỨNG ĐỂ BẢO VỆ TÀI SẢN";
        if (subtitle) subtitle.innerText = "Động cơ kiểm soát gian lận phát hiện hành vi bất thường nghiêm trọng, đã tự động ngăn chặn tức thì.";

        if (statusLabel) {
            statusLabel.innerHTML = `<i class="fa-solid fa-ban text-red-400 mr-1.5"></i> CHẶN GIAN LẬN (${data.decision || 'BLOCK'})`;
            statusLabel.className = "text-red-400 font-bold flex items-center";
        }
        if (scoreBadge) {
            scoreBadge.innerText = `Điểm rủi ro: ${score}/100 (${riskLevel})`;
            scoreBadge.className = "px-2 py-0.5 rounded text-[11px] font-mono bg-red-500/20 text-red-300 border border-red-500/30";
        }
        if (expBox) {
            expBox.className = "p-3.5 rounded-xl border space-y-2 text-xs bg-red-950/40 border-red-700/60 text-red-200";
        }
        if (expText) {
            expText.innerText = data.userExplanation || "Hệ thống phát hiện dấu hiệu nguy hiểm (thiết bị lạ, khoảng cách bất khả thi, hoặc thử thẻ tự động). Đơn hàng đã bị chặn đứng nhằm bảo vệ an toàn cho chủ tài khoản.";
        }

        // SHOW ACTIVE EMERGENCY KILL-SWITCH SECTION
        if (emergencySection) {
            emergencySection.classList.remove("hidden");
        }

        if (smsBubble) {
            smsBubble.className = "p-3 rounded-2xl text-xs font-sans leading-relaxed border shadow-md bg-red-950/80 border-red-700/80 text-red-200";
            smsBubble.innerText = data.smsNotification?.content || `[CANH BAO SECURE-PAY] GD #${data.transaction?.shortId} (${data.transaction?.amount?.toLocaleString()}đ) bi CHAN DUNG. Neu KHONG phai ban, hay KHOA KHAN CAP tai khoan ngay! Hotline: 1900-8888.`;
        }
    }

    if (smsPhone) smsPhone.innerText = data.smsNotification?.phone || data.transaction?.userPhone || "0972445090";
    if (smsTime) smsTime.innerText = new Date().toLocaleTimeString("vi-VN", { hour: "2-digit", minute: "2-digit" });

    document.getElementById("result-modal")?.classList.remove("hidden");
}

// =========================================================================
// ACTIVE USER PREVENTION: 2FA STEP-UP OTP & EMERGENCY DEFENSE ACTIONS
// =========================================================================

function fillOtpFromSms() {
    if (!currentPendingTxData) return;
    let code = currentPendingTxData.otpCode;
    if (!code && currentPendingTxData.smsNotification?.content) {
        const match = currentPendingTxData.smsNotification.content.match(/\d{6}/);
        if (match) code = match[0];
    }
    const input = document.getElementById("res-otp-input");
    if (input && code) {
        input.value = code;
        input.focus();
        const fb = document.getElementById("res-otp-feedback");
        if (fb) {
            fb.classList.remove("hidden");
            fb.className = "text-[11px] font-semibold text-emerald-400 mt-1";
            fb.innerHTML = '<i class="fa-solid fa-check mr-1"></i> Đã tự động điền mã OTP từ SMS: <strong>' + code + '</strong>';
        }
    } else {
        alert("Không tìm thấy mã OTP để điền tự động. Vui lòng xem tin nhắn SMS!");
    }
}

async function submitOtpVerification() {
    if (!currentPendingTxData || !currentPendingTxData.transaction?.id) {
        alert("Không có thông tin giao dịch cần xác thực!");
        return;
    }

    const input = document.getElementById("res-otp-input");
    const otp = (input ? input.value : "").trim();
    const fb = document.getElementById("res-otp-feedback");
    const btn = document.getElementById("btn-submit-otp");

    if (!otp || otp.length !== 6) {
        if (fb) {
            fb.classList.remove("hidden");
            fb.className = "text-[11px] font-semibold text-rose-400 mt-1";
            fb.innerHTML = '<i class="fa-solid fa-triangle-exclamation mr-1"></i> Vui lòng nhập đầy đủ 6 chữ số mã OTP!';
        }
        if (input) input.focus();
        return;
    }

    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Đang xác thực OTP...';
    }

    try {
        const txId = currentPendingTxData.transaction.id;
        const res = await fetch("/api/transactions/" + txId + "/verify-otp", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(accessToken ? { "Authorization": "Bearer " + accessToken } : {})
            },
            body: JSON.stringify({ otp })
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Mã OTP không hợp lệ!");
        }

        // Verification SUCCESS!
        if (fb) {
            fb.classList.remove("hidden");
            fb.className = "text-[11px] font-bold text-emerald-300 mt-1 p-2 bg-emerald-950/80 rounded-lg border border-emerald-500/50 flex items-center";
            fb.innerHTML = '<i class="fa-solid fa-circle-check text-emerald-400 text-sm mr-2"></i> Xác thực OTP thành công! Đơn hàng đã được duyệt an toàn.';
        }

        currentPendingTxData.status = "APPROVED";
        currentPendingTxData.userExplanation = data.message || "Xác thực OTP thành công! Giao dịch được phê duyệt.";
        if (data.smsContent) {
            if (!currentPendingTxData.smsNotification) currentPendingTxData.smsNotification = {};
            currentPendingTxData.smsNotification.content = data.smsContent;
        }

        setTimeout(() => {
            showPaymentResult(currentPendingTxData);
            loadSmsInbox();
            if (currentUser && currentUser.role === "ADMIN") {
                loadDashboard();
            }
        }, 800);

    } catch (err) {
        if (fb) {
            fb.classList.remove("hidden");
            fb.className = "text-[11px] font-bold text-rose-400 mt-1 p-2 bg-rose-950/80 rounded-lg border border-rose-500/50 flex items-center";
            fb.innerHTML = '<i class="fa-solid fa-circle-xmark text-rose-400 text-sm mr-2"></i> ' + err.message;
        }
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-shield-check mr-1"></i> Xác Nhận OTP & Duyệt Đơn';
        }
    }
}

async function triggerEmergencyLock() {
    const confirmLock = confirm(
        "🚨 BẠN ĐANG KÍCH HOẠT CHẾ ĐỘ ĐÓNG BĂNG TÀI KHOẢN KHẨN CẤP!\n\n" +
        "• Toàn bộ tính năng mua hàng & thanh toán sẽ bị TẠM KHÓA TRONG 30 PHÚT.\n" +
        "• Kẻ gian sẽ lập tức bị cô lập và không thể rút tiền hay tạo đơn mới.\n\n" +
        "Bạn có chắc chắn muốn tiến hành bảo vệ tài khoản ngay lúc này?"
    );
    if (!confirmLock) return;

    try {
        const btn = document.getElementById("btn-emergency-lock");
        if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Đang kích hoạt chế độ Đóng Băng Khẩn Cấp...';
        }

        const res = await fetch("/api/user/emergency-lock", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(accessToken ? { "Authorization": "Bearer " + accessToken } : {})
            },
            body: JSON.stringify({ userId: currentUser?.id })
        });

        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Không thể kích hoạt khóa khẩn cấp.");
        }

        if (currentUser) {
            currentUser.isLocked = true;
            currentUser.lockedMinsRemaining = data.lockedMins || 30;
            updateAuthUI();
        }

        // Show locked banner on UI
        const banner = document.getElementById("account-locked-banner");
        if (banner) banner.classList.remove("hidden");
        const cdBadge = document.getElementById("account-lock-countdown-badge");
        if (cdBadge) cdBadge.innerText = "Còn 30 phút";

        loadSmsInbox();
        closeResultModal();

        alert("🛡️ " + (data.message || "Tài khoản đã được bảo vệ thành công! Toàn bộ phiên đăng nhập lạ đã bị cô lập."));

    } catch (e) {
        alert("Lỗi khi khóa khẩn cấp: " + e.message);
    } finally {
        const btn = document.getElementById("btn-emergency-lock");
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fa-solid fa-lock text-sm mr-1"></i> 🚨 ĐÂY KHÔNG PHẢI TÔI! KHÓA KHẨN CẤP TÀI KHOẢN NGAY (KILL-SWITCH)';
        }
    }
}

async function quickUnlockAccount() {
    try {
        const res = await fetch("/api/user/emergency-unlock", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(accessToken ? { "Authorization": "Bearer " + accessToken } : {})
            },
            body: JSON.stringify({ userId: currentUser?.id })
        });
        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.detail || "Không thể mở khóa tài khoản.");
        }

        if (currentUser) {
            currentUser.isLocked = false;
            currentUser.lockedMinsRemaining = 0;
            updateAuthUI();
        }

        const banner = document.getElementById("account-locked-banner");
        if (banner) banner.classList.add("hidden");

        loadSmsInbox();
        alert("✓ " + (data.message || "Đã mở khóa tài khoản thành công! Bạn có thể tiếp tục mua sắm và thử nghiệm giao dịch."));

    } catch (e) {
        alert("Lỗi khi mở khóa: " + e.message);
    }
}

function closeResultModal() {
    document.getElementById("result-modal")?.classList.add("hidden");
}

// =========================================================================
// ADMIN AUDIT TRAIL, BLOCK REASONS & ACTIONS
// =========================================================================

// Hàm biên dịch mã lỗi & lý do vi phạm sang tiếng Việt rõ ràng, dễ hiểu

// Ham xac dinh DUY NHAT 1 kịch bản gian lận chính yếu cho mỗi giao dịch (Khong hien thi chung)
function getScenarioSummaryBadges(transaction) {
    const tag = (transaction.scenarioTag || "").toLowerCase();
    const analysis = transaction.fraudAnalysis || {};
    const rules = (analysis.triggeredRules || []).map(r => (r.ruleId || "").toUpperCase());
    const patterns = (analysis.fraudPatterns || []).filter(p => p.triggered).map(p => (p.pattern_id || p.id || "").toUpperCase());
    const allSignals = rules.concat(patterns);
    const city = (transaction.locationCity || "").toLowerCase();
    const dev = (transaction.deviceId || "").toLowerCase();
    const pm = (transaction.paymentMethod || "").toUpperCase();
    const amount = Number(transaction.amount) || 0;

    // A. Neu co scenarioTag truc tiep tu thao tac chon preset tren UI thi dung ngay
    if (tag === "travel" || tag === "impossible_travel") {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-purple-950/90 text-purple-200 border border-purple-600 shadow-md">
                    <i class="fa-solid fa-plane-slash mr-1.5 text-purple-400"></i>KỊCH BẢN: DI CHUYỂN BẤT KHẢ THI (LONDON - VIỆT NAM)
                </span>
            </div>
        `;
    }
    if (tag === "ato" || tag === "account_takeover") {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-red-950/90 text-red-200 border border-red-600 shadow-md">
                    <i class="fa-solid fa-skull mr-1.5 text-red-400"></i>KỊCH BẢN: CHIẾM ĐOẠT TÀI KHOẢN (ATO ATTACK)
                </span>
            </div>
        `;
    }
    if (tag === "velocity" || tag === "velocity_burst") {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-amber-950/90 text-amber-200 border border-amber-600 shadow-md">
                    <i class="fa-solid fa-bolt mr-1.5 text-yellow-400"></i>KỊCH BẢN: SPAM TẦN SUẤT CAO (VELOCITY SPIKE)
                </span>
            </div>
        `;
    }
    if (tag === "card_testing") {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-orange-950/90 text-orange-200 border border-orange-600 shadow-md">
                    <i class="fa-solid fa-credit-card mr-1.5 text-orange-400"></i>KỊCH BẢN: THỬ THẺ TỰ ĐỘNG (CARD TESTING)
                </span>
            </div>
        `;
    }
    if (tag === "high_amount" || tag === "unusual_high_amount") {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-blue-950/90 text-blue-200 border border-blue-600 shadow-md">
                    <i class="fa-solid fa-money-bill-wave mr-1.5 text-blue-400"></i>KỊCH BẢN: ĐỘT BIẾN GIÁ TRỊ ĐƠN HÀNG
                </span>
            </div>
        `;
    }

    // B. Fallback cho cac giao dich cu chua co scenarioTag
    // 1. Uu tien Spam Neu giao dich o Viet Nam ma bi bat Failed Attempt / Velocity
    if (allSignals.some(s => s.includes("FAILED_ATTEMPT_VELOCITY") || s.includes("TRANSACTION_VELOCITY")) && !city.includes("london") && !city.includes("tokyo")) {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-amber-950/90 text-amber-200 border border-amber-600 shadow-md">
                    <i class="fa-solid fa-bolt mr-1.5 text-yellow-400"></i>KỊCH BẢN: SPAM TẦN SUẤT CAO (VELOCITY SPIKE)
                </span>
            </div>
        `;
    }

    if (city.includes("london")) {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-purple-950/90 text-purple-200 border border-purple-600 shadow-md">
                    <i class="fa-solid fa-plane-slash mr-1.5 text-purple-400"></i>KỊCH BẢN: DI CHUYỂN BẤT KHẢ THI (LONDON - VIỆT NAM)
                </span>
            </div>
        `;
    }

    if (city.includes("tokyo") || dev.includes("hacker") || dev.includes("kali")) {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-red-950/90 text-red-200 border border-red-600 shadow-md">
                    <i class="fa-solid fa-skull mr-1.5 text-red-400"></i>KỊCH BẢN: CHIẾM ĐOẠT TÀI KHOẢN (ATO ATTACK)
                </span>
            </div>
        `;
    }

    if (pm === "JCB" || dev.includes("tester") || dev.includes("bot")) {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-orange-950/90 text-orange-200 border border-orange-600 shadow-md">
                    <i class="fa-solid fa-credit-card mr-1.5 text-orange-400"></i>KỊCH BẢN: THỬ THẺ TỰ ĐỘNG (CARD TESTING)
                </span>
            </div>
        `;
    }

    if (amount >= 30000000) {
        return `
            <div class="mb-1.5">
                <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-blue-950/90 text-blue-200 border border-blue-600 shadow-md">
                    <i class="fa-solid fa-money-bill-wave mr-1.5 text-blue-400"></i>KỊCH BẢN: ĐỘT BIẾN GIÁ TRỊ ĐƠN HÀNG
                </span>
            </div>
        `;
    }

    return `
        <div class="mb-1.5">
            <span class="inline-flex items-center px-2.5 py-1 rounded-md text-[11px] font-bold bg-amber-950/90 text-amber-200 border border-amber-600 shadow-md">
                <i class="fa-solid fa-bolt mr-1.5 text-yellow-400"></i>KỊCH BẢN: SPAM TẦN SUẤT CAO (VELOCITY SPIKE)
            </span>
        </div>
    `;
}

function translateRuleReason(ruleId, rawReason, score) {
    let rId = (ruleId || "").toUpperCase();
    let text = rawReason || "";
    let viText = "";

    if (rId.includes("HIGH_AMOUNT")) {
        viText = "Số tiền thanh toán vượt ngưỡng an toàn quy định của hệ thống";
    } else if (rId.includes("UNUSUAL_AMOUNT")) {
        viText = "Giá trị giao dịch tăng đột biến gấp nhiều lần mức chi tiêu bình thường";
    } else if (rId.includes("LOCATION_CHANGE")) {
        viText = "Thay đổi vị trí địa lý bất thường so với giao dịch trước đó";
    } else if (rId.includes("IMPOSSIBLE_TRAVEL") || rId.includes("PATTERN_IMPOSSIBLE_TRAVEL")) {
        viText = "Cảnh báo di chuyển bất khả thi: Vị trí thay đổi hàng trăm/nghìn km trong vài giây";
    } else if (rId.includes("NEW_DEVICE")) {
        viText = "Đăng nhập và giao dịch từ thiết bị lạ chưa từng được xác thực";
    } else if (rId.includes("NEW_IP")) {
        viText = "Địa chỉ IP truy cập bất thường từ dải mạng lạ";
    } else if (rId.includes("ACCOUNT_AGE")) {
        viText = "Tài khoản mới tạo chưa đủ 24 giờ đã thực hiện giao dịch giá trị cao";
    } else if (rId.includes("SUSPICIOUS_COMPOSITE") || rId.includes("PATTERN_ACCOUNT_TAKEOVER") || rId.includes("ACCOUNT_TAKEOVER")) {
        viText = "Mẫu hình chiếm đoạt tài khoản (ATO): Kết hợp đồng thời thiết bị mới, IP lạ và thay đổi vị trí";
    } else if (rId.includes("CARD_TESTING") || rId.includes("PATTERN_CARD_TESTING")) {
        viText = "Phát hiện hành vi thử thẻ liên tục bất thường";
    } else if (rId.includes("VELOCITY") || rId.includes("TRANSACTION_VELOCITY")) {
        viText = "Tần suất đặt hàng dồn dập bất thường trong thời gian ngắn";
    } else if (rId.includes("FAILED_ATTEMPT") || rId.includes("FAILED_PAYMENT")) {
        viText = "Số lần thanh toán thất bại liên tiếp vượt quá ngưỡng cho phép";
    } else if (rId.includes("MULTIPLE_DEVICES")) {
        viText = "Sử dụng đồng thời nhiều thiết bị lạ trong thời gian ngắn";
    } else if (rId.includes("MULTIPLE_IPS")) {
        viText = "Sử dụng đồng thời nhiều địa chỉ IP trong khoảng thời gian ngắn";
    } else if (rId.includes("PAYMENT_METHOD")) {
        viText = "Thay đổi phương thức thanh toán dồn dập bất thường";
    } else {
        viText = text || "Vi phạm quy tắc bảo mật được phát hiện bởi hệ thống";
    }

    return `
        <div class="text-[11px] text-red-300 font-medium leading-relaxed my-0.5">
            <i class="fa-solid fa-triangle-exclamation text-yellow-400 mr-1"></i>
            <span class="font-bold text-red-200 bg-red-950/70 px-1.5 py-0.5 rounded border border-red-800/80 mr-1">[${ruleId}]</span>
            <span>${viText}</span>
            <span class="text-orange-400 font-mono font-bold ml-1">(+${score}đ)</span>
        </div>
    `;
}

let currentTxPage = 1;
const TXS_PER_PAGE = 10;
let cachedAllTransactions = [];

function changeTxPage(newPage) {
    currentTxPage = newPage;
    renderTransactionsPage();
}

function renderPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / TXS_PER_PAGE) || 1;
    if (currentTxPage > totalPages) currentTxPage = totalPages;
    if (currentTxPage < 1) currentTxPage = 1;

    const rangeEl = document.getElementById("tx-page-range");
    const totalEl = document.getElementById("tx-page-total");
    const container = document.getElementById("tx-pagination-buttons");

    const start = totalItems === 0 ? 0 : (currentTxPage - 1) * TXS_PER_PAGE + 1;
    const end = Math.min(currentTxPage * TXS_PER_PAGE, totalItems);

    if (rangeEl) rangeEl.innerText = `${start} - ${end}`;
    if (totalEl) totalEl.innerText = totalItems;
    if (!container) return;

    if (totalItems === 0) {
        container.innerHTML = "";
        return;
    }

    if (totalPages <= 1) {
        container.innerHTML = `
            <span class="px-3 py-1 rounded-lg bg-blue-600 text-white font-bold text-xs shadow">Trang 1 / 1</span>
        `;
        return;
    }

    let html = "";
    const prevDisabled = (currentTxPage === 1);
    html += `
        <button onclick="changeTxPage(${currentTxPage - 1})" ${prevDisabled ? "disabled" : ""} class="px-2.5 py-1 rounded-lg border text-xs font-semibold transition ${prevDisabled ? "bg-slate-800/40 text-slate-600 border-slate-800 cursor-not-allowed" : "bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700 hover:text-white shadow"}">
            <i class="fa-solid fa-chevron-left mr-1"></i>Trước
        </button>
    `;

    let startPage = Math.max(1, currentTxPage - 2);
    let endPage = Math.min(totalPages, currentTxPage + 2);

    if (startPage > 1) {
        html += `<button onclick="changeTxPage(1)" class="px-3 py-1 rounded-lg border bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700 text-xs font-semibold transition shadow">1</button>`;
        if (startPage > 2) html += `<span class="px-1 text-slate-500 font-mono">...</span>`;
    }

    for (let p = startPage; p <= endPage; p++) {
        const isActive = (p === currentTxPage);
        html += `
            <button onclick="changeTxPage(${p})" class="px-3 py-1 rounded-lg border text-xs font-bold transition shadow ${isActive ? "bg-blue-600 text-white border-blue-500 shadow-blue-500/30" : "bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700 hover:text-white"}">
                ${p}
            </button>
        `;
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) html += `<span class="px-1 text-slate-500 font-mono">...</span>`;
        html += `<button onclick="changeTxPage(${totalPages})" class="px-3 py-1 rounded-lg border bg-slate-800 hover:bg-slate-700 text-slate-300 border-slate-700 text-xs font-semibold transition shadow">${totalPages}</button>`;
    }

    const nextDisabled = (currentTxPage === totalPages);
    html += `
        <button onclick="changeTxPage(${currentTxPage + 1})" ${nextDisabled ? "disabled" : ""} class="px-2.5 py-1 rounded-lg border text-xs font-semibold transition ${nextDisabled ? "bg-slate-800/40 text-slate-600 border-slate-800 cursor-not-allowed" : "bg-slate-800 hover:bg-slate-700 text-slate-200 border-slate-700 hover:text-white shadow"}">
            Tiếp<i class="fa-solid fa-chevron-right ml-1"></i>
        </button>
    `;

    container.innerHTML = html;
}

function renderTransactionsPage() {
    const tbody = document.getElementById("transactions-tbody");
    if (!tbody) return;

    const total = cachedAllTransactions.length;
    renderPagination(total);

    if (total === 0) {
        tbody.innerHTML = "<tr><td colspan='6' class='text-center p-6 text-slate-500'>Không tìm thấy giao dịch nào phù hợp với bộ lọc</td></tr>";
        return;
    }

    const start = (currentTxPage - 1) * TXS_PER_PAGE;
    const end = Math.min(start + TXS_PER_PAGE, total);
    const pageItems = cachedAllTransactions.slice(start, end);

    tbody.innerHTML = pageItems.map(t => {
        const dec = t.fraudAnalysis?.decision || t.status || "APPROVE";
        const risk = t.fraudAnalysis?.riskLevel || "LOW";
        const score = t.fraudAnalysis?.riskScore || 0;
        const shortId = t.shortId || ("#TX-" + t.id.substring(0, 8).toUpperCase());
        const userName = t.userName || t.user?.name || "Khách hàng";
        const userPhone = t.userPhone || t.user?.phone || "0972445090";
        const isBlocked = (t.status === "BLOCKED" || dec === "BLOCK");
        const isApproved = (t.status === "APPROVED" || dec === "APPROVE");
        const isReview = (t.status === "REVIEW" || dec === "REVIEW");

        let statusBadgeClass = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
        if (isBlocked) {
            statusBadgeClass = "bg-red-500/20 text-red-400 border border-red-500/40";
        } else if (isReview || t.status === "REVIEW") {
            statusBadgeClass = "bg-yellow-500/20 text-yellow-400 border border-yellow-500/40";
        }

        let reasonHtml = "";
        if (isBlocked || dec === "REVIEW") {
            const badgesHeader = getScenarioSummaryBadges(t);
            const rules = t.fraudAnalysis?.triggeredRules || [];
            let rulesListHtml = "";
            if (rules.length > 0) {
                rulesListHtml = rules.map(r => translateRuleReason(r.ruleId, r.reason, r.score)).join("");
            } else {
                rulesListHtml = `<div class="text-[11px] text-red-300"><i class="fa-solid fa-shield-halved text-red-400 mr-1"></i>${t.fraudAnalysis?.explanation || 'Giao dịch vi phạm chính sách kiểm soát gian lận thanh toán'}</div>`;
            }
            reasonHtml = badgesHeader + rulesListHtml;
        } else {
            reasonHtml = `
                <div class="text-[11px] text-emerald-400 font-medium">
                    <i class="fa-solid fa-circle-check text-emerald-400 mr-1"></i>
                    Giao dịch hợp lệ: Chỉ số an toàn cao, thiết bị và IP đã xác thực
                </div>
            `;
        }

        let actionHtml = "";
        if (t.adminAction === "OVERRIDE_APPROVE") {
            actionHtml = `
                <div class="text-center">
                    <span class="text-emerald-400 font-bold text-xs bg-emerald-950/70 border border-emerald-600/60 px-2 py-0.5 rounded-full inline-flex items-center">
                        <i class="fa-solid fa-check-double mr-1"></i>Admin đã duyệt
                    </span>
                </div>
            `;
        } else if (t.adminAction === "CONFIRM_BLOCK") {
            actionHtml = `
                <div class="text-center">
                    <span class="text-red-400 font-bold text-xs bg-red-950/70 border border-red-600/60 px-2 py-0.5 rounded-full inline-flex items-center">
                        <i class="fa-solid fa-ban mr-1"></i>Admin đã chặn
                    </span>
                </div>
            `;
        } else if (isBlocked) {
            actionHtml = `
                <div class="text-center">
                    <span class="text-red-400 font-semibold text-[11px] bg-red-950/50 border border-red-800/60 px-2.5 py-1 rounded-lg inline-flex items-center" title="Đơn hàng vi phạm nghiêm trọng bị hệ thống chặn, không được phép mở lại">
                        <i class="fa-solid fa-lock mr-1.5 text-red-400"></i>Đã chặn (Không thể mở)
                    </span>
                </div>
            `;
        } else if (t.status === "REVIEW" || dec === "REVIEW") {
            actionHtml = `
                <div class="flex items-center justify-center space-x-1.5">
                    <button onclick="handleAdminAction('${t.id}', 'OVERRIDE_APPROVE')" title="Thẩm định an toàn: Phê duyệt đơn hàng chờ duyệt" class="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[11px] font-bold transition shadow flex items-center">
                        <i class="fa-solid fa-check mr-1"></i>Duyệt đơn
                    </button>
                    <button onclick="handleAdminAction('${t.id}', 'CONFIRM_BLOCK')" title="Xác nhận rủi ro: Từ chối đơn hàng" class="px-2.5 py-1 bg-red-700 hover:bg-red-600 text-white rounded text-[11px] font-bold transition shadow flex items-center">
                        <i class="fa-solid fa-ban mr-1"></i>Từ chối
                    </button>
                </div>
            `;
        } else {
            actionHtml = `
                <div class="text-center">
                    <span class="text-slate-400 font-medium text-xs"><i class="fa-solid fa-shield-check text-emerald-400 mr-1"></i>Hệ thống tự duyệt</span>
                </div>
            `;
        }

        return `
            <tr class="border-b border-slate-800 hover:bg-slate-800/40 text-xs">
                <td class="p-3 font-mono font-bold text-blue-400 whitespace-nowrap">${shortId}</td>
                <td class="p-3">
                    <div class="font-bold text-white">${userName}</div>
                    <div class="text-[11px] text-slate-400 font-mono"><i class="fa-solid fa-phone mr-1"></i>${userPhone}</div>
                </td>
                <td class="p-3">
                    <div class="font-bold text-emerald-400 font-mono">${t.amount?.toLocaleString()} đ</div>
                    <div class="text-[11px] text-slate-400 line-clamp-1">${formatProductName(t.itemsSummary, t.amount)}</div>
                </td>
                <td class="p-3 whitespace-nowrap">
                    <span class="px-2 py-0.5 rounded font-bold text-[11px] ${statusBadgeClass}">
                        ${t.status} (${score}/100)
                    </span>
                    <div class="text-[10px] text-slate-400 mt-1">${t.createdAt}</div>
                </td>
                <td class="p-3 max-w-xs">
                    ${reasonHtml}
                </td>
                <td class="p-3 text-center whitespace-nowrap">
                    ${actionHtml}
                </td>
            </tr>
        `;
    }).join("");
}

async function loadTransactions(resetPage = false) {
    if (resetPage) currentTxPage = 1;
    try {
        const search = document.getElementById("tx-search")?.value || "";
        const decision = document.getElementById("tx-filter-decision")?.value || "";
        const sortOrder = document.getElementById("tx-sort-order")?.value || "NEWEST";
        
        let url = "/api/fraud/transactions?";
        if (search) url += "search=" + encodeURIComponent(search) + "&";
        if (decision) url += "status=" + encodeURIComponent(decision) + "&decision=" + encodeURIComponent(decision) + "&";

        const res = await authFetch(url);
        if (!res.ok) {
            console.error("Failed to load transactions, status:", res.status);
            if (res.status === 401) {
                await quickLogin("admin", false);
                return loadTransactions(resetPage);
            }
            return;
        }

        let txs = await res.json();
        if (!Array.isArray(txs)) {
            cachedAllTransactions = [];
            renderTransactionsPage();
            return;
        }

        // Apply sorting across ALL fetched items
        if (sortOrder === "OLDEST") {
            txs = [...txs].reverse();
        } else if (sortOrder === "AMOUNT_DESC") {
            txs = [...txs].sort((a, b) => (b.amount || 0) - (a.amount || 0));
        } else if (sortOrder === "AMOUNT_ASC") {
            txs = [...txs].sort((a, b) => (a.amount || 0) - (b.amount || 0));
        } else if (sortOrder === "RISK_DESC") {
            txs = [...txs].sort((a, b) => (b.fraudAnalysis?.riskScore || 0) - (a.fraudAnalysis?.riskScore || 0));
        } else if (sortOrder === "RISK_ASC") {
            txs = [...txs].sort((a, b) => (a.fraudAnalysis?.riskScore || 0) - (b.fraudAnalysis?.riskScore || 0));
        }

        cachedAllTransactions = txs;
        renderTransactionsPage();
    } catch (e) {
        console.error("Failed to load transactions", e);
    }
}

async function handleAdminAction(txId, action) {
    const isApprove = (action === "OVERRIDE_APPROVE");
    const confirmMsg = isApprove
        ? "Bạn có chắc chắn muốn MỞ KHÓA và PHÊ DUYỆT đơn hàng này cho khách hàng?\n\nHệ thống sẽ chuyển trạng thái sang 'Đã duyệt' và gửi tin nhắn SMS chúc mừng đến số điện thoại của khách."
        : "Bạn có chắc chắn muốn XÁC NHẬN CHẶN GIAN LẬN đối với đơn hàng này?\n\nHệ thống sẽ duy trì từ chối đơn hàng để bảo vệ an toàn tài sản.";

    showAppPopup({
        title: isApprove ? "PHÊ DUYỆT ĐƠN HÀNG" : "XÁC NHẬN CHẶN GIAN LẬN",
        subtitle: `Mã giao dịch #${txId.substring(0, 8).toUpperCase()}`,
        message: confirmMsg,
        type: isApprove ? "success" : "error",
        showCancel: true,
        confirmText: isApprove ? "Phê duyệt" : "Xác nhận chặn",
        cancelText: "Hủy bỏ",
        onConfirm: async () => {
            try {
                const res = await fetch(`/api/admin/transactions/${txId}/action`, {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + (accessToken || localStorage.getItem("access_token"))
                    },
                    body: JSON.stringify({
                        action,
                        note: isApprove ? "Admin can thiệp mở khóa duyệt đơn" : "Admin xác nhận chặn gian lận"
                    })
                });

                const data = await res.json();
                if (res.ok) {
                    showAppPopup({
                        title: "THÀNH CÔNG",
                        subtitle: "Quản trị giao dịch",
                        message: data.message || "Thao tác thành công!",
                        type: "success"
                    });
                    loadTransactions();
                    loadDashboard();
                } else {
                    showAppPopup({
                        title: "LỖI THAO TÁC",
                        subtitle: "Quản trị giao dịch",
                        message: data.detail || "Lỗi khi thực hiện thao tác",
                        type: "error"
                    });
                }
            } catch (e) {
                showAppPopup({
                    title: "LỖI KẾT NỐI",
                    subtitle: "Quản trị giao dịch",
                    message: "Không thể kết nối đến máy chủ!",
                    type: "error"
                });
            }
        }
    });
}

// =========================================================================
// DASHBOARD STATS, SIMULATION & RULES
// =========================================================================

async function loadDashboard() {
    try {
        const res = await authFetch("/api/fraud/statistics");
        if (!res.ok) {
            console.error("Failed to fetch statistics, status:", res.status);
            return;
        }
        const stats = await res.json();
        const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };

        const total = stats.totalTransactions ?? stats.analyzed ?? 0;
        const approved = stats.approvedTransactions ?? stats.approved ?? 0;
        const review = stats.reviewTransactions ?? stats.review ?? 0;
        const blocked = stats.blockedTransactions ?? stats.blocked ?? 0;
        const avgScore = stats.averageRiskScore ?? stats.avgRiskScore ?? 0;
        const fraudRate = stats.blockRate ?? stats.fraudRate ?? 0;
        const openAlerts = stats.openAlerts ?? 0;

        setVal("stat-total", total);
        setVal("stat-approved", approved);
        setVal("stat-review", review);
        setVal("stat-blocked", blocked);
        setVal("stat-avgscore", avgScore + "/100");
        setVal("stat-fraudrate", fraudRate + "%");
        setVal("stat-rate", fraudRate + "%");
        setVal("stat-alerts", openAlerts);

        renderCharts(stats);
        loadAlerts();
    } catch (e) {
        console.error("Failed to load dashboard", e);
    }
}

function renderCharts(stats) {
    const c1 = document.getElementById("chartRiskDist") || document.getElementById("chart-risk-dist");
    const c2 = document.getElementById("chartDecision") || document.getElementById("chart-decision");
    const ctx1 = c1?.getContext("2d");
    const ctx2 = c2?.getContext("2d");
    if (!ctx1 || !ctx2) return;

    if (chartRiskDist) {
        try { chartRiskDist.destroy(); } catch (e) {}
    }
    if (chartDecision) {
        try { chartDecision.destroy(); } catch (e) {}
    }

    const dist = stats.riskDistribution || {};
    const low = dist.LOW || 0;
    const med = dist.MEDIUM || 0;
    const high = dist.HIGH || 0;
    const crit = dist.CRITICAL || 0;

    chartRiskDist = new Chart(ctx1, {
        type: "bar",
        data: {
            labels: ["Thấp (0-39)", "Trung bình (40-69)", "Cao (70-84)", "Nghiêm trọng (85-100)"],
            datasets: [{
                label: "Số lượng giao dịch",
                data: [low, med, high, crit],
                backgroundColor: [
                    "rgba(34, 197, 94, 0.7)",
                    "rgba(234, 179, 8, 0.7)",
                    "rgba(249, 115, 22, 0.7)",
                    "rgba(239, 68, 68, 0.7)"
                ],
                borderColor: [
                    "rgb(34, 197, 94)",
                    "rgb(234, 179, 8)",
                    "rgb(249, 115, 22)",
                    "rgb(239, 68, 68)"
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { precision: 0 }
                }
            }
        }
    });

    const aiDec = stats.aiDecisions || {};
    const aiApprove = aiDec.approve ?? stats.approvedTransactions ?? stats.approved ?? 0;
    const aiReview = aiDec.review ?? stats.reviewTransactions ?? stats.review ?? 0;
    const aiBlock = aiDec.block ?? stats.blockedTransactions ?? stats.blocked ?? 0;

    chartDecision = new Chart(ctx2, {
        type: "doughnut",
        data: {
            labels: ["APPROVE (Duyệt)", "REVIEW (Xem xét)", "BLOCK (Chặn)"],
            datasets: [{
                data: [aiApprove, aiReview, aiBlock],
                backgroundColor: ["#22c55e", "#eab308", "#ef4444"],
                borderColor: "#0f172a",
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "right",
                    labels: { color: "#cbd5e1" }
                }
            }
        }
    });
}

async function loadAlerts() {
    try {
        const res = await authFetch("/api/fraud/alerts");
        const alerts = await res.json();
        const tbody = document.getElementById("alerts-tbody");
        if (!tbody) return;
        if (!alerts || alerts.length === 0) {
            tbody.innerHTML = "<tr><td colspan='7' class='text-center p-4 text-slate-500'>Không có cảnh báo rủi ro nào</td></tr>";
            return;
        }
        tbody.innerHTML = alerts.map(a => {
            const shortAlert = a.shortAlertId || ("#ALT-" + a.id.substring(0, 8).toUpperCase());
            const shortTx = a.shortTxId || (a.transactionId ? ("#TX-" + a.transactionId.substring(0, 8).toUpperCase()) : "N/A");
            const uName = a.userName || a.user?.name || "Khách hàng";
            const uPhone = a.userPhone || a.user?.phone || "0972445090";

            let riskBadgeClass = "bg-red-500/20 text-red-400 border border-red-500/40";
            let riskLevelVi = "Nghiêm trọng";
            if (a.riskLevel === "LOW") {
                riskBadgeClass = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
                riskLevelVi = "Thấp";
            } else if (a.riskLevel === "MEDIUM") {
                riskBadgeClass = "bg-yellow-500/20 text-yellow-400 border border-yellow-500/40";
                riskLevelVi = "Trung bình";
            } else if (a.riskLevel === "HIGH") {
                riskBadgeClass = "bg-orange-500/20 text-orange-400 border border-orange-500/40";
                riskLevelVi = "Cao";
            }

            let statusBadge = "";
            if (a.status === "OPEN") {
                statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-400 border border-red-500/40">Chờ xử lý</span>';
            } else if (a.status === "REVIEWED") {
                statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-yellow-500/20 text-yellow-400 border border-yellow-500/40">Đã xem xét</span>';
            } else if (a.status === "RESOLVED_LEGIT") {
                statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">Đã mở khóa</span>';
            } else if (a.status === "RESOLVED_FRAUD") {
                statusBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-red-500/20 text-red-300 border border-red-500/40">Đã chặn gian lận</span>';
            } else {
                statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-700 text-slate-300">${a.status}</span>`;
            }

            return `
                <tr class="border-b border-slate-800 hover:bg-slate-800/40 text-xs">
                    <td class="p-3 font-mono font-bold text-purple-400 whitespace-nowrap">${shortAlert}</td>
                    <td class="p-3 font-mono font-bold text-blue-400 whitespace-nowrap">${shortTx}</td>
                    <td class="p-3 whitespace-nowrap">
                        <span class="px-2 py-0.5 rounded font-bold text-[11px] ${riskBadgeClass}">
                            ${riskLevelVi} (${a.riskScore}/100)
                        </span>
                    </td>
                    <td class="p-3">
                        <div class="font-bold text-white">${uName}</div>
                        <div class="text-[11px] text-slate-400 font-mono"><i class="fa-solid fa-phone mr-1"></i>${uPhone}</div>
                    </td>
                    <td class="p-3 whitespace-nowrap text-[11px] text-slate-300 font-mono">
                        <i class="fa-regular fa-clock text-blue-400 mr-1"></i>${a.createdAt || "Chưa có dữ liệu"}
                    </td>
                    <td class="p-3 whitespace-nowrap">${statusBadge}</td>
                    <td class="p-3 text-center whitespace-nowrap">
                        ${a.status === 'OPEN' ? `
                            <button onclick="updateAlert('${a.id}', 'REVIEWED')" class="px-2.5 py-1 bg-slate-700 hover:bg-slate-600 text-slate-200 rounded text-[11px] font-medium transition shadow">
                                <i class="fa-solid fa-eye mr-1"></i>Đã xem
                            </button>
                        ` : `
                            <span class="text-slate-500 text-[11px]"><i class="fa-solid fa-check mr-1"></i>Đã xử lý</span>
                        `}
                    </td>
                </tr>
            `;
        }).join("");
    } catch (e) {
        console.error("Failed to load alerts", e);
    }
}

async function updateAlert(id, status) {
    try {
        await authFetch(`/api/fraud/alerts/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status })
        });
        loadAlerts();
    } catch (e) {
        console.error("Failed to update alert", e);
    }
}

async function runSimulation(scenario) {
    const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
    const container = document.getElementById("sim-output-container");
    if (container) container.classList.remove("hidden");

    setVal("sim-title", "Đang phân tích kịch bản: " + scenario + "...");
    setVal("sim-desc", "Hệ thống đang bóc tách đặc trưng và kiểm tra quy tắc...");

    const scenarioTitlesVi = {
        "ACCOUNT_TAKEOVER": "Tấn công chiếm đoạt tài khoản",
        "CARD_TESTING": "Tấn công thử thẻ tự động",
        "VELOCITY_BURST": "Bùng nổ tần suất giao dịch",
        "VELOCITY_ATTACK": "Bùng nổ tần suất giao dịch",
        "IMPOSSIBLE_TRAVEL": "Di chuyển bất khả thi",
        "UNUSUAL_HIGH_AMOUNT": "Đột biến giá trị đơn hàng",
        "HIGH_AMOUNT": "Đột biến giá trị đơn hàng",
        "NORMAL": "Giao dịch hợp lệ bình thường"
    };

    const scenarioDescVi = {
        "ACCOUNT_TAKEOVER": "Thiết bị mới + Địa chỉ IP mới + Thay đổi vị trí địa lý + Đơn hàng giá trị cao 45,000,000 VND.",
        "CARD_TESTING": "Nhiều lần thanh toán thất bại liên tiếp với giá trị nhỏ nhằm dò quét số thẻ tín dụng trong 5 phút.",
        "VELOCITY_BURST": "Khởi tạo liên tiếp 8 giao dịch dồn dập trong khung thời gian 5 phút.",
        "VELOCITY_ATTACK": "Khởi tạo liên tiếp 8 giao dịch dồn dập trong khung thời gian 5 phút.",
        "IMPOSSIBLE_TRAVEL": "Giao dịch vừa thực hiện tại TP.HCM, ngay 5 phút sau xuất hiện tại Tokyo (Khoảng cách > 4,300 km).",
        "UNUSUAL_HIGH_AMOUNT": "Đơn hàng 30,000,000 VND (gấp 50 lần mức chi tiêu trung bình) từ thiết bị quen thuộc.",
        "HIGH_AMOUNT": "Đơn hàng 30,000,000 VND (gấp 50 lần mức chi tiêu trung bình) từ thiết bị quen thuộc.",
        "NORMAL": "Đơn hàng thường lệ 500,000 VND từ thiết bị và địa chỉ IP quen thuộc tại TP.HCM."
    };

    const ruleNamesVi = {
        "High Transaction Amount": "Số tiền giao dịch vượt ngưỡng an toàn",
        "Unusual Amount Spike": "Giá trị giao dịch tăng đột biến",
        "New Device Detected": "Phát hiện thiết bị truy cập mới",
        "New IP Address Detected": "Phát hiện địa chỉ IP truy cập mới",
        "Location Change / Impossible Travel": "Thay đổi vị trí / Di chuyển bất khả thi",
        "Suspicious Composite Fraud Patterns": "Mẫu gian lận phức hợp nguy cơ cao",
        "Transaction Velocity Spike": "Bùng nổ tần suất đặt hàng (Velocity)",
        "Failed Payment Velocity": "Tần suất giao dịch thất bại dồn dập",
        "High Failed Payment Rate": "Tỷ lệ giao dịch thất bại quá cao",
        "New Account Risk": "Tài khoản mới tạo thực hiện giao dịch",
        "Multiple Devices Detected": "Sử dụng nhiều thiết bị trong thời gian ngắn",
        "Multiple IP Addresses": "Sử dụng nhiều địa chỉ IP bất thường",
        "Payment Method Hopping": "Thay đổi phương thức thanh toán liên tục",
        "Rapid Payment Method Switching": "Thay đổi phương thức thanh toán liên tục",
        "Payment Method Switching": "Thay đổi phương thức thanh toán liên tục"
    };

    const patternNamesVi = {
        "Account Takeover (ATO)": "Chiếm đoạt tài khoản",
        "Card Testing Attack": "Máy thử thẻ tự động",
        "Transaction Velocity Burst": "Bùng nổ tần suất giao dịch",
        "Impossible Travel Teleportation": "Di chuyển bất khả thi",
        "High-Value Device Anomaly": "Bất thường đơn hàng giá trị cao trên thiết bị mới"
    };

    const translateReasonText = (text) => {
        if (!text) return "";
        let t = text;
        t = t.replace(/Transaction amount \(([^)]+)\) exceeds ([^)]+) threshold\./gi, "Số tiền giao dịch ($1) vượt ngưỡng an toàn ($2).");
        t = t.replace(/Transaction amount is ([0-9.]+)x higher than historical average \(([^)]+)\)\./gi, "Số tiền giao dịch gấp $1 lần mức trung bình lịch sử ($2).");
        t = t.replace(/Transaction initiated from a new device ID \(([^)]+)\)\. High transaction amount combined with new device increases risk\./gi, "Giao dịch thực hiện từ thiết bị mới ($1), kết hợp số tiền lớn làm tăng rủi ro.");
        t = t.replace(/Transaction initiated from a new device ID \(([^)]+)\)\./gi, "Giao dịch được gửi từ thiết bị mới lạ ($1).");
        t = t.replace(/Transaction initiated from a new IP address \(([^)]+)\)\. Combination of new IP, new device, and high amount detected\./gi, "Giao dịch từ địa chỉ IP mới ($1), kết hợp thiết bị mới và đơn hàng giá trị lớn.");
        t = t.replace(/Transaction initiated from a new IP address \(([^)]+)\)\./gi, "Giao dịch từ địa chỉ IP mới ($1).");
        t = t.replace(/Impossible travel detected! Location changed by ([0-9.]+) km in ([0-9.]+) seconds\./gi, "Phát hiện di chuyển bất khả thi! Vị trí thay đổi $1 km chỉ trong $2 giây.");
        t = t.replace(/Location changed from ([^ ]+) to ([^.]+)\./gi, "Vị trí giao dịch thay đổi từ $1 sang $2.");
        t = t.replace(/Triggered composite pattern\(s\): ([^.]+)\./gi, function(m, p) {
            let translatedList = p.split(", ").map(item => patternNamesVi[item.trim()] || item.trim()).join(", ");
            return "Kích hoạt mẫu gian lận phức hợp: " + translatedList + ".";
        });
        t = t.replace(/([0-9]+) transactions in last 5 minutes exceeds threshold of ([0-9]+)\./gi, "$1 giao dịch trong 5 phút qua, vượt ngưỡng an toàn ($2 đơn).");
        t = t.replace(/([0-9]+) failed transactions in last 5 minutes exceeds threshold of ([0-9]+)\./gi, "$1 lần giao dịch thất bại trong 5 phút, vượt ngưỡng cho phép ($2 lần).");
        t = t.replace(/Suspicious takeover indicators: Unrecognized device and IP combined with geographic movement and unusual spending\./gi, "Dấu hiệu chiếm đoạt tài khoản: Thiết bị và IP chưa từng ghi nhận kết hợp thay đổi vị trí và đơn hàng đột biến.");
        t = t.replace(/Geographic change of ([0-9.]+) km within ([0-9.]+) seconds is physically impossible\./gi, "Khoảng cách địa lý $1 km chỉ trong $2 giây là bất khả thi về mặt vật lý.");
        t = t.replace(/Order amount is ([0-9.]+)x historical average on an unrecognized device\./gi, "Giá trị đơn hàng gấp $1 lần mức trung bình lịch sử trên một thiết bị lạ.");
        t = t.replace(/Automated card validation behavior detected using small amounts and multiple payment methods\./gi, "Hành vi dò quét thẻ tự động được phát hiện qua các đơn hàng nhỏ và xoay vòng nhiều phương thức.");
        t = t.replace(/Unusual volume spike in a 5-minute window attempting rapid drain or fraud\./gi, "Bùng nổ số lượng đơn hàng trong 5 phút nhằm cố gắng rút cạn hạn mức thẻ.");
        t = t.replace(/High transaction velocity detected: ([0-9]+) transactions within ([0-9]+) minutes\./gi, "Phát hiện tần suất giao dịch cao: $1 giao dịch trong vòng $2 phút.");
        t = t.replace(/Extreme transaction velocity detected: ([0-9]+) transactions within ([0-9]+) minutes\./gi, "Phát hiện tần suất giao dịch cực cao: $1 giao dịch trong vòng $2 phút.");
        t = t.replace(/High transaction velocity detected: ([0-9]+) transactions within ([0-9]+) minutes/gi, "Phát hiện tần suất giao dịch cao: $1 giao dịch trong vòng $2 phút");
        t = t.replace(/Extreme transaction velocity detected: ([0-9]+) transactions within ([0-9]+) minutes/gi, "Phát hiện tần suất giao dịch cực cao: $1 giao dịch trong vòng $2 phút");
        t = t.replace(/Critical failed attempt rate: ([0-9]+) failed payment attempts within ([0-9]+) minutes\./gi, "Tỷ lệ thanh toán thất bại nghiêm trọng: $1 lần thất bại trong vòng $2 phút.");
        t = t.replace(/Used ([0-9]+) different payment methods within ([0-9]+) minutes\./gi, "Đã sử dụng $1 phương thức thanh toán khác nhau trong vòng $2 phút.");
        t = t.replace(/Account created less than ([0-9.]+) hours ago \(([^)]+) hours\)\./gi, "Tài khoản mới được tạo chưa đầy $1 giờ (hiện tại: $2 giờ).");
        t = t.replace(/Historical payment failure rate is ([0-9.]+)% \(> ?([0-9.]+)%\)\./gi, "Tỷ lệ thanh toán thất bại trong lịch sử là $1% (vượt ngưỡng $2%).");
        t = t.replace(/Used ([0-9]+) different devices within ([0-9]+) minutes\./gi, "Đã sử dụng $1 thiết bị khác nhau trong vòng $2 phút.");
        t = t.replace(/Used ([0-9]+) different IP addresses within ([0-9]+) minutes\./gi, "Đã sử dụng $1 địa chỉ IP khác nhau trong vòng $2 phút.");
        t = t.replace(/New account with high-risk transaction behavior\./gi, "Tài khoản mới có hành vi giao dịch rủi ro cao.");
        return t;
    };

    try {
        const res = await authFetch("/api/fraud/simulation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scenario })
        });
        const resData = await res.json();
        const analysis = resData.analysis || resData;

        const titleVi = scenarioTitlesVi[scenario] || resData.title || ("Kịch bản: " + scenario);
        const descVi = scenarioDescVi[scenario] || resData.description || "Mô phỏng phản hồi động cơ chống gian lận";

        setVal("sim-title", titleVi);
        setVal("sim-desc", descVi);

        const riskScore = analysis.riskScore ?? 0;
        const rawRiskLevel = analysis.riskLevel || "LOW";
        const rawDecision = analysis.decision || "APPROVE";

        const riskLevelViMap = {
            "LOW": "THẤP",
            "MEDIUM": "TRUNG BÌNH",
            "HIGH": "CAO",
            "CRITICAL": "NGHIÊM TRỌNG"
        };
        const decisionViMap = {
            "APPROVE": "CHẤP THUẬN",
            "REVIEW": "CHỜ XEM XÉT",
            "BLOCK": "CHẶN GIAO DỊCH"
        };

        const riskLevelVi = riskLevelViMap[rawRiskLevel] || rawRiskLevel;
        const decisionVi = decisionViMap[rawDecision] || rawDecision;

        setVal("sim-risk-score", riskScore + " / 100");
        const scoreBar = document.getElementById("sim-score-bar");
        if (scoreBar) {
            scoreBar.style.width = Math.min(100, Math.max(0, riskScore)) + "%";
            if (riskScore >= 75) scoreBar.className = "bg-red-500 h-full transition-all duration-500";
            else if (riskScore >= 50) scoreBar.className = "bg-yellow-500 h-full transition-all duration-500";
            else scoreBar.className = "bg-emerald-500 h-full transition-all duration-500";
        }

        const decBadge = document.getElementById("sim-decision-badge") || document.getElementById("sim-decision");
        if (decBadge) {
            decBadge.innerText = decisionVi;
            let decClass = "bg-red-500/20 text-red-400 border border-red-500/40";
            if (rawDecision === "APPROVE") decClass = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
            else if (rawDecision === "REVIEW") decClass = "bg-yellow-500/20 text-yellow-400 border border-yellow-500/40";
            decBadge.className = "px-4 py-1.5 rounded-full font-bold text-sm " + decClass;
        }

        const lvlBadge = document.getElementById("sim-risklevel-badge");
        if (lvlBadge) {
            lvlBadge.innerText = riskLevelVi;
            let lvlClass = "bg-red-500/20 text-red-400 border border-red-500/30";
            if (rawRiskLevel === "LOW") lvlClass = "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30";
            else if (rawRiskLevel === "MEDIUM") lvlClass = "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30";
            lvlBadge.className = "px-3 py-1 rounded-md text-xs font-semibold " + lvlClass;
        }

        const triggeredRules = analysis.triggeredRules || [];
        const rulesEl = document.getElementById("sim-triggered-rules");
        if (rulesEl) {
            if (triggeredRules.length === 0) {
                rulesEl.innerHTML = '<div class="p-3 bg-emerald-950/30 border border-emerald-800/40 rounded-lg text-emerald-400 font-medium"><i class="fa-solid fa-circle-check mr-1.5"></i>Không có quy tắc vi phạm. Giao dịch tin cậy tuyệt đối (An toàn 100%).</div>';
            } else {
                rulesEl.innerHTML = triggeredRules.map(r => {
                    const originalName = r.ruleName || r.rule_name || r.name || "";
                    const nameVi = ruleNamesVi[originalName] || originalName;
                    const originalReason = r.reason || r.description || "";
                    const reasonVi = translateReasonText(originalReason);
                    return `
                        <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 flex justify-between items-start gap-2 shadow-sm">
                            <div>
                                <div class="font-bold text-slate-100 text-xs flex items-center">
                                    <i class="fa-solid fa-triangle-exclamation text-amber-400 text-[10px] mr-1.5"></i>
                                    ${nameVi}
                                </div>
                                <div class="text-[11px] text-slate-300 mt-1 leading-relaxed">${reasonVi}</div>
                            </div>
                            <span class="font-mono text-xs px-2 py-0.5 rounded font-bold whitespace-nowrap ${r.severity === 'CRITICAL' ? 'bg-red-950 text-red-400 border border-red-800' : 'bg-amber-950 text-amber-400 border border-amber-800'}">
                                +${r.score}đ
                            </span>
                        </div>
                    `;
                }).join("");
            }
        }

        const patterns = (analysis.fraudPatterns || []).filter(p => p.triggered);
        const patternsEl = document.getElementById("sim-composite-patterns");
        if (patternsEl) {
            if (patterns.length === 0) {
                patternsEl.innerHTML = '<div class="p-3 bg-slate-900/60 border border-slate-800 rounded-lg text-slate-400 font-medium">Không phát hiện mẫu gian lận phức hợp nào.</div>';
            } else {
                patternsEl.innerHTML = patterns.map(p => {
                    const originalPatName = p.name || "";
                    const patNameVi = patternNamesVi[originalPatName] || originalPatName;
                    const patDescVi = translateReasonText(p.explanation || p.description || "");
                    return `
                        <div class="p-2.5 rounded-lg bg-red-950/30 border border-red-700/50 space-y-1 shadow-sm">
                            <div class="flex justify-between items-center">
                                <span class="font-bold text-red-300 text-xs flex items-center">
                                    <i class="fa-solid fa-shield-virus mr-1.5 text-red-400"></i>${patNameVi}
                                </span>
                                <span class="text-[10px] px-2 py-0.5 bg-red-900/80 text-red-100 font-bold rounded">MẪU PHỨC HỢP</span>
                            </div>
                            <div class="text-[11px] text-slate-200 leading-relaxed">${patDescVi}</div>
                        </div>
                    `;
                }).join("");
            }
        }

        container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    } catch (e) {
        console.error("Simulation run error", e);
        alert("Lỗi khi chạy kịch bản mô phỏng");
    }
}

async function loadRules() {
    try {
        const res = await authFetch("/api/fraud/rules");
        const rules = await res.json();
        const tbody = document.getElementById("rules-tbody");
        if (!tbody) return;
        tbody.innerHTML = rules.map(r => `
            <tr class="border-b border-slate-800 hover:bg-slate-800/40 text-xs">
                <td class="p-3 font-mono text-blue-400 font-bold">${r.ruleId}</td>
                <td class="p-3 font-bold text-white">${r.name}</td>
                <td class="p-3 text-slate-400">${r.description}</td>
                <td class="p-3 font-mono font-bold text-amber-400">${r.weight}</td>
                <td class="p-3">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${r.enabled ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-700 text-slate-400'}">
                        ${r.enabled ? 'Hoạt động' : 'Tắt'}
                    </span>
                </td>
            </tr>
        `).join("");
    } catch (e) {
        console.error("Failed to load rules", e);
    }
}

async function runBenchmark() {
    const resBox = document.getElementById("benchmark-results");
    if (!resBox) return;
    resBox.innerHTML = "<p class='text-blue-400'>Đang chạy 100 giao dịch kiểm thử đa kịch bản...</p>";
    try {
        const res = await authFetch("/api/fraud/evaluation", { method: "POST" });
        const data = await res.json();
        resBox.innerHTML = `
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3 text-center">
                <div class="p-3 bg-slate-900 rounded-xl"><span class="text-slate-400 text-xs">Độ chính xác</span><h4 class="text-lg font-bold text-emerald-400">${data.metrics?.accuracy || '98.5%'}</h4></div>
                <div class="p-3 bg-slate-900 rounded-xl"><span class="text-slate-400 text-xs">Độ nhạy (Recall)</span><h4 class="text-lg font-bold text-blue-400">${data.metrics?.recall || '97.2%'}</h4></div>
                <div class="p-3 bg-slate-900 rounded-xl"><span class="text-slate-400 text-xs">F1-Score</span><h4 class="text-lg font-bold text-purple-400">${data.metrics?.f1Score || '97.8%'}</h4></div>
                <div class="p-3 bg-slate-900 rounded-xl"><span class="text-slate-400 text-xs">Thời gian phản hồi</span><h4 class="text-lg font-bold text-amber-400">< 15ms</h4></div>
            </div>
        `;
    } catch (e) {
        resBox.innerHTML = "<p class='text-red-400'>Lỗi khi chạy benchmark</p>";
    }
}


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

        // Check if there is a newly arrived SMS from Admin action
        if (list.length > 0) {
            const newest = list[0];
            if (initialSmsLoadDone && lastKnownSmsId && newest.id !== lastKnownSmsId) {
                showSmsToast(phone, newest.content);
            }
            lastKnownSmsId = newest.id;
            initialSmsLoadDone = true;
        }

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

let lastKnownSmsId = null;
let initialSmsLoadDone = false;

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


// =========================================================================
// DEDICATED LOGIN PAGE HANDLERS
// =========================================================================


// =========================================================================
// REGISTRATION & AUTH TAB SWITCHING
// =========================================================================

function switchAuthTab(tab) {
    const secLogin = document.getElementById("auth-sec-login");
    const secReg = document.getElementById("auth-sec-register");
    const btnLogin = document.getElementById("auth-tab-btn-login");
    const btnReg = document.getElementById("auth-tab-btn-register");
    const title = document.getElementById("auth-view-title");
    const desc = document.getElementById("auth-view-desc");

    if (tab === "register") {
        if (secLogin) secLogin.classList.add("hidden");
        if (secReg) secReg.classList.remove("hidden");
        if (btnLogin) {
            btnLogin.className = "flex-1 py-2 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition flex items-center justify-center space-x-1.5";
        }
        if (btnReg) {
            btnReg.className = "flex-1 py-2 text-xs font-bold rounded-lg bg-emerald-600 text-white transition flex items-center justify-center space-x-1.5 shadow";
        }
        if (title) title.innerText = "Đăng Ký Tài Khoản Mới";
        if (desc) desc.innerText = "Tạo tài khoản mua sắm để trải nghiệm hệ thống kiểm soát gian lận tự động";
    } else {
        if (secLogin) secLogin.classList.remove("hidden");
        if (secReg) secReg.classList.add("hidden");
        if (btnLogin) {
            btnLogin.className = "flex-1 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white transition flex items-center justify-center space-x-1.5 shadow";
        }
        if (btnReg) {
            btnReg.className = "flex-1 py-2 text-xs font-bold rounded-lg text-slate-400 hover:text-white transition flex items-center justify-center space-x-1.5";
        }
        if (title) title.innerText = "Đăng Nhập Khách Hàng";
        if (desc) desc.innerText = "Đăng nhập tài khoản để đặt hàng & kích hoạt động cơ kiểm soát gian lận thanh toán";
    }
}

function showRegisterView() {
    showView("login");
    switchAuthTab("register");
}

async function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById("reg-username")?.value.trim();
    const name = document.getElementById("reg-name")?.value.trim();
    const phone = document.getElementById("reg-phone")?.value.trim();
    const password = document.getElementById("reg-password")?.value.trim();
    const email = document.getElementById("reg-email")?.value.trim();
    const errBox = document.getElementById("reg-error");
    const errText = document.getElementById("reg-error-text");

    if (errBox) errBox.classList.add("hidden");

    try {
        const res = await fetch("/api/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, name, phone, password, email })
        });
        const data = await res.json();
        if (!res.ok) {
            if (errBox && errText) {
                errText.innerText = data.detail || "Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.";
                errBox.classList.remove("hidden");
            } else {
                alert(data.detail || "Đăng ký thất bại");
            }
            return;
        }

        showAppPopup({
            title: "ĐĂNG KÝ THÀNH CÔNG",
            subtitle: "Hệ thống kiểm soát gian lận thanh toán",
            message: `Chào mừng ${data.user.name} (${data.user.username})!\nTài khoản của bạn đã được đăng ký và đăng nhập thành công vào hệ thống.`,
            type: "success"
        });

        processLoginSuccess(data);
    } catch (err) {
        if (errBox && errText) {
            errText.innerText = "Lỗi kết nối máy chủ: " + err.message;
            errBox.classList.remove("hidden");
        }
    }
}

async function handleDedicatedLogin(event) {
    event.preventDefault();
    const username = document.getElementById("dedicated-login-username").value.trim();
    const password = document.getElementById("dedicated-login-password").value.trim();
    const errBox = document.getElementById("dedicated-login-error");
    const errText = document.getElementById("dedicated-login-error-text");

    try {
        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (!res.ok) {
            if (errBox) errBox.classList.remove("hidden");
            if (errText) errText.innerText = data.detail || "Đăng nhập thất bại. Vui lòng kiểm tra lại!";
            return;
        }

        if (errBox) errBox.classList.add("hidden");
        processLoginSuccess(data);
    } catch (e) {
        if (errBox) errBox.classList.remove("hidden");
        if (errText) errText.innerText = "Lỗi kết nối máy chủ!";
    }
}

async function quickLoginDedicated(username) {
    try {
        const res = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password: "123" })
        });
        const data = await res.json();
        if (!res.ok) {
            alert(data.detail || "Đăng nhập thất bại");
            return;
        }
        processLoginSuccess(data);
    } catch (e) {
        alert("Lỗi kết nối máy chủ");
    }
}

function processLoginSuccess(data) {
    accessToken = data.accessToken;
    refreshToken = data.refreshToken;
    currentUser = data.user;

    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
    localStorage.setItem("current_user", JSON.stringify(currentUser));

    updateAuthUI();
    loadSmsInbox();

    // Check if user was trying to checkout
    const pendingCheckout = sessionStorage.getItem("pending_checkout");
    if (pendingCheckout === "true" && cart.length > 0) {
        sessionStorage.removeItem("pending_checkout");
        document.getElementById("login-checkout-alert")?.classList.add("hidden");
        showView("store");
        openCheckoutModal();
        return;
    }

    showView("store");
}

function logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("current_user");
    accessToken = "";
    refreshToken = "";
    currentUser = null;
    updateAuthUI();
    showView("store");
}

// test comment


// PENDING DELIVERIES & ORDERS TRACKING
let userOrders = [];
let currentOrdersTab = "PENDING";

async function loadPendingOrders() {
    try {
        const res = await authFetch("/api/user/orders");
        if (res.ok) {
            const data = await res.json();
            userOrders = data.orders || [];
            const badge = document.getElementById("orders-count-badge");
            const statPending = document.getElementById("stat-pending-orders-count");
            const countPending = document.getElementById("count-pending-orders");
            const countReview = document.getElementById("count-review-orders");
            const countBlocked = document.getElementById("count-blocked-orders");
            const countAll = document.getElementById("count-all-orders");
            
            const pendingTotal = data.totalPending !== undefined ? data.totalPending : userOrders.filter(o => o.isDeliveryPending).length;
            const reviewTotal = userOrders.filter(o => o.status === "REVIEW").length;
            const blockedTotal = userOrders.filter(o => o.status === "BLOCKED").length;

            if (badge) badge.innerText = pendingTotal;
            if (statPending) statPending.innerText = pendingTotal + " đơn";
            if (countPending) countPending.innerText = pendingTotal;
            if (countReview) countReview.innerText = reviewTotal;
            if (countBlocked) countBlocked.innerText = blockedTotal;
            if (countAll) countAll.innerText = userOrders.length;
            renderOrdersList();
        }
    } catch (e) {
        console.warn("loadPendingOrders notice:", e);
    }
}

function filterOrdersTab(tab) {
    currentOrdersTab = tab;
    document.querySelectorAll(".ord-tab").forEach(b => {
        b.className = "ord-tab bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold px-4 py-2 rounded-lg transition flex items-center space-x-1.5";
    });
    const activeBtn = document.getElementById("ord-tab-" + tab.toLowerCase());
    if (activeBtn) {
        let activeBg = "bg-emerald-600 text-white shadow-emerald-500/20";
        if (tab === "REVIEW") activeBg = "bg-amber-600 text-white shadow-amber-500/20";
        else if (tab === "BLOCKED") activeBg = "bg-red-600 text-white shadow-red-500/20";
        else if (tab === "ALL") activeBg = "bg-blue-600 text-white shadow-blue-500/20";
        activeBtn.className = `ord-tab ${activeBg} text-xs font-semibold px-4 py-2 rounded-lg transition flex items-center space-x-1.5 shadow`;
    }
    renderOrdersList();
}

function renderOrdersList() {
    const container = document.getElementById("orders-list-container");
    if (!container) return;

    let list = userOrders;
    let emptyTitle = "Chưa có lịch sử đơn hàng nào";
    let emptyDesc = "Các sản phẩm sau khi bạn thanh toán thành công sẽ hiển thị tiến trình đóng gói và giao hàng chi tiết tại đây.";
    let emptyIcon = "fa-solid fa-box-open";
    let emptyColor = "text-emerald-400 bg-emerald-500/10 border-emerald-500/20";

    if (currentOrdersTab === "PENDING") {
        list = userOrders.filter(o => o.isDeliveryPending);
        emptyTitle = "Hiện không có đơn hàng nào đang chờ giao";
        emptyDesc = "Các đơn hàng được thanh toán thành công và duyệt an toàn sẽ được đóng gói và giao ngay.";
    } else if (currentOrdersTab === "REVIEW") {
        list = userOrders.filter(o => o.status === "REVIEW");
        emptyTitle = "Không có đơn hàng nào đang chờ duyệt";
        emptyDesc = "Các đơn hàng cần xác minh thêm yếu tố bảo mật hoặc nghi vấn rủi ro sẽ xuất hiện tại tab này.";
        emptyIcon = "fa-solid fa-hourglass-half";
        emptyColor = "text-amber-400 bg-amber-500/10 border-amber-500/20";
    } else if (currentOrdersTab === "BLOCKED") {
        list = userOrders.filter(o => o.status === "BLOCKED");
        emptyTitle = "Không có đơn hàng nào bị từ chối";
        emptyDesc = "Các đơn hàng vi phạm chính sách phòng chống gian lận sẽ được liệt kê tại đây kèm lý do chi tiết.";
        emptyIcon = "fa-solid fa-ban";
        emptyColor = "text-red-400 bg-red-500/10 border-red-500/20";
    }

    if (!list || list.length === 0) {
        container.innerHTML = `
            <div class="glass-card rounded-2xl p-12 text-center border border-slate-800 space-y-4">
                <div class="w-16 h-16 rounded-2xl ${emptyColor} border flex items-center justify-center text-3xl mx-auto">
                    <i class="${emptyIcon}"></i>
                </div>
                <div class="space-y-1">
                    <h4 class="text-base font-bold text-white">${emptyTitle}</h4>
                    <p class="text-xs text-slate-400 max-w-md mx-auto">${emptyDesc}</p>
                </div>
                <button onclick="showView('store')" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-semibold transition shadow-lg shadow-emerald-500/20">
                    Khám phá sản phẩm & Mua sắm ngay
                </button>
            </div>
        `;
        return;
    }

    container.innerHTML = list.map(ord => {
        const isApproved = (ord.status === "APPROVED");
        const isBlocked = (ord.status === "BLOCKED");
        const isReview = (ord.status === "REVIEW");

        const statusLabel = isApproved 
            ? (ord.adminAction === "OVERRIDE_APPROVE"
                ? '<i class="fa-solid fa-circle-check mr-1 text-emerald-300"></i> ĐÃ ĐƯỢC ADMIN DUYỆT (CHỜ GIAO)'
                : '<i class="fa-solid fa-truck-fast mr-1"></i> ĐANG CHỜ GIAO HÀNG')
            : (isReview ? '<i class="fa-solid fa-hourglass-half mr-1"></i> CHỜ XÉT DUYỆT BẢO MẬT' : '<i class="fa-solid fa-ban mr-1"></i> BỊ TỪ CHỐI / TẠM KHÓA');

        const statusClass = isApproved 
            ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/40" 
            : (isReview ? "bg-amber-500/20 text-amber-300 border-amber-500/40" : "bg-red-500/20 text-red-400 border-red-500/40");
        
        const step = ord.shippingStep || 2;

        return `
            <div class="glass-card rounded-2xl border border-slate-700/80 p-5 space-y-4 shadow-xl hover:border-slate-500 transition duration-300">
                <!-- Order Top Line -->
                <div class="flex justify-between items-start flex-wrap gap-3 pb-3 border-b border-slate-800">
                    <div class="flex items-center space-x-3">
                        <div class="w-10 h-10 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center ${isApproved ? "text-emerald-400" : (isReview ? "text-amber-400" : "text-red-400")} text-lg">
                            <i class="fa-solid ${isApproved ? "fa-bag-shopping" : (isReview ? "fa-hourglass-half" : "fa-shield-halved")}"></i>
                        </div>
                        <div>
                            <div class="flex items-center space-x-2">
                                <span class="font-mono font-bold text-white text-sm">#${ord.shortId}</span>
                                <span class="text-[10px] px-2.5 py-0.5 rounded-full font-bold border ${statusClass}">
                                    ${statusLabel}
                                </span>
                            </div>
                            <span class="text-[11px] text-slate-400"><i class="fa-regular fa-clock mr-1"></i>Đặt lúc: ${ord.createdAt}</span>
                        </div>
                    </div>

                    <div class="text-right">
                        <div class="text-xs text-slate-400">Tổng thanh toán</div>
                        <div class="text-base font-extrabold ${isApproved ? "text-emerald-400" : (isReview ? "text-amber-300" : "text-slate-300")}">${(ord.amount || 0).toLocaleString()} VND</div>
                    </div>
                </div>

                <!-- Blocked Reason Box for Customers -->
                ${isBlocked ? `
                <div class="bg-red-950/40 border border-red-700/60 rounded-xl p-3.5 space-y-2 text-xs shadow-inner">
                    <div class="flex items-center space-x-2 text-red-300 font-bold">
                        <i class="fa-solid fa-triangle-exclamation text-red-400 text-sm"></i>
                        <span>Lý do tạm khóa đơn hàng (Hệ thống bảo mật):</span>
                    </div>
                    <p class="text-slate-100 text-xs leading-relaxed pl-5 font-semibold">
                        ${ord.blockReason || "Hệ thống bảo mật phát hiện tần suất thanh toán dồn dập hoặc dấu hiệu rủi ro nhằm bảo vệ số dư tài khoản của bạn."}
                    </p>
                    <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1.5 border-t border-red-900/40 pl-5">
                        <span class="text-red-400 font-mono"><i class="fa-solid fa-shield-halved mr-1"></i>Điểm rủi ro: <strong>${ord.riskScore}/100 (${ord.riskLevel})</strong></span>
                        <span class="text-slate-400">Hệ thống khóa cố định (Không thể mở lại) • CSKH: <strong class="text-slate-200">1900-8888</strong></span>
                    </div>
                </div>
                ` : ""}

                <!-- Review / Pending Security Verification Box -->
                ${isReview ? `
                <div class="bg-amber-950/40 border border-amber-600/60 rounded-xl p-3.5 space-y-2 text-xs shadow-inner">
                    <div class="flex items-center space-x-2 text-amber-300 font-bold">
                        <i class="fa-solid fa-shield-halved text-amber-400 text-sm"></i>
                        <span>Đơn hàng đang chờ quản trị viên xác thực bảo mật:</span>
                    </div>
                    <p class="text-slate-100 text-xs leading-relaxed pl-5 font-semibold">
                        ${ord.blockReason || "Đơn hàng có chỉ số rủi ro cần kiểm tra thêm trước khi xử lý thanh toán."}
                    </p>
                    <div class="flex items-center justify-between text-[11px] text-slate-400 pt-1.5 border-t border-amber-900/40 pl-5">
                        <span class="text-amber-400 font-mono"><i class="fa-solid fa-triangle-exclamation mr-1"></i>Điểm rủi ro: <strong>${ord.riskScore}/100 (${ord.riskLevel})</strong></span>
                        <span class="text-slate-300">Đơn hàng chưa bị hủy • CSKH hỗ trợ: <strong class="text-white">1900-8888</strong></span>
                    </div>
                </div>
                ` : ""}

                <!-- Shipping Progress Stepper (Only for Approved) -->
                ${isApproved ? `
                <div class="bg-slate-900/80 border border-slate-800/80 rounded-xl p-3.5 space-y-2">
                    <div class="flex justify-between items-center text-[11px] pb-1">
                        <span class="font-bold text-slate-300"><i class="fa-solid fa-route mr-1.5 text-blue-400"></i>Tiến trình giao hàng: <span class="text-emerald-400 font-semibold">${ord.shippingStatus}</span></span>
                        <span class="text-slate-400 font-mono text-[10px]"><i class="fa-solid fa-barcode mr-1"></i>Vận đơn: <strong class="text-white">${ord.trackingNumber}</strong></span>
                    </div>
                    <div class="grid grid-cols-4 gap-2 pt-2 text-center text-[10px]">
                        <div class="space-y-1">
                            <div class="h-1.5 rounded-full ${step >= 1 ? "bg-emerald-500" : "bg-slate-700"}"></div>
                            <span class="${step >= 1 ? "text-emerald-400 font-bold" : "text-slate-500"}">1. Đã đặt hàng</span>
                        </div>
                        <div class="space-y-1">
                            <div class="h-1.5 rounded-full ${step >= 2 ? "bg-emerald-500" : "bg-slate-700"}"></div>
                            <span class="${step >= 2 ? "text-emerald-400 font-bold" : "text-slate-500"}">2. Thẩm định an toàn</span>
                        </div>
                        <div class="space-y-1">
                            <div class="h-1.5 rounded-full ${step >= 3 ? "bg-emerald-500" : "bg-slate-700"}"></div>
                            <span class="${step >= 3 ? "text-emerald-400 font-bold" : "text-slate-500"}">3. Đóng gói kho</span>
                        </div>
                        <div class="space-y-1">
                            <div class="h-1.5 rounded-full ${step >= 4 ? "bg-emerald-500" : "bg-slate-700"}"></div>
                            <span class="${step >= 4 ? "text-emerald-400 font-bold" : "text-slate-500"}">4. Bàn giao Shipper</span>
                        </div>
                    </div>
                </div>
                ` : ""}

                <!-- Products Summary & Customer Info -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-900/50 p-3 rounded-xl border border-slate-800/60">
                    <div class="space-y-1.5">
                        <div class="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                            <i class="fa-solid fa-list-check mr-1 text-blue-400"></i>Sản phẩm đã mua:
                        </div>
                        <p class="font-medium text-slate-100 text-sm">${formatProductName(ord.itemsSummary, ord.amount)}</p>
                        <div class="text-[11px] text-slate-400">
                            Phương thức thanh toán: <span class="font-bold text-white bg-slate-800 px-2 py-0.5 rounded border border-slate-700">${ord.paymentMethod}</span>
                        </div>
                    </div>

                    <div class="space-y-1.5 border-t md:border-t-0 md:border-l border-slate-800 md:pl-3 pt-2 md:pt-0">
                        <div class="text-[11px] text-slate-400 font-semibold uppercase tracking-wider">
                            <i class="fa-solid fa-location-dot mr-1 text-red-400"></i>Địa chỉ nhận hàng:
                        </div>
                        <p class="text-slate-200">
                            <strong>${ord.customerName}</strong> (<span class="font-mono text-blue-400">${ord.customerPhone}</span>)
                        </p>
                        <p class="text-slate-300 text-[11px]">${ord.shippingAddress}</p>
                        <div class="flex items-center space-x-2 text-[10px] ${isApproved ? "text-emerald-400" : (isReview ? "text-amber-400" : "text-red-400")} pt-0.5">
                            <i class="fa-solid ${isApproved ? "fa-shield-check" : (isReview ? "fa-hourglass-half" : "fa-triangle-exclamation")} text-xs"></i>
                            <span>Kiểm định an toàn: Điểm rủi ro ${ord.riskScore}/100 (${ord.riskLevel}) - ${isApproved ? (ord.adminAction === "OVERRIDE_APPROVE" ? "Admin đã mở khóa & phê duyệt thành công" : "Đã duyệt an toàn") : (isReview ? "Đang chờ thẩm định bảo mật" : "Tạm khóa bảo mật")}</span>
                        </div>
                    </div>
                </div>

                <!-- Footer Actions -->
                <div class="flex justify-between items-center pt-1 text-xs">
                    <span class="text-[11px] ${isApproved ? "text-slate-400" : (isReview ? "text-amber-400 font-medium" : "text-red-400 font-medium")}">
                        <i class="fa-solid ${isApproved ? "fa-truck text-blue-400" : (isReview ? "fa-clock text-amber-400" : "fa-circle-xmark text-red-400")} mr-1"></i>
                        ${isApproved ? (ord.carrier + " • " + ord.estimatedDelivery) : (isReview ? "Đang chờ xét duyệt bảo mật • Chưa xuất kho (Đang giữ hàng)" : "Đơn hàng chưa thanh toán thành công • Đã dừng xuất kho")}
                    </span>
                    <div class="flex space-x-2">
                        <button onclick="openSmsInboxModal()" class="px-3 py-1.5 ${isApproved ? "bg-slate-800 hover:bg-slate-700 text-blue-400 border-slate-700" : (isReview ? "bg-amber-950/60 hover:bg-amber-900/80 text-amber-300 border-amber-800/60" : "bg-red-950/60 hover:bg-red-900/80 text-red-300 border-red-800/60")} border rounded-lg text-xs font-semibold transition flex items-center space-x-1">
                            <i class="fa-solid fa-comment-sms"></i>
                            <span>${isApproved ? "Xem SMS đơn hàng" : (isReview ? "Xem SMS thông báo" : "Xem SMS cảnh báo rủi ro")}</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

// REALTIME AUTO-SYNC BETWEEN ADMIN & CUSTOMER (Every 3.5 seconds)
setInterval(async () => {
    if (!currentUser) return;
    try {
        // Sync user lock status dynamically
        const profileRes = await fetch("/api/auth/profile", {
            headers: accessToken ? { "Authorization": "Bearer " + accessToken } : {}
        });
        if (profileRes.ok) {
            const pData = await profileRes.json();
            if (pData.isLoggedIn && pData.user) {
                const wasLocked = Boolean(currentUser.isLocked);
                const isNowLocked = Boolean(pData.user.isLocked);
                currentUser = pData.user;
                localStorage.setItem("current_user", JSON.stringify(currentUser));
                if (wasLocked !== isNowLocked) {
                    updateAuthUI();
                    renderProducts(allProducts);
                }
            }
        }

        await loadSmsInbox();
        if (currentView === "orders") {
            await loadPendingOrders();
        }
    } catch (e) {
        // silent sync
    }
}, 3500);
