const express = require('express');
const session = require('express-session');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;

// Middleware phân tích dữ liệu body
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Cấu hình Session để quản lý phiên đăng nhập
app.use(
  session({
    secret: 'fullstack-auth-secret-key-2026',
    resave: false,
    saveUninitialized: false,
    cookie: {
      httpOnly: true,
      maxAge: 24 * 60 * 60 * 1000 // 1 ngày
    }
  })
);

// Phục vụ các file tĩnh (HTML, CSS, JS frontend)
app.use(express.static(path.join(__dirname, 'public')));

// Tài khoản mẫu
const VALID_CREDENTIALS = {
  username: 'admin',
  password: '12345'
};

// API: Kiểm tra trạng thái đăng nhập hiện tại
app.get('/api/me', (req, res) => {
  if (req.session && req.session.user) {
    return res.status(200).json({
      authenticated: true,
      user: req.session.user
    });
  }
  return res.status(200).json({
    authenticated: false,
    user: null
  });
});

// API: Đăng nhập
app.post('/api/login', (req, res) => {
  const { username, password } = req.body;

  // 1. Kiểm tra validation phía backend
  if (!username || !password) {
    return res.status(400).json({
      success: false,
      message: 'Vui lòng cung cấp đầy đủ tên đăng nhập và mật khẩu!'
    });
  }

  const cleanUsername = String(username).trim();
  const cleanPassword = String(password).trim();

  if (cleanUsername.length < 3) {
    return res.status(400).json({
      success: false,
      message: 'Tên đăng nhập phải có ít nhất 3 ký tự!'
    });
  }

  // 2. Kiểm tra thông tin xác thực
  if (
    cleanUsername === VALID_CREDENTIALS.username &&
    cleanPassword === VALID_CREDENTIALS.password
  ) {
    // Lưu phiên đăng nhập vào session
    req.session.user = {
      username: cleanUsername,
      role: 'Quản trị viên (Administrator)',
      loginAt: new Date().toISOString()
    };

    return res.status(200).json({
      success: true,
      message: 'Đăng nhập thành công! Chào mừng ' + cleanUsername + '.',
      user: req.session.user
    });
  }

  // 3. Đăng nhập thất bại
  return res.status(401).json({
    success: false,
    message: 'Tên đăng nhập hoặc mật khẩu không chính xác!'
  });
});

// API: Đăng xuất
app.post('/api/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({
        success: false,
        message: 'Lỗi khi đăng xuất, vui lòng thử lại!'
      });
    }
    res.clearCookie('connect.sid');
    return res.status(200).json({
      success: true,
      message: 'Đăng xuất thành công!'
    });
  });
});

// Khởi động server
app.listen(PORT, () => {
  console.log(`Server đang chạy tại: http://localhost:${PORT}`);
});
