const express = require('express');
const Database = require('better-sqlite3');
const cookieParser = require('cookie-parser');
const path = require('path');

const app = express();
const db = new Database(':memory:');

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cookieParser());

// Khởi tạo CSDL mô phỏng
db.exec(`
  CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT,
    bio TEXT
  );

  INSERT INTO users (username, password, role, bio) VALUES
  ('admin', 'admin123', 'admin', 'Administrator of SecureApp Lab'),
  ('john_doe', 'password123', 'user', 'Regular software developer'),
  ('jane_smith', 'welcome2026', 'user', 'Quality Assurance engineer');

  CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    description TEXT
  );

  INSERT INTO products (name, price, description) VALUES
  ('Laptop Dell XPS 15', 1899.99, 'Ultra-thin laptop with 4K OLED display'),
  ('Mechanical Keyboard', 120.50, 'RGB mechanical keyboard with red switches'),
  ('Wireless Gaming Mouse', 79.99, 'Ergonomic wireless gaming mouse 26k DPI'),
  ('Confidential Security Token', 9999.00, 'INTERNAL COMPANY ACCESS TOKEN - DO NOT DISCLOSE');

  CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author TEXT,
    content TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );

  INSERT INTO feedback (author, content) VALUES
  ('john_doe', 'Website giao diện rất trực quan và dễ sử dụng!'),
  ('jane_smith', 'Mong ứng dụng có thêm tính năng thanh toán trực tuyến.');
`);

// Mock sessions: token -> user object
const sessions = {
  'session_admin_token_xyz': { id: 1, username: 'admin', role: 'admin' },
  'session_john_token_123': { id: 2, username: 'john_doe', role: 'user' }
};

// UI Template Helper
function renderPage(title, body, currentUser = null) {
  return `
  <!DOCTYPE html>
  <html lang="vi">
  <head>
    <meta charset="UTF-8">
    <title>${title} - SecureApp Lab</title>
    <style>
      body { font-family: Segoe UI, Tahoma, Geneva, Verdana, sans-serif; margin: 0; background: #f4f6f9; color: #333; }
      nav { background: #1e293b; color: #fff; padding: 12px 24px; display: flex; justify-content: space-between; align-items: center; }
      nav a { color: #cbd5e1; text-decoration: none; margin-right: 16px; font-weight: 500; }
      nav a:hover { color: #fff; }
      .container { max-width: 960px; margin: 30px auto; background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
      .card { border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; margin-bottom: 16px; background: #fafafa; }
      input, textarea, button { padding: 8px 12px; margin: 6px 0; border: 1px solid #cbd5e1; border-radius: 4px; }
      button { background: #2563eb; color: #fff; border: none; cursor: pointer; }
      button:hover { background: #1d4ed8; }
      .vuln-badge { display: inline-block; background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 4px; font-size: 12px; margin-left: 8px; font-weight: bold; }
      .user-info { font-size: 14px; color: #94a3b8; }
      table { width: 100%; border-collapse: collapse; margin-top: 15px; }
      th, td { border: 1px solid #e2e8f0; padding: 10px; text-align: left; }
      th { background: #f8fafc; }
    </style>
  </head>
  <body>
    <nav>
      <div>
        <a href="/" style="font-size: 18px; font-weight: bold; color: #fff;">🛡️ SecureApp Vulnerable Lab</a>
        <a href="/">Trang chủ</a>
        <a href="/products">Tìm kiếm sản phẩm</a>
        <a href="/feedback">Góp ý (Feedback)</a>
        <a href="/profile?id=1">Hồ sơ người dùng</a>
        <a href="/admin">Trang Quản Trị</a>
      </div>
      <div>
        ${currentUser ? `<span>Xin chào, <b>${currentUser.username}</b> (${currentUser.role})</span> | <a href="/logout">Đăng xuất</a>` : '<a href="/login">Đăng nhập</a>'}
      </div>
    </nav>
    <div class="container">
      ${body}
    </div>
  </body>
  </html>
  `;
}

// Middleware xác thực (Cố tình có lỗ hổng Weak Session / Broken Access Control)
app.use((req, res, next) => {
  const token = req.cookies['auth_token'];
  if (token && sessions[token]) {
    req.user = sessions[token];
  }
  next();
});

