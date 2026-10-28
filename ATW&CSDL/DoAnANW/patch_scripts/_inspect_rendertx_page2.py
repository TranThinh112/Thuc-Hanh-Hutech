import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("function renderTransactionsPage")
if idx != -1:
    print(text[idx+1800:idx+3500])
