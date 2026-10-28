import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Page view before login
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("https://the-internet.herokuapp.com/login")
    page.wait_for_load_state("networkidle")
    page.screenshot(path="captures/page_login_view.png")
    
    # Fill login form
    page.fill('input#username', 'tomsmith')
    page.fill('input#password', 'SuperSecretPassword!')
    page.screenshot(path="captures/page_form_filled.png")
    
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    page.screenshot(path="captures/page_secure_view.png")
    
    print("Page screenshots saved successfully!")
    browser.close()
