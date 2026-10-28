import os, sys, time
from playwright.sync_api import sync_playwright

os.makedirs("screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 920})
    page.goto("http://127.0.0.1:8000", wait_until="networkidle")
    time.sleep(1)

    # 1. Homepage
    page.screenshot(path="screenshots/ui_01_store_homepage.png")
    print("1. Homepage captured")

    # 2. Login View
    page.evaluate("showView('login')")
    time.sleep(0.6)
    page.screenshot(path="screenshots/ui_02_login_view.png")
    print("2. Login View captured")

    # Quick login as thinh (USER)
    page.evaluate("quickLogin('thinh')")
    time.sleep(1)

    # 3. Cart Modal
    page.evaluate("if (window.products && window.products.length > 0) { addToCart(window.products[0].id); addToCart(window.products[1].id); }")
    page.evaluate("toggleCartModal(true)")
    time.sleep(0.6)
    page.screenshot(path="screenshots/ui_03_cart_modal.png")
    print("3. Cart Modal captured")

    # 4. Checkout Modal
    page.evaluate("toggleCartModal(false); openCheckoutModal();")
    time.sleep(0.6)
    page.screenshot(path="screenshots/ui_04_checkout_modal.png")
    print("4. Checkout Modal captured")

    # 5. Payment Result Blocked (Trigger ATO attack preset)
    page.evaluate("setPreset('ato')")
    time.sleep(0.5)
    # Submit payment
    page.evaluate("document.getElementById('checkout-form').dispatchEvent(new Event('submit', { cancelable: true }))")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_05_payment_result_blocked.png")
    print("5. Payment Result Blocked captured")
    page.evaluate("closeResultModal()")
    time.sleep(0.5)

    # 6. Payment Result Step-up OTP (Trigger Travel preset which leads to REVIEW)
    page.evaluate("openCheckoutModal()")
    time.sleep(0.5)
    page.evaluate("setPreset('travel')")
    time.sleep(0.5)
    page.evaluate("document.getElementById('checkout-form').dispatchEvent(new Event('submit', { cancelable: true }))")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_06_payment_result_otp.png")
    print("6. Payment Result OTP captured")
    page.evaluate("closeResultModal()")
    time.sleep(0.5)

    # 7. SMS Inbox Modal
    page.evaluate("if (typeof openSmsInboxModal === 'function') openSmsInboxModal(); else if (typeof openSmsModal === 'function') openSmsModal(); else { const btn = document.querySelector('[onclick*=\"Sms\"], [onclick*=\"sms\"]'); if (btn) btn.click(); }")
    time.sleep(0.8)
    page.screenshot(path="screenshots/ui_07_sms_modal.png")
    print("7. SMS Inbox Modal captured")
    page.evaluate("if (typeof closeSmsInboxModal === 'function') closeSmsInboxModal(); else if (typeof closeSmsModal === 'function') closeSmsModal(); else { const modal = document.getElementById('sms-inbox-modal'); if (modal) modal.classList.add('hidden'); }")
    time.sleep(0.5)

    # 8. User Orders
    page.evaluate("showView('orders')")
    time.sleep(1)
    page.screenshot(path="screenshots/ui_08_user_orders.png")
    print("8. User Orders captured")

    # Now Login as ADMIN
    page.evaluate("async () => { await quickLogin('admin', false); showView('admin'); switchAdminTab('dashboard'); }")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_09_admin_dashboard_kpi.png")
    print("9. Admin Dashboard captured")

    # 10. Admin Transactions
    page.evaluate("switchAdminTab('transactions')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_10_admin_transactions.png")
    print("10. Admin Transactions captured")

    # 11. Admin Simulation ATO
    page.evaluate("switchAdminTab('simulation')")
    time.sleep(1)
    page.evaluate("runSimulation('ATO')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_11_admin_simulation_ato.png")
    print("11. Admin Simulation ATO captured")

    # 12. Admin Simulation Travel
    page.evaluate("runSimulation('IMPOSSIBLE_TRAVEL')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_12_admin_simulation_travel.png")
    print("12. Admin Simulation Travel captured")

    # 13. Admin Rules Management
    page.evaluate("switchAdminTab('rules')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_13_admin_rules.png")
    print("13. Admin Rules captured")

    # 14. Admin Evaluation / Benchmark
    page.evaluate("switchAdminTab('evaluation')")
    time.sleep(1)
    page.evaluate("async () => { if (typeof runBenchmark === 'function') await runBenchmark(); }")
    time.sleep(3)
    page.screenshot(path="screenshots/ui_14_admin_evaluation.png")
    print("14. Admin Evaluation captured")

    browser.close()
print("All captures finished successfully!")
