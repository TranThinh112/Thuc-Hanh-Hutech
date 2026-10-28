import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
from demo_common import OUTPUT_DIR, WEBM_DIR, HUD_INJECTION_JS, transcode_to_mp4, reset_user

# =========================================================================
# SCENARIO 1: GIAO DỊCH HỢP LỆ (LEGITIMATE)
# =========================================================================
def record_scenario_1():
    print("\n[1/7] Recording Scenario 1: Giao Dịch Hợp Lệ (Legitimate)...")
    webm_dir = os.path.join(WEBM_DIR, "s1")
    os.makedirs(webm_dir, exist_ok=True)
    mp4_out = os.path.join(OUTPUT_DIR, "01_legit_transaction.mp4")

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
                'KỊCH BẢN 1: HỢP LỆ (LEGITIMATE)',
                'linear-gradient(135deg, #10b981, #059669)',
                'BƯỚC 1/3: KHÁCH HÀNG THỰC HIỆN MUA SẮM',
                'Khách hàng Thịnh (User) mua hàng từ thiết bị & địa chỉ IP quen thuộc',
                'Hồ sơ người dùng: IP <b style=\"color:#38bdf8;\">113.161.44.12 (Hà Nội)</b> | Thiết bị: <b style=\"color:#38bdf8;\">Windows PC Chrome</b>. Lịch sử chi tiêu đều đặn và uy tín.'
            );
            window.moveDemoCursor(960, 480);
        }""")
        page.wait_for_timeout(2600)

        # Stage 2: Open Checkout & Select Legit
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 1: HỢP LỆ (LEGITIMATE)',
                'linear-gradient(135deg, #10b981, #059669)',
                'BƯỚC 2/3: NẠP THÔNG TIN THANH TOÁN',
                'Chọn kịch bản Hợp Lệ: Đơn hàng 500.000 VND - Thẻ Visa quen thuộc',
                'Số tiền trong ngưỡng cho phép, vị trí địa lý hoàn toàn trùng khớp vị trí đăng nhập lần gần nhất.'
            );
            openCheckoutModal();
        }""")
        page.wait_for_timeout(1000)

        page.evaluate("""() => {
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'legit\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('legit');
        }""")
        page.wait_for_timeout(1800)

        # Stage 3: Submit Order
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 1: HỢP LỆ (LEGITIMATE)',
                'linear-gradient(135deg, #10b981, #059669)',
                'BƯỚC 3/3: ĐỐI SOÁT & PHÊ DUYỆT TỰ ĐỘNG',
                'Bấm Xác Nhận Thanh Toán -> Kích hoạt Real-time Fraud Engine',
                'Hệ thống AI & Rule Engine quét song song 15 chỉ số rủi ro trong < 50ms...'
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
                'KẾT QUẢ: PHÊ DUYỆT (APPROVE)',
                'linear-gradient(135deg, #10b981, #059669)',
                'ĐIỂM RỦI RO: 0/100 (LOW RISK)',
                'Đơn hàng được duyệt tự động ngay lập tức - Trải nghiệm thanh toán mượt mà!',
                '• Trạng thái: <b style=\"color:#34d399;\">APPROVED</b> | Vi phạm: <b style=\"color:#34d399;\">0 luật</b> | Điểm rủi ro: <b style=\"color:#34d399;\">0/100</b>.<br>• Khách hàng tin cậy không bị gián đoạn hay phải xác thực rườm rà.'
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
# SCENARIO 2: CHIẾM ĐOẠT TÀI KHOẢN (ACCOUNT TAKEOVER - ATO)
# =========================================================================
def record_scenario_2():
    print("\n[2/7] Recording Scenario 2: Chiếm Đoạt Tài Khoản (ATO)...")
    webm_dir = os.path.join(WEBM_DIR, "s2")
    os.makedirs(webm_dir, exist_ok=True)
    mp4_out = os.path.join(OUTPUT_DIR, "02_account_takeover.mp4")

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
                'KỊCH BẢN 2: CHIẾM ĐOẠT TÀI KHOẢN (ATO)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 1/3: KẺ GIAN ĐỘT NHẬP TÀI KHOẢN',
                'Kẻ xấu chiếm đoạt phiên làm việc và thực hiện thanh toán rút cạn tiền',
                'Hacker sử dụng mạng ẩn danh <b style=\"color:#f87171;\">Tor/Proxy</b>, thiết bị tấn công <b style=\"color:#f87171;\">Kali Linux</b>, đặt đơn hàng trị giá tới <b style=\"color:#f87171;\">45.000.000 VND</b>.'
            );
            window.moveDemoCursor(960, 480);
        }""")
        page.wait_for_timeout(2800)

        # Stage 2: Open Checkout & Choose ATO Preset
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 2: CHIẾM ĐOẠT TÀI KHOẢN (ATO)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 2/3: NẠP THÔNG SỐ TẤN CÔNG (ATO)',
                'Nạp kịch bản: IP Tokyo (150.249.195.10) - Thiết bị lạ - Số tiền vọt gấp 90 lần',
                'Các chỉ số vi phạm nghiêm trọng: New Unknown Device, Anonymous Tor IP, Impossible Velocity & Amount Spike.'
            );
            openCheckoutModal();
        }""")
        page.wait_for_timeout(1000)

        page.evaluate("""() => {
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'ato\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('ato');
        }""")
        page.wait_for_timeout(1800)

        # Stage 3: Submit Order
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 2: CHIẾM ĐOẠT TÀI KHOẢN (ATO)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 3/3: KÍCH HOẠT CƠ CHẾ PHÒNG THỦ KHẨN CẤP',
                'Bấm Xác Nhận Thanh Toán -> AI phát hiện đa chỉ số nguy hiểm',
                'Động cơ chống gian lận lập tức phát hiện sự bất thường nghiêm trọng và kích hoạt cơ chế khóa bảo vệ.'
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
                'Giao Dịch Bị Chặn Đứng Tức Thì - Bảo Vệ Toàn Bộ 45 Triệu Đồng Cho Nạn Nhân',
                '• Vi phạm 4 quy tắc trọng yếu: <b style=\"color:#f87171;\">RULE_ATO_NEW_DEVICE_HIGH_AMOUNT, TOR_PROXY_IP, IMPOSSIBLE_TRAVEL</b>.<br>• Kích hoạt tin nhắn cảnh báo SMS khẩn cấp tới số điện thoại chủ thẻ và cho phép khóa tài khoản 30 phút.'
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
# SCENARIO 3: DI CHUYỂN BẤT KHẢ THI (IMPOSSIBLE TRAVEL)
# =========================================================================
def record_scenario_3():
    print("\n[3/7] Recording Scenario 3: Di Chuyển Bất KhẢ Thi (Impossible Travel)...")
    webm_dir = os.path.join(WEBM_DIR, "s3")
    os.makedirs(webm_dir, exist_ok=True)
    mp4_out = os.path.join(OUTPUT_DIR, "03_impossible_travel.mp4")

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
                'KỊCH BẢN 3: DI CHUYỂN BẤT KHẢ THI (IMPOSSIBLE TRAVEL)',
                'linear-gradient(135deg, #f97316, #c2410c)',
                'BƯỚC 1/3: PHÁT HIỆN BẤT THƯỜNG VỀ VỊ TRÍ ĐỊA LÝ',
                'Người dùng vừa đăng nhập ở Hà Nội, 5 phút sau có giao dịch từ London!',
                'Khoảng cách giữa Hà Nội và London là <b style=\"color:#fb923c;\">~9.200 km</b>. Để đi hết khoảng cách này trong 5 phút, vận tốc yêu cầu vượt <b style=\"color:#fb923c;\">100.000 km/h</b> (bất khả thi về mặt vật lý).'
            );
            window.moveDemoCursor(960, 480);
        }""")
        page.wait_for_timeout(2800)

        # Stage 2: Open Checkout & Choose Travel Preset
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 3: DI CHUYỂN BẤT KHẢ THI (IMPOSSIBLE TRAVEL)',
                'linear-gradient(135deg, #f97316, #c2410c)',
                'BƯỚC 2/3: NẠP DỮ LIỆU IP VƯƠNG QUỐC ANH',
                'Nạp kịch bản: IP 82.165.197.1 (London, UK) - Khoảng cách 9.200km trong 5 phút',
                'Thuật toán khoảng cách cung lớn Haversine (Haversine Great-Circle Distance) tự động đối chiếu tọa độ GPS và thời gian giữa 2 phiên.'
            );
            openCheckoutModal();
        }""")
        page.wait_for_timeout(1000)

        page.evaluate("""() => {
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'travel\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('travel');
        }""")
        page.wait_for_timeout(1800)

        # Stage 3: Submit Order
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 3: DI CHUYỂN BẤT KHẢ THI (IMPOSSIBLE TRAVEL)',
                'linear-gradient(135deg, #f97316, #c2410c)',
                'BƯỚC 3/3: PHÂN TÍCH GIA TỐC VẬN TỐC DI CHUYỂN',
                'Bấm Xác Nhận Thanh Toán -> Kiểm tra trần vận tốc di chuyển hàng không (900 km/h)',
                'Hệ thống so sánh vận tốc tính toán (>100.000 km/h) với ngưỡng trần máy bay thương mại (900 km/h)...'
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
                'ĐIỂM RỦI RO: 82/100 (CRITICAL RISK)',
                'Phát Hiện Dấu Hiệu Sử Dụng Proxy/VPN Quốc Tế Hoặc Chia Sẻ Tài Khoản',
                '• Vi phạm: <b style=\"color:#f87171;\">RULE_IMPOSSIBLE_TRAVEL (Haversine Speed > 900 km/h)</b>.<br>• Ngăn chặn kẻ trộm sử dụng đường truyền VPN vượt biên giới nhằm né tránh kiểm duyệt.'
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
    record_scenario_1()
    record_scenario_2()
    record_scenario_3()
    print(f"\n[DONE] Scenarios 1-3 completed in {time.time() - t0:.1f}s")