// 1. Trang chủ
app.get('/', (req, res) => {
  res.send(renderPage('Trang chủ', `
    <h2>Chào mừng đến với Lab Đánh giá An Toàn Thông Tin Web</h2>
    <p>Ứng dụng này được thiết kế có chủ đích các lỗ hổng theo chuẩn <b>OWASP Top 10</b> để phục vụ bài thực hành:</p>
    <ul>
      <li><b>1. SQL Injection (SQLi):</b> Nằm ở Form Đăng nhập và Tìm kiếm sản phẩm.</li>
      <li><b>2. Cross-Site Scripting (Reflected & Stored XSS):</b> Nằm ở Kết quả Tìm kiếm và Trang Góp ý (Feedback).</li>
      <li><b>3. Broken Authentication:</b> Cơ chế Session Token có thể đoán trước hoặc bypass qua SQLi.</li>
      <li><b>4. Broken Access Control (BOLA/IDOR):</b> Xem hồ sơ người dùng khác tuỳ ý qua <code>/profile?id=X</code>.</li>
      <li><b>5. Broken Access Control (Privilege Escalation):</b> Trang quản trị <code>/admin</code> chỉ kiểm tra client-side hoặc header giả mạo.</li>
    </ul>
    <p>Hãy khởi động Burp Suite / OWASP ZAP và cấu hình proxy tới cổng 3000 để bắt đầu kiểm thử!</p>
  `, req.user));
});

// 2. Chức năng Đăng nhập - LỖ HỔNG: SQL Injection & Broken Authentication
app.get('/login', (req, res) => {
  res.send(renderPage('Đăng nhập', `
    <h2>Đăng nhập tài khoản <span class="vuln-badge">SQLi Vulnerable</span></h2>
    <form method="POST" action="/login">
      <div><label>Tên đăng nhập:</label><br><input type="text" name="username" style="width:300px" required></div>
      <div><label>Mật khẩu:</label><br><input type="password" name="password" style="width:300px" required></div>
      <button type="submit">Đăng nhập</button>
    </form>
    <div style="margin-top:20px; font-size:13px; color:#64748b;">
      <p><i>Gợi ý kiểm thử SQLi:</i> Thử nghiệm chèn <code>admin' --</code> hoặc <code>' OR 1=1 --</code> vào ô đăng nhập.</p>
    </div>
  `, req.user));
});

app.post('/login', (req, res) => {
  const { username, password } = req.body;
  // LỖ HỔNG SQL INJECTION DO NỐI CHUỖI TRỰC TIẾP
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
  try {
    const user = db.prepare(query).get();
    if (user) {
      const token = `session_${user.username}_token_${user.id === 1 ? 'xyz' : '123'}`;
      sessions[token] = user;
      // LỖ HỔNG: Cookie không có cờ HttpOnly, không có Secure, không có SameSite
      res.cookie('auth_token', token);
      res.redirect('/profile?id=' + user.id);
    } else {
      res.send(renderPage('Lỗi đăng nhập', `
        <h3 style="color:red">Đăng nhập thất bại! Sai tên tài khoản hoặc mật khẩu.</h3>
        <p>Query đã thực thi: <code>${query}</code></p>
        <a href="/login">Thử lại</a>
      `, req.user));
    }
  } catch (err) {
    // Trả về chi tiết lỗi SQL -> Error-based SQL Injection disclosure
    res.send(renderPage('Lỗi SQL', `
      <h3 style="color:red">Lỗi SQL Database:</h3>
      <pre style="background:#fee2e2; padding:15px; border-radius:4px;">${err.message}\nQuery: ${query}</pre>
      <a href="/login">Quay lại</a>
    `, req.user));
  }
});

// 3. Tìm kiếm sản phẩm - LỖ HỔNG: Reflected XSS & UNION SQL Injection
app.get('/products', (req, res) => {
  const q = req.query.q || '';
  let items = [];
  let error = null;

  if (q) {
    try {
      // LỖ HỔNG SQL INJECTION
      const query = `SELECT id, name, price, description FROM products WHERE name LIKE '%${q}%'`;
      items = db.prepare(query).all();
    } catch (e) {
      error = e.message;
    }
  } else {
    items = db.prepare(`SELECT id, name, price, description FROM products`).all();
  }

  let rows = items.map(it => `
    <tr>
      <td>${it.id}</td>
      <td><b>${it.name}</b></td>
      <td>$${it.price}</td>
      <td>${it.description}</td>
    </tr>
  `).join('');

  res.send(renderPage('Tìm kiếm sản phẩm', `
    <h2>Danh sách sản phẩm <span class="vuln-badge">SQLi & Reflected XSS</span></h2>
    <form method="GET" action="/products">
      <input type="text" name="q" value="${q}" placeholder="Nhập tên sản phẩm..." style="width:300px">
      <button type="submit">Tìm kiếm</button>
    </form>

    ${q ? `<p>Kết quả tìm kiếm cho: <b>${q}</b></p>` : ''} <!-- LỖ HỔNG REFLECTED XSS (không encode ${q}) -->

    ${error ? `<pre style="background:#fee2e2; padding:10px; color:#b91c1c;">Lỗi SQL: ${error}</pre>` : ''}

    <table>
      <thead>
        <tr><th>ID</th><th>Tên sản phẩm</th><th>Đơn giá</th><th>Mô tả</th></tr>
      </thead>
      <tbody>
        ${rows}
      </tbody>
    </table>
  `, req.user));
});

