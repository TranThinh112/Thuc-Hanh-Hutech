import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
for f in funcs:
    if any(k in f.lower() for k in ['load', 'render', 'open', 'show', 'run', 'switch', 'detail', 'modal']):
        print(f)
