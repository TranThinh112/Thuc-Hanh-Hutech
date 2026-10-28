with open("python_app/fraud/constants.py", "r", encoding="utf-8") as f:
    text = f.read()

if "Hồ Chí Minh" not in text:
    old_c = '"Ho Chi Minh City": {"lat": 10.8231, "lng": 106.6297, "country": "Vietnam"},'
    new_c = '"Ho Chi Minh City": {"lat": 10.8231, "lng": 106.6297, "country": "Vietnam"},\n    "Hồ Chí Minh": {"lat": 10.8231, "lng": 106.6297, "country": "Vietnam"},\n    "Hà Nội": {"lat": 21.0285, "lng": 105.8542, "country": "Vietnam"},'
    text = text.replace(old_c, new_c)
    with open("python_app/fraud/constants.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Updated CITY_COORDINATES with Vietnamese names!")
else:
    print("Already present")
