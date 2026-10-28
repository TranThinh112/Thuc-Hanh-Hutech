import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    page = browser.new_page()
    page.on("console", lambda msg: print("CONSOLE:", msg.type, msg.text))
    page.on("pageerror", lambda err: print("PAGE ERROR:", err))
    page.goto("http://127.0.0.1:8000")
    page.wait_for_load_state("networkidle")
    browser.close()
