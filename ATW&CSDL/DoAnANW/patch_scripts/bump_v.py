with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('/static/app.js?v=2.2', '/static/app.js?v=2.3')
with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Bumped to v=2.3")
