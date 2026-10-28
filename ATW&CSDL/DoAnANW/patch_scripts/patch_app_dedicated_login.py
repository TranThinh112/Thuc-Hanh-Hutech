with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update initAuth to allow guest browsing if not logged in
old_init_auth = """async function initAuth() {
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
}"""

new_init_auth = """async function initAuth() {
    accessToken = localStorage.getItem("access_token") || "";
    refreshToken = localStorage.getItem("refresh_token") || "";

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

    // Default: Guest visitor (cho phép lướt sản phẩm tự do, thanh toán mới cần đăng nhập)
    currentUser = null;
    updateAuthUI();
}"""

js = js.replace(old_init_auth, new_init_auth)

# 2. Update updateAuthUI for Guest vs User vs Admin
old_update_auth = """function updateAuthUI() {
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
}"""

new_update_auth = """function updateAuthUI() {
    const navLoginBtn = document.getElementById("nav-login-btn");
    const userCapsule = document.getElementById("user-auth-capsule");
    const nameEl = document.getElementById("nav-user-name");
    const roleEl = document.getElementById("nav-user-role");
    const phoneEl = document.getElementById("nav-user-phone");
    const adminBtn = document.getElementById("nav-admin-btn");
    const storeBtn = document.getElementById("nav-store-btn");

    if (!currentUser) {
        // GUEST VISITOR MODE
        if (navLoginBtn) navLoginBtn.classList.remove("hidden");
        if (userCapsule) userCapsule.classList.add("hidden");
        if (adminBtn) adminBtn.classList.add("hidden");
        if (storeBtn) storeBtn.classList.add("hidden");
        return;
    }

    // LOGGED IN MODE
    if (navLoginBtn) navLoginBtn.classList.add("hidden");
    if (userCapsule) userCapsule.classList.remove("hidden");

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

    // Role Enforcement: USER only sees Storefront. ADMIN sees both Store & Admin Center.
    if (currentUser.role === "USER") {
        if (adminBtn) adminBtn.classList.add("hidden");
        if (storeBtn) storeBtn.classList.add("hidden");
    } else if (currentUser.role === "ADMIN") {
        if (adminBtn) adminBtn.classList.remove("hidden");
    }
}"""

js = js.replace(old_update_auth, new_update_auth)

# 3. Update showView to support 'store', 'admin', 'login'
old_show_view = """function showView(viewName) {
    const viewStore = document.getElementById("view-store");
    const viewAdmin = document.getElementById("view-admin");
    const navStoreBtn = document.getElementById("nav-store-btn");
    const navAdminBtn = document.getElementById("nav-admin-btn");

    if (viewName === "admin") {
        if (!currentUser || currentUser.role !== "ADMIN") {
            alert("TRUY CẬP BỊ TỪ CHỐI!\\n\\nTài khoản của bạn (" + (currentUser?.name || "Khách") + " - " + (currentUser?.role || "USER") + ") chỉ có quyền mua sắm tại Cửa Hàng TMĐT.\\nChỉ tài khoản Quản Trị Viên (ADMIN) mới có quyền truy cập Trang Quản Trị!");
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
}"""

new_show_view = """function showView(viewName) {
    const viewStore = document.getElementById("view-store");
    const viewAdmin = document.getElementById("view-admin");
    const viewLogin = document.getElementById("view-login");
    const navStoreBtn = document.getElementById("nav-store-btn");
    const navAdminBtn = document.getElementById("nav-admin-btn");

    if (viewName === "admin") {
        if (!currentUser) {
            alert("Vui lòng đăng nhập tài khoản Quản Trị Viên (Admin) để truy cập!");
            showView("login");
            return;
        }
        if (currentUser.role !== "ADMIN") {
            alert("TRUY CẬP BỊ TỪ CHỐI!\\n\\nTài khoản của bạn (" + currentUser.name + " - USER) chỉ có quyền mua sắm tại Cửa Hàng TMĐT.\\nChỉ tài khoản Quản Trị Viên (ADMIN) mới có quyền truy cập Trang Quản Trị!");
            showView("store");
            return;
        }
        viewStore?.classList.add("hidden");
        viewLogin?.classList.add("hidden");
        viewAdmin?.classList.remove("hidden");
        if (navStoreBtn) navStoreBtn.classList.remove("hidden");
        if (navAdminBtn) navAdminBtn.classList.add("hidden");
        loadDashboard();
    } else if (viewName === "login") {
        viewStore?.classList.add("hidden");
        viewAdmin?.classList.add("hidden");
        viewLogin?.classList.remove("hidden");
        if (navStoreBtn) navStoreBtn.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        // 'store' view
        viewStore?.classList.remove("hidden");
        viewAdmin?.classList.add("hidden");
        viewLogin?.classList.add("hidden");
        if (navStoreBtn) navStoreBtn.classList.add("hidden");
        if (currentUser && currentUser.role === "ADMIN" && navAdminBtn) {
            navAdminBtn.classList.remove("hidden");
        }
    }
}"""

js = js.replace(old_show_view, new_show_view)

# 4. Require login on buyNow and openCheckoutModal
old_buy_now = """function buyNow(id) {
    const item = allProducts.find(p => p.id === id);
    if (item) {
        cart = [item];
        updateCartUI();
        openCheckoutModal();
    }
}"""

new_buy_now = """function buyNow(id) {
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
}"""

js = js.replace(old_buy_now, new_buy_now)

old_open_chk = """function openCheckoutModal() {
    if (cart.length === 0) {
        alert("Giỏ hàng đang trống! Vui lòng chọn sản phẩm.");
        return;
    }
    const sum = cart.reduce((acc, i) => acc + i.price, 0);"""

new_open_chk = """function openCheckoutModal() {
    if (cart.length === 0) {
        alert("Giỏ hàng đang trống! Vui lòng chọn sản phẩm.");
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

    const sum = cart.reduce((acc, i) => acc + i.price, 0);"""

js = js.replace(old_open_chk, new_open_chk)

# 5. Add Dedicated Login Handlers
dedicated_login_js = """
// =========================================================================
// DEDICATED LOGIN PAGE HANDLERS
// =========================================================================

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
"""

js += "\n" + dedicated_login_js

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Updated app.js with dedicated login page handling and guest checkout enforcement!")
