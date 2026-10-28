import re

with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

js_ids = re.findall(r'document\.getElementById\("([^"]+)"\)', js)
html_ids = set(re.findall(r'id="([^"]+)"', html))

missing = [jid for jid in set(js_ids) if jid not in html_ids]
print("IDs in JS but missing in HTML:", missing)
