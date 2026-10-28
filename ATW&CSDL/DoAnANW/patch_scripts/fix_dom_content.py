with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

old_event = """document.addEventListener("DOMContentLoaded", async () => {
    await initAuth();
    loadProducts();
    if (currentUser && currentUser.role === "ADMIN") {
        loadDashboard();
    }
});"""

new_event = """document.addEventListener("DOMContentLoaded", () => {
    // 1. Load products immediately without waiting for auth
    loadProducts();

    // 2. Initialize auth in parallel
    initAuth().then(() => {
        if (currentUser && currentUser.role === "ADMIN") {
            loadDashboard();
        }
    }).catch(err => {
        console.warn("Auth initialization issue:", err);
    });
});"""

js = js.replace(old_event, new_event)

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Updated DOMContentLoaded to call loadProducts immediately!")
