import asyncio
from playwright.async_api import async_playwright
import os

os.makedirs('screenshots', exist_ok=True)

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 800},
            device_scale_factor=1.5
        )
        page = await context.new_page()

        # 1. Giao diện đăng nhập ban đầu
        await page.goto('http://localhost:8080')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='screenshots/01_form_dang_nhap.png')
        print("Captured: 01_form_dang_nhap.png")

        # 2. Kiểm tra dữ liệu để trống (Client Validation)
        await page.click('#submitBtn')
        await page.wait_for_timeout(500)
        await page.screenshot(path='screenshots/02_loi_de_trong.png')
        print("Captured: 02_loi_de_trong.png")

        # 3. Đăng nhập thất bại (Sai mật khẩu - HTTP 401)
        await page.fill('#username', 'admin')
        await page.fill('#password', 'wrongpass999')
        await page.click('#submitBtn')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='screenshots/03_dang_nhap_that_bai.png')
        print("Captured: 03_dang_nhap_that_bai.png")

        # 4. Nhập đúng tài khoản & bấm nút hiện mật khẩu
        await page.fill('#username', 'admin')
        await page.fill('#password', '12345')
        # Bấm toggle password (id là togglePasswordBtn)
        await page.click('#togglePasswordBtn')
        await page.wait_for_timeout(500)
        await page.screenshot(path='screenshots/04_nhap_dung_hien_mat_khau.png')
        print("Captured: 04_nhap_dung_hien_mat_khau.png")

        # Ẩn lại mật khẩu và submit
        await page.click('#togglePasswordBtn')
        await page.click('#submitBtn')

        # 5. Đăng nhập thành công và Dashboard phiên làm việc
        await page.wait_for_selector('#dashboardCard:not(.hidden)', timeout=5000)
        await page.wait_for_timeout(1000)
        await page.screenshot(path='screenshots/05_dang_nhap_thanh_cong.png')
        print("Captured: 05_dang_nhap_thanh_cong.png")

        # 6. Kiểm tra lại việc tải lại trang vẫn giữ phiên (Session persistence)
        await page.reload()
        await page.wait_for_selector('#dashboardCard:not(.hidden)', timeout=5000)
        await page.wait_for_timeout(800)
        await page.screenshot(path='screenshots/06_duy_tri_session_khi_f5.png')
        print("Captured: 06_duy_tri_session_khi_f5.png")

        await browser.close()
        print("Hoàn thành chụp tất cả ảnh!")

asyncio.run(run())
