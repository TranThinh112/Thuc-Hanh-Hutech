import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(1412, 1432):
    print(f"{i+1}: {repr(lines[i])}")
