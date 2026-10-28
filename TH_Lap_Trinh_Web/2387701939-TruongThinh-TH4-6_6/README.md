# TH4 (06/06): Entity Framework Core Code-First & Phân Hệ Admin Area

* **Học phần:** Thực hành Lập trình Web
* **Sinh viên:** Trần Tăng Trường Thịnh - 2387701939

---

## 📌 Chức Năng Chính
1. **EF Core Code-First:** Kết nối Microsoft SQL Server, khai báo model `Product`, `Category` và áp dụng Migration tự động tạo bảng.
2. **Phân hệ Admin riêng biệt:** Tổ chức thư mục `Areas/Admin` dành cho việc quản trị cơ sở dữ liệu.
3. **Thao tác dữ liệu quan hệ:** Tự động nạp dữ liệu danh mục khi chỉnh sửa hoặc thêm mới sản phẩm qua dropdown select list.

---

## 🖼️ Hình Ảnh Sản Phẩm Trong Hệ Thống

![Sản Phẩm AirPods Pro 2](THLTW_Buoi_4/wwwroot/images/AirPods%20Pro%202.jpg)
*Hình ảnh sản phẩm AirPods Pro 2 được quản lý trong cơ sở dữ liệu*

![Sản Phẩm Dell XPS 13](THLTW_Buoi_4/wwwroot/images/Dell%20XPS%2013.jpg)
*Hình ảnh sản phẩm máy tính Dell XPS 13 kết nối dữ liệu EF Core*