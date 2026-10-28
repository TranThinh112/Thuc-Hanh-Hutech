import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('python_app/static/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

def show_func_full(name):
    idx = text.find(f"function {name}")
    if idx != -1:
        print(f"=== {name} ===")
        print(text[idx:idx+1500])

show_func_full("showView")
