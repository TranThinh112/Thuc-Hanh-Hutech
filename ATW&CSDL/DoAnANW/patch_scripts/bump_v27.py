with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
html = re.sub(r'/static/app\.js\?v=[\d\.]+', '/static/app.js?v=2.7', html)

with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Bumped to v=2.7")
