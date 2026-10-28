import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    post_info = {}
    def on_response(resp):
        if resp.request.method == "POST" and "authenticate" in resp.url:
            post_info["url"] = resp.url
            post_info["status"] = resp.status
            post_info["status_text"] = resp.status_text
            post_info["request_headers"] = resp.request.headers
            post_info["response_headers"] = resp.headers
            post_info["post_data"] = resp.request.post_data
    page.on("response", on_response)
    
    resp_get = page.goto("https://the-internet.herokuapp.com/login")
    get_info = {
        "url": resp_get.url,
        "status": resp_get.status,
        "request_headers": resp_get.request.headers,
        "response_headers": resp_get.headers
    }
    
    page.fill('input#username', 'tomsmith')
    page.fill('input#password', 'SuperSecretPassword!')
    with page.expect_navigation():
        page.click('button[type="submit"]')
        
    print("--- GET INFO ---")
    print("Status:", get_info["status"])
    print("Content-Type:", get_info["response_headers"].get("content-type"))
    print("Server:", get_info["response_headers"].get("server"))
    
    print("\n--- POST INFO ---")
    print("POST Status:", post_info.get("status"))
    print("POST URL:", post_info.get("url"))
    print("Location header:", post_info.get("response_headers", {}).get("location"))
    print("Set-Cookie header:", post_info.get("response_headers", {}).get("set-cookie"))
    print("POST Data:", post_info.get("post_data"))
    
    browser.close()
