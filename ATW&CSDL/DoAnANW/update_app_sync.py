with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Add syncLocationFromCity function and update setPreset
sync_func = """
function syncLocationFromCity() {
    const citySelect = document.getElementById("chk-city");
    const city = citySelect ? citySelect.value : "Hà Nội";
    const ipEl = document.getElementById("chk-ip");
    const devEl = document.getElementById("chk-device");
    const addrEl = document.getElementById("chk-cust-address");

    if (city === "Tokyo") {
        if (ipEl) ipEl.value = "185.220.101.5";
        if (devEl) devEl.value = "device_hacker_kali";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Shibuya, Tokyo, Japan";
    } else if (city === "London") {
        if (ipEl) ipEl.value = "45.142.120.10";
        if (devEl) devEl.value = "device_bot_script";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Westminster, London, UK";
    } else if (city === "New York") {
        if (ipEl) ipEl.value = "198.51.100.25";
        if (devEl) devEl.value = "device_foreign_pc";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Manhattan, New York, USA";
    } else if (city === "Hồ Chí Minh") {
        if (ipEl) ipEl.value = "14.161.12.99";
        if (devEl) devEl.value = "device_thinh_iphone";
        if (addrEl && addrEl.value.includes("Hà Nội")) addrEl.value = "Quận 1, TP. Hồ Chí Minh";
    } else {
        if (ipEl) ipEl.value = "113.161.44.12";
        if (devEl) devEl.value = "device_thinh_iphone";
        if (addrEl && (addrEl.value.includes("Tokyo") || addrEl.value.includes("London"))) addrEl.value = "Số 15 Cầu Giấy, Hà Nội";
    }
}
"""

if "function syncLocationFromCity" not in js:
    js = sync_func + "\n" + js

# 2. Update setPreset to sync dropdown value
old_set_preset = """function setPreset(type) {
    const ip = document.getElementById("chk-ip");
    const dev = document.getElementById("chk-device");
    const city = document.getElementById("chk-city");

    if (type === "legit") {
        if (ip) ip.value = "113.161.44.12";
        if (dev) dev.value = "device_thinh_iphone";
        if (city) city.value = "Hà Nội";
    } else if (type === "ato") {
        if (ip) ip.value = "185.220.101.5";
        if (dev) dev.value = "device_hacker_kali";
        if (city) city.value = "Tokyo";
    } else if (type === "travel") {
        if (ip) ip.value = "45.142.120.10";
        if (dev) dev.value = "device_bot_script";
        if (city) city.value = "London";
    }
}"""

new_set_preset = """function setPreset(type) {
    const ip = document.getElementById("chk-ip");
    const dev = document.getElementById("chk-device");
    const city = document.getElementById("chk-city");
    const addr = document.getElementById("chk-cust-address");

    if (type === "legit") {
        if (city) city.value = "Hà Nội";
        if (ip) ip.value = "113.161.44.12";
        if (dev) dev.value = "device_thinh_iphone";
        if (addr) addr.value = "Số 15 Cầu Giấy, Hà Nội";
    } else if (type === "ato") {
        if (city) city.value = "Tokyo";
        if (ip) ip.value = "185.220.101.5";
        if (dev) dev.value = "device_hacker_kali";
        if (addr) addr.value = "Shibuya, Tokyo, Japan";
    } else if (type === "travel") {
        if (city) city.value = "London";
        if (ip) ip.value = "45.142.120.10";
        if (dev) dev.value = "device_bot_script";
        if (addr) addr.value = "Westminster, London, UK";
    }
}"""

js = js.replace(old_set_preset, new_set_preset)

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Updated app.js with syncLocationFromCity and updated setPreset!")
