with open("python_app/main.py", "r", encoding="utf-8") as f:
    code = f.read()

old_res = "return FileResponse(os.path.join(static_path, 'index.html'))"
new_res = "return FileResponse(os.path.join(static_path, 'index.html'), headers={'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'})"

code = code.replace(old_res, new_res)

with open("python_app/main.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated FileResponse headers in main.py")
