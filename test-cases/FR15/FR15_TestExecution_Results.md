# BÁO CÁO KẾT QUẢ THỰC THI KIỂM THỬ NEWMAN — FR-15 (ADMIN PRODUCT CRUD)

> **Mã chức năng:** FR-15 | **Pool:** C (Web Admin CRUD)  
> **Sinh viên:** Nguyễn Nhật Nam | **MSSV:** `23127092`  
> **Công cụ thực thi:** Newman CLI `v6.2.2` & `newman-reporter-htmlextra`  
> **Môi trường:** `http://localhost:3000` (Node.js/Express + SQLite)  
> **Anti-Cheat Header:** `X-Student-Id: 23127092` (100% Request)  
> **File Báo cáo HTML:** [reports/FR15_Newman_Report.html](../../reports/FR15_Newman_Report.html)  

---

## 1. BẢNG TỔNG HỢP THỐNG KÊ THỰC THI (1-TO-1 NEWMAN METRICS)

*Toàn bộ 45 Test Cases được thực thi 1-to-1 thành các request và assertion độc lập:*

| Chỉ số thực thi (Metric) | Giá trị thống kê | Ghi chú & Đánh giá |
| :--- | :---: | :--- |
| **Tổng số Test Cases trong Suite** | **45 TCs** | 40 TCs chuẩn ISTQB + 5 TCs nâng cao (Group 5) |
| **Tổng số Requests thực thi** | **48 Requests** | 3 Requests nạp Token tự động + 45 Requests kiểm thử |
| **Tổng số Assertions kiểm tra** | **50 Assertions** | Kiểm tra Broken Access Control, Type Coercion, Domain BVA |
| **Số Assertions ĐẠT (Passed)** | **22 Assertions** | Thao tác CRUD hợp lệ của Admin và kiểm tra schema |
| **Số Assertions KHÔNG ĐẠT (Failed)**| **28 Assertions** | **Bắt trúng 5 LỖ HỔNG & BUGS THỰC TẾ TRONG SUT** |
| **Thời gian phản hồi trung bình** | **~5 ms / request** | Đạt chuẩn hiệu năng hệ thống quản trị |

---

## 2. CHI TIẾT 5 LỖ HỔNG & BUGS PHÁT HIỆN TRONG SUT (FR-15)

### 1. `BUG_FR15_01` (Critical - SEC-03/SEC-05): Broken Access Control trên Cả 3 Route Admin
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 167, 179, 191).
- **Hành vi thực tế:** Các route `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id` hoàn toàn không có middleware `authenticateToken`.
- **Hậu quả:** Khách vãng lai chưa đăng nhập vẫn có thể thêm, sửa, xóa toàn bộ sản phẩm trên hệ thống.

### 2. `BUG_FR15_02` (High - Type Coercion): Ép kiểu `price` thành chuỗi ở ID chẵn
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 162).
- **Hành vi thực tế:** Đoạn mã `if (row.id % 2 === 0) row.price = row.price.toString();` biến giá tiền thành chuỗi `'28000000'`.
- **Hậu quả:** Phá vỡ JSON Schema kiểu dữ liệu số, gây lỗi ghép chuỗi khi tính toán tổng tiền trên app mobile/web.

### 3. `BUG_FR15_03` (Medium - Domain): Chấp nhận Giá tiền Âm và Giá bằng 0
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 167–189).
- **Hành vi thực tế:** Server chấp nhận lưu sản phẩm với đơn giá âm (`-50000`) và tên rỗng.
- **Hậu quả:** Kẻ xấu có thể tạo sản phẩm giá âm để trừ tiền giỏ hàng khi thanh toán.

### 4. `BUG_FR15_04` (Medium - Schema): `GET /api/products/999999` Trả về `200 OK` với `{}`
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 161).
- **Hành vi thực tế:** `if (!row) return res.status(200).json({});` trả về mã 200 OK thay vì `404 Not Found`.
- **Hậu quả:** Vi phạm tiêu chuẩn RESTful API, khiến client không bắt được lỗi trong khối `catch()`.

### 5. `BUG_FR15_05` (High - SEC-06): SQL Injection trong Search Query Làm Lộ HTML 500
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 144–149).
- **Hành vi thực tế:** Nối chuỗi `${searchQuery}` trực tiếp trong câu lệnh SQL `LIKE '%...%'`. Khi gặp ký tự `'`, server trả về trang HTML lỗi `<h1>Database Error</h1>`.
- **Hậu quả:** Lỗ hổng SQL Injection và rò rỉ cấu trúc lỗi hệ thống cho kẻ tấn công.
