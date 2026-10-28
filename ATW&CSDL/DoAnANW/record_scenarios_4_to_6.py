import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
from demo_common import OUTPUT_DIR, WEBM_DIR, HUD_INJECTION_JS, transcode_to_mp4, reset_user

# =========================================================================
# SCENARIO 4: ĐỘT BIẾN SỐ TIỀN & XÁC THỰC BƯỚC NHẢY (STEP-UP 2FA OTP)
# =========================================================================
def record_scenario_4():
    print("\n[4/7] Recording Scenario 4: Đột Biến Số Tiền & Step-up OTP...")
    webm_dir = os.path.join(WEBM_DIR, "s4")
    os.makedirs(webm_dir, exist_ok=True)
    mp4_out = os.path.join(OUTPUT_DIR, "04_unusual_amount_otp.mp4")

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
        reset_user(page)
        page.evaluate(HUD_INJECTION_JS)

        # Stage 1: Context
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 4: ĐỘT BIẾN SỐ TIỀN & 2FA OTP',
                'linear-gradient(135deg, #eab308, #ca8a04)',
                'BƯỚC 1/4: ĐƠN HÀNG GIÁ TRỊ CAO BẤT THƯỜNG',
                'Khách hàng quen thuộc đặt mua đơn hàng tăng vọt 68.000.000 VND',
                'Thiết bị và IP vẫn là <b style=\"color:#facc15;\">chính chủ tại Hà Nội</b>, nhưng giá trị tăng gấp 50 lần so với đơn thông thường. Hệ thống không chặn cực đoan mà đưa vào diện CẦN XÁC MINH (REVIEW).'
            );
            window.moveDemoCursor(960, 480);
        }""")
        page.wait_for_timeout(2800)

        # Stage 2: Open Checkout & Choose High Amount Preset
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 4: ĐỘT BIẾN SỐ TIỀN & 2FA OTP',
                'linear-gradient(135deg, #eab308, #ca8a04)',
                'BƯỚC 2/4: NẠP THÔNG SỐ ĐƠN HÀNG 68 TRIỆU',
                'Nạp kịch bản: Số tiền 68.000.000 VND (Spike Amount) - Thiết bị quen',
                'Hệ thống đánh giá điểm rủi ro ở mức trung bình cao (52/100) và kích hoạt cơ chế Step-up 2FA Challenge.'
            );
            openCheckoutModal();
        }""")
        page.wait_for_timeout(1000)

        page.evaluate("""() => {
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'high_amount\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('high_amount');
        }""")
        page.wait_for_timeout(1800)

        # Stage 3: Submit Order -> Triggers REVIEW & OTP Challenge
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 4: ĐỘT BIẾN SỐ TIỀN & 2FA OTP',
                'linear-gradient(135deg, #eab308, #ca8a04)',
                'BƯỚC 3/4: KÍCH HOẠT THỬ THÁCH BẢO MẬT BƯỚC NHẢY (STEP-UP 2FA)',
                'Hệ thống tự động phát hành mã Smart OTP 6 số gửi qua SMS tới điện thoại chính chủ',
                'Thay vì từ chối đơn hàng của khách VIP, hệ thống yêu cầu xác thực OTP để bảo vệ tài khoản mà vẫn giữ chân khách hàng.'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(2500)

        # Stage 4: Fill OTP and Verify
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 4: ĐỘT BIẾN SỐ TIỀN & 2FA OTP',
                'linear-gradient(135deg, #38bdf8, #0284c7)',
                'BƯỚC 4/4: NGƯỜI DÙNG NHẬP MÃ OTP VÀ XÁC THỰC',
                'Đọc mã OTP từ SMS, tự động điền vào ô và bấm Xác Nhận OTP để hoàn tất đơn hàng',
                'Người dùng kiểm tra tin nhắn SMS bảo mật, xác thực danh tính chính chủ và hoàn tất giao dịch an toàn.'
            );
            fillOtpFromSms();
            const btnVerify = document.getElementById('btn-submit-otp');
            if (btnVerify) {
                const rect = btnVerify.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
        }""")
        page.wait_for_timeout(1000)

        page.evaluate("submitOtpVerification()")
        page.wait_for_timeout(2500)

        # Stage 5: Final Result (APPROVED!)
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KẾT QUẢ: DUYỆT ĐƠN AN TOÀN (APPROVED)',
                'linear-gradient(135deg, #10b981, #059669)',
                'XÁC THỰC 2FA THÀNH CÔNG - GIAO DỊCH 68.000.000đ ĐÃ ĐƯỢC DUYỆT',
                'Cân Bằng Hoàn Hảo Giữa Bảo Mật Khắt Khe & Trải Nghiệm Mua Sắm Khách Hàng',
                '• Đơn hàng chuyển sang: <b style=\"color:#34d399;\">APPROVED</b>.<br>• Giải pháp bảo vệ hữu hiệu ngăn chặn kẻ trộm nhưng không làm mất doanh thu đơn hàng giá trị cao.'
            );
            window.moveDemoCursor(960, 420);
        }""")
        page.wait_for_timeout(3600)

        page.evaluate("closeResultModal()")
        page.wait_for_timeout(800)

        context.close()
        raw_webm = page.video.path()
        browser.close()

    transcode_to_mp4(raw_webm, mp4_out)

