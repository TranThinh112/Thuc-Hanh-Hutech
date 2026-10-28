import sys, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 900})
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(1000)

    # Emergency unlock first to ensure fresh state
    page.evaluate("fetch('/api/user/emergency-unlock', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'})")
    page.evaluate("quickLogin('thinh')")
    page.wait_for_timeout(1000)

    presets = ['legit', 'high_amount', 'ato', 'travel', 'card_testing', 'velocity']

    for pr in presets:
        page.evaluate("openCheckoutModal()")
        page.wait_for_timeout(400)
        page.evaluate(f"setPreset('{pr}')")
        page.wait_for_timeout(400)

        # Trigger submit
        page.evaluate("""() => {
            const form = document.getElementById('checkout-form');
            form.requestSubmit();
        }""")
        page.wait_for_timeout(1500)

        # Check result
        res_title = page.evaluate("document.getElementById('res-title')?.innerText || ''")
        res_status = page.evaluate("document.getElementById('res-status-label')?.innerText || ''")
        res_score = page.evaluate("document.getElementById('res-score-badge')?.innerText || ''")
        otp_hidden = page.evaluate("document.getElementById('res-otp-section')?.classList.contains('hidden')")
        
        print(f"[{pr:12}] Title: {res_title[:35]} | Status: {res_status:15} | Score: {res_score:10} | OTP: {not otp_hidden}")

        # Close result modal
        page.evaluate("closeResultModal()")
        page.wait_for_timeout(500)

    browser.close()
