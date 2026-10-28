import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("First 40 lines of app.js:")
for i, l in enumerate(lines[:40]):
    print(f"{i+1}: {l.rstrip()}")
print("...")
print("Last 40 lines of app.js:")
for i, l in enumerate(lines[-40:]):
    print(f"{len(lines)-40+i+1}: {l.rstrip()}")
