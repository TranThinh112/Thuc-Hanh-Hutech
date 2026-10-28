import re
with open("python_app/static/app.js", encoding="utf-8") as f:
    code = f.read()

funcs = re.findall(r'function\s+([a-zA-Z0-9_]*checkout[a-zA-Z0-9_]*|[a-zA-Z0-9_]*Checkout[a-zA-Z0-9_]*)\(', code)
print("Checkout funcs:", funcs)
submits = re.findall(r'function\s+([a-zA-Z0-9_]*submit[a-zA-Z0-9_]*|[a-zA-Z0-9_]*Submit[a-zA-Z0-9_]*)\(', code)
print("Submit funcs:", submits)
for l in code.split('\n'):
    if 'checkout-form' in l or 'openCheckoutModal' in l or 'processPayment' in l or 'createTransaction' in l:
        print(l[:100])
