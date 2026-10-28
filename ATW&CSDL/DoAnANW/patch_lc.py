with open("python_app/main.py", "r", encoding="utf-8") as f:
    text = f.read()

target = '"locationCity": tx.location_city,'
if '"locationCountry": tx.location_country,' not in text:
    text = text.replace(target, target + '\n            "locationCountry": tx.location_country,')
    with open("python_app/main.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Added locationCountry successfully")