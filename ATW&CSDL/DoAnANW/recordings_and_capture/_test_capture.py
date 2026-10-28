import os, sys, time
from playwright.sync_api import sync_playwright

os.makedirs("screenshots", exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    print("Navigating to http://127.0.0.1:8000 ...")
    page.goto("http://127.0.0.1:8000", wait_until="networkidle")
    time.sleep(1)
    
    # 1. Store homepage
    page.screenshot(path="screenshots/ui_01_store_homepage.png")
    print("Saved ui_01_store_homepage.png")
    
    browser.close()
print("Test capture finished.")
