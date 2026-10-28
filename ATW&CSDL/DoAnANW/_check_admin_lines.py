import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="view-admin"' in l or 'id="adm-tab-dashboard"' in l or 'id="stat-total"' in l:
        print(f"Line {i+1}: {l.strip()}")
