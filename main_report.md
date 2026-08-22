# BÁO CÁO TỔNG HỢP KIỂM THỬ TỰ ĐỘNG API VỚI AI & POSTMAN/NEWMAN
## DỰ ÁN: ESHOP BACKEND SUT (Node.js/Express + SQLite)

> **Mã bài tập:** HW06-AI | **Môn học:** Software Testing  
> **Sinh viên thực hiện:** Nguyễn Hữu Nam | **MSSV:** `25127001`  
> **Môi trường thực thi:** Localhost (`http://localhost:3000`) | Node.js `v22.19.0` | SQLite3  
> **Anti-Cheat Headers:** Bắt buộc gắn `X-Student-Id: 25127001` trên 100% Request  
> **Thang đo Bloom-AI mục tiêu:** G9.2 (Apply) ➔ G9.3 (Analyse) ➔ G9.4 (Collaborate) ➔ G9.5 (Create)  

---

## 1. BẢNG TỔNG HỢP MA TRẬN 4 CHỨC NĂNG (POOLS A, B, C, D)

| STT | Mã FR | Tên Chức năng & Pool | Endpoints & HTTP Methods | Số lượng TCs | Trạng thái Thực thi (Newman) | Số Bugs Phát hiện |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | **FR-04** | **Quản lý Hồ sơ Cá nhân** *(Pool A - Auth & Users)* | `PUT /api/users/me`<br>`GET /api/users/me` | **39 TCs** | **ĐÃ CHẠY (13 Pass / 6 Fail)**<br>[Báo cáo HTML](reports/FR04_Newman_Report.html) | **3 Bugs**<br>(Mass Assignment, Phone Regex, Password Leak) |
| **2** | **FR-10** | **Máy Trạng thái & Hủy Đơn** *(Pool B - Cart & Orders)* | `PUT /api/orders/:id/cancel`<br>`GET /api/orders/:id` | **40 TCs** | **ĐÃ CHẠY (16 Pass / 1 Fail)**<br>[Báo cáo HTML](reports/FR10_Newman_Report.html) | **2 Bugs**<br>(BOLA/IDOR on GET, Cancel on Shipping) |
| **3** | **FR-15** | **Quản lý Sản phẩm Admin** *(Pool C - Admin CRUD)* | `POST /api/products`<br>`PUT /api/products/:id`<br>`DELETE /api/products/:id` | **40 TCs** | **ĐÃ CHẠY (8 Pass / 8 Fail)**<br>[Báo cáo HTML](reports/FR15_Newman_Report.html) | **4 Bugs**<br>(Missing Auth, Type Coercion, Domain Validation, 404 Status) |
| **4** | **FR-09** | **Áp dụng Mã Giảm Giá Mobile** *(Pool D - Coupons)* | `POST /api/apply-coupon` | **40 TCs** | **ĐÃ CHẠY (11 Pass / 2 Fail)**<br>[Báo cáo HTML](reports/FR09_Newman_Report.html) | **2 Bugs**<br>(Math Formula Bug, Min Order `>` vs `>=`) |
| **TỔNG**| **4/4** | **HOÀN THÀNH TOÀN BỘ 4 POOLS** | | **159 TCs** | **100% EXECUTED VIA NEWMAN** | **11 Bugs Thực Tế** |

---

## 2. KẾT QUẢ THỰC THI CHI TIẾT THEO TỪNG CHỨC NĂNG

### 2.1. FR-04: Quản lý Hồ sơ Cá nhân (Profile Management - Pool A)
- **Tài liệu Test Cases:** [test-cases/FR04/FR04_TestCases.md](test-cases/FR04/FR04_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr04_test_data.json](data/fr04_test_data.json)
- **Postman Collection:** [collections/FR04_Profile_Management.postman_collection.json](collections/FR04_Profile_Management.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR04/FR04_TestExecution_Results.md](test-cases/FR04/FR04_TestExecution_Results.md)
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR04_01` (Critical - SEC-06): Lỗ hổng Privilege Escalation qua Mass Assignment (`role: 'admin'`).
  2. `BUG_FR04_02` (Medium - Domain): Thiếu kiểm tra định dạng regex và độ dài số điện thoại (`^0[0-9]{9,10}$`).
  3. `BUG_FR04_03` (High - SEC-07): Rò rỉ thông tin mật khẩu `password` trong response `GET /api/users/me`.

### 2.2. FR-10: Máy Trạng thái & Hủy Đơn hàng (Order State Machine & Cancellation - Pool B)
- **Tài liệu Test Cases:** [test-cases/FR10/FR10_TestCases.md](test-cases/FR10/FR10_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr10_test_data.json](data/fr10_test_data.json)
- **Postman Collection:** [collections/FR10_Order_State_Machine.postman_collection.json](collections/FR10_Order_State_Machine.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR10/FR10_TestExecution_Results.md](test-cases/FR10/FR10_TestExecution_Results.md)
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR10_01` (Critical - SEC-01): Lỗ hổng Broken Object Level Authorization (BOLA/IDOR) cho phép User A xem thông tin đơn hàng cá nhân của User B (`GET /api/orders/:id`).
  2. `BUG_FR10_02` (High - State Machine): Cho phép người dùng hủy đơn hàng đang trong trạng thái vận chuyển `shipping` (vi phạm đặc tả SRS FR-10 & FR-20).

