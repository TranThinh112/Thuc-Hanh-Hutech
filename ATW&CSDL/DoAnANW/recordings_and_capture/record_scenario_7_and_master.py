import os, sys, time, subprocess
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
from demo_common import OUTPUT_DIR, WEBM_DIR, HUD_INJECTION_JS, transcode_to_mp4, ffmpeg_exe

# =========================================================================
# SCENARIO 7: QUẢN TRỊ, PHÁP Y & LUẬT ĐỘNG (ADMIN SOC FORENSICS & RULES)
# =========================================================================
def record_scenario_7():
    print("\n[7/7] Recording Scenario 7: Quản Trị, Pháp Y & Luật Động (Admin SOC)...")
    webm_dir = os.path.join(WEBM_DIR, "s7")
    os.makedirs(webm_dir, exist_ok=True)
    mp4_out = os.path.join(OUTPUT_DIR, "07_admin_forensics_rules.mp4")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=webm_dir,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1000)

        # Login as ADMIN
        page.evaluate("async () => { await quickLogin('admin', false); showView('admin'); switchAdminTab('dashboard'); }")
        page.wait_for_timeout(1000)
        page.evaluate(HUD_INJECTION_JS)

        # Stage 1: SOC Dashboard & KPI
        page.evaluate("""() => {
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN: BẢNG ĐIỀU KHIỂN SOC',
                'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                'PHẦN 1/4: THEO DÕI THỜI GIAN THỰC & CHỈ SỐ KPI',
                'Trung tâm giám sát an ninh thanh toán số (Fraud SOC Dashboard)',
                '• Cung cấp chỉ số thời gian thực: Tổng đơn xử lý, Tỉ lệ chặn gian lận, Doanh thu được bảo vệ an toàn và Biểu đồ phân bổ mức độ rủi ro (Low / Medium / High / Critical).'
            );
            window.moveDemoCursor(650, 300);
        }""")
        page.wait_for_timeout(3500)

        # Stage 2: Audit Logs & Forensic Radar Chart
        page.evaluate("""() => {
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN: PHÁP Y SỐ GIAO DỊCH',
                'linear-gradient(135deg, #8b5cf6, #6d28d9)',
                'PHẦN 2/4: TRUY VẾT & ĐIỀU TRA GIAO DỊCH (FORENSICS)',
                'Phân tích chi tiết giao dịch bất thường với Radar Chart đa chiều & Bản đồ IP',
                'Chuyên viên an ninh (Fraud Analyst) có thể xem xét biểu đồ radar 5 chiều: Vị trí địa lý, Thiết bị, Vận tốc, Tần suất, Giá trị; đồng thời tra cứu IP trên bản đồ toàn cầu.'
            );
            switchAdminTab('transactions');
            window.moveDemoCursor(960, 400);
        }""")
        page.wait_for_timeout(3500)

        # Stage 3: Attack Simulation
        page.evaluate("""() => {
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN: MÔ PHỎNG TẤN CÔNG (SIMULATION)',
                'linear-gradient(135deg, #f97316, #c2410c)',
                'PHẦN 3/4: THỬ NGHIỆM ĐỘNG CƠ VỚI CÁC CUỘC TẤN CÔNG GIẢ LẬP',
                'Kiểm tra khả năng phản ứng của AI với các kịch bản tấn công thực tế',
                'Quản trị viên có thể kích hoạt các kịch bản: ATO, Impossible Travel, Card Testing ngay trong giao diện để kiểm chứng độ nhạy của động cơ.'
            );
            switchAdminTab('simulation');
            runSimulation('ATO');
            window.moveDemoCursor(800, 350);
        }""")
        page.wait_for_timeout(3200)

        # Stage 4: Dynamic Rules Management & ROC-AUC Benchmark
        page.evaluate("""() => {
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN: ĐIỀU CHỈNH LUẬT & ĐÁNH GIÁ MÔ HÌNH',
                'linear-gradient(135deg, #10b981, #059669)',
                'PHẦN 4/4: QUẢN LÝ LUẬT ĐỘNG (DYNAMIC RULES) & ĐÁNH GIÁ MÔ HÌNH ROC-AUC',
                'Thay đổi trọng số quy tắc gian lận theo thời gian thực (Zero Downtime)',
                '• Bảng luật động cho phép bật/tắt luật hoặc thay đổi trọng số ngay lập tức.<br>• Chạy Benchmark kiểm tra độ chính xác, Confusion Matrix và diện tích dưới đường cong ROC-AUC.'
            );
            switchAdminTab('rules');
            window.moveDemoCursor(900, 380);
        }""")
        page.wait_for_timeout(3200)

        # Switch to evaluation and run benchmark
        page.evaluate("""() => {
            switchAdminTab('evaluation');
            if (typeof runBenchmark === 'function') runBenchmark();
            window.moveDemoCursor(960, 450);
        }""")
        page.wait_for_timeout(3500)

        context.close()
        raw_webm = page.video.path()
        browser.close()

    transcode_to_mp4(raw_webm, mp4_out)

# =========================================================================
# MASTER VIDEO CONCATENATION: FULL_DEMO_ALL_SCENARIOS.mp4
# =========================================================================
def concatenate_all_videos():
    print("\n[MASTER] Concatenating all 7 scenarios into FULL_DEMO_ALL_SCENARIOS.mp4 ...")
    mp4_files = [
        os.path.join(OUTPUT_DIR, "01_legit_transaction.mp4"),
        os.path.join(OUTPUT_DIR, "02_account_takeover.mp4"),
        os.path.join(OUTPUT_DIR, "03_impossible_travel.mp4"),
        os.path.join(OUTPUT_DIR, "04_unusual_amount_otp.mp4"),
        os.path.join(OUTPUT_DIR, "05_velocity_burst.mp4"),
        os.path.join(OUTPUT_DIR, "06_card_testing_bot.mp4"),
        os.path.join(OUTPUT_DIR, "07_admin_forensics_rules.mp4"),
    ]

    for f in mp4_files:
        if not os.path.exists(f):
            print(f"Error: Required video file missing: {f}")
            return False

    concat_txt = os.path.join(OUTPUT_DIR, "concat_list.txt")
    with open(concat_txt, "w", encoding="utf-8") as f:
        for vid in mp4_files:
            clean_path = os.path.abspath(vid).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    master_mp4 = os.path.join(OUTPUT_DIR, "00_FULL_DEMO_ALL_SCENARIOS.mp4")
    cmd = [
        ffmpeg_exe, "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        master_mp4
    ]
    subprocess.run(cmd, check=True)
    size_mb = os.path.getsize(master_mp4) / (1024 * 1024)
    print(f"\n🎉 MASTER DEMO VIDEO GENERATED SUCCESSFULLY!")
    print(f"Path: {master_mp4} ({size_mb:.2f} MB)")
    return True

if __name__ == "__main__":
    t0 = time.time()
    record_scenario_7()
    concatenate_all_videos()
    print(f"\n[DONE] Scenario 7 and Master video completed in {time.time() - t0:.1f}s")
