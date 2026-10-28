document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const usernameError = document.getElementById('usernameError');
  const passwordError = document.getElementById('passwordError');
  const alertMessage = document.getElementById('alertMessage');
  const alertIcon = document.getElementById('alertIcon');
  const alertText = document.getElementById('alertText');
  const submitBtn = document.getElementById('submitBtn');
  const btnLoader = document.getElementById('btnLoader');
  const togglePasswordBtn = document.getElementById('togglePasswordBtn');
  const eyeIcon = document.getElementById('eyeIcon');

  const loginCard = document.getElementById('loginCard');
  const dashboardCard = document.getElementById('dashboardCard');
  const currentUsername = document.getElementById('currentUsername');
  const currentUserRole = document.getElementById('currentUserRole');
  const currentLoginTime = document.getElementById('currentLoginTime');
  const logoutBtn = document.getElementById('logoutBtn');

  // Kiểm tra phiên đăng nhập đã tồn tại trước đó chưa
  checkSession();

  // Chức năng ẩn / hiện mật khẩu
  if (togglePasswordBtn) {
    togglePasswordBtn.addEventListener('click', () => {
      const isPassword = passwordInput.getAttribute('type') === 'password';
      passwordInput.setAttribute('type', isPassword ? 'text' : 'password');
      eyeIcon.innerHTML = isPassword
        ? '<path d="m15 18-.722-3.25"/><path d=" 2 8a10.645 10.645 0 0 0 20 0"/><path d="m20 15-1.726-2.05"/><path d="m4 15 1.726-2.05"/><path d="m9 18 .722-3.25"/>'
        : '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>';
    });
  }

  // Xóa cảnh báo khi người dùng gõ
  usernameInput.addEventListener('input', () => {
    clearInputError(usernameInput, usernameError);
  });

  passwordInput.addEventListener('input', () => {
    clearInputError(passwordInput, passwordError);
  });

  // Xử lý gửi Form Đăng nhập qua AJAX Fetch
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    // 1. Validation Frontend (kiểm tra không được để trống)
    let isValid = true;

    if (!username) {
      showInputError(usernameInput, usernameError, 'Vui lòng nhập tên đăng nhập!');
      isValid = false;
    } else {
      clearInputError(usernameInput, usernameError);
    }

    if (!password) {
      showInputError(passwordInput, passwordError, 'Vui lòng nhập mật khẩu!');
      isValid = false;
    } else {
      clearInputError(passwordInput, passwordError);
    }

    if (!isValid) return;

    // 2. Gửi AJAX (Fetch API) lên máy chủ backend
    setLoading(true);

    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showAlert('success', '✓', data.message || 'Đăng nhập thành công!');
        loginForm.reset();
        
        setTimeout(() => {
          showDashboard(data.user);
        }, 800);
      } else {
        showAlert('error', '✕', data.message || 'Đăng nhập thất bại!');
      }
    } catch (error) {
      console.error('Fetch error:', error);
      showAlert('error', '✕', 'Không thể kết nối đến máy chủ. Vui lòng kiểm tra lại!');
    } finally {
      setLoading(false);
    }
  });

  // Xử lý Đăng xuất
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async () => {
      try {
        const response = await fetch('/api/logout', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
          loginCard.classList.remove('hidden');
          dashboardCard.classList.add('hidden');
          showAlert('success', '✓', 'Bạn đã đăng xuất an toàn.');
        }
      } catch (err) {
        console.error(err);
      }
    });
  }

  // Hàm kiểm tra session
  async function checkSession() {
    try {
      const res = await fetch('/api/me');
      const data = await res.json();
      if (data.authenticated && data.user) {
        showDashboard(data.user);
      }
    } catch (e) {
      console.error('Check session error:', e);
    }
  }

  function showDashboard(user) {
    currentUsername.textContent = user.username;
    currentUserRole.textContent = user.role || 'Người dùng';
    const loginDate = user.loginAt ? new Date(user.loginAt) : new Date();
    currentLoginTime.textContent = loginDate.toLocaleTimeString('vi-VN') + ' - ' + loginDate.toLocaleDateString('vi-VN');
    
    loginCard.classList.add('hidden');
    dashboardCard.classList.remove('hidden');
  }

  function showInputError(input, errorElement, message) {
    input.classList.add('is-invalid');
    errorElement.textContent = message;
  }

  function clearInputError(input, errorElement) {
    input.classList.remove('is-invalid');
    errorElement.textContent = '';
  }

  function showAlert(type, icon, text) {
    alertMessage.className = `alert ${type}`;
    alertIcon.textContent = icon;
    alertText.textContent = text;
    alertMessage.classList.remove('hidden');
  }

  function hideAlert() {
    alertMessage.classList.add('hidden');
  }

  function setLoading(isLoading) {
    if (isLoading) {
      submitBtn.disabled = true;
      btnLoader.classList.remove('hidden');
    } else {
      submitBtn.disabled = false;
      btnLoader.classList.add('hidden');
    }
  }
});
