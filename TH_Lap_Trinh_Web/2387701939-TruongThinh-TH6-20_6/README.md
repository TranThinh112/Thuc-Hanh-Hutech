# TH6 (20/06): Xây Dựng Dịch Vụ RESTful Web API Trong ASP.NET Core

* **Học phần:** Thực hành Lập trình Web
* **Sinh viên:** Trần Tăng Trường Thịnh - 2387701939

---

## 📌 Chức Năng Chính
1. **Thiết kế RESTful Web API:** Xây dựng `ProductsApiController` với các endpoints chuẩn RESTful:
   * `GET /api/productsapi`: Lấy toàn bộ danh sách sản phẩm (JSON format).
   * `GET /api/productsapi/{id}`: Xem chi tiết sản phẩm theo mã ID.
   * `POST /api/productsapi`: Tạo mới một sản phẩm vào cơ sở dữ liệu.
   * `PUT /api/productsapi/{id}`: Cập nhật thông tin sản phẩm.
   * `DELETE /api/productsapi/{id}`: Xóa sản phẩm khỏi hệ thống.
2. **Định dạng dữ liệu JSON:** Chuẩn hóa cấu trúc response mã lỗi HTTP (`200 OK`, `201 Created`, `404 Not Found`, `400 Bad Request`).
3. **Frontend tích hợp AJAX/Fetch:** Giao diện gọi API bất đồng bộ để tải và cập nhật dữ liệu mượt mà không cần reload trang.

---

## 🖼️ Hình Ảnh Minh Họa

![Dữ Liệu Sản Phẩm API](images/04c03472-3f23-4080-b6e7-c1af746d919b.png)
*Sản phẩm mẫu được truy xuất và cung cấp thông qua dịch vụ RESTful API*

![Trực Quan Hóa Dữ Liệu](images/075f21e1-4eac-42eb-8dd9-5c27188cb53f.png)
*Minh họa dữ liệu hệ thống được đồng bộ hóa qua API endpoints*