import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
import re
scripts = re.findall(r'<script[^>]*>.*?</script>', html, re.DOTALL)
print(f"Total script tags: {len(scripts)}")
for s in scripts:
    print(s[:150])
