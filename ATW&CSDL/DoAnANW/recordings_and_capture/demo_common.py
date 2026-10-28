import os, sys, time, subprocess, imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

OUTPUT_DIR = "demo_videos"
WEBM_DIR = os.path.join(OUTPUT_DIR, "raw_webm")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WEBM_DIR, exist_ok=True)
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

HUD_INJECTION_JS = """
(() => {
    if (document.getElementById('demo-hud')) return;

    // Custom CSS for animations
    const style = document.createElement('style');
    style.innerHTML = `
        @keyframes ripple {
            0% { transform: translate(-50%, -50%) scale(0.6); opacity: 1; }
            100% { transform: translate(-50%, -50%) scale(2.8); opacity: 0; }
        }
        .hud-ripple {
            position: fixed;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 2.5px solid #38bdf8;
            pointer-events: none;
            z-index: 10000001;
            animation: ripple 0.5s cubic-bezier(0.1, 0.8, 0.3, 1) forwards;
        }
    `;
    document.head.appendChild(style);

    // Glowing Virtual Cursor Pointer
    const cur = document.createElement('div');
    cur.id = 'demo-cursor';
    cur.style.cssText = `
        position: fixed;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: rgba(56, 189, 248, 0.9);
        border: 2px solid #ffffff;
        box-shadow: 0 0 18px rgba(56, 189, 248, 0.95);
        pointer-events: none;
        z-index: 10000000;
        transform: translate(-50%, -50%);
        left: 960px;
        top: 540px;
        transition: left 0.4s cubic-bezier(0.22, 1, 0.36, 1), top 0.4s cubic-bezier(0.22, 1, 0.36, 1), transform 0.15s ease;
    `;
    document.body.appendChild(cur);

    // High-Tech Bottom Floating HUD
    const hud = document.createElement('div');
    hud.id = 'demo-hud';
    hud.style.cssText = `
        position: fixed;
        bottom: 18px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 1380px;
        background: rgba(8, 14, 30, 0.95);
        backdrop-filter: blur(20px);
        border: 1.5px solid rgba(59, 130, 246, 0.55);
        border-radius: 16px;
        padding: 14px 26px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.9), 0 0 25px rgba(59, 130, 246, 0.2);
        z-index: 9999999;
        color: #f8fafc;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        transition: all 0.3s ease;
    `;
    hud.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span id="hud-badge" style="background: linear-gradient(135deg, #10b981, #059669); color:#fff; font-size:12px; font-weight:800; padding:4px 14px; border-radius:999px; text-transform:uppercase; letter-spacing:0.5px; box-shadow:0 0 10px rgba(16, 185, 129, 0.4);">
                    KỊCH BẢN DEMO
                </span>
                <span id="hud-step" style="background: rgba(59, 130, 246, 0.2); color:#60a5fa; font-size:11px; font-weight:700; padding:3px 10px; border-radius:6px; border:1px solid rgba(59, 130, 246, 0.3);">
                    BƯỚC 1
                </span>
            </div>
            <div style="color:#94a3b8; font-size:12px; font-weight:600; display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#10b981; box-shadow:0 0 8px #10b981;"></span>
                <span>FRAUDSHIELD AI ENGINE - LIVE DEMO</span>
            </div>
        </div>
        <div id="hud-title" style="font-size:16px; font-weight:700; color:#38bdf8; margin-bottom:3px;">
            Tiêu đề kịch bản
        </div>
        <div id="hud-desc" style="font-size:13px; color:#cbd5e1; line-height:1.45;">
            Nội dung giải thích chi tiết cơ chế phát hiện gian lận...
        </div>
    `;
    document.body.appendChild(hud);

    window.updateDemoHUD = (badgeText, badgeColor, stepText, titleText, descText) => {
        const b = document.getElementById('hud-badge');
        const s = document.getElementById('hud-step');
        const t = document.getElementById('hud-title');
        const d = document.getElementById('hud-desc');
        if (b) {
            b.innerText = badgeText;
            b.style.background = badgeColor;
        }
        if (s) s.innerText = stepText;
        if (t) t.innerText = titleText;
        if (d) d.innerHTML = descText;
    };

    window.moveDemoCursor = (x, y) => {
        const c = document.getElementById('demo-cursor');
        if (c) {
            c.style.left = x + 'px';
            c.style.top = y + 'px';
        }
    };

    window.triggerCursorClick = (x, y) => {
        const r = document.createElement('div');
        r.className = 'hud-ripple';
        r.style.left = x + 'px';
        r.style.top = y + 'px';
        document.body.appendChild(r);
        setTimeout(() => r.remove(), 550);
    };
})();
"""

def transcode_to_mp4(raw_webm, mp4_out):
    print(f"Transcoding {raw_webm} -> {mp4_out} ...")
    cmd = [
        ffmpeg_exe, "-y",
        "-i", raw_webm,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        mp4_out
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    size_mb = os.path.getsize(mp4_out) / (1024 * 1024)
    print(f"  -> Finished: {mp4_out} ({size_mb:.2f} MB)")

def reset_user(page):
    page.evaluate("fetch('/api/user/emergency-unlock', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'})")
    page.evaluate("quickLogin('thinh')")
    page.wait_for_timeout(600)
