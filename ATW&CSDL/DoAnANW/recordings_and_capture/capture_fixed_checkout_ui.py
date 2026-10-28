import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 920})
    page.goto("http://127.0.0.1:8000", wait_until="networkidle")
    time.sleep(1)

    # Login as thinh
    page.evaluate("quickLogin('thinh', false)")
    time.sleep(1.5)

    # 4. Checkout Modal
    page.evaluate("""
        () => {
            const popup = document.getElementById('custom-popup-modal');
            if (popup) popup.classList.add('hidden');
            cart = [allProducts[0], allProducts[1]];
            updateCartUI();
            openCheckoutModal();
        }
    """)
    time.sleep(1.2)
    page.screenshot(path="screenshots/ui_04_checkout_modal.png")
    print("UI 04 taken")

    # 5. Payment Blocked
    page.evaluate("""
        () => {
            const popup = document.getElementById('custom-popup-modal');
            if (popup) popup.classList.add('hidden');
            setPreset('ato');
            document.getElementById('checkout-form').dispatchEvent(new Event('submit', { cancelable: true }));
        }
    """)
    page.wait_for_selector("#result-modal:not(.hidden)", timeout=10000)
    time.sleep(1.5)
    page.screenshot(path="screenshots/ui_05_payment_result_blocked.png")
    print("UI 05 taken")

    # Close result modal
    page.evaluate("closeResultModal()")
    time.sleep(0.8)

    # 6. Payment OTP
    page.evaluate("""
        () => {
            const popup = document.getElementById('custom-popup-modal');
            if (popup) popup.classList.add('hidden');
            cart = [allProducts[0], allProducts[1]];
            updateCartUI();
            openCheckoutModal();
        }
    """)
    time.sleep(0.8)
    page.evaluate("""
        () => {
            setPreset('travel');
            document.getElementById('checkout-form').dispatchEvent(new Event('submit', { cancelable: true }));
        }
    """)
    page.wait_for_selector("#result-modal:not(.hidden)", timeout=10000)
    time.sleep(1.5)
    page.screenshot(path="screenshots/ui_06_payment_result_otp.png")
    print("UI 06 taken")

    browser.close()

print("Recapture complete!")
