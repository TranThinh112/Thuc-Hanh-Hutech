with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# Make openLoginModal seamlessly show the dedicated login view or modal
js = js.replace(
    'function openLoginModal() {\n    document.getElementById("login-modal")?.classList.remove("hidden");\n}',
    'function openLoginModal() {\n    showView("login");\n}'
)

# In quickLogin, also sync with dedicated page elements and load SMS
js = js.replace(
    'updateAuthUI();\n        closeLoginModal();',
    'updateAuthUI();\n        closeLoginModal();\n        loadSmsInbox();\n        showView("store");'
)

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Synchronized openLoginModal to showView('login').")
