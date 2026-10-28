import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 950})
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(1000)
    page.evaluate("quickLogin('thinh')")
    page.evaluate("openCheckoutModal()")
    page.wait_for_timeout(500)

    page.evaluate("""() => {
        const hud = document.createElement('div');
        hud.id = 'demo-hud';
        hud.style.cssText = `
            position: fixed;
            bottom: 16px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 1200px;
            background: rgba(10, 15, 30, 0.94);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(59, 130, 246, 0.5);
            border-radius: 14px;
            padding: 14px 22px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
            z-index: 9999999;
            color: #f8fafc;
            font-family: system-ui, -apple-system, sans-serif;
        `;
        hud.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="background: linear-gradient(135deg, #10b981, #059669); color:#fff; font-size:11px; font-weight:800; padding:3px 10px; border-radius:999px; text-transform:uppercase;">
                    Kịch Bản 1: Giao Dịch Hợp Lệ (Legitimate)
                </span>
                <span style="color:#38bdf8; font-size:11px; font-weight:600;">
                    🛡️ AI & Rule Engine Fraud Prevention
                </span>
            </div>
            <div style="font-size:15px; font-weight:700; color:#38bdf8; margin-bottom:4px;">
                Chọn Kịch bản Hợp lệ: Thiết bị quen, IP Hà Nội, Giá trị 500.000đ
            </div>
            <div style="font-size:12px; color:#cbd5e1; line-height:1.4;">
                Thông số giao dịch hoàn toàn nằm trong ngưỡng lịch sử an toàn -> Risk Engine dự kiến phê duyệt ngay lập tức (APPROVE).
            </div>
        `;
        document.body.appendChild(hud);
    }""")
    
    page.screenshot(path="screenshots/test_checkout_with_hud.png")
    browser.close()

print("Screenshot captured to screenshots/test_checkout_with_hud.png")
