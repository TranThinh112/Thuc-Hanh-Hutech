with open("python_app/static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

# 1. Fix renderProducts grid selector
js = js.replace(
    'const grid = document.getElementById("products-grid");',
    'const grid = document.getElementById("store-product-grid") || document.getElementById("products-grid");'
)

# 2. Fix switchAdminTab section selector
js = js.replace(
    'const sec = document.getElementById("sec-" + t);',
    'const sec = document.getElementById("adm-sec-" + t) || document.getElementById("sec-" + t);'
)

# 3. Fix loadDashboard element selectors with null-safety
old_dashboard_code = """async function loadDashboard() {
    try {
        const res = await fetch("/api/fraud/statistics");
        const stats = await res.json();
        document.getElementById("stat-total").innerText = stats.totalTransactions || 0;
        document.getElementById("stat-blocked").innerText = stats.blockedTransactions || 0;
        document.getElementById("stat-rate").innerText = (stats.blockRate || 0) + "%";
        document.getElementById("stat-alerts").innerText = stats.openAlerts || 0;
        renderCharts(stats);
        loadAlerts();
    } catch (e) {
        console.error("Failed to load dashboard", e);
    }
}"""

new_dashboard_code = """async function loadDashboard() {
    try {
        const res = await fetch("/api/fraud/statistics");
        const stats = await res.json();
        const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
        setVal("stat-total", stats.totalTransactions || 0);
        setVal("stat-blocked", stats.blockedTransactions || 0);
        setVal("stat-review", stats.reviewTransactions || 0);
        setVal("stat-approved", stats.approvedTransactions || 0);
        setVal("stat-fraudrate", (stats.blockRate || 0) + "%");
        setVal("stat-rate", (stats.blockRate || 0) + "%");
        setVal("stat-avgscore", (stats.averageRiskScore || 0) + "/100");
        setVal("stat-alerts", stats.openAlerts || 0);
        renderCharts(stats);
        loadAlerts();
    } catch (e) {
        console.error("Failed to load dashboard", e);
    }
}"""
js = js.replace(old_dashboard_code, new_dashboard_code)

# 4. Fix renderCharts selectors
old_charts_code = """    const ctx1 = document.getElementById("chart-risk-dist")?.getContext("2d");
    const ctx2 = document.getElementById("chart-decision")?.getContext("2d");"""

new_charts_code = """    const c1 = document.getElementById("chartRiskDist") || document.getElementById("chart-risk-dist");
    const c2 = document.getElementById("chartDecision") || document.getElementById("chart-decision");
    const ctx1 = c1?.getContext("2d");
    const ctx2 = c2?.getContext("2d");"""
js = js.replace(old_charts_code, new_charts_code)

# 5. Fix runSimulation element selectors with null-safety
old_sim_code = """async function runSimulation(scenario) {
    document.getElementById("sim-title").innerText = "Giả lập: " + scenario;
    try {
        const res = await fetch("/api/fraud/simulation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scenario })
        });
        const data = await res.json();
        document.getElementById("sim-desc").innerText = data.scenarioDescription || "";
        document.getElementById("sim-score").innerText = data.riskScore + "/100 (" + data.riskLevel + ")";
        document.getElementById("sim-decision").innerText = data.decision;
        document.getElementById("sim-decision").className = "font-bold text-xs px-2.5 py-0.5 rounded " + (data.decision === "APPROVE" ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400");
        document.getElementById("sim-signals").innerHTML = data.signals.map(s => `
            <li class="flex items-start space-x-2 text-xs">
                <span class="font-bold ${s.severity === 'CRITICAL' ? 'text-red-400' : 'text-amber-400'}">[+${s.score}đ]</span>
                <span class="text-slate-300 font-mono">${s.reason}</span>
            </li>
        `).join("");
        document.getElementById("sim-explanation").innerText = data.explanation || "";
    } catch (e) {
        alert("Lỗi khi chạy kịch bản mô phỏng");
    }
}"""

new_sim_code = """async function runSimulation(scenario) {
    const setVal = (id, val) => { const el = document.getElementById(id); if (el) el.innerText = val; };
    setVal("sim-title", "Giả lập: " + scenario);
    try {
        const res = await fetch("/api/fraud/simulation", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scenario })
        });
        const data = await res.json();
        setVal("sim-desc", data.scenarioDescription || "");
        setVal("sim-score", data.riskScore + "/100 (" + data.riskLevel + ")");
        setVal("sim-risk-score", data.riskScore + "/100");
        const decBadge = document.getElementById("sim-decision") || document.getElementById("sim-decision-badge");
        if (decBadge) {
            decBadge.innerText = data.decision;
            decBadge.className = "font-bold text-xs px-2.5 py-0.5 rounded " + (data.decision === "APPROVE" ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/40" : "bg-red-500/20 text-red-400 border border-red-500/40");
        }
        const lvlBadge = document.getElementById("sim-risklevel-badge");
        if (lvlBadge) {
            lvlBadge.innerText = data.riskLevel;
            lvlBadge.className = "px-2.5 py-0.5 rounded text-xs font-bold " + (data.riskLevel === "LOW" ? "bg-emerald-500/20 text-emerald-400" : "bg-red-500/20 text-red-400");
        }
        const signalsEl = document.getElementById("sim-signals") || document.getElementById("sim-triggered-rules");
        if (signalsEl) {
            signalsEl.innerHTML = (data.signals || []).map(s => `
                <div class="flex items-start space-x-2 text-xs p-2 rounded bg-slate-900/60 border border-slate-800">
                    <span class="font-bold ${s.severity === 'CRITICAL' ? 'text-red-400' : 'text-amber-400'}">[+${s.score}đ]</span>
                    <span class="text-slate-300 font-mono">${s.reason}</span>
                </div>
            `).join("");
        }
        setVal("sim-explanation", data.explanation || "");
    } catch (e) {
        alert("Lỗi khi chạy kịch bản mô phỏng");
    }
}"""
js = js.replace(old_sim_code, new_sim_code)

with open("python_app/static/app.js", "w", encoding="utf-8") as f:
    f.write(js)

print("Updated app.js with correct element mappings and safety checks.")
