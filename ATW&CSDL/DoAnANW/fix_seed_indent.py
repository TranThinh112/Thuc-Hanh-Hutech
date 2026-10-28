with open("python_app/seed.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("    ]\n        db.add_all(products)\n    db.commit()", "    ]\n    db.add_all(products)\n    db.commit()")

with open("python_app/seed.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed seed.py indentation.")
