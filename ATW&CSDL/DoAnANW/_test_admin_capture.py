import os, sys, time
from playwright.sync_api import sync_playwright

os.makedirs("screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1480, "height": 960})
    page.goto("http://127.0.0.1:8000", wait_until="networkidle")
    time.sleep(1)

    # 1. Login as ADMIN
    page.evaluate("async () => { await quickLogin('admin', false); showView('admin'); switchAdminTab('dashboard'); }")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_07_admin_dashboard_kpi.png")
    print("ui_07_admin_dashboard_kpi captured")

    # 2. Admin Transactions
    page.evaluate("switchAdminTab('transactions')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_08_admin_transactions.png")
    print("ui_08_admin_transactions captured")

    # 3. Admin Simulation (run an attack scenario)
    page.evaluate("switchAdminTab('simulation')")
    time.sleep(1)
    # trigger ATO simulation
    page.evaluate("runSimulation('ATO')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_10_admin_simulation_ato.png")
    print("ui_10_admin_simulation_ato captured")

    # trigger Impossible Travel simulation
    page.evaluate("runSimulation('IMPOSSIBLE_TRAVEL')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_11_admin_simulation_travel.png")
    print("ui_11_admin_simulation_travel captured")

    # 4. Admin Rules Management
    page.evaluate("switchAdminTab('rules')")
    time.sleep(2)
    page.screenshot(path="screenshots/ui_12_admin_rules.png")
    print("ui_12_admin_rules captured")

    # 5. Admin Evaluation / Benchmark
    page.evaluate("switchAdminTab('evaluation')")
    time.sleep(1)
    page.evaluate("async () => { if (typeof runBenchmark === 'function') await runBenchmark(); }")
    time.sleep(3)
    page.screenshot(path="screenshots/ui_13_admin_evaluation.png")
    print("ui_13_admin_evaluation captured")

    browser.close()
print("Admin captures done!")
