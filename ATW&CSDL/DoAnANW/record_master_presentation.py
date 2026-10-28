import os, sys, time, subprocess, imageio_ffmpeg
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

OUTPUT_DIR = "demo_videos"
WEBM_DIR = os.path.join(OUTPUT_DIR, "raw_webm", "presentation")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WEBM_DIR, exist_ok=True)
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

from demo_common import HUD_INJECTION_JS, transcode_to_mp4

def record_full_presentation():
    print("\n==================================================================")
    print(" BẮT ĐẦU QUAY VIDEO DEMO TOÀN DIỆN HỆ THỐNG FRAUD DETECTION SYSTEM")
    print(" (Bao gồm: Giao diện User, Các Kịch bản Tấn công, Biện pháp Khắc phục Client & Trang Admin SOC)")
    print("==================================================================\n")

    mp4_out = os.path.join(OUTPUT_DIR, "00_FULL_DEMO_ALL_SCENARIOS.mp4")

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=WEBM_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        page.goto("http://127.0.0.1:8000")
        page.wait_for_timeout(1000)

        # Unlock and login as customer Thinh
        page.evaluate("""async () => {
            await fetch('/api/user/emergency-unlock', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'});
            await quickLogin('thinh', false);
            showView('store');
        }""")
        page.wait_for_timeout(1000)
        page.evaluate(HUD_INJECTION_JS)

        # -------------------------------------------------------------
        # PHẦN 1: GIỚI THIỆU GIAO DIỆN NGƯỜI DÙNG & CỬA HÀNG (STOREFRONT)
        # -------------------------------------------------------------
        print("-> Đang quay: Phần 1 - Giới thiệu giao diện Người dùng (Storefront & Mua sắm)...")
        page.evaluate("""() => {
            window.updateDemoHUD(
                'PHẦN 1: GIAO DIỆN NGƯỜI DÙNG',
                'linear-gradient(135deg, #0ea5e9, #0284c7)',
                'TỔNG QUAN HỆ THỐNG THƯƠNG MẠI ĐIỆN TỬ & CỔNG THANH TOÁN',
                'Khách hàng Thịnh (User) đăng nhập, trải nghiệm mua sắm trên sàn thương mại điện tử',
                '• Giao diện hiển thị danh mục sản phẩm công nghệ cao, giỏ hàng trực tuyến và thông tin khách hàng chính chủ (Hà Nội).<br>• Tích hợp hệ sinh thái bảo vệ thanh toán tự động thời gian thực (Real-time Fraud Prevention Engine).'
            );
            window.moveDemoCursor(960, 400);
        }""")
        page.wait_for_timeout(3500)

        # Bấm chọn sản phẩm đầu tiên để mở Checkout Form
        page.evaluate("""() => {
            window.updateDemoHUD(
                'PHẦN 1: GIAO DIỆN NGƯỜI DÙNG',
                'linear-gradient(135deg, #0ea5e9, #0284c7)',
                'CỔNG THANH TOÁN & GIẢ LẬP ĐIỆN THOẠI SMS BẢO MẬT',
                'Khám phá Form thanh toán, các trường kiểm soát rủi ro và màn hình SMS ảo',
                '• Form thanh toán gồm: Thông tin cá nhân, Số tiền, Phương thức thanh toán (VISA/ATM), IP và Thiết bị.<br>• Tích hợp màn hình <b>Điện Thoại Ảo SMS</b> nhận mã xác thực OTP 2FA và cảnh báo xâm nhập thời gian thực.'
            );
            buyNow(allProducts[0].id);
            window.moveDemoCursor(650, 480);
        }""")
        page.wait_for_timeout(4000)

        # -------------------------------------------------------------
        # KỊCH BẢN 1: GIAO DỊCH HỢP LỆ (LEGITIMATE)
        # -------------------------------------------------------------
        print("-> Đang quay: Kịch bản 1 - Giao dịch hợp lệ...")
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 1: GIAO DỊCH HỢP LỆ',
                'linear-gradient(135deg, #10b981, #059669)',
                'BƯỚC 1/2: NẠP DỮ LIỆU ĐƠN HÀNG THƯỜNG',
                'Khách hàng Thịnh thanh toán đơn hàng 500.000đ từ thiết bị và vị trí quen thuộc',
                '• Hồ sơ: IP <b>113.161.44.12 (Hà Nội)</b>, thiết bị quen thuộc <b>Windows PC Chrome</b>, thẻ <b>VISA</b>.'
            );
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'legit\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('legit');
        }""")
        page.wait_for_timeout(2000)

        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 1: GIAO DỊCH HỢP LỆ',
                'linear-gradient(135deg, #10b981, #059669)',
                'BƯỚC 2/2: AI QUÉT ĐA CHỈ SỐ & PHÊ DUYỆT TỨC THÌ',
                'Giao dịch được phê duyệt tự động (APPROVE) - Không làm gián đoạn trải nghiệm',
                '• Điểm rủi ro: <b style=\"color:#34d399;\">0/100 (LOW RISK)</b> | Vi phạm: <b style=\"color:#34d399;\">0 luật</b>.<br>• Khách hàng tin cậy được thanh toán ngay lập tức (Frictionless Experience).'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(3500)
        page.evaluate("closeResultModal();")
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # KỊCH BẢN 2: CHIẾM ĐOẠT TÀI KHOẢN (ATO) & KHẮC PHỤC CLIENT
        # -------------------------------------------------------------
        print("-> Đang quay: Kịch bản 2 - Chiếm đoạt tài khoản (ATO) & Biện pháp khắc phục Client...")
        page.evaluate("""() => {
            buyNow(allProducts[0].id);
            window.updateDemoHUD(
                'KỊCH BẢN 2: CHIẾM ĐOẠT TÀI KHOẢN (ATO)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 1/3: KẺ GIAN ĐỘT NHẬP VỚI THIẾT BỊ HACKER & IP PROXY',
                'Hacker dùng Kali Linux từ IP Tokyo đặt mua đơn hàng lớn 45.000.000đ',
                '• Thông số tấn công: IP <b>185.220.101.5 (Tokyo Tor/Proxy)</b>, Thiết bị lạ <b>Kali Linux</b>, Giá trị vọt gấp 90 lần.'
            );
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'ato\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('ato');
        }""")
        page.wait_for_timeout(2200)

        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 2: CHIẾM ĐOẠT TÀI KHOẢN (ATO)',
                'linear-gradient(135deg, #ef4444, #b91c1c)',
                'BƯỚC 2/3: HỆ THỐNG RA QUYẾT ĐỊNH CHẶN ĐỨNG (BLOCK)',
                'AI chấm điểm tối đa 100/100 (CRITICAL) - Ngăn chặn thiệt hại 45 triệu đồng',
                '• Vi phạm 4 luật: <i>RULE_ATO_NEW_DEVICE, TOR_PROXY_IP, IMPOSSIBLE_TRAVEL, SPIKE_AMOUNT</i>.<br>• Điện thoại ảo bên phải lập tức nhận <b>SMS Cảnh báo Đỏ khẩn cấp</b> gửi đến chủ tài khoản.'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(3500)

        # Biện pháp khắc phục Client: Bấm Khóa khẩn cấp & Mở khóa an toàn
        page.evaluate("""() => {
            window.updateDemoHUD(
                'BIỆN PHÁP KHẮC PHỤC Ở CLIENT: ATO',
                'linear-gradient(135deg, #ef4444, #7f1d1d)',
                'BƯỚC 3/3: KHÓA KHẨN CẤP & CƠ CHẾ BẢO VỆ CHÍNH CHỦ',
                'Người dùng nhấn nút Khóa Tài Khoản 30 phút hoặc dùng cơ chế Mở khóa an toàn',
                '• Client cung cấp nút <b>\"Khóa Khẩn Cấp Tài Khoản\"</b> đóng băng ví ngay lập tức.<br>• Khi chủ tài khoản xác minh danh tính, hệ thống hỗ trợ khôi phục an toàn qua cơ chế Emergency Unlock.'
            );
            const lockBtn = document.getElementById('btn-emergency-lock');
            if (lockBtn) {
                const rect = lockBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
        }""")
        page.wait_for_timeout(2500)
        page.evaluate("""async () => {
            closeResultModal();
            // Client remediation: unfreeze account for next tests
            await fetch('/api/user/emergency-unlock', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: '{}'});
            await quickLogin('thinh', false);
        }""")
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # KỊCH BẢN 3: DI CHUYỂN BẤT KHẢ THI (IMPOSSIBLE TRAVEL)
        # -------------------------------------------------------------
        print("-> Đang quay: Kịch bản 3 - Di chuyển bất khả thi...")
        page.evaluate("""() => {
            buyNow(allProducts[0].id);
            window.updateDemoHUD(
                'KỊCH BẢN 3: DI CHUYỂN BẤT KHẢ THI',
                'linear-gradient(135deg, #a855f7, #7e22ce)',
                'BƯỚC 1/2: PHÁT HIỆN KHOẢNG CÁCH ĐỊA LÝ PHI LÝ',
                'Vừa giao dịch tại Hà Nội, 5 phút sau xuất hiện đơn hàng mới từ London (Anh Quốc)',
                '• Khoảng cách tính toán: <b>9.200 km</b> | Thời gian chênh lệch: <b>< 5 phút</b>.<br>• Vận tốc ước tính vượt <b>100.000 km/h</b> (Vượt xa giới hạn vật lý của máy bay siêu thanh).'
            );
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'travel\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('travel');
        }""")
        page.wait_for_timeout(2200)

        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 3: DI CHUYỂN BẤT KHẢ THI',
                'linear-gradient(135deg, #a855f7, #7e22ce)',
                'BƯỚC 2/2: ĐỘNG CƠ HAVERSINE KÍCH HOẠT CHẶN (BLOCK)',
                'Quyết định: BLOCK (Điểm rủi ro: 82/100 CRITICAL) - Ngăn ngừa chia sẻ tài khoản hoặc VPN gian lận',
                '• Định luật Haversine Great-Circle phát hiện tốc độ dịch chuyển phi lý.<br>• Giao dịch bị từ chối bảo vệ an toàn hạn mức của thẻ.'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(3500)
        page.evaluate("closeResultModal();")
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # KỊCH BẢN 4: ĐỘT BIẾN SỐ TIỀN & XÁC THỰC BƯỚC NHẢY (STEP-UP 2FA OTP)
        # -------------------------------------------------------------
        print("-> Đang quay: Kịch bản 4 - Đột biến số tiền & Xác thực OTP ở Client...")
        page.evaluate("""() => {
            buyNow(allProducts[0].id);
            window.updateDemoHUD(
                'KỊCH BẢN 4: ĐỘT BIẾN SỐ TIỀN & OTP',
                'linear-gradient(135deg, #eab308, #ca8a04)',
                'BƯỚC 1/3: ĐƠN HÀNG 68.000.000đ GẤP 50 LẦN LỊCH SỬ',
                'Thiết bị chính chủ nhưng giá trị đơn tăng đột ngột -> Hệ thống đưa vào diện REVIEW',
                '• Không chặn cực đoan làm mất khách VIP, AI kích hoạt cơ chế <b>Step-up 2FA Challenge</b>.'
            );
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'high_amount\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('high_amount');
        }""")
        page.wait_for_timeout(2200)

        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 4: ĐỘT BIẾN SỐ TIỀN & OTP',
                'linear-gradient(135deg, #eab308, #ca8a04)',
                'BƯỚC 2/3: MÃ SMART OTP 6 SỐ TỰ ĐỘNG GỬI ĐẾN ĐIỆN THOẠI SMS',
                'Màn hình SMS ảo nhận mã OTP bảo mật -> Yêu cầu người dùng xác thực',
                '• Điểm rủi ro: <b>52/100 (MEDIUM)</b> | Quyết định: <b>REVIEW</b>.<br>• Phía Client xuất hiện ô nhập mã OTP cùng hướng dẫn chi tiết.'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(2800)

        # Biện pháp khắc phục Client: Điền OTP và Xác thực thành công
        page.evaluate("""() => {
            window.updateDemoHUD(
                'BIỆN PHÁP KHẮC PHỤC Ở CLIENT: STEP-UP 2FA OTP',
                'linear-gradient(135deg, #10b981, #059669)',
                'BƯỚC 3/3: NGƯỜI DÙNG NHẬP MÃ OTP VÀ ĐƯỢC DUYỆT (APPROVED)',
                'Bấm \"Điền nhanh OTP\" từ tin nhắn SMS và nhấn \"Xác thực OTP\"',
                '• Khách hàng chứng minh được mình là chính chủ sở hữu SIM điện thoại.<br>• Đơn hàng lập tức được chuyển sang: <b style=\"color:#34d399;\">APPROVED</b> thành công tốt đẹp!'
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
        page.wait_for_timeout(3500)
        page.evaluate("closeResultModal();")
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # KỊCH BẢN 5: BÙNG NỔ TẦN SUẤT (VELOCITY BURST)
        # -------------------------------------------------------------
        print("-> Đang quay: Kịch bản 5 - Bùng nổ tần suất & Cơ chế Cooldown...")
        page.evaluate("""() => {
            buyNow(allProducts[0].id);
            window.updateDemoHUD(
                'KỊCH BẢN 5: BÙNG NỔ TẦN SUẤT (VELOCITY)',
                'linear-gradient(135deg, #f59e0b, #d97706)',
                'BƯỚC 1/2: PHÁT HIỆN ĐẶT ĐƠN DỒN DẬP TRONG THỜI GIAN NGẮN',
                'Người dùng hoặc script đặt hàng liên tục nhiều lần trong vòng dưới 1 phút',
                '• Vi phạm cơ chế Sliding Window Rate Limit (> 3 đơn / 5 phút) -> Điểm rủi ro: <b>70/100</b>.'
            );
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'velocity\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('velocity');
        }""")
        page.wait_for_timeout(2000)

        page.evaluate("""() => {
            window.updateDemoHUD(
                'BIỆN PHÁP KHẮC PHỤC Ở CLIENT: COOLDOWN & THROTTLING',
                'linear-gradient(135deg, #f59e0b, #d97706)',
                'BƯỚC 2/2: HỆ THỐNG YÊU CẦU HẠ NHIỆT (COOLDOWN)',
                'Quyết định: REVIEW - Client hiển thị khuyến nghị giãn cách giao dịch',
                '• Biện pháp ở Client: Người dùng chờ 1-2 phút để cửa sổ trượt hạ nhiệt trước khi gửi đơn tiếp.<br>• Giúp chống lại tấn công vét cạn và sự cố click nhầm nhiều lần.'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(3500)
        page.evaluate("closeResultModal();")
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # KỊCH BẢN 6: BOT THỬ THẺ TỰ ĐỘNG (CARD TESTING BOTNET)
        # -------------------------------------------------------------
        print("-> Đang quay: Kịch bản 6 - Bot thử thẻ tự động...")
        page.evaluate("""() => {
            buyNow(allProducts[0].id);
            window.updateDemoHUD(
                'KỊCH BẢN 6: BOT THỬ THẺ TỰ ĐỘNG',
                'linear-gradient(135deg, #ef4444, #991b1b)',
                'BƯỚC 1/2: PHÁT HIỆN BOTNET QUÉT ĐƠN HÀNG VI MÔ (99.000đ)',
                'Kẻ gian dùng bot tự động đổi số thẻ (JCB, Visa) thử hạn mức bằng đơn giá trị nhỏ',
                '• Thiết bị: <b>device_bot_tester_01</b> | Thẻ: <b>JCB</b> | Giá trị: <b>99.000đ</b>.'
            );
            const btn = document.querySelector('button[onclick*=\"setPreset(\\\'card_testing\\\')\"]');
            if (btn) {
                const rect = btn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            setPreset('card_testing');
        }""")
        page.wait_for_timeout(2000)

        page.evaluate("""() => {
            window.updateDemoHUD(
                'KỊCH BẢN 6: BOT THỬ THẺ TỰ ĐỘNG',
                'linear-gradient(135deg, #ef4444, #991b1b)',
                'BƯỚC 2/2: CHẶN ĐỨNG BOTNET VÀ ĐƯA VÀO DANH SÁCH ĐEN',
                'Quyết định: BLOCK (Điểm rủi ro: 100/100 CRITICAL) - Bảo vệ cổng thanh toán',
                '• Vi phạm luật: <i>RULE_CARD_TESTING_MICRO_TX, BOTNET_FINGERPRINT</i>.<br>• Biện pháp: Khóa thẻ, từ chối bot và yêu cầu chuyển sang phương thức thanh toán an toàn.'
            );
            const submitBtn = document.getElementById('checkout-submit-btn');
            if (submitBtn) {
                const rect = submitBtn.getBoundingClientRect();
                window.moveDemoCursor(rect.left + rect.width / 2, rect.top + rect.height / 2);
                window.triggerCursorClick(rect.left + rect.width / 2, rect.top + rect.height / 2);
            }
            document.getElementById('checkout-form').requestSubmit();
        }""")
        page.wait_for_timeout(3500)
        page.evaluate("closeResultModal();")
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # PHẦN QUẢN TRỊ VIÊN: TRUNG TÂM GIÁM SÁT SOC (ADMIN DASHBOARD)
        # -------------------------------------------------------------
        print("-> Đang quay: Phần Quản trị viên - 5 Phân hệ Giám sát SOC...")
        page.evaluate("""async () => {
            await quickLogin('admin', false);
            showView('admin');
            switchAdminTab('dashboard');
        }""")
        page.wait_for_timeout(1000)

        # Tab 1: Dashboard KPI & Biểu đồ
        page.evaluate("""() => {
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN SOC: BẢNG ĐIỀU KHIỂN',
                'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                'PHÂN HỆ 1/5: THEO DÕI THỜI GIAN THỰC & CHỈ SỐ KPI',
                'Trung tâm giám sát toàn diện hoạt động phòng chống gian lận thương mại',
                '• Cung cấp 6 thẻ KPI: Tổng đơn, Tỉ lệ duyệt (Approve), Chờ (Review), Chặn (Block), Điểm rủi ro trung bình, Tỷ lệ gian lận.<br>• 2 Biểu đồ phân tích: Phân bổ rủi ro (Risk Distribution) & Tỉ lệ phân loại quyết định.'
            );
            window.moveDemoCursor(650, 320);
        }""")
        page.wait_for_timeout(4000)

        # Tab 2: Transactions & Forensics (Radar Chart & IP Map)
        page.evaluate("""() => {
            switchAdminTab('transactions');
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN SOC: PHÁP Y GIAO DỊCH (FORENSICS)',
                'linear-gradient(135deg, #8b5cf6, #6d28d9)',
                'PHÂN HỆ 2/5: TRUY VẾT CHI TIẾT & BIỂU ĐỒ RADAR 5 CHIỀU',
                'Điều tra sâu từng giao dịch với Biểu đồ Radar 5 khía cạnh và Bản đồ định vị IP',
                '• Chuyên viên an ninh xem xét 5 trục rủi ro: Địa lý, Thiết bị, Vận tốc, Tần suất, Giá trị đơn hàng.<br>• Định vị tọa độ địa lý IP trên bản đồ toàn cầu nhằm phát hiện nguồn gốc tấn công.'
            );
            window.moveDemoCursor(960, 420);
        }""")
        page.wait_for_timeout(4500)

        # Tab 3: Simulation (Mô phỏng tấn công)
        page.evaluate("""() => {
            switchAdminTab('simulation');
            runSimulation('ATO');
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN SOC: MÔ PHỎNG TẤN CÔNG',
                'linear-gradient(135deg, #f97316, #c2410c)',
                'PHÂN HỆ 3/5: KIỂM THỬ ĐỘNG CƠ VỚI CÁC KỊCH BẢN GIẢ LẬP',
                'Kiểm tra khả năng phản ứng của AI với các kịch bản tấn công nguy hiểm',
                '• Giả lập các cuộc tấn công ATO, Impossible Travel, Bot Testing.<br>• Quan sát điểm số rủi ro, thanh đo Score Bar và các Composite Rules được kích hoạt tức thì.'
            );
            window.moveDemoCursor(800, 380);
        }""")
        page.wait_for_timeout(4000)

        # Tab 4: Rules Engine (Quản trị luật động)
        page.evaluate("""() => {
            switchAdminTab('rules');
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN SOC: QUẢN TRỊ LUẬT ĐỘNG',
                'linear-gradient(135deg, #14b8a6, #0f766e)',
                'PHÂN HỆ 4/5: CẤU HÌNH LUẬT THỜI GIAN THỰC (ZERO-DOWNTIME)',
                'Bật/Tắt (Toggle Switch) và điều chỉnh trọng số luật mà không cần restart server',
                '• Cho phép các chuyên gia an ninh điều chỉnh linh hoạt chính sách phòng ngừa theo tình hình thực tế.<br>• Cơ chế cập nhật luật động đảm bảo hệ thống luôn sẵn sàng 24/7.'
            );
            window.moveDemoCursor(950, 420);
        }""")
        page.wait_for_timeout(4000)

        # Tab 5: Evaluation & ROC-AUC Benchmark
        page.evaluate("""() => {
            switchAdminTab('evaluation');
            window.updateDemoHUD(
                'QUẢN TRỊ VIÊN SOC: ĐÁNH GIÁ MÔ HÌNH AI',
                'linear-gradient(135deg, #ec4899, #be185d)',
                'PHÂN HỆ 5/5: ĐO LƯỜNG HIỆU NĂNG MACHINE LEARNING & ROC-AUC',
                'Đo lường độ chuẩn xác với ma trận Accuracy, Precision, Recall và F1-Score',
                '• Đảm bảo tỷ lệ phát hiện gian lận đạt mức tối đa (>98%) đồng thời hạn chế tối thiểu báo động giả (False Positive).<br>• Khẳng định tính hiệu quả và độ tin cậy vượt trội của mô hình học máy.'
            );
            window.moveDemoCursor(960, 400);
        }""")
        page.wait_for_timeout(4500)

        # Tổng kết toàn bộ
        page.evaluate("""() => {
            window.updateDemoHUD(
                'KẾT LUẬN TỔNG THỂ HỆ THỐNG',
                'linear-gradient(135deg, #10b981, #047857)',
                'HỆ THỐNG PHÁT HIỆN & PHÒNG CHỐNG GIAN LẬN TOÀN DIỆN',
                'Bảo Vệ Đa Lớp: AI Học Máy + Luật Heuristic + Thẩm Định Tức Thời + Trung Tâm SOC Hiện Đại',
                '• Kết hợp mượt mà giữa trải nghiệm khách hàng và an toàn thông tin mức doanh nghiệp.<br>• Hoàn thành trọn vẹn kịch bản demo hệ thống phòng chống gian lận thanh toán trực tuyến.'
            );
            window.moveDemoCursor(960, 540);
        }""")
        page.wait_for_timeout(4500)

        context.close()
        raw_webm = page.video.path()
        browser.close()

    print(f"\n-> Đang chuyển đổi định dạng sang MP4 Full HD 1080p: {mp4_out} ...")
    transcode_to_mp4(raw_webm, mp4_out)
    print("\n✅ HOÀN TẤT THÀNH CÔNG QUAY VIDEO DEMO CHÍNH!")

if __name__ == "__main__":
    record_full_presentation()
