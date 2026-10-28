import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up figure
fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis("off")

# Colors
bg_tier1 = "#EBF5FB"  # soft blue
border_tier1 = "#2980B9"
bg_tier2 = "#EAFAF1"  # soft green
border_tier2 = "#27AE60"
bg_tier3 = "#FEF9E7"  # soft yellow/orange
border_tier3 = "#D4AC0D"

# Title
ax.text(6, 6.6, "SƠ ĐỒ KIẾN TRÚC MÔ HÌNH 3 LỚP (3-TIER WEB ARCHITECTURE)", 
        ha="center", va="center", fontsize=15, fontweight="bold", color="#1B2631")
ax.text(6, 6.25, "Ứng dụng xác thực người dùng: the-internet.herokuapp.com/login", 
        ha="center", va="center", fontsize=11, fontstyle="italic", color="#566573")

# Tier 1: Client
box1 = patches.FancyBboxPatch((0.6, 1.2), 3.0, 4.6, boxstyle="round,pad=0.2",
                             ec=border_tier1, fc=bg_tier1, lw=2.5)
ax.add_patch(box1)
ax.text(2.1, 5.5, "TẦNG TRÌNH DIỄN\n(Presentation Tier)", ha="center", va="center", fontsize=11, fontweight="bold", color="#1B4F72")
ax.text(2.1, 4.9, "[ Web Browser - Client ]", ha="center", va="center", fontsize=10, fontweight="bold", color="#2980B9")

client_desc = (
    "• Trình duyệt Chrome / Firefox\n"
    "• HTML5 Form Đăng nhập\n"
    "• CSS3 & JavaScript (JQuery)\n"
    "• Gửi yêu cầu HTTP/HTTPS\n"
    "• Render DOM & Thông báo UI\n"
    "• Quản lý Client-side State\n"
    "  (Cookies / LocalSession)"
)
ax.text(0.9, 3.2, client_desc, ha="left", va="center", fontsize=9, color="#2C3E50", linespacing=1.6)

# Tier 2: Application Server
box2 = patches.FancyBboxPatch((4.5, 1.2), 3.0, 4.6, boxstyle="round,pad=0.2",
                             ec=border_tier2, fc=bg_tier2, lw=2.5)
ax.add_patch(box2)
ax.text(6.0, 5.5, "TẦNG ỨNG DỤNG\n(Application / Logic Tier)", ha="center", va="center", fontsize=11, fontweight="bold", color="#145A32")
ax.text(6.0, 4.9, "[ Backend Web Server ]", ha="center", va="center", fontsize=10, fontweight="bold", color="#27AE60")

server_desc = (
    "• Web Server: Heroku Router\n"
    "• Ruby on Rails / Sinatra App\n"
    "• Tiếp nhận GET /login (Render)\n"
    "• Xử lý POST /authenticate:\n"
    "  - Bóc tách form body\n"
    "  - Xác thực thông tin login\n"
    "  - Thiết lập Session / Cookie\n"
    "  - Trả 303 See Other Redirect"
)
ax.text(4.8, 3.2, server_desc, ha="left", va="center", fontsize=9, color="#2C3E50", linespacing=1.6)

# Tier 3: Database
box3 = patches.FancyBboxPatch((8.4, 1.2), 3.0, 4.6, boxstyle="round,pad=0.2",
                             ec=border_tier3, fc=bg_tier3, lw=2.5)
ax.add_patch(box3)
ax.text(9.9, 5.5, "TẦNG DỮ LIỆU\n(Data Tier)", ha="center", va="center", fontsize=11, fontweight="bold", color="#7D6608")
ax.text(9.9, 4.9, "[ Database & Storage ]", ha="center", va="center", fontsize=10, fontweight="bold", color="#B7950B")

db_desc = (
    "• Hệ quản trị CSDL:\n"
    "  PostgreSQL / MySQL / SQLite\n"
    "• Bảng `users`:\n"
    "  - id, username\n"
    "  - password_hash (Bcrypt)\n"
    "• Bảng `sessions`:\n"
    "  - session_id, user_id\n"
    "• Thực thi truy vấn:\n"
    "  SELECT * FROM users WHERE..."
)
ax.text(8.7, 3.2, db_desc, ha="left", va="center", fontsize=9, color="#2C3E50", linespacing=1.6)

# Arrows between Tier 1 and 2
ax.annotate("", xy=(4.4, 3.8), xytext=(3.7, 3.8),
            arrowprops=dict(arrowstyle="->", lw=2, color="#2980B9"))
ax.text(4.05, 4.05, "1. HTTP Request\n(GET / POST)", ha="center", va="center", fontsize=8, fontweight="bold", color="#1B4F72")

ax.annotate("", xy=(3.7, 2.5), xytext=(4.4, 2.5),
            arrowprops=dict(arrowstyle="->", lw=2, color="#27AE60"))
ax.text(4.05, 2.25, "2. HTTP Response\n(200 OK / 303 Redirect)", ha="center", va="center", fontsize=8, fontweight="bold", color="#145A32")

# Arrows between Tier 2 and 3
ax.annotate("", xy=(8.3, 3.8), xytext=(7.6, 3.8),
            arrowprops=dict(arrowstyle="->", lw=2, color="#27AE60"))
ax.text(7.95, 4.05, "3. Query Auth\n(SQL SELECT)", ha="center", va="center", fontsize=8, fontweight="bold", color="#145A32")

ax.annotate("", xy=(7.6, 2.5), xytext=(8.3, 2.5),
            arrowprops=dict(arrowstyle="->", lw=2, color="#B7950B"))
ax.text(7.95, 2.25, "4. Return Data\n(Hash/Record)", ha="center", va="center", fontsize=8, fontweight="bold", color="#7D6608")

# Attack Surface Note Banner at Bottom
box_att = patches.FancyBboxPatch((0.6, 0.25), 10.8, 0.65, boxstyle="round,pad=0.1",
                                ec="#C0392B", fc="#FDEDEC", lw=1.5)
ax.add_patch(box_att)
ax.text(6.0, 0.58, "⚠️ BỀ MẶT TẤN CÔNG TIÊU BIỂU (ATTACK SURFACE)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#922B21")
ax.text(6.0, 0.38, "Client-side: XSS, Phishing, Tampering | Web App: SQL Injection, Brute-force/Credential Stuffing, CSRF, Insecure Session | DB: Data Exfiltration, Priv Escalation", ha="center", va="center", fontsize=8, color="#78281F")

plt.tight_layout()
plt.savefig("captures/architecture_diagram.png", dpi=300)
print("Saved architecture diagram to captures/architecture_diagram.png")
