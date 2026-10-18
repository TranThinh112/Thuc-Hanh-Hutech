# Thực Hành Lập Trình Web (ASP.NET Core MVC & Web API)

Thư mục chứa mã nguồn các bài thực hành môn **Thực hành Lập trình Web** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Công nghệ cốt lõi:** C# .NET, ASP.NET Core MVC, Entity Framework Core, Repository Pattern, Dependency Injection, RESTful Web API, SQL Server, Bootstrap, JavaScript.

---

## Danh Sách Các Bài Thực Hành (Labs)

### 1. `2387701939-TruongThinh-TH1-16_5` (Thực Hành 1 - 16/05)
* **Mục tiêu:** Thiết kế giao diện Web Responsive cơ bản.
* **Nội dung kỹ thuật:**
  * Xây dựng layout trang chủ và trang danh mục/chi tiết sản phẩm bằng HTML5, CSS3 và Bootstrap Grid.
  * Hiển thị danh mục sản phẩm, banner quảng cáo và hình ảnh trực quan.
  * Tích hợp JavaScript xử lý tương tác cơ bản trên trang sản phẩm (`product.js`).

### 2. `2387701939-TranTangTruongThinh-TH2` (Thực Hành 2)
* **Mục tiêu:** Xây dựng ứng dụng quản lý sản phẩm bằng ASP.NET Core MVC với dữ liệu mô phỏng.
* **Nội dung kỹ thuật:**
  * Áp dụng kiến trúc thiết kế **Repository Pattern** (`IProductRepository`, `MockProductRepository`) giúp tách biệt tầng truy cập dữ liệu và nghiệp vụ.
  * Hiện thực đầy đủ các chức năng CRUD (Create, Read, Update, Delete) sản phẩm:
    * Xem danh sách sản phẩm kèm hình ảnh, phân loại danh mục.
    * Thêm mới sản phẩm có tính năng **Upload file hình ảnh** lưu vào thư mục `wwwroot/images`.
    * Cập nhật thông tin sản phẩm và xóa sản phẩm khỏi danh sách.
  * Sử dụng Data Annotations để xác thực dữ liệu đầu vào (Validation) trên ViewModel/Model.

### 3. `2387701939-TruongThinh-TH4-6_6` (Thực Hành 4 - 06/06)
* **Mục tiêu:** Kết nối cơ sở dữ liệu quan hệ với Entity Framework Core và phân chia phân hệ Quản trị.
* **Nội dung kỹ thuật:**
  * Cấu hình DbContext kết nối SQL Server LocalDB / Express thông qua chuỗi kết nối trong `appsettings.json`.
  * Quản lý lược đồ CSDL bằng **EF Core Code-First Migrations**.
  * Thiết lập phân hệ quản trị bằng **Areas (Admin Area)**: tách riêng giao diện người dùng thường và bảng điều khiển dành cho Quản trị viên quản lý danh mục và sản phẩm.

### 4. `2387701939-TruongThinh-TH5-14_6` (Thực Hành 5 - 14/06)
* **Mục tiêu:** Phát triển tính năng Giỏ hàng trực tuyến (Shopping Cart) và Quản lý phiên (Session).
* **Nội dung kỹ thuật:**
  * Xây dựng module Giỏ hàng lưu trữ thông tin sản phẩm đã chọn, số lượng và tính tổng tiền tự động.
  * Viết tiện ích mở rộng `SessionExtensions` (sử dụng `JsonSerializer`) để lưu trữ đối tượng giỏ hàng phức tạp vào `ISession`.
  * Các chức năng người dùng: Thêm vào giỏ hàng từ trang danh sách, cập nhật số lượng, xóa sản phẩm khỏi giỏ và chuyển sang quy trình đặt hàng/thanh toán (Checkout).

### 5. `2387701939-TruongThinh-TH6-20_6` (Thực Hành 6 - 20/06)
* **Mục tiêu:** Xây dựng và tiêu thụ dịch vụ RESTful Web API.
* **Nội dung kỹ thuật:**
  * Phát triển `ProductApiController` theo kiến trúc RESTful API, cung cấp các endpoint chuẩn:
    * `GET /api/products`: Lấy toàn bộ danh sách sản phẩm.
    * `GET /api/products/{id}`: Lấy chi tiết một sản phẩm theo ID.
    * `POST /api/products`: Thêm mới sản phẩm từ dữ liệu JSON.
    * `PUT /api/products/{id}`: Cập nhật thông tin sản phẩm.
    * `DELETE /api/products/{id}`: Xóa sản phẩm.
  * Tích hợp đồng thời cả giao diện Web MVC truyền thống và API backend cho ứng dụng client.

---

## Hướng Dẫn Chạy Dự Án
1. Mở file giải pháp (`.sln` hoặc `.slnx`) bằng **Visual Studio 2022** hoặc Visual Studio Code.
2. Kiểm tra chuỗi kết nối trong `appsettings.json` trỏ tới SQL Server của bạn.
3. Chạy cập nhật database trong Terminal:
   ```bash
   dotnet ef database update
   ```
4. Khởi chạy ứng dụng bằng lệnh:
   ```bash
   dotnet run
   ```