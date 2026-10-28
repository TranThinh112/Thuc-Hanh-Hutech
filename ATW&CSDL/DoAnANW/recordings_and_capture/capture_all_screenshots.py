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
    time.sleep(0.5)
    page.screenshot(path="screenshots/ui_02_login_view.png")
    print("2. Login View captured")

    # Quick login as thinh (USER)
    page.evaluate("quickLogin('thinh')")
    time.sleep(1)

    # 3. Cart Modal
    # Add first product to cart
    page.evaluate("if (window.products && window.products.length > 0) { addToCart(window.products[0].id); addToCart(window.products[1].id); }")
    page.evaluate("toggleCartModal(true)")
    time.sleep(0.5)
    page.screenshot(path="screenshots/ui_03_cart_modal.png")
    print("3. Cart Modal captured")

    # 4. Checkout Modal
    page.evaluate("toggleCartModal(false); openCheckoutModal();")
    time.sleep(0.5)
    page.screenshot(path="screenshots/ui_04_checkout_modal.png")
    print("4. Checkout Modal captured")

    # 5. Orders View (as user thinh)
    page.evaluate("closeCheckoutModal(); showView('orders');")
    time.sleep(1)
    page.screenshot(path="screenshots/ui_05_user_orders.png")
    print("5. User Orders captured")

    # 6. SMS Inbox Modal
    page.evaluate("if (typeof openSmsInboxModal === 'function') openSmsInboxModal(); else if (typeof openSmsModal === 'function') openSmsModal(); else { const btn = document.querySelector('[onclick*=\"Sms\"], [onclick*=\"sms\"]'); if (btn) btn.click(); }")
    time.sleep(0.5)
    page.screenshot(path="screenshots/ui_06_sms_modal.png")
    print("6. SMS Inbox Modal captured")

    # Login as ADMIN
    page.evaluate("quickLogin('admin')")
    time.sleep(1)

    # 7. Admin Dashboard KPI & Overview
    page.evaluate("showView('admin'); switchAdminTab('dashboard');")
    time.sleep(1)
    page.screenshot(path="screenshots/ui_07_admin_dashboard_kpi.png")
    print("7. Admin Dashboard KPI captured")

    # 8. Admin Transactions List
    page.evaluate("switchAdminTab('transactions')")
    time.sleep(1)
    page.screenshot(path="screenshots/ui_08_admin_transactions.png")
    print("8. Admin Transactions captured")

    # 9. Admin Transaction Detail / Forensic Inspector Modal
    # Click the first 'Chi tiết' button or open modal for high-risk tx
    page.evaluate("""
        const detailBtns = document.querySelectorAll('button[onclick*="openTxDetail"], button[onclick*="viewTx"], button[onclick*="Detail"], button[onclick*="tx-detail"]');
        if (detailBtns.length > 0) {
            detailBtns[0].click();
        } else {
            const btns = Array.from(document.querySelectorAll('button')).filter(b => b.textContent.includes('Chi tiết') || b.textContent.includes('Pháp y'));
            if (btns.length > 0) btns[0].click();
        }
    """)
    time.sleep(1)
    page.screenshot(path="screenshots/ui_09_admin_transaction_detail.png")
    print("9. Admin Transaction Detail Modal captured")

    # Close modal if open
    page.keyboard.press("Escape")
    time.sleep(0.5)

    # 10. Admin Simulation Tab - Run ATO scenario
    page.evaluate("switchAdminTab('simulation')")
    time.sleep(0.5)
    # trigger ATO simulation
    page.evaluate("""
        const simBtns = document.querySelectorAll('button[onclick*=\"sim\"], button[onclick*=\"Sim\"]');
        if (simBtns.length > 0) simBtns[0].click();
    """)
    time.sleep(1.5)
    page.screenshot(path="screenshots/ui_10_admin_simulation_ato.png")
    print("10. Admin Simulation ATO captured")

    # 11. Admin Simulation Tab - Run Impossible Travel
    page.evaluate("""
        const simBtns = Array.from(document.querySelectorAll('button[onclick*=\"sim\"], button[onclick*=\"Sim\"], .sim-card button'));
        const travelBtn = simBtns.find(b => b.textContent.includes('Impossible') || b.textContent.includes('Di chuyển'));
        if (travelBtn) travelBtn.click();
    """)
    time.sleep(1.5)
    page.screenshot(path="screenshots/ui_11_admin_simulation_travel.png")
    print("11. Admin Simulation Impossible Travel captured")

    # 12. Admin Dynamic Rules Tab
    page.evaluate("switchAdminTab('rules')")
    time.sleep(1)
    page.screenshot(path="screenshots/ui_12_admin_rules.png")
    print("12. Admin Dynamic Rules captured")

    # 13. Admin Evaluation & Benchmark Tab
    page.evaluate("switchAdminTab('evaluation')")
    time.sleep(0.5)
    # Click evaluate button if available
    page.evaluate("""
        const evalBtn = document.querySelector('button[onclick*=\"Evaluation\"], button[onclick*=\"eval\"]');
        if (evalBtn) evalBtn.click();
    """)
    time.sleep(2)
    page.screenshot(path="screenshots/ui_13_admin_evaluation.png")
    print("13. Admin Evaluation Benchmark captured")

    browser.close()
print("All screenshots successfully captured!")
