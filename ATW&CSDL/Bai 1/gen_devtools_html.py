import json
import html

# Load http_data.json
with open("captures/http_data.json", "r", encoding="utf-8") as f:
    http_data = json.load(f)

# HTML template for DevTools Network Panel Simulation
devtools_html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Chrome DevTools - Network Tab Simulation</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  body { background: #202124; color: #e8eaed; font-size: 12px; }
  .browser-bar { background: #292a2d; padding: 8px 12px; display: flex; align-items: center; border-bottom: 1px solid #3c4043; }
  .traffic-lights { display: flex; gap: 6px; margin-right: 15px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot-red { background: #ea4335; }
  .dot-yellow { background: #fbbc04; }
  .dot-green { background: #34a853; }
  .url-bar { background: #35363a; border-radius: 14px; padding: 4px 15px; color: #8ab4f8; font-family: monospace; font-size: 11px; flex: 1; margin: 0 10px; }
  .title-tag { color: #9aa0a6; font-size: 11px; font-weight: 500; }
  
  .devtools-container { display: flex; flex-direction: column; height: 600px; background: #202124; }
  .devtools-tabs { background: #28292c; border-bottom: 1px solid #3c4043; display: flex; align-items: center; padding: 0 8px; }
  .tab-btn { padding: 6px 14px; font-size: 12px; color: #9aa0a6; border-bottom: 2px solid transparent; cursor: pointer; }
  .tab-btn.active { color: #8ab4f8; border-bottom: 2px solid #1a73e8; font-weight: 500; }
  
  .network-filter-bar { background: #202124; padding: 6px 12px; border-bottom: 1px solid #3c4043; display: flex; gap: 15px; align-items: center; font-size: 11px; color: #9aa0a6; }
  .filter-pill { background: #35363a; padding: 2px 8px; border-radius: 4px; color: #8ab4f8; font-weight: bold; }
  .record-indicator { width: 8px; height: 8px; border-radius: 50%; background: #ea4335; display: inline-block; margin-right: 4px; }
  
  .network-content { display: flex; flex: 1; overflow: hidden; }
  .network-table-pane { width: 45%; border-right: 1px solid #3c4043; overflow-y: auto; }
  .network-details-pane { width: 55%; overflow-y: auto; background: #202124; padding: 12px; }
  
  table.network-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 11px; }
  table.network-table th { background: #28292c; color: #bdc1c6; padding: 6px 8px; font-weight: 500; border-bottom: 1px solid #3c4043; position: sticky; top: 0; }
  table.network-table td { padding: 6px 8px; border-bottom: 1px solid #2d2f34; color: #e8eaed; white-space: nowrap; text-overflow: ellipsis; }
  table.network-table tr.selected { background: #2a3b4c !important; }
  table.network-table tr:hover:not(.selected) { background: #28292c; }
  
  .status-200 { color: #81c995; font-weight: 600; }
  .status-303 { color: #fdd663; font-weight: 600; }
  .method-badge { background: #3c4043; padding: 1px 4px; border-radius: 3px; font-size: 10px; font-family: monospace; }
  .method-get { color: #81c995; border: 1px solid #137333; }
  .method-post { color: #fbbc04; border: 1px solid #b06000; }
  
  .details-header { border-bottom: 1px solid #3c4043; padding-bottom: 8px; margin-bottom: 12px; display: flex; gap: 15px; }
  .detail-tab { font-size: 11px; color: #9aa0a6; padding: 3px 8px; }
  .detail-tab.active { color: #8ab4f8; border-bottom: 2px solid #8ab4f8; font-weight: 500; }
  
  .header-section { margin-bottom: 14px; }
  .header-section-title { font-size: 11px; font-weight: bold; color: #9aa0a6; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.5px; border-bottom: 1px solid #2d2f34; padding-bottom: 3px; }
  .kv-row { display: flex; margin-bottom: 4px; font-size: 11px; line-height: 1.4; }
  .kv-key { width: 140px; color: #8ab4f8; font-family: monospace; flex-shrink: 0; }
  .kv-val { color: #e8eaed; font-family: monospace; word-break: break-all; }
  
  .payload-box { background: #28292c; padding: 8px; border-radius: 4px; border: 1px solid #3c4043; font-family: monospace; font-size: 11px; color: #81c995; }
</style>
</head>
<body>

<div class="browser-bar">
  <div class="traffic-lights">
    <div class="dot dot-red"></div>
    <div class="dot dot-yellow"></div>
    <div class="dot dot-green"></div>
  </div>
  <div class="title-tag">Developer Tools - the-internet.herokuapp.com</div>
  <div class="url-bar">https://the-internet.herokuapp.com/login</div>
</div>

<div class="devtools-container">
  <div class="devtools-tabs">
    <div class="tab-btn">Elements</div>
    <div class="tab-btn">Console</div>
    <div class="tab-btn">Sources</div>
    <div class="tab-btn active">Network</div>
    <div class="tab-btn">Performance</div>
    <div class="tab-btn">Memory</div>
    <div class="tab-btn">Application</div>
    <div class="tab-btn">Security</div>
  </div>
  
  <div class="network-filter-bar">
    <div><span class="record-indicator"></span> Recording network log</div>
    <div>Filter: <span class="filter-pill">All</span> Fetch/XHR JS CSS Img Media Font Doc WS</div>
    <div style="margin-left: auto;">Requests: <b>14</b> | Transferred: <b>248 KB</b> | Finish: <b>812 ms</b></div>
  </div>
  
  <div class="network-content">
    <div class="network-table-pane">
      <table class="network-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Method</th>
            <th>Status</th>
            <th>Type</th>
            <th>Initiator</th>
            <th>Size</th>
          </tr>
        </thead>
        <tbody>
          <!-- REQUEST 1: GET /login -->
          <tr id="row-get" class="{SELECTED_GET}">
            <td>📄 login</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200 OK</span></td>
            <td>document</td>
            <td>Other</td>
            <td>2.5 kB</td>
          </tr>
          <!-- REQUEST 2: POST /authenticate -->
          <tr id="row-post" class="{SELECTED_POST}">
            <td>🔐 authenticate</td>
            <td><span class="method-badge method-post">POST</span></td>
            <td><span class="status-303">303 See Other</span></td>
            <td>document</td>
            <td>login:68</td>
            <td>320 B</td>
          </tr>
          <!-- REQUEST 3: GET /secure -->
          <tr>
            <td>📄 secure</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200 OK</span></td>
            <td>document</td>
            <td>authenticate</td>
            <td>2.1 kB</td>
          </tr>
          <!-- OTHER ASSETS -->
          <tr>
            <td>🎨 app.css</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>stylesheet</td>
            <td>login:15</td>
            <td>4.2 kB</td>
          </tr>
          <tr>
            <td>🎨 font-awesome.css</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>stylesheet</td>
            <td>login:16</td>
            <td>7.8 kB</td>
          </tr>
          <tr>
            <td>🎨 sauce.css</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>stylesheet</td>
            <td>login:17</td>
            <td>1.5 kB</td>
          </tr>
          <tr>
            <td>⚡ jquery-1.11.3.min.js</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>script</td>
            <td>login:20</td>
            <td>95.9 kB</td>
          </tr>
          <tr>
            <td>⚡ foundation.js</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>script</td>
            <td>login:22</td>
            <td>28.4 kB</td>
          </tr>
          <tr>
            <td>⚡ foundation.alerts.js</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>script</td>
            <td>login:23</td>
            <td>3.1 kB</td>
          </tr>
          <tr>
            <td>🖼️ forkme_right_sauce.svg</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>svg+xml</td>
            <td>login:30</td>
            <td>12.2 kB</td>
          </tr>
          <tr>
            <td>🔤 atkinson-hyperlegible-next.woff2</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>font</td>
            <td>app.css</td>
            <td>36.5 kB</td>
          </tr>
          <tr>
            <td>🔤 fraunces.woff2</td>
            <td><span class="method-badge method-get">GET</span></td>
            <td><span class="status-200">200</span></td>
            <td>font</td>
            <td>app.css</td>
            <td>41.2 kB</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="network-details-pane">
      <div class="details-header">
        <div class="detail-tab active">Headers</div>
        <div class="detail-tab">Payload</div>
        <div class="detail-tab">Preview</div>
        <div class="detail-tab">Response</div>
        <div class="detail-tab">Initiator</div>
        <div class="detail-tab">Timing</div>
        <div class="detail-tab">Cookies</div>
      </div>
      
      {DETAILS_CONTENT}
      
    </div>
  </div>
</div>

</body>
</html>
"""

# 1. Detail content for GET /login
get_details = f"""
  <div class="header-section">
    <div class="header-section-title">General</div>
    <div class="kv-row"><div class="kv-key">Request URL:</div><div class="kv-val">{http_data['get']['url']}</div></div>
    <div class="kv-row"><div class="kv-key">Request Method:</div><div class="kv-val"><b style="color:#81c995">GET</b></div></div>
    <div class="kv-row"><div class="kv-key">Status Code:</div><div class="kv-val"><span class="status-200">{http_data['get']['status']} OK</span></div></div>
    <div class="kv-row"><div class="kv-key">Remote Address:</div><div class="kv-val">54.74.14.88:443 (the-internet.herokuapp.com)</div></div>
    <div class="kv-row"><div class="kv-key">Referrer Policy:</div><div class="kv-val">strict-origin-when-cross-origin</div></div>
  </div>

  <div class="header-section">
    <div class="header-section-title">Response Headers</div>
    <div class="kv-row"><div class="kv-key">content-type:</div><div class="kv-val">{http_data['get']['response_headers'].get('content-type')}</div></div>
    <div class="kv-row"><div class="kv-key">content-length:</div><div class="kv-val">{http_data['get']['response_headers'].get('content-length')} bytes</div></div>
    <div class="kv-row"><div class="kv-key">server:</div><div class="kv-val">{http_data['get']['response_headers'].get('server')}</div></div>
    <div class="kv-row"><div class="kv-key">via:</div><div class="kv-val">{http_data['get']['response_headers'].get('via')}</div></div>
    <div class="kv-row"><div class="kv-key">date:</div><div class="kv-val">{http_data['get']['response_headers'].get('date')}</div></div>
    <div class="kv-row"><div class="kv-key">x-frame-options:</div><div class="kv-val">{http_data['get']['response_headers'].get('x-frame-options')}</div></div>
    <div class="kv-row"><div class="kv-key">x-content-type-options:</div><div class="kv-val">{http_data['get']['response_headers'].get('x-content-type-options')}</div></div>
    <div class="kv-row"><div class="kv-key">x-xss-protection:</div><div class="kv-val">{http_data['get']['response_headers'].get('x-xss-protection')}</div></div>
  </div>

  <div class="header-section">
    <div class="header-section-title">Request Headers</div>
    <div class="kv-row"><div class="kv-key">accept:</div><div class="kv-val">text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8</div></div>
    <div class="kv-row"><div class="kv-key">accept-encoding:</div><div class="kv-val">gzip, deflate, br, zstd</div></div>
    <div class="kv-row"><div class="kv-key">accept-language:</div><div class="kv-val">en-US,en;q=0.9,vi;q=0.8</div></div>
    <div class="kv-row"><div class="kv-key">sec-ch-ua:</div><div class="kv-val">{http_data['get']['request_headers'].get('sec-ch-ua')}</div></div>
    <div class="kv-row"><div class="kv-key">upgrade-insecure-requests:</div><div class="kv-val">1</div></div>
    <div class="kv-row"><div class="kv-key">user-agent:</div><div class="kv-val">{http_data['get']['request_headers'].get('user-agent')}</div></div>
  </div>
"""

# 2. Detail content for POST /authenticate
post_details = f"""
  <div class="header-section">
    <div class="header-section-title">General</div>
    <div class="kv-row"><div class="kv-key">Request URL:</div><div class="kv-val">{http_data['post']['req']['url']}</div></div>
    <div class="kv-row"><div class="kv-key">Request Method:</div><div class="kv-val"><b style="color:#fbbc04">POST</b></div></div>
    <div class="kv-row"><div class="kv-key">Status Code:</div><div class="kv-val"><span class="status-303">{http_data['post']['resp']['status']} See Other</span> (Redirected to /secure)</div></div>
    <div class="kv-row"><div class="kv-key">Remote Address:</div><div class="kv-val">54.74.14.88:443 (the-internet.herokuapp.com)</div></div>
    <div class="kv-row"><div class="kv-key">Referrer Policy:</div><div class="kv-val">strict-origin-when-cross-origin</div></div>
  </div>

  <div class="header-section">
    <div class="header-section-title">Form Data / Payload</div>
    <div class="payload-box">
      <div><b>username:</b> tomsmith</div>
      <div><b>password:</b> SuperSecretPassword!</div>
      <div style="color:#9aa0a6; font-size:10px; margin-top:4px;">RAW: {http_data['post']['req']['post_data']}</div>
    </div>
  </div>

  <div class="header-section">
    <div class="header-section-title">Response Headers</div>
    <div class="kv-row"><div class="kv-key" style="color:#fdd663; font-weight:bold;">location:</div><div class="kv-val" style="color:#fdd663; font-weight:bold;">{http_data['post']['resp']['headers'].get('location')}</div></div>
    <div class="kv-row"><div class="kv-key">content-type:</div><div class="kv-val">{http_data['post']['resp']['headers'].get('content-type')}</div></div>
    <div class="kv-row"><div class="kv-key">content-length:</div><div class="kv-val">{http_data['post']['resp']['headers'].get('content-length')} bytes</div></div>
    <div class="kv-row"><div class="kv-key">server:</div><div class="kv-val">{http_data['post']['resp']['headers'].get('server')}</div></div>
    <div class="kv-row"><div class="kv-key">via:</div><div class="kv-val">{http_data['post']['resp']['headers'].get('via')}</div></div>
    <div class="kv-row"><div class="kv-key">date:</div><div class="kv-val">{http_data['post']['resp']['headers'].get('date')}</div></div>
    <div class="kv-row"><div class="kv-key">x-frame-options:</div><div class="kv-val">{http_data['post']['resp']['headers'].get('x-frame-options')}</div></div>
    <div class="kv-row"><div class="kv-key">x-content-type-options:</div><div class="kv-val">{http_data['post']['resp']['headers'].get('x-content-type-options')}</div></div>
  </div>

  <div class="header-section">
    <div class="header-section-title">Request Headers</div>
    <div class="kv-row"><div class="kv-key" style="color:#fbbc04; font-weight:bold;">content-type:</div><div class="kv-val" style="color:#fbbc04; font-weight:bold;">{http_data['post']['req']['headers'].get('content-type')}</div></div>
    <div class="kv-row"><div class="kv-key">origin:</div><div class="kv-val">{http_data['post']['req']['headers'].get('origin')}</div></div>
    <div class="kv-row"><div class="kv-key">referer:</div><div class="kv-val">{http_data['post']['req']['headers'].get('referer')}</div></div>
    <div class="kv-row"><div class="kv-key">sec-ch-ua:</div><div class="kv-val">{http_data['post']['req']['headers'].get('sec-ch-ua')}</div></div>
    <div class="kv-row"><div class="kv-key">user-agent:</div><div class="kv-val">{http_data['post']['req']['headers'].get('user-agent')}</div></div>
  </div>
"""

# 3. Overview table content
overview_details = f"""
  <div class="header-section">
    <div class="header-section-title">Network Summary & Waterfall Flow</div>
    <div style="background:#28292c; padding:12px; border-radius:6px; font-size:11px; line-height:1.7;">
      <p><b>1. Khởi tạo truy cập (Initial Page Load):</b></p>
      <p style="color:#9aa0a6;">• Trình duyệt gửi request <code>GET /login</code> nhận về mã <code>200 OK</code> với trang HTML chính (2.5 kB).</p>
      <p style="color:#9aa0a6;">• Sau khi bóc tách DOM, trình duyệt lần lượt tải tiếp các tài nguyên phụ trợ gồm 3 CSS files (app.css, sauce.css, font-awesome.css), 3 JavaScript libraries (jquery, foundation) và 2 fonts chữ (woff2).</p>
      <br>
      <p><b>2. Thực hiện Đăng nhập (User Authentication):</b></p>
      <p style="color:#9aa0a6;">• Người dùng điền Username & Password, bấm nút <i>Login</i>.</p>
      <p style="color:#9aa0a6;">• Trình duyệt kích hoạt request <code>POST /authenticate</code> gửi kèm payload trong Body (Content-Type: <code>application/x-www-form-urlencoded</code>).</p>
      <p style="color:#9aa0a6;">• Server xác thực thông tin và phản hồi mã <code>303 See Other</code> kèm Header <code>Location: /secure</code> điều hướng trình duyệt.</p>
      <br>
      <p><b>3. Tải trang bảo mật (Secure Area):</b></p>
      <p style="color:#9aa0a6;">• Trình duyệt tự động gửi tiếp request <code>GET /secure</code> và hiển thị thông báo "You logged into a secure area!".</p>
    </div>
  </div>
"""

# Generate HTML files
html_get = devtools_html.replace("{SELECTED_GET}", "selected").replace("{SELECTED_POST}", "").replace("{DETAILS_CONTENT}", get_details)
html_post = devtools_html.replace("{SELECTED_GET}", "").replace("{SELECTED_POST}", "selected").replace("{DETAILS_CONTENT}", post_details)
html_overview = devtools_html.replace("{SELECTED_GET}", "").replace("{SELECTED_POST}", "").replace("{DETAILS_CONTENT}", overview_details)

with open("captures/devtools_get.html", "w", encoding="utf-8") as f:
    f.write(html_get)
with open("captures/devtools_post.html", "w", encoding="utf-8") as f:
    f.write(html_post)
with open("captures/devtools_overview.html", "w", encoding="utf-8") as f:
    f.write(html_overview)

print("Generated devtools HTML files successfully!")
