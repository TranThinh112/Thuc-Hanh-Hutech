import sys
sys.stdout.reconfigure(encoding="utf-8")
with open("python_app/static/index.html", encoding="utf-8") as f:
    text = f.read()

start = text.find("res-title")
print(text[start-500:start+2000])
