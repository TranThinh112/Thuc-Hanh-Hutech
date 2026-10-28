with open("python_app/static/index.html", encoding="utf-8") as f:
    h = f.read()
idx = h.find('id="result-modal"')
if idx != -1:
    print(h[idx-50:idx+2000])
