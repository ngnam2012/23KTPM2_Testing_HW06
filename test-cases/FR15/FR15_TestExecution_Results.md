# FR-15: Báo cáo Kết quả Thực thi Kiểm thử & Phân tích Lỗi (Test Execution Results & Bug Report)

> **Mã chức năng:** FR-15 (Pool C - Web Admin Product CRUD)  
> **MSSV (X-Student-Id):** `25127001`  
> **Môi trường thực thi:** Localhost (`http://localhost:3000`) | Node.js `v22.19.0` | SQLite3  
> **Công cụ:** Newman `v6.2.2` & `newman-reporter-htmlextra`  
> **File Collection:** [FR15_Admin_Product_CRUD.postman_collection.json](../../collections/FR15_Admin_Product_CRUD.postman_collection.json)  
> **File Báo cáo HTML:** [FR15_Newman_Report.html](../../reports/FR15_Newman_Report.html) (Dung lượng: ~350 KB)  
> **File Báo cáo JSON:** [FR15_Newman_Report.json](../../reports/FR15_Newman_Report.json)

---

## 1. TỔNG QUAN THỐNG KÊ THỰC THI (EXECUTIVE SUMMARY)

| Chỉ số kiểm thử | Giá trị đo lường |
| :--- | :--- |
| **Tổng số Iterations** | 1 |
| **Tổng số Requests đã gửi** | 15 |
| **Tổng số Test Scripts thực thi** | 15 |
| **Tổng số Pre-request Scripts (Gắn Header `X-Student-Id`)** | 15 (100% Passed) |
| **Tổng số Chai Assertions kiểm tra** | 16 |
| **Số Assertions ĐẠT (Passed)** | **8** (50.0%) |
| **Số Assertions KHÔNG ĐẠT (Failed - Bắt trúng Bug SUT)** | **8** (50.0%) |
| **Thời gian phản hồi trung bình (Average Response Time)** | **7 ms** (Min: 2ms, Max: 20ms) |
| **Tổng thời gian chạy bộ test (Total Duration)** | 1323 ms (~1.3 giây) |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG NHÓM TEST CASES

| Nhóm kiểm thử | Số Requests | Số Assertions | Passed | Failed | Đánh giá & Phát hiện |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **0. Setup & Auth** | 2 | 2 | 2 | 0 | Đăng nhập Admin & User thường lấy Token thành công |
| **Group 1: Broken Access Control** | 4 | 4 | 1 | **3** | **Bắt 3 lỗ hổng nghiêm trọng:** Cả 3 route Admin hoàn toàn không check Auth/Role |
| **Group 2: Domain & Boundary Values** | 3 | 3 | 0 | **3** | **Bắt 3 lỗi Domain:** Server chấp nhận giá âm, giá 0, tên rỗng |
| **Group 3: Type Coercion & Schema** | 3 | 4 | 2 | **2** | **Bắt 2 lỗi:** Ép kiểu price thành chuỗi ở ID chẵn & 404 trả về 200 |
| **Group 4: CRUD Lifecycle & Integrity** | 3 | 3 | 3 | 0 | Vòng đời Thêm/Sửa/Xóa Admin và xử lý SQLi an toàn |
| **TỔNG CỘNG** | **15** | **16** | **8** | **8** | **Hoàn thành 100% mục tiêu & phát hiện 4 nhóm Bugs lớn** |

---

## 3. DANH SÁCH 8 ASSERTIONS THẤT BẠI (FAILURES & BUG CAPTURES)

```
  #  failure         detail                                                                                                               
                                                                                                                                          
 1.  AssertionError  TC_FR15_BAC_01: CRITICAL SEC-03 - Unauthenticated POST MUST return 401                                               
                     expected response to have status code 401 but got 200                                                                
                     inside "Group 1 / TC_FR15_BAC_01: Unauthenticated POST Product (Bug Hunter)" 
                                                                                                                                          
 2.  AssertionError  TC_FR15_BAC_04: CRITICAL BFLA - Regular user MUST return 403 Forbidden                                               
                     expected response to have status code 403 but got 200                                                                
                     inside "Group 1 / TC_FR15_BAC_04: Regular User POST Product (Bug Hunter)"    
                                                                                                                                          
 3.  AssertionError  TC_FR15_BAC_10: Forged token rejected with 403                                                                       
                     expected response to have status code 403 but got 200                                                                
                     inside "Group 1 / TC_FR15_BAC_10: Forged Token on POST"                      
                                                                                                                                          
 4.  AssertionError  TC_FR15_DOM_01: Price 0 rejected with 400 Bad Request                                                                
                     expected response to have status code 400 but got 200                                                                
                     inside "Group 2 / TC_FR15_DOM_01: Zero Price Rejection"                                   
                                                                                                                                          
 5.  AssertionError  TC_FR15_DOM_02: Negative price rejected with 400                                                                     
                     expected response to have status code 400 but got 200                                                                
                     inside "Group 2 / TC_FR15_DOM_02: Negative Price Rejection"                               
                                                                                                                                          
 6.  AssertionError  TC_FR15_DOM_06: Empty name rejected with 400                                                                         
                     expected response to have status code 400 but got 200                                                                
                     inside "Group 2 / TC_FR15_DOM_06: Empty Name Rejection"                                   
                                                                                                                                          
 7.  AssertionError  TC_FR15_TYPE_01: CRITICAL - Price MUST be number not string                                                          
                     expected '28000000' to be a number (got string)                                                                      
                     inside "Group 3 / TC_FR15_TYPE_01: Even ID Price Type Coercion Bug Check"        
                                                                                                                                          
 8.  AssertionError  TC_FR15_SCHEMA_05: Non-existent product MUST return 404 Not Found                                                    
                     expected response to have status code 404 but got 200 (returned {})                                                  
                     inside "Group 3 / TC_FR15_SCHEMA_05: Non-existent Product 404 Status Check"
```

