import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

ids = re.findall(r'id=["\']([^"\']+)["\']', html)
print(f"Total IDs: {len(ids)}")
relevant = [i for i in ids if any(k in i.lower() for k in ['view', 'modal', 'tab', 'admin', 'store', 'cart', 'order', 'checkout', 'rule', 'sim', 'eval', 'login', 'stat', 'tx'])]
print("Key UI component IDs:")
for r in relevant:
    print(" -", r)