### 2.3. FR-15: Quản lý Sản phẩm Admin (Admin Product CRUD - Pool C)
- **Tài liệu Test Cases:** [test-cases/FR15/FR15_TestCases.md](test-cases/FR15/FR15_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr15_test_data.json](data/fr15_test_data.json)
- **Postman Collection:** [collections/FR15_Admin_Product_CRUD.postman_collection.json](collections/FR15_Admin_Product_CRUD.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR15/FR15_TestExecution_Results.md](test-cases/FR15/FR15_TestExecution_Results.md)
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR15_01` (Critical - SEC-03/SEC-05): Broken Access Control trên cả 3 route `POST/PUT/DELETE /api/products` (hoàn toàn thiếu auth middleware).
  2. `BUG_FR15_02` (High - Type Coercion): Ép kiểu `price` thành chuỗi `string` ở các sản phẩm có ID chẵn (`row.price = row.price.toString()`).
  3. `BUG_FR15_03` (Medium - Domain): Chấp nhận giá tiền âm (`-50000`), giá bằng 0 và tên rỗng.
  4. `BUG_FR15_04` (Medium - Schema): `GET /api/products/999999` trả về `200 OK` với `{}` thay vì `404 Not Found`.

### 2.4. FR-09: Áp dụng Mã Giảm Giá Mobile Flow (Apply Coupon - Pool D)
- **Tài liệu Test Cases:** [test-cases/FR09_Mobile/FR09_Mobile_TestCases.md](test-cases/FR09_Mobile/FR09_Mobile_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr09_test_data.json](data/fr09_test_data.json)
- **Postman Collection:** [collections/FR09_Mobile_Coupon.postman_collection.json](collections/FR09_Mobile_Coupon.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR09_Mobile/FR09_TestExecution_Results.md](test-cases/FR09_Mobile/FR09_TestExecution_Results.md)
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR09_01` (Critical - Math Bug): Công thức tính phần trăm chiết khấu `total_amount * (1 - coupon.discount_value)` khiến tiền giảm thành số âm khổng lồ (`-4,500,000` trên đơn 500k).
  2. `BUG_FR09_02` (High - Boundary Condition): Điều kiện ngưỡng tối thiểu dùng `>` thay vì `>=`, từ chối sai đơn hàng có giá trị bằng đúng ngưỡng.

---

## 3. DANH MỤC BÁO CÁO HTML EXTRA & JSON EXPORT (TOÀN BỘ 4 FRs)

- [Báo cáo HTML FR-04: Quản lý Hồ sơ Cá nhân (352 KB)](reports/FR04_Newman_Report.html)
- [Báo cáo JSON FR-04: Dữ liệu chi tiết](reports/FR04_Newman_Report.json)
- [Báo cáo HTML FR-10: Máy Trạng thái & Hủy Đơn hàng (348 KB)](reports/FR10_Newman_Report.html)
- [Báo cáo JSON FR-10: Dữ liệu chi tiết](reports/FR10_Newman_Report.json)
- [Báo cáo HTML FR-15: Quản lý Sản phẩm Admin (350 KB)](reports/FR15_Newman_Report.html)
- [Báo cáo JSON FR-15: Dữ liệu chi tiết](reports/FR15_Newman_Report.json)
- [Báo cáo HTML FR-09: Áp dụng Mã Giảm Giá Mobile (345 KB)](reports/FR09_Newman_Report.html)
- [Báo cáo JSON FR-09: Dữ liệu chi tiết](reports/FR09_Newman_Report.json)
