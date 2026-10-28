from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(1000)
    page.evaluate("quickLogin('thinh')")
    page.evaluate("openCheckoutModal()")
    page.wait_for_timeout(500)
    
    # Inject test HUD
    page.evaluate("""() => {
        const hud = document.createElement('div');
        hud.id = 'demo-hud';
        hud.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 88%;
            max-width: 1400px;
            background: rgba(10, 15, 30, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(59, 130, 246, 0.5);
            border-radius: 14px;
            padding: 14px 24px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
            z-index: 9999999;
            color: #f8fafc;
            font-family: system-ui, -apple-system, sans-serif;
        `;
        hud.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="background: linear-gradient(135deg, #10b981, #059669); color:#fff; font-size:12px; font-weight:800; padding:4px 12px; border-radius:999px;">
                    DEMO SCENARIO HUD
                </span>
                <span style="color:#38bdf8; font-size:13px; font-weight:600;">
                    AI Fraud Detection Engine
                </span>
            </div>
            <div style="font-size:16px; font-weight:700; color:#38bdf8; margin-bottom:4px;">
                Kiểm tra vị trí hiển thị HUD tại độ phân giải chuẩn 1080p Full HD
            </div>
            <div style="font-size:13px; color:#cbd5e1;">
                Thử nghiệm xem nút Xác nhận thanh toán có bị che khuất không.
            </div>
        `;
        document.body.appendChild(hud);
    }""")
    
    page.screenshot(path='screenshots/test_1080p_checkout.png')
    browser.close()
print("Screenshot captured")
