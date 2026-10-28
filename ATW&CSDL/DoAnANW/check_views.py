import re

with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

views = re.findall(r'<div id="(view-[^"]+)"', html)
print("Current views in HTML:", views)
