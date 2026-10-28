import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

def show_func(name):
    idx = text.find(f"function {name}")
    if idx != -1:
        print(f"=== {name} ===")
        print(text[idx:idx+800])

show_func("showView")
show_func("quickLogin")
