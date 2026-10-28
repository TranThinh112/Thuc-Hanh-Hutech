# -*- coding: utf-8 -*-
import sys

with open("python_app/main.py", "r", encoding="utf-8") as f:
    text = f.read()

target_old = """    # Tinh toan toa do chuan
    if city == "Tokyo":
        lat, lng = 35.6762, 139.6503
    elif city == "London":
        lat, lng = 51.5074, -0.1278
    elif city == "New York":
        lat, lng = 40.7128, -74.0060
    elif city == "Hồ Chí Minh":
        lat, lng = 10.8231, 106.6297
    elif city == "Đà Nẵng":
        lat, lng = 16.0544, 108.2022
    else:
        city = "Hà Nội"
        country = "Vietnam"
        lat, lng = 21.0285, 105.8542"""

target_new = """    # Tinh toan toa do chuan va nhan dien vi tri IP that neu co
    from .fraud.constants import CITY_COORDINATES
    if is_public_ip(ip_address) and (not payload.get("locationCity") or payload.get("locationCity") == "Hà Nội") and city not in ["Tokyo", "London", "New York"]:
        geo_real = resolve_ip_geo(ip_address)
        if geo_real:
            city = geo_real["city"]
            country = geo_real["country"]
            lat = geo_real["lat"]
            lng = geo_real["lng"]
            CITY_COORDINATES[city] = {"lat": lat, "lng": lng, "country": country}
    elif city in CITY_COORDINATES:
        lat = CITY_COORDINATES[city]["lat"]
        lng = CITY_COORDINATES[city]["lng"]
        country = CITY_COORDINATES[city].get("country", country)
    elif city == "Tokyo":
        lat, lng = 35.6762, 139.6503
    elif city == "London":
        lat, lng = 51.5074, -0.1278
    elif city == "New York":
        lat, lng = 40.7128, -74.0060
    elif city == "Hồ Chí Minh":
        lat, lng = 10.8231, 106.6297
    elif city == "Đà Nẵng":
        lat, lng = 16.0544, 108.2022
    else:
        city = "Hà Nội"
        country = "Vietnam"
        lat, lng = 21.0285, 105.8542"""

if target_old in text:
    text = text.replace(target_old, target_new)
    with open("python_app/main.py", "w", encoding="utf-8") as f:
        f.write(text)
    print("Enhanced GeoIP coordinates in main.py")
else:
    print("target_old not found in main.py")