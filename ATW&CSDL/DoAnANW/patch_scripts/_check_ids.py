import re
with open("python_app/static/index.html", encoding="utf-8") as f:
    h = f.read()
for id_name in re.findall(r'id="([^"]*)"', h):
    if any(k in id_name.lower() for k in ['modal', 'view', 'tab', 'admin']):
        print(id_name)
