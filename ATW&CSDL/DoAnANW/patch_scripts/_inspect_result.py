import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("python_app/static/app.js", encoding="utf-8") as f:
    text = f.read()

start = text.find("function showPaymentResult")
print(text[start:start+2500])
