import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 900})
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(1000)

    page.evaluate("""() => {
        // Inject cursor
        const cur = document.createElement('div');
        cur.id = 'demo-cursor';
        cur.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: rgba(56, 189, 248, 0.75);
            border: 2px solid #ffffff;
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.9);
            pointer-events: none;
            z-index: 10000000;
            transform: translate(-50%, -50%);
            left: 500px;
            top: 350px;
        `;
        document.body.appendChild(cur);

        // Inject HUD
        const hud = document.createElement('div');
        hud.id = 'demo-hud';
        hud.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 92%;
            max-width: 1250px;
            background: rgba(10, 15, 30, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(59, 130, 246, 0.5);
            border-radius: 16px;
            padding: 16px 24px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85);
            z-index: 9999999;
            color: #f8fafc;
            font-family: system-ui, -apple-system, sans-serif;
        `;
        hud.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="background: linear-gradient(135deg, #10b981, #059669); color:#fff; font-size:12px; font-weight:800; padding:4px 12px; border-radius:999px; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 0 10px rgba(16, 185, 129, 0.4);">
                        KỊCH BẢN 1: HỢP LỆ (LEGITIMATE)
                    </span>
                    <span style="background: rgba(59, 130, 246, 0.2); color:#60a5fa; font-size:11px; font-weight:600; padding:3px 10px; border-radius:6px; border:1px solid rgba(59, 130, 246, 0.3);">
                        Trạng Thái: KHỞI TẠO ĐƠN HÀNG
                    </span>
                </div>
                <div style="color:#94a3b8; font-size:12px; font-weight:500;">
                    <i class="fa-solid fa-shield-halved text-emerald-400 mr-1"></i> FraudShield AI - Real-time Engine
                </div>
            </div>
            <div style="font-size:16px; font-weight:700; color:#38bdf8; margin-bottom:6px;">
                Bước 1: Người dùng Thịnh đặt mua sản phẩm với thông tin quen thuộc
            </div>
            <div style="font-size:13px; color:#cbd5e1; line-height:1.5;">
                Hệ thống nạp hồ sơ người dùng: IP <b style="color:#38bdf8;">113.161.44.12 (Hà Nội)</b> | Thiết bị: <b style="color:#38bdf8;">Windows PC</b> | Giá trị: <b style="color:#34d399;">500.000 VND</b>. Tất cả dấu hiệu đều nằm trong hạn mức tin cậy lịch sử.
            </div>
        `;
        document.body.appendChild(hud);
    }""")
    
    page.screenshot(path="screenshots/test_hud_styling.png")
    browser.close()

print("Screenshot captured to screenshots/test_hud_styling.png")
