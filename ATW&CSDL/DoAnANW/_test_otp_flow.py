import sys
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto("http://127.0.0.1:8000")
    time.sleep(1)
    page.evaluate("fetch('/api/user/emergency-unlock', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'})")
    page.evaluate("quickLogin('thinh')")
    time.sleep(0.5)
    page.evaluate("openCheckoutModal()")
    time.sleep(0.5)
    page.evaluate("setPreset('high_amount')")
    time.sleep(0.5)
    page.evaluate("document.getElementById('checkout-form').requestSubmit()")
    time.sleep(2)
    
    print("Modal title after submit:", page.evaluate("document.getElementById('res-title')?.innerText"))
    print("OTP section hidden?", page.evaluate("document.getElementById('res-otp-section')?.classList.contains('hidden')"))
    
    # Fill OTP
    page.evaluate("fillOtpFromSms()")
    otp_val = page.evaluate("document.getElementById('res-otp-input')?.value")
    print("Filled OTP value:", otp_val)
    
    # Submit OTP
    page.evaluate("submitOtpVerification()")
    time.sleep(2)
    print("Modal title after OTP verify:", page.evaluate("document.getElementById('res-title')?.innerText"))
    print("Modal status label:", page.evaluate("document.getElementById('res-status-label')?.innerText"))
    browser.close()
