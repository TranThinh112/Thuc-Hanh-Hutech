import sqlite3
con = sqlite3.connect("py_dev.db")
row = con.execute("SELECT location_city, shipping_address, ip_address, device_id FROM transactions WHERE id LIKE '43d76783%'").fetchone()
print("City stored in DB for 43D76783:", row)
