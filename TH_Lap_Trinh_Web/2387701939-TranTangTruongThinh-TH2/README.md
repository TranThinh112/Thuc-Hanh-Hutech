# TH2: Kiến Trúc MVC Với Repository Pattern & Tải Tệp Lên (File Upload)

* **Học phần:** Thực hành Lập trình Web (ASP.NET Core MVC)
* **Sinh viên:** Trần Tăng Trường Thịnh - 2387701939

---

## 📌 Chức Năng Chính
1. **Kiến trúc Repository Pattern:** Khởi tạo `IProductRepository` và `MockProductRepository` quản lý dữ liệu trong bộ nhớ.
2. **Quản lý sản phẩm (CRUD):** Thêm sản phẩm mới, hiển thị danh sách, cập nhật thông tin và xóa sản phẩm.
3. **Xử lý File Upload:** Cho phép tải ảnh đại diện sản phẩm (`IFormFile`), lưu trữ vào thư mục `wwwroot/images` và hiển thị trực tiếp trên View.

---

## 🖼️ Hình Ảnh Giao Diện Sản Phẩm

![Ảnh Sản Phẩm Mẫu](LT_Web_Buoi2/wwwroot/images/04c03472-3f23-4080-b6e7-c1af746d919b.png)
*Hình ảnh sản phẩm được tải lên và lưu trữ qua tính năng File Upload của ứng dụng*

![Danh Mục Sản Phẩm](LT_Web_Buoi2/wwwroot/images/075f21e1-4eac-42eb-8dd9-5c27188cb53f.png)
*Minh họa hiển thị sản phẩm mẫu trong hệ thống bán hàng*