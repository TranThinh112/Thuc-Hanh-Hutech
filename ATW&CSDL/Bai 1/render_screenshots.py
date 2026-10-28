import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 680})
    
    # 1. DevTools Overview
    cur_dir = os.path.abspath("captures")
    page.goto(f"file:///{cur_dir}/devtools_overview.html")
    page.screenshot(path="captures/screenshot_network_overview.png")
    
    # 2. DevTools GET detail
    page.goto(f"file:///{cur_dir}/devtools_get.html")
    page.screenshot(path="captures/screenshot_get_headers.png")
    
    # 3. DevTools POST detail
    page.goto(f"file:///{cur_dir}/devtools_post.html")
    page.screenshot(path="captures/screenshot_post_headers.png")
    
    print("DevTools screenshots generated successfully!")
    browser.close()
