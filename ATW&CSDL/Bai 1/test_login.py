import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    requests_log = []
    
    def on_request(req):
        requests_log.append({
            'method': req.method,
            'url': req.url,
            'resource_type': req.resource_type,
            'post_data': req.post_data
        })
    page.on('request', on_request)
    
    resp_get = page.goto('https://the-internet.herokuapp.com/login')
    print('GET response status:', resp_get.status)
    
    page.fill('input#username', 'tomsmith')
    page.fill('input#password', 'SuperSecretPassword!')
    with page.expect_navigation():
        page.click('button[type="submit"]')
        
    print('Current URL after submit:', page.url)
    print('Total requests recorded:', len(requests_log))
    for r in requests_log:
        print(r['method'], r['url'], r['resource_type'], r.get('post_data'))
    browser.close()
