from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page(viewport={"width": 1600, "height": 900})
    page.goto("http://127.0.0.1:8000")
    time.sleep(1)
    page.evaluate("quickLogin('thinh')")
    time.sleep(0.5)

    # Test preset legit
    page.evaluate("openCheckoutModal()")
    time.sleep(0.5)
    page.evaluate("setPreset('legit')")
    print("Legit preset set")
    
    # Check fields
    amt = page.evaluate("document.getElementById('chk-amount').value")
    city = page.evaluate("document.getElementById('chk-city-sim')?.value || document.getElementById('chk-city')?.value")
    ip = page.evaluate("document.getElementById('chk-ip').value")
    dev = page.evaluate("document.getElementById('chk-device').value")
    print(f"Preset legit: amt={amt}, city={city}, ip={ip}, dev={dev}")
    browser.close()
