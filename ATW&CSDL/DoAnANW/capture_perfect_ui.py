import os, sys, time
from playwright.sync_api import sync_playwright

os.makedirs("screenshots", exist_ok=True)

def cleanup_modals(page):
    page.evaluate("""
        () => {
            const modals = ['custom-popup-modal', 'cart-modal', 'checkout-modal', 'result-modal', 'sms-inbox-modal'];
            modals.forEach(id => {
                const el = document.getElementById(id);
                if (el) el.classList.add('hidden');
            });
        }
    """)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 920})
    page.goto("http://127.0.0.1:8000", wait_until="networkidle")
    time.sleep(1)

    # 1. Storefront Catalog / Homepage
    cleanup_modals(page)
    page.evaluate("showView('store')")
    time.sleep(1)
    page.screenshot(path="screenshots/ui_01_store_homepage.png")
    print("1. Homepage captured")

    # 2. Login View
    cleanup_modals(page)
    page.evaluate("showView('login')")
    time.sleep(0.8)
    page.screenshot(path="screenshots/ui_02_login_view.png")
    print("2. Login View captured")

    # Log in as thinh (user)
    page.evaluate("quickLogin('thinh', false)")
    time.sleep(1.2)

    # 3. Cart Modal
    cleanup_modals(page)
    page.evaluate("""
        () => {
            if (window.products && window.products.length > 0) {
                cart = [];
                addToCart(window.products[0].id);
                addToCart(window.products[1].id);
            }
            toggleCartModal(true);
        }
    """)
    time.sleep(1)
    page.screenshot(path="screenshots/ui_03_cart_modal.png")
    print("3. Cart Modal captured")
    page.evaluate("toggleCartModal(false)")
    time.sleep(0.5)

    # 4. Checkout Modal with preset HUD
    cleanup_modals(page)
    page.evaluate("""
        () => {
            if (cart.length === 0 && window.products && window.products.length > 0) {
                addToCart(window.products[0].id);
                addToCart(window.products[1].id);
            }
            openCheckoutModal();
        }
    """)
    time.sleep(1)
    page.screenshot(path="screenshots/ui_04_checkout_modal.png")
    print("4. Checkout Modal captured")

    # 5. Payment Result Blocked (Trigger ATO attack preset)
    page.evaluate("setPreset('ato')")
    time.sleep(0.6)
    page.evaluate("document.getElementById('checkout-form').dispatchEvent(new Event('submit', { cancelable: true }))")
    time.sleep(2.5)
    page.screenshot(path="screenshots/ui_05_payment_result_blocked.png")
    print("5. Payment Result Blocked captured")
    page.evaluate("closeResultModal()")
    time.sleep(0.5)

    # 6. Payment Result Step-up OTP (Trigger Travel preset which leads to REVIEW)
    cleanup_modals(page)
    page.evaluate("""
        () => {
            if (cart.length === 0 && window.products && window.products.length > 0) {
                addToCart(window.products[0].id);
                addToCart(window.products[1].id);
            }
            openCheckoutModal();
        }
    """)
    time.sleep(0.8)
    page.evaluate("setPreset('travel')")
    time.sleep(0.6)
    page.evaluate("document.getElementById('checkout-form').dispatchEvent(new Event('submit', { cancelable: true }))")
    time.sleep(2.5)
    page.screenshot(path="screenshots/ui_06_payment_result_otp.png")
    print("6. Payment Result OTP captured")
    page.evaluate("closeResultModal()")
    time.sleep(0.5)

    # 7. SMS Inbox Modal
    cleanup_modals(page)
    page.evaluate("""
        () => {
            if (typeof openSmsInboxModal === 'function') openSmsInboxModal();
            else if (typeof openSmsModal === 'function') openSmsModal();
            else {
                const el = document.getElementById('sms-inbox-modal');
                if (el) el.classList.remove('hidden');
            }
        }
    """)
    time.sleep(1)
    page.screenshot(path="screenshots/ui_07_sms_modal.png")
    print("7. SMS Inbox Modal captured")
    cleanup_modals(page)
    time.sleep(0.5)

    # 8. User Orders
    cleanup_modals(page)
    page.evaluate("showView('orders')")
    time.sleep(1.5)
    page.screenshot(path="screenshots/ui_08_user_orders.png")
    print("8. User Orders captured")

    # Log in as ADMIN
    page.evaluate("async () => { await quickLogin('admin', false); }")
    time.sleep(1.5)

    # 9. Admin Dashboard KPI
    cleanup_modals(page)
    page.evaluate("""
        () => {
            showView('admin');
            switchAdminTab('dashboard');
        }
    """)
    time.sleep(2.5)
    page.screenshot(path="screenshots/ui_09_admin_dashboard_kpi.png")
    print("9. Admin Dashboard captured")

    # 10. Admin Transactions
    cleanup_modals(page)
    page.evaluate("switchAdminTab('transactions')")
    time.sleep(2.5)
    page.screenshot(path="screenshots/ui_10_admin_transactions.png")
    print("10. Admin Transactions captured")

    # 11. Admin Simulation ATO
    cleanup_modals(page)
    page.evaluate("""
        () => {
            switchAdminTab('simulation');
            setTimeout(() => { runSimulation('ATO'); }, 400);
        }
    """)
    time.sleep(2.5)
    page.screenshot(path="screenshots/ui_11_admin_simulation_ato.png")
    print("11. Admin Simulation ATO captured")

    # 12. Admin Simulation Travel
    cleanup_modals(page)
    page.evaluate("""
        () => {
            switchAdminTab('simulation');
            setTimeout(() => { runSimulation('IMPOSSIBLE_TRAVEL'); }, 400);
        }
    """)
    time.sleep(2.5)
    page.screenshot(path="screenshots/ui_12_admin_simulation_travel.png")
    print("12. Admin Simulation Travel captured")

    # 13. Admin Rules Management
    cleanup_modals(page)
    page.evaluate("switchAdminTab('rules')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_13_admin_rules.png")
    print("13. Admin Rules captured")

    # 14. Admin Evaluation / Benchmark
    cleanup_modals(page)
    page.evaluate("""
        async () => {
            switchAdminTab('evaluation');
            if (typeof runBenchmark === 'function') {
                await runBenchmark();
            }
        }
    """)
    time.sleep(3.5)
    page.screenshot(path="screenshots/ui_14_admin_evaluation.png")
    print("14. Admin Evaluation captured")

    browser.close()

print("ALL SCREENSHOTS CAPTURED PERFECTLY!")
