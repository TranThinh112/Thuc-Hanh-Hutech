import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("python_app/static/index.html", encoding="utf-8") as f:
    text = f.read()

start = text.find("submitPayment")
print(text[start-200:start+400])