---

## 4. BÁO CÁO LỖ HỔNG & LỖI HỆ THỐNG THEO CHUẨN ISTQB (BUG REPORTS)

### BUG 1: [LỖ HỔNG BẢO MẬT ĐẶC BIỆT NGHIÊM TRỌNG - CRITICAL] Lỗ hổng Broken Access Control / BFLA (SEC-03 & SEC-05)
- **Mã Bug:** `BUG_FR15_01`
- **Mức độ nghiêm trọng (Severity):** Critical / Blocker
- **Độ ưu tiên (Priority):** P1 (High)
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 167, 179, 191)
  ```javascript
  app.post("/api/products", (req, res) => { ... });
  app.put("/api/products/:id", (req, res) => { ... });
  app.delete("/api/products/:id", (req, res) => { ... });
  ```
- **Hành vi thực tế:** Cả 3 route quản trị sản phẩm **hoàn toàn không gắn middleware `authenticateToken`** và không kiểm tra `role === 'admin'`. Khách vãng lai và người dùng thường có thể tự do Thêm, Sửa, Xóa bất kỳ sản phẩm nào trên sàn thương mại điện tử!
- **Hành vi kỳ vọng:** Bắt buộc phải thêm middleware xác thực và phân quyền: `app.post("/api/products", authenticateToken, requireAdmin, ...)`.

---

### BUG 2: [LỖI ÉP KIỂU NGẦM - MEDIUM/HIGH] Ép kiểu dữ liệu `price` thành chuỗi ở các sản phẩm có ID chẵn (Type Coercion Bug)
- **Mã Bug:** `BUG_FR15_02`
- **Mức độ nghiêm trọng (Severity):** High
- **Độ ưu tiên (Priority):** P2
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 162)
  ```javascript
  app.get("/api/products/:id", (req, res) => {
    db.get("SELECT * FROM products WHERE id = ?", [req.params.id], (err, row) => {
      if (!row) return res.status(200).json({});
      if (row.id % 2 === 0) row.price = row.price.toString();
      res.json(row);
    });
  });
  ```
- **Hành vi thực tế:** Khi gọi `GET /api/products/2` (hoặc ID chẵn 4, 6, 8), giá tiền bị biến thành chuỗi `"28000000"` thay vì số nguyên `28000000`. Điều này phá vỡ JSON Schema của các ứng dụng Mobile/Frontend và gây lỗi tính toán toán học.
- **Hành vi kỳ vọng:** Thuộc tính `price` bắt buộc phải luôn luôn là kiểu `number`.

---

### BUG 3: [LỖI THIẾU VALIDATION DỮ LIỆU ĐẦU VÀO - MEDIUM] Chấp nhận giá tiền âm, giá bằng 0 và tên rỗng
- **Mã Bug:** `BUG_FR15_03`
- **Mức độ nghiêm trọng (Severity):** Medium
- **Độ ưu tiên (Priority):** P2
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 167–176)
- **Hành vi thực tế:** Gửi `price: -50000`, `price: 0`, hoặc `name: ""` thì server vẫn trả về `200 OK` và lưu vào database SQLite.
- **Hành vi kỳ vọng:** Server phải kiểm tra `if (!name || price <= 0)` và trả về `400 Bad Request`.

---

### BUG 4: [LỖI HTTP STATUS CODE - LOW/MEDIUM] Trả về 200 OK với object rỗng `{}` khi xem sản phẩm không tồn tại
- **Mã Bug:** `BUG_FR15_04`
- **Mức độ nghiêm trọng (Severity):** Medium
- **Độ ưu tiên (Priority):** P3
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 161)
  ```javascript
  if (!row) return res.status(200).json({});
  ```
- **Hành vi thực tế:** `GET /api/products/999999` trả về HTTP `200 OK` với body `{}`.
- **Hành vi kỳ vọng:** Phải trả về HTTP `404 Not Found` kèm `{"error": "Product not found"}`.
