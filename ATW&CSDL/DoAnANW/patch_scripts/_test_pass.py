with open('python_app/seed.py', 'r', encoding='utf-8') as f:
    text = f.read()
import re
print('\n'.join([line for line in text.splitlines() if 'password' in line.lower()][:10]))
