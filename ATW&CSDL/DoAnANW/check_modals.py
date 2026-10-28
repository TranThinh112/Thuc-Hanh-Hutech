import re

with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

modals = re.findall(r'<div id="([^"]+)"[^>]*class="([^"]+)"', html)
for m_id, m_class in modals:
    if "modal" in m_id or "toast" in m_id:
        print(f"Modal {m_id}: hidden={('hidden' in m_class)} | class={m_class[:80]}")