# =========================================================================
# SCENARIO 5: BÙNG NỔ TẦN SUẤT GIAO DỊCH (VELOCITY BURST / SPAM)
# =========================================================================
def record_scenario_5():
    print("\n[5/7] Recording Scenario 5: Bùng Nổ Tần Suất Giao Dịch (Velocity Burst)...")
    webm_dir = os.path.join(WEBM_DIR, "s5")
    os.makedirs(webm_dir, exist_ok=True)
    mp4_out = os.path.join(OUTPUT_DIR, "05_velocity_burst.mp4")

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
        reset_user(page)
        page.evaluate(HUD_INJECTION_JS)

        # Stage 1: Context
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 5: BÙNG NỔ TẦN SUẤT (VELOCITY BURST)',
                'linear-gradient(135deg, #a855f7, #7e22ce)',
                'BƯỚC 1/3: MÔ PHỎNG TẤN CÔNG SPAM GIAO DỊCH LIÊN TỤC',
                'Nhiều yêu cầu đặt đơn gửi tới dồn dập chỉ trong vài giây',
                'Hacker hoặc bot tự động cố gắng gửi hàng loạt lệnh thanh toán nhằm vét hàng tồn kho hoặc thử vận may vét mã coupon giảm giá.'
            );
            window.moveDemoCursor(960, 480);
        }""")
        page.wait_for_timeout(2800)

        # Stage 2: Open Checkout & Choose Velocity Preset
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 5: BÙNG NỔ TẦN SUẤT (VELOCITY BURST)',
                'linear-gradient(135deg, #a855f7, #7e22ce)',
                'BƯỚC 2/3: NẠP KỊCH BẢN BÙNG NỔ TẦN SUẤT',
                'Nạp kịch bản: Sliding Window Counter (>3 đơn trong 5 phút)',
                'Bộ đếm cửa sổ trượt (Sliding Window Counter) theo dõi chặt chẽ số lượng đơn hàng phát sinh trên cùng một User ID và IP.'
            );
            openCheckoutModal();
        }""")
        page.wait_for_timeout(1000)

        page.evaluate("""() => {
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'velocity\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('velocity');
        }""")
        page.wait_for_timeout(1800)

        # Stage 3: Submit Order
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 5: BÙNG NỔ TẦN SUẤT (VELOCITY BURST)',
                'linear-gradient(135deg, #a855f7, #7e22ce)',
                'BƯỚC 3/3: PHÁT HIỆN VƯỢT NGƯỠNG RATE-LIMIT',
                'Bấm Xác Nhận Thanh Toán -> Kiểm tra tần suất giao dịch trong cửa sổ thời gian',
                'Động cơ đối chiếu tần suất giao dịch thực tế với hạn mức chính sách bảo mật hệ thống...'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(2200)

        # Stage 4: Result Inspection
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KẾT QUẢ: CẢNH BÁO TẦN SUẤT (REVIEW)',
                'linear-gradient(135deg, #eab308, #ca8a04)',
                'ĐIỂM RỦI RO: 70/100 (HIGH RISK)',
                'Phát Hiện Hành Vi Giao Dịch Dồn Dập Bất Thường - Cần Xác Minh Bước Nhảy',
                '• Vi phạm: <b style=\"color:#facc15;\">RULE_HIGH_VELOCITY_BURST (Sliding Window > 3 req/5m)</b>.<br>• Chặn đứng các hành vi spam bot vét kho flash sale, bảo vệ tài nguyên máy chủ khỏi bị nghẽn (DoS).'
            );
            window.moveDemoCursor(960, 420);
        }""")
        page.wait_for_timeout(4000)

        page.evaluate("closeResultModal()")
        page.wait_for_timeout(800)

        context.close()
        raw_webm = page.video.path()
        browser.close()

    transcode_to_mp4(raw_webm, mp4_out)

# =========================================================================
# SCENARIO 6: THỬ THẺ TỰ ĐỘNG BẰNG BOT (CARD TESTING BOTNET)
# =========================================================================
def record_scenario_6():
    print("\n[6/7] Recording Scenario 6: Thử Thẻ Tự Động Bằng Bot (Card Testing)...")
    webm_dir = os.path.join(WEBM_DIR, "s6")
    os.makedirs(webm_dir, exist_ok=True)
    mp4_out = os.path.join(OUTPUT_DIR, "06_card_testing_bot.mp4")

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
        reset_user(page)
        page.evaluate(HUD_INJECTION_JS)

        # Stage 1: Context
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 6: BOT THỬ THẺ (CARD TESTING)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 1/3: MÔ HÌNH TỘI PHẠM SỬ DỤNG BOTNET DÒ THẺ RỦI RO CAO',
                'Tội phạm dùng bot thử hàng loạt thẻ tín dụng bị lộ dữ liệu trên mạng',
                'Đặc trưng của đòn tấn công: Đơn hàng giá trị rất nhỏ (<100k) để thăm dò hạn mức, sử dụng thẻ quốc tế và công cụ giả lập tự động.'
            );
            window.moveDemoCursor(960, 480);
        }""")
        page.wait_for_timeout(2800)

        # Stage 2: Open Checkout & Choose Card Testing Preset
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 6: BOT THỬ THẺ (CARD TESTING)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 2/3: NẠP DẤU VẾT BOTNET',
                'Nạp kịch bản: Thẻ JCB - Đơn giá 99.000đ - Thiết bị device_bot_tester_01',
                'Hệ thống phân tích dấu vân tay thiết bị (Device Fingerprinting) và nhận diện mẫu hình giao dịch vi mô bất thường.'
            );
            openCheckoutModal();
        }""")
        page.wait_for_timeout(1000)

        page.evaluate("""() => {
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'card_testing\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('card_testing');
        }""")
        page.wait_for_timeout(1800)

        # Stage 3: Submit Order
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 6: BOT THỬ THẺ (CARD TESTING)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 3/3: PHÂN TÍCH CHỮ KÝ BOT & CHẶN ĐỨNG TỨC THÌ',
                'Bấm Xác Nhận Thanh Toán -> AI phát hiện mẫu hình Botnet Card Testing',
                'Khớp mẫu hình chữ ký thiết bị botnet và hành vi thử thẻ hàng loạt của tổ chức tội phạm...'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(2200)

        # Stage 4: Result Inspection
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KẾT QUẢ: CHẶN GIAN LẬN (BLOCK)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'ĐIỂM RỦI RO: 100/100 (CRITICAL RISK)',
                'Chặn Đứng Botnet Thử Thẻ - Miễn Nhiễm Phạt Phí Giao Dịch Rác Từ Tổ Chức Thẻ',
                '• Vi phạm: <b style=\"color:#f87171;\">RULE_CARD_TESTING_BOTNET, UNKNOWN_BOT_DEVICE</b>.<br>• Giúp doanh nghiệp tránh bị Visa/Mastercard phạt phí giao dịch thẻ rác và hạn chế rủi ro bồi hoàn (chargeback).'
            );
            window.moveDemoCursor(960, 420);
        }""")
        page.wait_for_timeout(4000)

        page.evaluate("closeResultModal()")
        page.wait_for_timeout(800)

        context.close()
        raw_webm = page.video.path()
        browser.close()

    transcode_to_mp4(raw_webm, mp4_out)

if __name__ == "__main__":
    t0 = time.time()
    record_scenario_4()
    record_scenario_5()
    record_scenario_6()
    print(f"\n[DONE] Scenarios 4-6 completed in {time.time() - t0:.1f}s")
