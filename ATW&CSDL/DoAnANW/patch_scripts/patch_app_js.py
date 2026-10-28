with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    js_content = f.read()

old_fetch = """        const res = await fetch("/api/transactions", {
            method: "POST",
            headers,
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        closeCheckoutModal();"""

new_fetch = """        const res = await fetch("/api/transactions", {
            method: "POST",
            headers,
            body: JSON.stringify(payload)
        });

        const textResponse = await res.text();
        let data;
        try {
            data = JSON.parse(textResponse);
        } catch (jsonErr) {
            data = { detail: textResponse || ("Lỗi máy chủ (HTTP " + res.status + ")") };
        }
        closeCheckoutModal();"""

if old_fetch in js_content:
    js_content = js_content.replace(old_fetch, new_fetch, 1)
    with open("python_app/static/app.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Patched python_app/static/app.js successfully.")
else:
    print("Warning: old_fetch not found in python_app/static/app.js!")
