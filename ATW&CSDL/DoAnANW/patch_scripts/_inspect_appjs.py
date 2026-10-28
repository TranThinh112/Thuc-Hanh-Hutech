with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Length of app.js:", len(text))
matches = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
print("Some functions in app.js:", matches[:35])
