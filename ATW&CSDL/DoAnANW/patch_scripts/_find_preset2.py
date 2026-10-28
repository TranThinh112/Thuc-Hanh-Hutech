import sys
sys.stdout.reconfigure(encoding='utf-8')
with open("python_app/static/app.js", encoding="utf-8") as f:
    code = f.read()

idx = code.find("function setPreset")
print(code[idx:idx+1500])
