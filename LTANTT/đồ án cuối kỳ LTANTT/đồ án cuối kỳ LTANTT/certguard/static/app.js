// JavaScript nhỏ, nạp từ file riêng để tuân thủ Content-Security-Policy (không có script inline)
document.addEventListener("DOMContentLoaded", () => {
  // Xác nhận trước khi xóa
  document.querySelectorAll("form[data-confirm]").forEach(f =>
    f.addEventListener("submit", e => { if (!confirm(f.dataset.confirm)) e.preventDefault(); }));

  // Hiển thị trạng thái "đang quét" khi gửi form chạy lâu
  document.querySelectorAll("form[data-busy]").forEach(f =>
    f.addEventListener("submit", () => {
      const b = f.querySelector("button");
      if (b) { b.disabled = true; b.textContent = f.dataset.busy; }
    }));

  // Sao chép lệnh đối chứng
  document.querySelectorAll("[data-copy]").forEach(b =>
    b.addEventListener("click", () => {
      navigator.clipboard.writeText(b.dataset.copy).then(() => {
        const t = b.textContent; b.textContent = "Đã chép"; setTimeout(() => b.textContent = t, 1200);
      });
    }));

  // Độ dài thanh "sắp hết hạn"
  document.querySelectorAll("[data-w]").forEach(el => { el.style.width = el.dataset.w + "%"; });
});
