import sys
sys.stdout.reconfigure(encoding='utf-8')
with open("python_app/static/app.js", encoding="utf-8") as f:
    code = f.read()

idx = code.find("async function submitPayment")
if idx == -1:
    idx = code.find("function submitPayment")
print(code[idx:idx+2000])
