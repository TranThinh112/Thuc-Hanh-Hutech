import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = re.findall(r'function\s+([a-zA-Z0-9_]*tx[a-zA-Z0-9_]*|[a-zA-Z0-9_]*dashboard[a-zA-Z0-9_]*|[a-zA-Z0-9_]*sim[a-zA-Z0-9_]*|[a-zA-Z0-9_]*eval[a-zA-Z0-9_]*)\s*\(', text, re.I)
print("Related functions:", funcs)
