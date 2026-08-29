# BÁO CÁO KẾT QUẢ THỰC THI KIỂM THỬ NEWMAN — FR-10 (ORDER STATE MACHINE)

> **Mã chức năng:** FR-10 | **Pool:** B (Cart & Orders)  
> **Sinh viên:** Nguyễn Nhật Nam | **MSSV:** `23127092`  
> **Công cụ thực thi:** Newman CLI `v6.2.2` & `newman-reporter-htmlextra`  
> **Môi trường:** `http://localhost:3000` (Node.js/Express + SQLite)  
> **Anti-Cheat Header:** `X-Student-Id: 23127092` (100% Request)  
> **File Báo cáo HTML:** [reports/FR10_Newman_Report.html](../../reports/FR10_Newman_Report.html)  

---

## 1. BẢNG TỔNG HỢP THỐNG KÊ THỰC THI (1-TO-1 NEWMAN METRICS)

*Toàn bộ 45 Test Cases được thực thi 1-to-1 thành các request và assertion độc lập:*

| Chỉ số thực thi (Metric) | Giá trị thống kê | Ghi chú & Đánh giá |
| :--- | :---: | :--- |
| **Tổng số Test Cases trong Suite** | **45 TCs** | 40 TCs chuẩn ISTQB + 5 TCs nâng cao (Group 5) |
| **Tổng số Requests thực thi** | **48 Requests** | 3 Requests nạp Token tự động + 45 Requests kiểm thử |
| **Tổng số Assertions kiểm tra** | **52 Assertions** | Kiểm tra State Transitions, BOLA, TOCTOU Race Condition |
| **Số Assertions ĐẠT (Passed)** | **20 Assertions** | Hủy đơn hợp lệ khi `pending`/`confirmed`, từ chối hủy đơn đã hủy |
| **Số Assertions KHÔNG ĐẠT (Failed)**| **32 Assertions** | **Bắt trúng 3 LỖ HỔNG & BUGS THỰC TẾ TRONG SUT** |
| **Thời gian phản hồi trung bình** | **~5 ms / request** | Đạt chuẩn hiệu năng Mobile SLA (< 200ms) |

---

## 2. CHI TIẾT 3 LỖ HỔNG & BUGS PHÁT HIỆN TRONG SUT (FR-10)

### 1. `BUG_FR10_01` (Critical - SEC-01): Lỗ hổng Broken Object Level Authorization (BOLA/IDOR) trên `GET /api/orders/:id`
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 344–349).
- **Hành vi thực tế:** Route `GET /api/orders/:id` hoàn toàn không có middleware xác thực token `authenticateToken` và không kiểm tra quyền sở hữu đơn hàng `user_id`.
- **Hậu quả:** Khách vãng lai và User A có thể xem trọn vẹn thông tin đơn hàng, tổng tiền, địa chỉ giao hàng của User B.

### 2. `BUG_FR10_02` (High - State Machine): Vi phạm Vòng đời Đơn hàng — Cho phép Hủy đơn hàng `shipping`
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 328–331).
- **Hành vi thực tế:** Lập trình viên sử dụng Blacklist kiểm tra `if (order.status === 'delivered' || order.status === 'canceled')` nhưng bỏ quên trạng thái `shipping`.
- **Hậu quả:** Người dùng thông thường có thể hủy các đơn hàng đang trên đường vận chuyển, gây tổn thất nghiêm trọng trong vận hành logistics.

### 3. `BUG_FR10_03` (Medium - Info Disclosure): Dò quét ID Đơn hàng qua Phản hồi Bất đối xứng
- **Vị trí mã nguồn:** `eshop-sut/backend/server.js` (Dòng 323 vs 345).
- **Hành vi thực tế:** Khi truy cập đơn hàng của người khác, PUT trả về `404 Not Found` (có check user_id) nhưng GET trả về `200 OK` (không check user_id).
- **Hậu quả:** Kẻ tấn công có thể lợi dụng sự bất đối xứng này để dò quét toàn bộ dải ID đơn hàng tồn tại trên hệ thống.
