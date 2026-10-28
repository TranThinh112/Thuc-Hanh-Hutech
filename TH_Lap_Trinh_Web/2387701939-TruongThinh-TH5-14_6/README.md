# TH5 (14/06): Xây Dựng Giỏ Hàng (Shopping Cart) Bằng Session & Checkout

* **Học phần:** Thực hành Lập trình Web (ASP.NET Core MVC)
* **Sinh viên:** Trần Tăng Trường Thịnh - 2387701939

---

## 📌 Chức Năng Chính
1. **Lưu trữ Giỏ hàng bằng Session:**
   * Sử dụng Extension phương thức `SetObjectAsJson` và `GetObjectFromJson` để lưu trữ đối tượng Cart trong `ISession`.
2. **Quy trình mua sắm hoàn chỉnh:**
   * Thêm sản phẩm vào giỏ hàng từ trang danh sách.
   * Cập nhật số lượng sản phẩm, tự động tính tổng tiền thanh toán.
   * Xóa từng sản phẩm hoặc làm rỗng giỏ hàng.
3. **Tạo đơn hàng & Lưu hóa đơn:** Lưu thông tin khách hàng vào bảng `Orders` và chi tiết các món hàng vào bảng `OrderDetails`.

---

## 🖼️ Hình Ảnh Sản Phẩm Giỏ Hàng

![Sản Phẩm Giỏ Hàng](images/04c03472-3f23-4080-b6e7-c1af746d919b.png)
*Minh họa sản phẩm được thêm vào danh mục giỏ hàng thanh toán*

![Sản Phẩm Mua Sắm](images/075f21e1-4eac-42eb-8dd9-5c27188cb53f.png)
*Minh họa giao diện hiển thị các mặt hàng trong quy trình Checkout*