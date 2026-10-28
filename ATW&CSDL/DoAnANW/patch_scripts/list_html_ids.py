with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

import re
all_ids = sorted(re.findall(r'id="([^"]+)"', html))
print(f"All IDs in index.html ({len(all_ids)}):")
for i in all_ids:
    print(" ", i)
