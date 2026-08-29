# BÁO CÁO KẾT QUẢ THỰC THI KIỂM THỬ NEWMAN — FR-04 (PROFILE MANAGEMENT)

> **Mã chức năng:** FR-04 | **Pool:** A (Auth & Users)  
> **Sinh viên:** Nguyễn Nhật Nam | **MSSV:** `23127092`  
> **Công cụ thực thi:** Newman CLI `v6.2.2` & `newman-reporter-htmlextra`  
> **Môi trường:** `http://localhost:3000` (Node.js/Express + SQLite)  
> **Anti-Cheat Header:** `X-Student-Id: 23127092` (100% Request)  
> **File Báo cáo HTML:** [reports/FR04_Newman_Report.html](../../reports/FR04_Newman_Report.html)  

---

## 1. BẢNG TỔNG HỢP THỐNG KÊ THỰC THI (1-TO-1 NEWMAN METRICS)

*Toàn bộ 44 Test Cases được thực thi 1-to-1 thành các request và assertion độc lập:*

| Chỉ số thực thi (Metric) | Giá trị thống kê | Ghi chú & Đánh giá |
| :--- | :---: | :--- |
| **Tổng số Test Cases trong Suite** | **44 TCs** | 39 TCs chuẩn ISTQB + 5 TCs nâng cao (Group 5) |
| **Tổng số Requests thực thi** | **47 Requests** | 3 Requests nạp Token tự động + 44 Requests kiểm thử |
| **Tổng số Assertions kiểm tra** | **59 Assertions** | Kiểm tra Status, Schema, Phone Regex, Role Immutability |
| **Số Assertions ĐẠT (Passed)** | **21 Assertions** | Các ca Happy Path hợp lệ và từ chối token giả mạo |
| **Số Assertions KHÔNG ĐẠT (Failed)**| **38 Assertions** | **Bắt trúng 5 LỖ HỔNG & BUGS THỰC TẾ TRONG SUT** |
| **Thời gian phản hồi trung bình** | **~6 ms / request** | Đạt chuẩn hiệu năng Mobile SLA (< 200ms) |

---

## 2. CHI TIẾT 5 LỖ HỔNG & BUGS PHÁT HIỆN TRONG SUT (FR-04)

### 1. `BUG_FR04_01` (Critical - SEC-06): Lỗ hổng Privilege Escalation qua Mass Assignment
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 124–127).
- **Hành vi thực tế:** Server nhận trường `{"role": "admin"}` từ request PUT của User thường và thực thi câu lệnh SQL `UPDATE users SET role = 'admin' WHERE id = ?`.
- **Hậu quả:** Người dùng thông thường tự leo thang đặc quyền thành Quản trị viên tối cao.

### 2. `BUG_FR04_02` (Medium - Domain): Thiếu Regex Validation Số Điện Thoại
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 118–135).
- **Hành vi thực tế:** Chấp nhận lưu số điện thoại chứa chữ cái hoặc độ dài sai định dạng (9 số, 12 số) và trả về `200 OK`.
- **Hậu quả:** Dữ liệu số điện thoại khách hàng bị sai cấu trúc chuẩn quốc gia `^0[0-9]{9,10}$`.

### 3. `BUG_FR04_03` (High - SEC-07): Rò rỉ Trường Mật khẩu trong `GET /api/users/me`
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 112–116).
- **Hành vi thực tế:** Câu lệnh `SELECT * FROM users WHERE id = ?` trả về cả trường `password` trong JSON response.
- **Hậu quả:** Phơi bày mã băm mật khẩu người dùng cho client.

### 4. `BUG_FR04_04` (High - Data Integrity): Partial Update Xóa Trắng Dữ Liệu Cũ thành `NULL`
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 119–122).
- **Hành vi thực tế:** Gửi payload cập nhật chỉ có `name` (khuyết `phone` và `shipping_address`) làm backend xóa sạch SĐT và địa chỉ cũ thành `NULL`.
- **Hậu quả:** Phá hủy dữ liệu hồ sơ cá nhân của khách hàng.

### 5. `BUG_FR04_05` (High - SEC-07): Rò rỉ Toàn Bộ Metadata An Ninh Tài Khoản
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 113).
- **Hành vi thực tế:** Câu lệnh `SELECT *` làm lộ `reset_token`, `login_attempts`, `locked_until`.
- **Hậu quả:** Kẻ tấn công có thể lấy mã OTP khôi phục mật khẩu mà không cần truy cập email.
