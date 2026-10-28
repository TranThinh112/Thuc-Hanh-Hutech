with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update script tag with cache-buster
html = html.replace(
    '<script src="/static/app.js"></script>',
    '<script src="/static/app.js?v=2.2"></script>'
)

with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html updated with cache-buster version 2.2!")