// 4. Góp ý phản hồi - LỖ HỔNG: Stored XSS
app.get('/feedback', (req, res) => {
  const feedbackList = db.prepare(`SELECT * FROM feedback ORDER BY id DESC`).all();
  const listHtml = feedbackList.map(f => `
    <div class="card">
      <p style="margin:0 0 6px 0;"><b>Tác giả:</b> ${f.author} <small style="color:#64748b">(${f.created_at})</small></p>
      <p style="margin:0;">${f.content}</p> <!-- LỖ HỔNG STORED XSS: In thẳng HTML ra giao diện mà không encode -->
    </div>
  `).join('');

  res.send(renderPage('Góp ý', `
    <h2>Góp ý phản hồi <span class="vuln-badge">Stored XSS</span></h2>
    <form method="POST" action="/feedback">
      <div><label>Họ tên / Nickname:</label><br><input type="text" name="author" style="width:300px" required></div>
      <div><label>Nội dung góp ý:</label><br><textarea name="content" style="width:100%; height:80px;" required></textarea></div>
      <button type="submit">Gửi góp ý</button>
    </form>
    <hr style="margin:25px 0; border:0; border-top:1px solid #e2e8f0;">
    <h3>Danh sách góp ý từ cộng đồng:</h3>
    ${listHtml}
  `, req.user));
});

app.post('/feedback', (req, res) => {
  const { author, content } = req.body;
  // Dữ liệu độc hại được lưu trực tiếp vào CSDL
  db.prepare(`INSERT INTO feedback (author, content) VALUES (?, ?)`).run(author, content);
  res.redirect('/feedback');
});

// 5. Xem hồ sơ người dùng - LỖ HỔNG: IDOR (Insecure Direct Object References)
app.get('/profile', (req, res) => {
  const userId = req.query.id;
  if (!userId) {
    return res.redirect('/login');
  }

  // Không kiểm tra xem người yêu cầu có quyền xem hồ sơ của ID này không
  const profile = db.prepare(`SELECT id, username, role, bio FROM users WHERE id = ?`).get(userId);
  if (!profile) {
    return res.status(404).send(renderPage('Không tìm thấy', '<h3>Không tìm thấy người dùng!</h3>', req.user));
  }

  res.send(renderPage('Hồ sơ cá nhân', `
    <h2>Hồ sơ người dùng <span class="vuln-badge">IDOR / BOLA</span></h2>
    <div class="card">
      <p><b>User ID:</b> ${profile.id}</p>
      <p><b>Username:</b> ${profile.username}</p>
      <p><b>Vai trò (Role):</b> <span style="font-weight:bold; color:#2563eb;">${profile.role}</span></p>
      <p><b>Tiểu sử / Bio bí mật:</b> ${profile.bio}</p>
    </div>
    <p style="font-size:13px; color:#64748b;">Gợi ý IDOR: Thay đổi tham số <code>?id=1</code>, <code>?id=2</code>, <code>?id=3</code> trên thanh địa chỉ để xem toàn bộ thông tin nhạy cảm của người khác.</p>
  `, req.user));
});

// 6. Trang quản trị - LỖ HỔNG: Broken Access Control & Bypass Authorization
app.get('/admin', (req, res) => {
  // Lỗ hổng: Kiểm tra quyền hạn lỏng lẻo chỉ dựa vào cookie hoặc header giả mạo X-Role-Override
  const user = req.user;
  const roleOverride = req.headers['x-role-override'];

  if ((user && user.role === 'admin') || roleOverride === 'admin') {
    const allUsers = db.prepare(`SELECT id, username, password, role FROM users`).all();
    const rows = allUsers.map(u => `
      <tr>
        <td>${u.id}</td>
        <td>${u.username}</td>
        <td><code style="background:#fee2e2; color:#b91c1c; padding:2px 6px;">${u.password}</code> (Lộ Plaintext Password)</td>
        <td>${u.role}</td>
      </tr>
    `).join('');

    return res.send(renderPage('Quản trị hệ thống', `
      <h2>Khu vực Quản Trị Hệ Thống (Admin Panel)</h2>
      <p style="color:green">Quyền truy cập hợp lệ: <b>Administrator</b></p>
      <h3>Bảng quản lý tài khoản và mật khẩu:</h3>
      <table>
        <thead><tr><th>ID</th><th>Username</th><th>Password</th><th>Role</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    `, user));
  }

  return res.status(403).send(renderPage('Bị từ chối', `
    <h2 style="color:red">403 Forbidden - Truy cập bị từ chối</h2>
    <p>Chỉ tài khoản Administrator mới có quyền xem trang này!</p>
    <p><i>Gợi ý Broken Access Control:</i> Thử thêm HTTP Header <code>X-Role-Override: admin</code> vào Burp Suite request để vượt qua bộ lọc quyền.</p>
  `, user));
});

// 7. Đăng xuất
app.get('/logout', (req, res) => {
  res.clearCookie('auth_token');
  res.redirect('/');
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`SecureApp Lab is running at http://localhost:${PORT}`);
});
