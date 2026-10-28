p1 = """// SecurePay AI Fraud Detection & E-Commerce Frontend Logic

let allProducts = [];
let cart = [];
let currentUser = null;
let accessToken = localStorage.getItem("access_token") || "";
let refreshToken = localStorage.getItem("refresh_token") || "";
let chartRiskDist = null, chartDecision = null;

document.addEventListener("DOMContentLoaded", async () => {
    await initAuth();
    loadProducts();
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
    if (!currentUser) return;

    const nameEl = document.getElementById("nav-user-name");
    const roleEl = document.getElementById("nav-user-role");
    const phoneEl = document.getElementById("nav-user-phone");
    const adminBtn = document.getElementById("nav-admin-btn");
    const storeBtn = document.getElementById("nav-store-btn");

    if (nameEl) nameEl.innerText = currentUser.name;
    if (phoneEl) phoneEl.innerText = currentUser.phone || "0972445090";

    if (roleEl) {
        roleEl.innerText = currentUser.role;
        if (currentUser.role === "ADMIN") {
            roleEl.className = "text-[10px] px-1.5 py-0.2 rounded font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40";
        } else {
            roleEl.className = "text-[10px] px-1.5 py-0.2 rounded font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
        }
    }

    // Role Enforcement: USER only sees Storefront. ADMIN sees both.
    if (currentUser.role === "USER") {
        if (adminBtn) adminBtn.classList.add("hidden");
        if (storeBtn) storeBtn.classList.add("hidden");
        showView("store");
    } else if (currentUser.role === "ADMIN") {
        if (adminBtn) adminBtn.classList.remove("hidden");
    }
}

function openLoginModal() {
    document.getElementById("login-modal")?.classList.remove("hidden");
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

        if (showAlert) {
            alert(`Đăng nhập thành công!\nTài khoản: ${currentUser.name}\nSố điện thoại: ${currentUser.phone}\nQuyền: ${currentUser.role}`);
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
        alert(`Đăng nhập thành công!\nTài khoản: ${currentUser.name} (${currentUser.role})`);
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
    const viewStore = document.getElementById("view-store");
    const viewAdmin = document.getElementById("view-admin");
    const navStoreBtn = document.getElementById("nav-store-btn");
    const navAdminBtn = document.getElementById("nav-admin-btn");

    if (viewName === "admin") {
        if (!currentUser || currentUser.role !== "ADMIN") {
            alert("TRUY CẬP BỊ TỪ CHỐI!\n\nTài khoản của bạn (" + (currentUser?.name || "Khách") + " - " + (currentUser?.role || "USER") + ") chỉ có quyền mua sắm tại Cửa Hàng TMĐT.\nChỉ tài khoản Quản Trị Viên (ADMIN) mới có quyền truy cập Trang Quản Trị!");
            showView("store");
            return;
        }
        viewStore?.classList.add("hidden");
        viewAdmin?.classList.remove("hidden");
        if (navStoreBtn) navStoreBtn.classList.remove("hidden");
        if (navAdminBtn) navAdminBtn.classList.add("hidden");
        loadDashboard();
    } else {
        viewStore?.classList.remove("hidden");
        viewAdmin?.classList.add("hidden");
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
        const sec = document.getElementById("sec-" + t);
        if (btn) btn.className = (t === tabId) ? "px-3 py-1.5 rounded bg-blue-600 font-semibold text-white" : "px-3 py-1.5 rounded bg-slate-800 text-slate-300";
        if (sec) sec.classList.toggle("hidden", t !== tabId);
    });
    if (tabId === "dashboard") loadDashboard();
    if (tabId === "transactions") loadTransactions();
    if (tabId === "rules") loadRules();
}
"""

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(p1)
print("Part 1 written")
