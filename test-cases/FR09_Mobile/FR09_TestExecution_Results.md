# FR-09: Báo cáo Kết quả Thực thi Kiểm thử & Phân tích Lỗi (Test Execution Results & Bug Report)

> **Mã chức năng:** FR-09 (Pool D / Mobile - Apply Coupon Flow)  
> **MSSV (X-Student-Id):** `25127001`  
> **Môi trường thực thi:** Localhost (`http://localhost:3000`) | Node.js `v22.19.0` | SQLite3  
> **Công cụ:** Newman `v6.2.2` & `newman-reporter-htmlextra`  
> **File Collection:** [FR09_Mobile_Coupon.postman_collection.json](../../collections/FR09_Mobile_Coupon.postman_collection.json)  
> **File Báo cáo HTML:** [FR09_Newman_Report.html](../../reports/FR09_Newman_Report.html) (Dung lượng: ~345 KB)  
> **File Báo cáo JSON:** [FR09_Newman_Report.json](../../reports/FR09_Newman_Report.json)

---

## 1. TỔNG QUAN THỐNG KÊ THỰC THI (EXECUTIVE SUMMARY)

| Chỉ số kiểm thử | Giá trị đo lường |
| :--- | :--- |
| **Tổng số Iterations** | 1 |
| **Tổng số Requests đã gửi** | 12 |
| **Tổng số Test Scripts thực thi** | 12 |
| **Tổng số Pre-request Scripts (Gắn Header `X-Student-Id`)** | 12 (100% Passed) |
| **Tổng số Chai Assertions kiểm tra** | 13 |
| **Số Assertions ĐẠT (Passed)** | **11** (84.6%) |
| **Số Assertions KHÔNG ĐẠT (Failed - Bắt trúng Bug SUT)** | **2** (15.4%) |
| **Thời gian phản hồi trung bình (Average Response Time)** | **5 ms** (Min: 2ms, Max: 21ms) |
| **Tổng thời gian chạy bộ test (Total Duration)** | 1033 ms (~1.0 giây) |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG NHÓM TEST CASES

| Nhóm kiểm thử | Số Requests | Số Assertions | Passed | Failed | Đánh giá & Phát hiện |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Group 1: Decision Table (C1 - C5)** | 6 | 7 | 6 | **1** | **Bắt 1 lỗi biên C3:** Đơn hàng bằng đúng giá trị tối thiểu bị từ chối sai |
| **Group 2: Math & Calculation** | 2 | 2 | 1 | **1** | **Bắt 1 lỗi công thức toán học nghiêm trọng:** Chiết khấu ra số âm |
| **Group 3: Domain & Security** | 2 | 2 | 2 | 0 | Chặn code rỗng (400), xử lý SQLi tham số an toàn |
| **Group 4: Schema & Mobile SLA** | 2 | 2 | 2 | 0 | JSON Schema chuẩn xác & Response Time < 200ms (5ms) |
| **TỔNG CỘNG** | **12** | **13** | **11** | **2** | **Bắt trọn vẹn 2 lỗi toán học & logic cốt lõi của FR-09** |

---

## 3. CHI TIẾT 2 ASSERTIONS BẮT TRÚNG BUG SUT

```
  #  failure         detail                                                                                                                           
                                                                                                                                                      
 1.  AssertionError  TC_FR09_COND_07: CRITICAL C3 BOUNDARY - Total EQUAL to min_order_amount MUST return 200 OK                                       
                     expected response to have status code 200 but got 400                                                                            
                     inside "Group 1 / TC_FR09_COND_07: Boundary Equal to Min Order Amount (SAVE10 on 300k - Bug Hunter)" 
                                                                                                                                                      
 2.  AssertionError  TC_FR09_MATH_01: CRITICAL MATH - 10% on 500k MUST yield discount_amount = +50,000                                                
                     expected -4500000 to deeply equal 50000 (Calculated -4.5 million discount!)                                                     
                     inside "Group 2 / TC_FR09_MATH_01: Percent Formula Calculation (Bug Hunter)"
```

---

## 4. BÁO CÁO LỖI HỆ THỐNG THEO CHUẨN ISTQB (BUG REPORTS)

### BUG 1: [LỖI TÍNH TOÁN TOÁN HỌC ĐẶC BIỆT NGHIÊM TRỌNG - CRITICAL] Lỗi công thức tính phần trăm chiết khấu ra số âm khổng lồ
- **Mã Bug:** `BUG_FR09_01`
- **Mức độ nghiêm trọng (Severity):** Critical / Blocker
- **Độ ưu tiên (Priority):** P1 (High)
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 399–401 & 419–421)
  ```javascript
  if (coupon.type === "percent") {
    discount_amount = Math.floor(
      total_amount * (1 - coupon.discount_value),
    );
  }
  ```
- **Các bước tái hiện (Steps to Reproduce):**
  1. Gửi request `POST /api/apply-coupon` với body:
     ```json
     {
       "code": "SAVE10",
       "total_amount": 500000,
       "user_id": 1
     }
     ```
- **Kết quả thực tế (Actual Result):** Với `discount_value = 10`, code tính `500,000 * (1 - 10) = -4,500,000`. Kết quả `discount_amount = -4500000` và `final_amount = 5000000` (khách hàng bị đội giá gấp 10 lần!).
- **Kết quả kỳ vọng (Expected Result):** Công thức đúng bắt buộc phải là:
  ```javascript
  discount_amount = Math.floor(total_amount * (coupon.discount_value / 100));
  ```
  Với đơn 500,000 ₫ và giảm 10%, `discount_amount = 50000` và `final_amount = 450000`.

---

### BUG 2: [LỖI ĐIỀU KIỆN BIÊN NGHIỆP VỤ - HIGH] Lỗi so sánh ngưỡng đơn hàng tối thiểu (`>` thay vì `>=`)
- **Mã Bug:** `BUG_FR09_02`
- **Mức độ nghiêm trọng (Severity):** High
- **Độ ưu tiên (Priority):** P2
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 379)
  ```javascript
  if (total_amount > coupon.min_order_amount) { ... }
  ```
- **Các bước tái hiện (Steps to Reproduce):**
  1. Mã `SAVE10` có `min_order_amount = 300000`.
  2. Gửi request áp dụng mã với `total_amount = 300000` (bằng đúng ngưỡng).
- **Kết quả thực tế (Actual Result):** Server trả về `400 Bad Request` với thông báo `"Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫..."` và từ chối áp dụng mã.
- **Kết quả kỳ vọng (Expected Result):** Theo SRS C3, điều kiện là lớn hơn hoặc bằng (`>=`). Đơn hàng 300,000 ₫ phải được chấp nhận và trả về `200 OK`.
