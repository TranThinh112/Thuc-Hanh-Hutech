# -*- coding: utf-8 -*-
with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    text = f.read()

auth_fetch_func = """
function authFetch(url, options = {}) {
    options = options || {};
    options.headers = options.headers || {};
    const token = accessToken || localStorage.getItem("access_token");
    if (token) {
        options.headers["Authorization"] = "Bearer " + token;
    }
    return fetch(url, options);
}
"""

if "function authFetch" not in text:
    target = 'let chartRiskDist = null, chartDecision = null;'
    text = text.replace(target, target + "\n" + auth_fetch_func)

# Replace fetch with authFetch for admin fraud routes
text = text.replace('const res = await fetch(url);', 'const res = await authFetch(url);')
text = text.replace('const res = await fetch("/api/fraud/statistics");', 'const res = await authFetch("/api/fraud/statistics");')
text = text.replace('const res = await fetch("/api/fraud/alerts");', 'const res = await authFetch("/api/fraud/alerts");')
text = text.replace('await fetch(`/api/fraud/alerts/${id}`,', 'await authFetch(`/api/fraud/alerts/${id}`,')
text = text.replace('const res = await fetch("/api/fraud/rules");', 'const res = await authFetch("/api/fraud/rules");')
text = text.replace('const res = await fetch("/api/fraud/simulation",', 'const res = await authFetch("/api/fraud/simulation",')
text = text.replace('const res = await fetch("/api/fraud/evaluation",', 'const res = await authFetch("/api/fraud/evaluation",')

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated app.js with authFetch")