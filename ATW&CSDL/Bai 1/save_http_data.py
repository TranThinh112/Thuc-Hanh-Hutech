import json
from playwright.sync_api import sync_playwright

captured = {"post_req": None, "post_resp": None}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    def handle_request(req):
        if req.method == "POST":
            captured["post_req"] = {
                "url": req.url,
                "method": req.method,
                "headers": req.headers,
                "post_data": req.post_data
            }
            
    def handle_response(resp):
        if resp.request.method == "POST":
            captured["post_resp"] = {
                "url": resp.url,
                "status": resp.status,
                "status_text": resp.status_text,
                "headers": resp.headers
            }
            
    page.on("request", handle_request)
    page.on("response", handle_response)
    
    resp_get = page.goto("https://the-internet.herokuapp.com/login")
    get_info = {
        "url": resp_get.url,
        "status": resp_get.status,
        "request_headers": resp_get.request.headers,
        "response_headers": resp_get.headers
    }
    
    page.fill('input#username', 'tomsmith')
    page.fill('input#password', 'SuperSecretPassword!')
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")
    
    full_data = {
        "get": get_info,
        "post": {
            "req": captured["post_req"],
            "resp": captured["post_resp"]
        }
    }
    with open("captures/http_data.json", "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=2, ensure_ascii=False)
        
    print("Saved http_data.json successfully!")
    browser.close()
