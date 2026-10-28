with open("python_app/static/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update checkout form in index.html to have City/Province selection right in customer info
old_cust_addr = """                    <div>
                        <label class="block text-slate-300 mb-1">Địa chỉ nhận hàng</label>
                        <input id="chk-cust-address" type="text" value="Số 15 Cầu Giấy, Hà Nội" required class="w-full bg-slate-900 border border-slate-700 p-2 rounded text-white focus:outline-none focus:border-blue-500">
                    </div>"""

new_cust_addr = """                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div>
                            <label class="block text-slate-300 mb-1">Tỉnh / Thành Phố giao hàng (Vị trí)</label>
                            <select id="chk-city" onchange="syncLocationFromCity()" class="w-full bg-slate-900 border border-slate-700 p-2 rounded text-white focus:outline-none focus:border-blue-500 font-semibold text-xs">
                                <option value="Hà Nội" selected>Hà Nội (Việt Nam)</option>
                                <option value="Hồ Chí Minh">TP. Hồ Chí Minh (Việt Nam)</option>
                                <option value="Đà Nẵng">Đà Nẵng (Việt Nam)</option>
                                <option value="Tokyo">Tokyo (Nhật Bản - Cách 4,300 km)</option>
                                <option value="London">London (Anh Quốc - Cách 9,200 km)</option>
                                <option value="New York">New York (Hoa Kỳ - Cách 13,000 km)</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-slate-300 mb-1">Địa chỉ nhận hàng chi tiết</label>
                            <input id="chk-cust-address" type="text" value="Số 15 Cầu Giấy, Hà Nội" required class="w-full bg-slate-900 border border-slate-700 p-2 rounded text-white focus:outline-none focus:border-blue-500">
                        </div>
                    </div>"""

if old_cust_addr in html:
    html = html.replace(old_cust_addr, new_cust_addr)

# Also remove the duplicate or sync the old chk-city in sim section if any
html = html.replace('id="chk-city" type="text"', 'id="chk-city-sim" type="text"')

with open("python_app/static/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html location dropdown!")
