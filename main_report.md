# BÁO CÁO TỔNG HỢP KIỂM THỬ TỰ ĐỘNG API VỚI AI & POSTMAN/NEWMAN
## DỰ ÁN: ESHOP BACKEND SUT (Node.js/Express + SQLite)

> **Mã bài tập:** HW06-AI | **Môn học:** Software Testing (CS423 / CSC13003)  
> **Sinh viên thực hiện:** Nguyễn Nhật Nam | **MSSV:** `23127092` | **Lớp:** `23KTPM2`  
> **Repository:** [https://github.com/ngnam2012/23KTPM2_Testing_HW06](https://github.com/ngnam2012/23KTPM2_Testing_HW06)  
> **Môi trường thực thi:** Localhost (`http://localhost:3000`) | Node.js `v22.19.0` | SQLite3  
> **Anti-Cheat Headers:** Bắt buộc gắn `X-Student-Id: 23127092` trên 100% Request  
> **Thang đo Bloom-AI đạt được:** **G9.2 (Apply) ➔ G9.3 (Analyse) ➔ G9.4 (Collaborate) ➔ G9.5 (Create)**  

---

## 1. BẢNG TỔNG HỢP MA TRẬN 4 CHỨC NĂNG (POOLS A, B, C, D)

*Toàn bộ 179 Test Cases được chuyển đổi 1-to-1 thành các request và test script độc lập trong Postman Collection và đã được thực thi 100% qua Newman CLI.*

| STT | Mã FR | Tên Chức năng & Phân vùng (Pool) | Endpoints & HTTP Methods | Số lượng TCs | Trạng thái Thực thi (Newman 1-to-1) | Số Bugs Thực tế Phát hiện |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | **FR-04** | **Quản lý Hồ sơ Cá nhân** *(Pool A - Auth & Users)* | `PUT /api/users/me`<br>`GET /api/users/me` | **44 TCs** | **44/44 TCs ĐÃ CHẠY**<br>(47 Reqs, 59 Assertions: 21 Pass / 38 Fail)<br>[Báo cáo HTML](reports/FR04_Newman_Report.html) | **5 Bugs**<br>(Mass Assignment, Phone Regex, Password Leak, NULL Wipe, Metadata Leak) |
| **2** | **FR-10** | **Máy Trạng thái & Hủy Đơn** *(Pool B - Cart & Orders)* | `PUT /api/orders/:id/cancel`<br>`GET /api/orders/:id` | **45 TCs** | **45/45 TCs ĐÃ CHẠY**<br>(48 Reqs, 52 Assertions: 20 Pass / 32 Fail)<br>[Báo cáo HTML](reports/FR10_Newman_Report.html) | **3 Bugs**<br>(BOLA/IDOR on GET, Cancel on Shipping, Blind ID Enumeration) |
| **3** | **FR-15** | **Quản lý Sản phẩm Admin** *(Pool C - Admin CRUD)* | `POST /api/products`<br>`PUT /api/products/:id`<br>`DELETE /api/products/:id` | **45 TCs** | **45/45 TCs ĐÃ CHẠY**<br>(48 Reqs, 50 Assertions: 22 Pass / 28 Fail)<br>[Báo cáo HTML](reports/FR15_Newman_Report.html) | **5 Bugs**<br>(Missing Auth, Type Coercion, Domain Validation, 404 Status, SQLi HTML Leak) |
| **4** | **FR-09** | **Áp dụng Mã Giảm Giá Mobile** *(Pool D - Coupons)* | `POST /api/apply-coupon` | **45 TCs** | **45/45 TCs ĐÃ CHẠY**<br>(48 Reqs, 50 Assertions: 22 Pass / 28 Fail)<br>[Báo cáo HTML](reports/FR09_Newman_Report.html) | **3 Bugs**<br>(Math Formula Bug, Min Order `>` vs `>=`, Spoofed User ID) |
| **TỔNG**| **4/4** | **HOÀN THÀNH TOÀN BỘ 4 POOLS** | **Tất cả các Endpoints** | **179 TCs** | **179/179 TCs ĐÃ THỰC THI (100%)**<br>(191 Reqs, 211 Assertions: 85 Pass / 126 Fail) | **16 BUGS THỰC TẾ TRONG SUT** |

---

## 2. KẾT QUẢ THỰC THI CHI TIẾT THEO TỪNG CHỨC NĂNG

### 2.1. FR-04: Quản lý Hồ sơ Cá nhân (Profile Management - Pool A)
- **Tài liệu Test Cases:** [test-cases/FR04/FR04_TestCases.md](test-cases/FR04/FR04_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr04_test_data.json](data/fr04_test_data.json)
- **Postman Collection:** [collections/FR04_Profile_Management.postman_collection.json](collections/FR04_Profile_Management.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR04/FR04_TestExecution_Results.md](test-cases/FR04/FR04_TestExecution_Results.md) *(47 Requests, 59 Assertions: 21 Pass / 38 Fail)*
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR04_01` (Critical - SEC-06): Lỗ hổng Privilege Escalation qua Mass Assignment (`role: 'admin'`).
  2. `BUG_FR04_02` (Medium - Domain): Thiếu kiểm tra định dạng regex và độ dài số điện thoại (`^0[0-9]{9,10}$`).
  3. `BUG_FR04_03` (High - SEC-07): Rò rỉ thông tin mật khẩu `password` trong response `GET /api/users/me`.
  4. `BUG_FR04_04` (High - Data Integrity): Phá hủy dữ liệu ngầm khi Partial Update (xóa trắng `phone` và `shipping_address` thành `NULL`).
  5. `BUG_FR04_05` (High - SEC-07): Rò rỉ toàn bộ metadata an ninh tài khoản (`reset_token`, `login_attempts`, `locked_until`).

### 2.2. FR-10: Máy Trạng thái & Hủy Đơn hàng (Order State Machine & Cancellation - Pool B)
- **Tài liệu Test Cases:** [test-cases/FR10/FR10_TestCases.md](test-cases/FR10/FR10_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr10_test_data.json](data/fr10_test_data.json)
- **Postman Collection:** [collections/FR10_Order_State_Machine.postman_collection.json](collections/FR10_Order_State_Machine.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR10/FR10_TestExecution_Results.md](test-cases/FR10/FR10_TestExecution_Results.md) *(48 Requests, 52 Assertions: 20 Pass / 32 Fail)*
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR10_01` (Critical - SEC-01): Lỗ hổng Broken Object Level Authorization (BOLA/IDOR) cho phép User A xem thông tin đơn hàng cá nhân của User B (`GET /api/orders/:id`).
  2. `BUG_FR10_02` (High - State Machine): Cho phép người dùng hủy đơn hàng đang trong trạng thái vận chuyển `shipping` (vi phạm đặc tả SRS FR-10 & FR-20).
  3. `BUG_FR10_03` (Medium - Info Disclosure): Phản hồi bất đối xứng giữa PUT (404) và GET (200) cho phép dò quét ID đơn hàng của người dùng khác.

### 2.3. FR-15: Quản lý Sản phẩm Admin (Admin Product CRUD - Pool C)
- **Tài liệu Test Cases:** [test-cases/FR15/FR15_TestCases.md](test-cases/FR15/FR15_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr15_test_data.json](data/fr15_test_data.json)
- **Postman Collection:** [collections/FR15_Admin_Product_CRUD.postman_collection.json](collections/FR15_Admin_Product_CRUD.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR15/FR15_TestExecution_Results.md](test-cases/FR15/FR15_TestExecution_Results.md) *(48 Requests, 50 Assertions: 22 Pass / 28 Fail)*
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR15_01` (Critical - SEC-03/SEC-05): Broken Access Control trên cả 3 route `POST/PUT/DELETE /api/products` (hoàn toàn thiếu auth middleware).
  2. `BUG_FR15_02` (High - Type Coercion): Ép kiểu `price` thành chuỗi `string` ở các sản phẩm có ID chẵn (`row.price = row.price.toString()`).
  3. `BUG_FR15_03` (Medium - Domain): Chấp nhận giá tiền âm (`-50000`), giá bằng 0 và tên rỗng.
  4. `BUG_FR15_04` (Medium - Schema): `GET /api/products/999999` trả về `200 OK` với `{}` thay vì `404 Not Found`.
  5. `BUG_FR15_05` (High - SEC-06): SQL Injection trong tìm kiếm sản phẩm làm lộ lỗi HTML `<h1>Database Error</h1>`.

### 2.4. FR-09: Áp dụng Mã Giảm Giá Mobile Flow (Apply Coupon - Pool D)
- **Tài liệu Test Cases:** [test-cases/FR09_Mobile/FR09_Mobile_TestCases.md](test-cases/FR09_Mobile/FR09_Mobile_TestCases.md)
- **Dữ liệu kiểm thử:** [data/fr09_test_data.json](data/fr09_test_data.json)
- **Postman Collection:** [collections/FR09_Mobile_Coupon.postman_collection.json](collections/FR09_Mobile_Coupon.postman_collection.json)
- **Báo cáo thực thi Newman:** [test-cases/FR09_Mobile/FR09_TestExecution_Results.md](test-cases/FR09_Mobile/FR09_TestExecution_Results.md) *(48 Requests, 50 Assertions: 22 Pass / 28 Fail)*
- **Tổng kết lỗi phát hiện:**
  1. `BUG_FR09_01` (Critical - Math Inversion): Lỗi công thức tính phần trăm chiết khấu `Math.floor(total_amount * (1 - discount_value))` làm tiền giảm giá ra số âm (-4.5tr ₫) và đội giá đơn hàng lên gấp 10 lần.
  2. `BUG_FR09_02` (High - Condition C3 Boundary): Lỗi toán tử so sánh `total_amount > min_order_amount` làm từ chối các đơn hàng có giá trị bằng đúng ngưỡng tối thiểu.
  3. `BUG_FR09_03` (Medium - Security & Quota): Thiếu xác thực token cho phép kẻ xấu giả mạo `user_id` trong body để vượt qua hạn mức số lần sử dụng của coupon.

---

## 3. BẢNG TỔNG HỢP 16 LỖ HỔNG & BUGS PHÁT HIỆN TRONG SUT (BUG TRACKER)

| Mã Bug | Chức năng | Tên Lỗi & Mô Tả | Mức độ (Severity) | Vị trí Mã nguồn (server.js) | Hành vi Thực tế vs Kỳ vọng Nghiệp vụ |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **`BUG_FR04_01`** | FR-04 | Privilege Escalation qua Mass Assignment `role='admin'` | **Critical** | Dòng 124–127 | **Thực tế:** Client gửi `{"role": "admin"}` được ghi đè trực tiếp vào CSDL.<br>**Kỳ vọng:** Chặn cập nhật quyền, chỉ Admin mới được gán role. |
| **`BUG_FR04_02`** | FR-04 | Thiếu Regex & Length Validation số điện thoại | **Medium** | Dòng 118–135 | **Thực tế:** Chấp nhận lưu chuỗi ký tự chữ hoặc độ dài sai.<br>**Kỳ vọng:** Bắt buộc tuân thủ regex `^0[0-9]{9,10}$`. |
| **`BUG_FR04_03`** | FR-04 | Rò rỉ trường mật khẩu `password` trong `GET /api/users/me` | **High** | Dòng 112–116 | **Thực tế:** Câu lệnh `SELECT *` trả về hash mật khẩu.<br>**Kỳ vọng:** Loại bỏ trường `password` khỏi JSON phản hồi. |
| **`BUG_FR04_04`** | FR-04 | Partial Update xóa trắng SĐT và địa chỉ thành `NULL` | **High** | Dòng 119–122 | **Thực tế:** Gửi payload chỉ có `name` làm xóa mất SĐT và địa chỉ cũ.<br>**Kỳ vọng:** Bảo toàn giá trị các trường khuyết. |
| **`BUG_FR04_05`** | FR-04 | Rò rỉ metadata an ninh (`reset_token`, `login_attempts`) | **High** | Dòng 113 | **Thực tế:** Lộ mã OTP khôi phục mật khẩu.<br>**Kỳ vọng:** Che giấu toàn bộ metadata an ninh nội bộ. |
| **`BUG_FR10_01`** | FR-10 | Lỗ hổng BOLA/IDOR trên `GET /api/orders/:id` | **Critical** | Dòng 344–349 | **Thực tế:** Hoàn toàn thiếu middleware auth, ai cũng xem được đơn người khác.<br>**Kỳ vọng:** Bắt buộc đăng nhập và kiểm tra quyền sở hữu đơn hàng. |
| **`BUG_FR10_02`** | FR-10 | Vi phạm State Machine: Cho phép hủy đơn hàng `shipping` | **High** | Dòng 328–331 | **Thực tế:** Blacklist chỉ chặn `delivered`/`canceled`, bỏ sót `shipping`.<br>**Kỳ vọng:** Chỉ Admin mới được hủy đơn đang giao hàng. |
| **`BUG_FR10_03`** | FR-10 | Dò quét ID đơn hàng qua phản hồi bất đối xứng PUT và GET | **Medium** | Dòng 323 vs 345 | **Thực tế:** PUT trả 404 nhưng GET trả 200 giúp dò quét ID tồn tại.<br>**Kỳ vọng:** Thống nhất phân quyền chặt chẽ trên mọi endpoint. |
| **`BUG_FR15_01`** | FR-15 | Broken Access Control trên `POST/PUT/DELETE /api/products` | **Critical** | Dòng 167, 179, 191 | **Thực tế:** Cả 3 route Admin hoàn toàn không có `authenticateToken`.<br>**Kỳ vọng:** Bắt buộc xác thực quyền Admin (`role = 'admin'`). |
| **`BUG_FR15_02`** | FR-15 | Ép kiểu `price` thành chuỗi ở sản phẩm có ID chẵn | **High** | Dòng 162 | **Thực tế:** `row.id % 2 === 0` ép giá thành chuỗi `'28000000'`.<br>**Kỳ vọng:** Giá tiền luôn là kiểu số (`number`). |
| **`BUG_FR15_03`** | FR-15 | Chấp nhận giá tiền âm (`-50000`) và giá bằng 0 | **High** | Dòng 167–189 | **Thực tế:** Lưu giá âm gây lỗi nghiêm trọng khi tính tiền giỏ hàng.<br>**Kỳ vọng:** Từ chối với `400 Bad Request` khi `price <= 0`. |
| **`BUG_FR15_04`** | FR-15 | `GET /api/products/999999` trả về `200 OK` với `{}` | **Medium** | Dòng 161 | **Thực tế:** Trả về `200 OK` kèm object rỗng.<br>**Kỳ vọng:** Trả về `404 Not Found` theo chuẩn RESTful. |
| **`BUG_FR15_05`** | FR-15 | SQL Injection trong tìm kiếm sản phẩm làm lộ HTML 500 | **High** | Dòng 144–149 | **Thực tế:** Nối chuỗi `${searchQuery}` gây lỗi SQLi và lộ HTML 500.<br>**Kỳ vọng:** Dùng Parameterized Query và trả về JSON chuẩn. |
| **`BUG_FR09_01`** | FR-09 | Lỗi công thức tính phần trăm `1 - discount_value` | **Critical** | Dòng 400, 420 | **Thực tế:** `500k * (1 - 10) = -4.5tr`, đội giá đơn hàng lên 10 lần.<br>**Kỳ vọng:** `Math.floor(total_amount * (discount_value / 100))`. |
| **`BUG_FR09_02`** | FR-09 | Lỗi toán tử ngưỡng tối thiểu `>` thay vì `>=` | **High** | Dòng 379 | **Thực tế:** Đơn hàng bằng đúng ngưỡng tối thiểu bị từ chối 400.<br>**Kỳ vọng:** Chấp nhận theo quy tắc `total_amount >= min_order_amount`. |
| **`BUG_FR09_03`** | FR-09 | Thiếu xác thực token cho phép giả mạo `user_id` | **Medium** | Dòng 363–364 | **Thực tế:** Client tự gửi `user_id` trong body để dùng mã vô hạn.<br>**Kỳ vọng:** Trích xuất `user_id` từ JWT token đăng nhập. |

---

## 4. DANH MỤC CÁC TÍNH NĂNG POSTMAN NÂNG CAO ĐÃ ÁP DỤNG (POSTMAN FEATURES LIST)

Theo yêu cầu Section 6 & 14 trong đề bài HW06, toàn bộ các tính năng chuyên sâu của Postman đã được khai thác triệt để:

| STT | Tính năng Postman (Feature) | Mục đích & Cách thức áp dụng trong Dự án |
| :---: | :--- | :--- |
| **1** | **Postman Collections v2.1.0** | Tổ chức 4 bộ collection tương ứng với 4 nhóm chức năng (FR-04, FR-10, FR-15, FR-09) và 1 collection tự động sinh (`AutoGenerated_Collection`). |
| **2** | **Collection & Environment Variables** | Tham số hóa các biến động: `{{baseUrl}}` (`http://localhost:3000`), `{{studentId}}` (`23127092`), `{{user_token_A}}`, `{{user_token_B}}`, `{{admin_token}}`. |
| **3** | **Dynamic Pre-request Scripts** | Tự động hóa thiết lập dữ liệu trước khi gọi API: Tự động inject Header `X-Student-Id: 23127092` trên 100% request, sinh email ngẫu nhiên `uuid` cho flow đăng ký. |
| **4** | **Postman Chai BDD Assertions** | Viết kịch bản kiểm thử tự động xác minh: Status code (`to.have.status`), JSON Schema, kiểm tra ranh giới số học (`to.be.above`, `to.be.at.least`), và kiểm tra tính bất biến của trường nhạy cảm (`to.not.have.property('password')`). |
| **5** | **JSON Schema Validation (Ajv/tv4)** | Xác thực cấu trúc dữ liệu phản hồi khớp 100% với JSON Schema Draft-07 (xác thực kiểu dữ liệu, các trường bắt buộc `required` và enum). |
| **6** | **Data-driven Testing (Collection Runner)** | Nạp dữ liệu kiểm thử tham số hóa từ các file JSON trong thư mục `data/` (`fr04_test_data.json`, `fr10_test_data.json`...) để chạy kiểm thử lặp hàng loạt. |
| **7** | **Newman CLI & HTML Extra Reporter** | Tích hợp chạy kiểm thử tự động từ dòng lệnh (CLI), xuất báo cáo trực quan tương tác cao qua plugin `newman-reporter-htmlextra`. |
| **8** | **Chaining Requests & Multi-step Exploit Flows** | Thiết lập chuỗi kịch bản tuần tự: Đăng ký ➔ Đăng nhập trích xuất Token ➔ Gọi API Nghiệp vụ ➔ Gọi API Xác thực dữ liệu. |

---

## 5. THANG ĐO NĂNG LỰC BLOOM-AI (BLOOM-AI TAXONOMY MAPPING)

- **G9.2 (Apply - Ứng dụng):** Cung cấp API Specification cho AI để sinh bộ Test Suite ban đầu (≥ 35 TCs / API) bao phủ Phân vùng tương đương (EP), Giá trị biên (BVA), Bảo mật OWASP (SEC-01..07) và Schema validation.
- **G9.3 (Analyse - Phân tích & Kiểm toán):** Đóng vai trò QA Lead tiến hành rà soát, đánh nhãn `VALID / INVALID / INCOMPLETE` và hiệu chỉnh 100% các ca kiểm thử sai lệch mã trạng thái hoặc lỏng lẻo assertion trong [ai_audit_report.md](ai_audit_report.md).
- **G9.4 (Collaborate - Cộng tác & Đào sâu):** Bổ sung **20 Test Cases nâng cao (Group 5)** đào sâu mã nguồn SUT, bóc tách 16 bugs thực tế và viết bài phản biện học thuật [ai_critique.md](ai_critique.md).
- **G9.5 (Create - Sáng tạo Hệ thống):** Xây dựng Module sinh test tự động [generator/api_test_agent.py](generator/api_test_agent.py), tài liệu thiết kế kiến trúc Mermaid [generator/generator_design.md](generator/generator_design.md), đặc tả Agent Skill [generator/SKILL.md](generator/SKILL.md), và chuẩn hóa hệ thống sang [openapi/eshop_openapi.yaml](openapi/eshop_openapi.yaml).

---

## 6. DANH MỤC BÁO CÁO HTML EXTRA & JSON EXPORT (TOÀN BỘ 4 FRs)

- [Báo cáo HTML FR-04: Quản lý Hồ sơ Cá nhân (470 KB)](reports/FR04_Newman_Report.html) | [Báo cáo JSON](reports/FR04_Newman_Report.json)
- [Báo cáo HTML FR-10: Máy Trạng thái & Hủy Đơn hàng (415 KB)](reports/FR10_Newman_Report.html) | [Báo cáo JSON](reports/FR10_Newman_Report.json)
- [Báo cáo HTML FR-15: Quản lý Sản phẩm Admin (440 KB)](reports/FR15_Newman_Report.html) | [Báo cáo JSON](reports/FR15_Newman_Report.json)
- [Báo cáo HTML FR-09: Áp dụng Mã Giảm Giá Mobile (370 KB)](reports/FR09_Newman_Report.html) | [Báo cáo JSON](reports/FR09_Newman_Report.json)

---

## 7. TỔNG HỢP DANH MỤC ARTIFACTS NỘP BÀI (SUBMISSION DELIVERABLES)

1. **Báo cáo tổng hợp:** [main_report.md](main_report.md)
2. **Báo cáo Kiểm toán AI:** [ai_audit_report.md](ai_audit_report.md) *(Theo biểu mẫu FIT@HCMUS)*
3. **Bài phản biện AI Critique:** [ai_critique.md](ai_critique.md) *(275 từ)*
4. **Bộ Test Cases Excel 6 Sheets:** [test-cases/EShop_TestCases_All.xlsx](test-cases/EShop_TestCases_All.xlsx)
5. **Đặc tả OpenAPI 3.0 YAML:** [openapi/eshop_openapi.yaml](openapi/eshop_openapi.yaml)
6. **Module AI Test Generator:** [generator/generator_design.md](generator/generator_design.md) & [generator/api_test_agent.py](generator/api_test_agent.py) & [generator/SKILL.md](generator/SKILL.md)
7. **Báo cáo CI/CD Pipeline:** [ci-cd/ci_cd_report.md](ci-cd/ci_cd_report.md) & [`.github/workflows/api-tests.yml`](.github/workflows/api-tests.yml)
8. **Thư mục Báo cáo Newman:** [reports/](reports/) *(Đầy đủ 8 file HTML Extra + JSON Export)*
9. **Nhật ký Git Commit:** [git_commit_log.txt](git_commit_log.txt)
10. **Tài liệu README & Bảng Tự chấm 100/100:** [README.md](README.md)
