p2 = """
// =========================================================================
// STOREFRONT & PRODUCTS
// =========================================================================

async function loadProducts() {
    try {
        const res = await fetch("/api/store/products");
        allProducts = await res.json();
        renderProducts(allProducts);
    } catch (e) {
        console.error("Failed to load products", e);
    }
}

function renderProducts(products) {
    const grid = document.getElementById("products-grid");
    if (!grid) return;
    grid.innerHTML = products.map(p => `
        <div class="glass-card rounded-2xl border border-slate-700/80 overflow-hidden shadow-xl hover:border-slate-500 transition duration-300 flex flex-col justify-between group">
            <div class="relative overflow-hidden h-48 bg-slate-800">
                <img src="${p.imageUrl}" alt="${p.name}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
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
                        <button onclick="addToCart('${p.id}')" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs transition">
                            + Giỏ hàng
                        </button>
                        <button onclick="buyNow('${p.id}')" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg text-xs transition shadow">
                            Mua ngay
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join("");
}

function filterCategory(cat) {
    document.querySelectorAll(".cat-btn").forEach(b => {
        if (b.innerText.includes(cat) || (cat === "ALL" && b.innerText.includes("Tất cả"))) {
            b.className = "cat-btn bg-blue-600 text-white text-xs font-medium px-4 py-2 rounded-lg transition";
        } else {
            b.className = "cat-btn bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium px-4 py-2 rounded-lg transition";
        }
    });
    if (cat === "ALL") {
        renderProducts(allProducts);
    } else {
        renderProducts(allProducts.filter(p => p.category === cat));
    }
}

function filterProducts() {
    const term = document.getElementById("store-search").value.toLowerCase();
    renderProducts(allProducts.filter(p => p.name.toLowerCase().includes(term) || p.description.toLowerCase().includes(term)));
}

function addToCart(id) {
    const item = allProducts.find(p => p.id === id);
    if (item) {
        cart.push(item);
        updateCartUI();
        toggleCartModal(true);
    }
}

function buyNow(id) {
    const item = allProducts.find(p => p.id === id);
    if (item) {
        cart = [item];
        updateCartUI();
        openCheckoutModal();
    }
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
    if (cart.length === 0) {
        alert("Giỏ hàng đang trống! Vui lòng chọn sản phẩm.");
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

function setPreset(type) {
    const ip = document.getElementById("chk-ip");
    const dev = document.getElementById("chk-device");
    const city = document.getElementById("chk-city");

    if (type === "legit") {
        if (ip) ip.value = "113.161.44.12";
        if (dev) dev.value = "device_thinh_iphone";
        if (city) city.value = "Hà Nội";
    } else if (type === "ato") {
        if (ip) ip.value = "185.220.101.5";
        if (dev) dev.value = "device_hacker_kali";
        if (city) city.value = "Tokyo";
    } else if (type === "travel") {
        if (ip) ip.value = "45.142.120.10";
        if (dev) dev.value = "device_bot_script";
        if (city) city.value = "London";
    }
}
"""

with open("python_app/static/app.js", "a", encoding="utf-8") as f:
    f.write(p2)
print("Part 2 written")
