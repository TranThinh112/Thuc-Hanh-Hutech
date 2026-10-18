# Học Phần Lập Trình Web (ASP.NET Core MVC)

Kho lưu trữ toàn bộ các bài tập thực hành theo từng tuần, bài tập giữa kỳ và đề tài thuyết trình triển khai ứng dụng của học phần **Lập trình Web** - Trường Đại học Công nghệ TP.HCM (HUTECH).

* **Sinh viên thực hiện:** Trần Tăng Trường Thịnh
* **MSSV:** 2387701939
* **Nền tảng công nghệ:** C#, .NET 8 / ASP.NET Core MVC, Entity Framework Core, SQL Server, HTML5, CSS3, Bootstrap, Railway Cloud Platform.

---

## Cấu Trúc Các Buổi Học & Dự Án

### 1. `Web_buoi2_20_4` (Buổi 2 - 20/04)
* **Chủ đề:** Thiết kế giao diện Web Responsive với HTML5 & CSS3.
* **Nội dung:**
  * Bố cục trang web hiện đại sử dụng Grid System của Bootstrap.
  * Tích hợp icon từ Font Awesome, font chữ Raleway.
  * Tối ưu hóa hiển thị trên các kích thước màn hình khác nhau.

### 2. `Web_Buoi3__8_5` (Buổi 3 - 08/05)
* **Chủ đề:** Làm quen kiến trúc ASP.NET Core MVC.
* **Nội dung:**
  * Tìm hiểu mô hình Model - View - Controller, routing mặc định.
  * Xây dựng controller hiển thị bài tập sản phẩm (`/Home/BaiTap2`).
  * Xây dựng controller quản lý danh sách sinh viên (`/Student/Index`).
  * Báo cáo thực hành: `TruongThinhBuoi3.docx`.

### 3. `Web_Buoi4_15_5` (Buổi 4 - 15/05)
* **Chủ đề:** Ứng dụng Quản lý Công việc (Task Management CRUD).
* **Nội dung:**
  * Thiết kế Model Task và ràng buộc dữ liệu.
  * Xây dựng các Action và View: Xem danh sách, Thêm mới, Sửa thông tin, Xóa công việc, Xem chi tiết.
  * Tài liệu báo cáo: `Trần Tăng Trường Thịnh 2387701939_Web_Buoi4.docx` và file PDF tương ứng.

### 4. `Web_buoi5_22_5` (Buổi 5 - 22/05)
* **Chủ đề:** Ứng dụng Quản lý Sách (Book Store) với Entity Framework Core.
* **Nội dung:**
  * Kết nối cơ sở dữ liệu với `ApplicationDbContext`.
  * Thực hiện các thao tác CRUD danh mục và thông tin sách.
  * Báo cáo thực hành: `Trần_Tăng_Trường_Thịnh_Web_buoi_5.docx` và file PDF.

### 5. `Web_buoi6_29_5` (Buổi 6 - 29/05)
* **Chủ đề:** Tích hợp Xác thực (Authentication) & Phân quyền (Authorization).
* **Nội dung:**
  * Cài đặt ASP.NET Core Identity: Chức năng Đăng ký tài khoản, Đăng nhập.
  * Phân quyền tài khoản quản trị (Role Admin) và người dùng thông thường (User).
  * Khu vực quản lý sản phẩm dành riêng cho Admin.
  * Hướng dẫn dòng lệnh .NET CLI (`HDSD.txt`):
    ```bash
    dotnet clean Web_buoi_6.csproj
    dotnet build Web_buoi_6.csproj
    dotnet watch run --project Web_buoi_6.csproj
    ```

### 6. `Web_buoi7_5_6_Giua_Ky` (Buổi 7 - 05/06 - Kiểm Tra Giữa Kỳ)
* **Chủ đề:** Đồ án bài thi kiểm tra giữa kỳ.
* **Nội dung:**
  * Tích hợp toàn diện các kỹ năng đã học: Kiến trúc MVC chuẩn, phân hệ `Areas/Identity`, Entity Framework Core Migrations.
  * Xây dựng hệ thống quản lý dữ liệu hoàn chỉnh, tích hợp tính năng thời tiết (`WeatherController`) và quản trị hệ thống.

### 7. `Web_Buoi_8_12_6` (Buổi 8 - 12/06)
* **Chủ đề:** Hoàn thiện và nâng cao tính năng ứng dụng ASP.NET Core MVC.
* **Nội dung:** Tinh chỉnh routing, xử lý ngoại lệ ErrorViewModel, quản lý tài nguyên tĩnh (`wwwroot`).

### 8. `Thuyet_Trinh` (Chuyên Đề Báo Cáo Triển Khai Cloud)
* **Tên chuyên đề:** *Hướng dẫn Deploy Project ASP.NET Core lên nền tảng đám mây Railway*
* **Tài liệu & Sản phẩm:**
  * `Slide_Thuyet_trinh_Deploy_Project_LTW.pdf`: Slide thuyết trình báo cáo.
  * `Demo-Deploy.mp4`: Video clip ghi lại quy trình build và deploy lên Railway.
  * `link.txt`: Link slide Canva và đường dẫn demo ứng dụng trực tuyến (`webbasic-production-cdb1.up.railway.app`).
  * **Điểm kỹ thuật quan trọng:**
    * Railway cấp phát cổng động (`PORT`) qua biến môi trường.
    * Ứng dụng đọc `Environment.GetEnvironmentVariable("PORT")` và bind địa chỉ lắng nghe về `http://0.0.0.0:$PORT` để nhận lưu lượng từ Internet.

### 9. `HDKN.txt` (Cẩm Nang Dòng Lệnh Migrations & Solution)
* Ghi chép nhanh các câu lệnh Entity Framework Core và CLI thông dụng:
  * Tạo Migration và Cập nhật Database:
    ```bash
    Add-Migration <TenMigration>
    Update-Database
    dotnet ef migrations add <TenMigration> --context ApplicationDbContext
    dotnet ef database update --context ApplicationDbContext
    ```
  * Chèn dữ liệu hạt giống (Seed Data) bằng `migrationBuilder.InsertData(...)`.
  * Khởi tạo file Solution `.sln` và gán project vào solution.