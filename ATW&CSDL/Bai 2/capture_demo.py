import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1200, 'height': 800})
        page = await context.new_page()

        # 1. Trang ban đầu
        await page.goto('http://localhost:8080')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='screenshots/01_login_initial.png', full_page=True)
        print("Captured: 01_login_initial.png")

        # 2. Validation lỗi để trống
        await page.click('#submitBtn')
        await page.wait_for_timeout(500)
        await page.screenshot(path='screenshots/02_validation_empty.png', full_page=True)
        print("Captured: 02_validation_empty.png")

        # 3. Đăng nhập sai
        await page.fill('#username', 'admin')
        await page.fill('#password', 'wrongpass')
        await page.click('#submitBtn')
        await page.wait_for_timeout(800)
        await page.screenshot(path='screenshots/03_login_failure.png', full_page=True)
        print("Captured: 03_login_failure.png")

        # 4. Đăng nhập thành công
        await page.fill('#username', 'admin')
        await page.fill('#password', '12345')
        await page.click('#submitBtn')
        # Đợi hiển thị dashboard thành công
        await page.wait_for_selector('#dashboardCard:not(.hidden)', timeout=5000)
        await page.wait_for_timeout(800)
        await page.screenshot(path='screenshots/04_login_success.png', full_page=True)
        print("Captured: 04_login_success.png")

        await browser.close()

asyncio.run(run())
