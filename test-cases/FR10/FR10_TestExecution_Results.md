# FR-10: Báo cáo Kết quả Thực thi Kiểm thử & Phân tích Lỗi (Test Execution Results & Bug Report)

> **Mã chức năng:** FR-10 (Pool B - Order State Machine & Cancellation)  
> **MSSV (X-Student-Id):** `25127001`  
> **Môi trường thực thi:** Localhost (`http://localhost:3000`) | Node.js `v22.19.0` | SQLite3  
> **Công cụ:** Newman `v6.2.2` & `newman-reporter-htmlextra`  
> **File Collection:** [FR10_Order_State_Machine.postman_collection.json](../../collections/FR10_Order_State_Machine.postman_collection.json)  
> **File Báo cáo HTML:** [FR10_Newman_Report.html](../../reports/FR10_Newman_Report.html) (Dung lượng: ~348 KB)  
> **File Báo cáo JSON:** [FR10_Newman_Report.json](../../reports/FR10_Newman_Report.json)

---

## 1. TỔNG QUAN THỐNG KÊ THỰC THI (EXECUTIVE SUMMARY)

| Chỉ số kiểm thử | Giá trị đo lường |
| :--- | :--- |
| **Tổng số Iterations** | 1 |
| **Tổng số Requests đã gửi** | 15 |
| **Tổng số Test Scripts thực thi** | 15 |
| **Tổng số Pre-request Scripts (Gắn Header `X-Student-Id`)** | 15 (100% Passed) |
| **Tổng số Chai Assertions kiểm tra** | 17 |
| **Số Assertions ĐẠT (Passed)** | **16** (94.1%) |
| **Số Assertions KHÔNG ĐẠT (Failed - Bắt Bug SUT)** | **1** (5.9%) |
| **Thời gian phản hồi trung bình (Average Response Time)** | **6 ms** (Min: 1ms, Max: 26ms) |
| **Tổng thời gian chạy bộ test (Total Duration)** | 1381 ms (~1.4 giây) |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG NHÓM TEST CASES

| Nhóm kiểm thử | Số Requests | Số Assertions | Passed | Failed | Đánh giá & Phát hiện |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **0. Setup & Auth Seed** | 6 | 6 | 6 | 0 | Tạo User A, User B và tự động đặt hàng tạo Order A1 & B1 |
| **Group 1: State Valid Transitions** | 2 | 4 | 4 | 0 | Hủy đơn `pending` ➔ chuyển sang `canceled` thành công |
| **Group 2: State Invalid Transitions** | 1 | 1 | 1 | 0 | Hủy lần 2 đơn đã hủy bị chặn với `400 Bad Request` |
| **Group 3: Security & BOLA/IDOR** | 4 | 4 | 3 | **1** | **Bắt lỗ hổng BOLA (SEC-01):** User A xem trộm được đơn của User B |
| **Group 4: Boundary & Schema** | 2 | 2 | 2 | 0 | ID 999999 trả về 404, JSON Schema đơn hàng chuẩn xác |
| **TỔNG CỘNG** | **15** | **17** | **16** | **1** | **Xác thực toàn diện máy trạng thái & bắt lỗ hổng BOLA** |

---

## 3. CHI TIẾT TEST ASSERTION BẮT LỖ HỔNG (FAILURE ANALYSIS)

```
  #  failure         detail                                                                                                           
                                                                                                                                      
 1.  AssertionError  TC_FR10_SEC_02: CRITICAL BOLA - Unauthorized user MUST NOT view other's order (403/404)                          
                     expected 200 to be one of [ 403, 404 ]                                                                           
                     at assertion:0 in test-script                                                                                    
                     inside "Group 3 - Security & BOLA/IDOR / TC_FR10_SEC_02: BOLA on GET - User A views User B's Order (Bug Hunter)" 
```

---

## 4. BÁO CÁO LỖ HỔNG BẢO MẬT & LỖI HỆ THỐNG THEO CHUẨN ISTQB

### BUG 1: [LỖ HỔNG BẢO MẬT NGHIÊM TRỌNG - CRITICAL] Lỗ hổng Broken Object Level Authorization (BOLA/IDOR) trên API Xem chi tiết đơn hàng (SEC-01)
- **Mã Bug:** `BUG_FR10_01`
- **Mức độ nghiêm trọng (Severity):** Critical / Blocker
- **Độ ưu tiên (Priority):** P1 (High)
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 344–349)
  ```javascript
  app.get("/api/orders/:id", (req, res) => {
    db.get("SELECT * FROM orders WHERE id = ?", [req.params.id], (err, order) => {
      if (!order) return res.status(404).json({ error: "Order not found" });
      res.json(order);
    });
  });
  ```
- **Các bước tái hiện (Steps to Reproduce):**
  1. Đăng nhập tài khoản User A lấy Token A.
  2. Tài khoản User B đặt một đơn hàng (ví dụ: `order_id = 5`).
  3. Dùng Token của User A gửi request `GET /api/orders/5`.
- **Kết quả thực tế (Actual Result):** Server trả về `200 OK` kèm toàn bộ dữ liệu đơn hàng nhạy cảm của User B (địa chỉ giao hàng `shipping_address`, tổng tiền `total_amount`, trạng thái đơn).
- **Kết quả kỳ vọng (Expected Result):** Route `GET /api/orders/:id` bắt buộc phải có middleware `authenticateToken` và kiểm tra quyền sở hữu `WHERE id = ? AND (user_id = ? OR req.user.role = 'admin')`, nếu không khớp phải từ chối với `403 Forbidden` hoặc `404 Not Found`.

---

### BUG 2: [LỖI NGHIỆP VỤ - LOGIC BUG] Vi phạm ràng buộc máy trạng thái: Không chặn hủy đơn hàng đang giao (`shipping`)
- **Mã Bug:** `BUG_FR10_02`
- **Mức độ nghiêm trọng (Severity):** High
- **Độ ưu tiên (Priority):** P2
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 328–331)
  ```javascript
  // Lỗi: Chỉ chặn 'delivered' và 'canceled', bỏ sót 'shipping'
  if (order.status === "delivered" || order.status === "canceled") {
    return res.status(400).json({ error: "Cannot cancel this order." });
  }
  ```
- **Kết quả thực tế:** Khi đơn hàng chuyển sang `shipping`, User thường gọi `PUT /api/orders/:id/cancel` thì server vẫn cập nhật sang `canceled`.
- **Kết quả kỳ vọng:** Phải từ chối hủy đơn khi đang vận chuyển (`400 Bad Request`).
