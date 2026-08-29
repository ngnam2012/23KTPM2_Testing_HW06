# BÁO CÁO KẾT QUẢ THỰC THI KIỂM THỬ NEWMAN — FR-09 (MOBILE APPLY COUPON)

> **Mã chức năng:** FR-09 | **Pool:** D (Mobile Coupons)  
> **Sinh viên:** Nguyễn Nhật Nam | **MSSV:** `23127092`  
> **Công cụ thực thi:** Newman CLI `v6.2.2` & `newman-reporter-htmlextra`  
> **Môi trường:** `http://localhost:3000` (Node.js/Express + SQLite)  
> **Anti-Cheat Header:** `X-Student-Id: 23127092` (100% Request)  
> **File Báo cáo HTML:** [reports/FR09_Newman_Report.html](../../reports/FR09_Newman_Report.html)  

---

## 1. BẢNG TỔNG HỢP THỐNG KÊ THỰC THI (1-TO-1 NEWMAN METRICS)

*Toàn bộ 45 Test Cases được thực thi 1-to-1 thành các request và assertion độc lập:*

| Chỉ số thực thi (Metric) | Giá trị thống kê | Ghi chú & Đánh giá |
| :--- | :---: | :--- |
| **Tổng số Test Cases trong Suite** | **45 TCs** | 40 TCs chuẩn ISTQB + 5 TCs nâng cao (Group 5) |
| **Tổng số Requests thực thi** | **48 Requests** | 3 Requests nạp Token tự động + 45 Requests kiểm thử |
| **Tổng số Assertions kiểm tra** | **50 Assertions** | Kiểm tra Decision Table C1-C5, Math Bug, C3 Boundary |
| **Số Assertions ĐẠT (Passed)** | **22 Assertions** | Áp dụng mã fixed hợp lệ và từ chối mã hết hạn/không tồn tại |
| **Số Assertions KHÔNG ĐẠT (Failed)**| **28 Assertions** | **Bắt trúng 3 LỖ HỔNG & BUGS THỰC TẾ TRONG SUT** |
| **Thời gian phản hồi trung bình** | **~5 ms / request** | Đạt chuẩn hiệu năng Mobile SLA (< 200ms) |

---

## 2. CHI TIẾT 3 LỖ HỔNG & BUGS PHÁT HIỆN TRONG SUT (FR-09)

### 1. `BUG_FR09_01` (Critical - Math Inversion): Lỗi Công thức Tính Phần trăm Chiết khấu Đảo ngược
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 400 & 420).
- **Hành vi thực tế:** Đoạn mã tính `discount_amount = Math.floor(total_amount * (1 - coupon.discount_value));`. Với mã `SAVE10` (10%), `500,000 * (1 - 10) = -4,500,000` ₫.
- **Hậu quả:** Tiền giảm giá bị âm và tổng tiền thanh toán bị đội giá lên 10 lần (thành 5,000,000 ₫).

### 2. `BUG_FR09_02` (High - Condition C3 Boundary): Lỗi Toán tử Ranh giới `>` thay vì `>=`
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 379).
- **Hành vi thực tế:** Kiểm tra `if (total_amount > coupon.min_order_amount)` từ chối các đơn hàng có giá trị bằng đúng ngưỡng tối thiểu với `400 Bad Request`.
- **Hậu quả:** Vi phạm đặc tả SRS FR-09 Điều kiện C3 (*"Tổng giá trị đơn hàng `total_amount >= min_order_amount` (Lớn hơn hoặc BẰNG)"*).

### 3. `BUG_FR09_03` (Medium - Security & Quota): Thiếu Xác thực Token Cho Phép Giả Mạo `user_id`
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 363–364).
- **Hành vi thực tế:** Endpoint `POST /api/apply-coupon` không có JWT authentication và tin tưởng mù quáng `user_id` gửi lên từ body.
- **Hậu quả:** Kẻ xấu có thể thay đổi `user_id` ngẫu nhiên để vượt qua hạn mức số lần sử dụng coupon (`max_uses_per_user`).
