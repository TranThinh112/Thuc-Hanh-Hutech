# -*- coding: utf-8 -*-
with open("run_full_system_test.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace('alerts = res_alerts.json()["alerts"]', 'alerts = res_alerts.json()')

with open("run_full_system_test.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated run_full_system_test.py")