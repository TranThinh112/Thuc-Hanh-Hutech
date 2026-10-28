import os, time, subprocess, imageio_ffmpeg
from playwright.sync_api import sync_playwright

os.makedirs("test_video_out", exist_ok=True)
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(
        viewport={"width": 1600, "height": 900},
        record_video_dir="test_video_out/",
        record_video_size={"width": 1600, "height": 900}
    )
    page = context.new_page()
    page.goto("http://127.0.0.1:8000")
    page.wait_for_timeout(1000)

    # Inject HUD
    page.evaluate("""() => {
        const hud = document.createElement('div');
        hud.id = 'demo-hud';
        hud.style.cssText = `
            position: fixed;
            bottom: 24px;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            max-width: 1200px;
            background: rgba(11, 19, 43, 0.94);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(59, 130, 246, 0.5);
            border-radius: 16px;
            padding: 16px 24px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85);
            z-index: 9999999;
            color: #f8fafc;
            font-family: system-ui, -apple-system, sans-serif;
            transition: all 0.3s ease;
        `;
        hud.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                <span style="background: linear-gradient(90deg, #10b981, #059669); color:#fff; font-size:12px; font-weight:800; padding:4px 12px; border-radius:999px; letter-spacing:0.5px; text-transform:uppercase;">
                    Kịch Bản 1: Giao Dịch Hợp Lệ (Legitimate)
                </span>
                <span style="color:#38bdf8; font-size:12px; font-weight:600;">
                    🛡️ AI & Rule Engine Fraud Prevention
                </span>
            </div>
            <div style="font-size:16px; font-weight:700; color:#38bdf8; margin-bottom:4px;">
                Khách hàng mua hàng từ thiết bị & địa chỉ IP tin cậy
            </div>
            <div style="font-size:13px; color:#cbd5e1; line-height:1.4;">
                Thông số: Hà Nội | Thiết bị Windows PC quen thuộc | Đơn giá: 500,000 VND | Risk Score: 0/100 (APPROVE)
            </div>
        `;
        document.body.appendChild(hud);
    }""")
    page.wait_for_timeout(2000)

    # Click login
    page.evaluate("quickLogin('thinh')")
    page.wait_for_timeout(1000)

    context.close()
    video_path = page.video.path()
    browser.close()

print("Recorded webm:", video_path)

# Convert to mp4 using imageio_ffmpeg
mp4_out = "test_video_out/test_sample.mp4"
cmd = [
    ffmpeg, "-y",
    "-i", video_path,
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    mp4_out
]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Converted to MP4:", os.path.exists(mp4_out), "Size:", os.path.getsize(mp4_out) if os.path.exists(mp4_out) else 0)
