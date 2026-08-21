# FR-04: Báo cáo Kết quả Thực thi Kiểm thử & Phân tích Lỗi (Test Execution Results & Bug Report)

> **Mã chức năng:** FR-04 (Pool A - Profile Management)  
> **MSSV (X-Student-Id):** `25127001`  
> **Môi trường thực thi:** Localhost (`http://localhost:3000`) | Node.js `v22.19.0` | SQLite3  
> **Công cụ:** Newman `v6.2.2` & `newman-reporter-htmlextra`  
> **File Collection:** [FR04_Profile_Management.postman_collection.json](../../collections/FR04_Profile_Management.postman_collection.json)  
> **File Báo cáo HTML:** [FR04_Newman_Report.html](../../reports/FR04_Newman_Report.html) (Dung lượng: ~352 KB)  
> **File Báo cáo JSON:** [FR04_Newman_Report.json](../../reports/FR04_Newman_Report.json)

---

## 1. TỔNG QUAN THỐNG KÊ THỰC THI (EXECUTIVE SUMMARY)

| Chỉ số kiểm thử | Giá trị đo lường |
| :--- | :--- |
| **Tổng số Iterations** | 1 |
| **Tổng số Requests đã gửi** | 16 |
| **Tổng số Test Scripts thực thi** | 16 |
| **Tổng số Pre-request Scripts (Gắn X-Student-Id)** | 16 (100% Passed) |
| **Tổng số Chai Assertions kiểm tra** | 19 |
| **Số Assertions ĐẠT (Passed)** | **13** (68.4%) |
| **Số Assertions KHÔNG ĐẠT (Failed - Bắt trúng Bug SUT)** | **6** (31.6%) |
| **Thời gian phản hồi trung bình (Average Response Time)** | **8 ms** (Min: 1ms, Max: 44ms) |
| **Tổng dung lượng dữ liệu nhận về** | ~1.45 KB |
| **Tổng thời gian chạy bộ test (Total Duration)** | 1525 ms (~1.5 giây) |

---

## 2. BẢNG CHI TIẾT KẾT QUẢ TỪNG NHÓM TEST CASES

| Nhóm kiểm thử | Số Requests | Số Assertions | Passed | Failed | Đánh giá & Phát hiện |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **0. Setup & Auth** | 2 | 2 | 2 | 0 | Đăng ký & Đăng nhập cấp JWT Token thành công |
| **Group 1: Domain EP & BVA** | 7 | 7 | 3 | **4** | **Bắt 4 lỗi:** SUT không validate độ dài và định dạng số điện thoại |
| **Group 2: Security & Auth** | 4 | 4 | 4 | 0 | Chặn đúng Token rác (403), thiếu Auth (401), xử lý an toàn SQLi |
| **Group 3: State & Data Integrity** | 2 | 3 | 2 | **1** | **Bắt 1 lỗi nghiêm trọng:** Sau khi gửi role='admin', role bị đổi thật |
| **Group 4: Schema & Data Leak** | 1 | 3 | 2 | **1** | **Bắt 1 lỗi bảo mật:** API GET làm rò rỉ trường `password` |
| **TỔNG CỘNG** | **16** | **19** | **13** | **6** | **Hoàn thành 100% mục tiêu kiểm thử & tìm ra 3 Bugs thực tế** |

---

## 3. DANH SÁCH CHI TIẾT 6 TEST ASSERTIONS THẤT BẠI (FAILURES)

```
  #  failure         detail                                                                                                        
                                                                                                                                   
 1.  AssertionError  TC_FR04_EP_03: Status code is 400 Bad Request                                                                 
                     expected response to have status code 400 but got 200                                                         
                     inside "Group 1 / TC_FR04_EP_03: Invalid Phone (Not starting with 0)"          
                                                                                                                                   
 2.  AssertionError  TC_FR04_EP_04: Status code is 400 Bad Request                                                                 
                     expected response to have status code 400 but got 200                                                         
                     inside "Group 1 / TC_FR04_EP_04: Invalid Phone with Letters"                   
                                                                                                                                   
 3.  AssertionError  TC_FR04_EP_06: Status code is 400 Bad Request                                                                 
                     expected response to have status code 400 but got 200                                                         
                     inside "Group 1 / TC_FR04_EP_06: BVA Phone 9 Digits (Min-1)"                   
                                                                                                                                   
 4.  AssertionError  TC_FR04_EP_07: Status code is 400 Bad Request                                                                 
                     expected response to have status code 400 but got 200                                                         
                     inside "Group 1 / TC_FR04_EP_07: BVA Phone 12 Digits (Max+1)"                  
                                                                                                                                   
 5.  AssertionError  TC_FR04_STATE_05: CRITICAL - Role MUST remain 'user'                                                          
                     expected 'admin' to deeply equal 'user'                                                                       
                     inside "Group 3 / TC_FR04_STATE_05: Role Immutability Security Assertion"            
                                                                                                                                   
 6.  AssertionError  TC_FR04_SCHEMA_02: SEC-07 Password field MUST NOT be exposed                                                  
                     expected { id: 3, …(9) } to not have property 'password'                                                      
                     inside "Group 4 / TC_FR04_SCHEMA_02: User Profile JSON Schema & No Password Exposure"
```

---

## 4. BÁO CÁO LỖ HỔNG & LỖI HỆ THỐNG THEO CHUẨN ISTQB (BUG REPORTS)

### BUG 1: [LỖ HỔNG NGHIÊM TRỌNG - CRITICAL] Lỗ hổng Privilege Escalation via Mass Assignment (SEC-06)
- **Mã Bug:** `BUG_FR04_01`
- **Mức độ nghiêm trọng (Severity):** Critical / Blocker
- **Độ ưu tiên (Priority):** P1 (High)
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 124–127)
  ```javascript
  if (role) {
    query += ", role = ?";
    params.push(role);
  }
  ```
- **Các bước tái hiện (Steps to Reproduce):**
  1. Đăng nhập tài khoản User thường (`role = 'user'`).
  2. Gửi request `PUT /api/users/me` với payload:
     ```json
     {
       "name": "Attacker User",
       "phone": "0912345678",
       "role": "admin"
     }
     ```
  3. Gửi request `GET /api/users/me` để kiểm tra thông tin tài khoản.
- **Kết quả thực tế (Actual Result):** CSDL SQLite cập nhật trường `role` của tài khoản thành `'admin'`. User thường đã tự leo quyền quản trị tối cao.
- **Kết quả kỳ vọng (Expected Result):** Server phải bỏ qua trường `role` hoặc từ chối sửa `role`, quyền của user bắt buộc phải được giữ nguyên là `'user'`.

---

### BUG 2: [LỖI TRUNG BÌNH - MEDIUM] Thiếu ràng buộc Regex kiểm tra định dạng và độ dài số điện thoại
- **Mã Bug:** `BUG_FR04_02`
- **Mức độ nghiêm trọng (Severity):** Medium
- **Độ ưu tiên (Priority):** P2
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 118–135)
- **Các bước tái hiện (Steps to Reproduce):**
  1. Gửi request `PUT /api/users/me` với các giá trị phone không hợp lệ:
     - Phone bắt đầu bằng số khác 0: `"1912345678"`
     - Phone chứa chữ cái: `"091234567a"`
     - Phone 9 số (thiếu): `"091234567"`
     - Phone 12 số (thừa): `"091234567890"`
- **Kết quả thực tế (Actual Result):** Server trả về `200 OK` và lưu toàn bộ chuỗi không hợp lệ vào database.
- **Kết quả kỳ vọng (Expected Result):** Server phải trả về `400 Bad Request` kèm thông báo lỗi cụ thể khi số điện thoại không thỏa mãn biểu thức chính quy `^0[0-9]{9,10}$`.

---

### BUG 3: [LỖ HỔNG BẢO MẬT - HIGH] Rò rỉ thông tin nhạy cảm (Mật khẩu/Hash) trong API thông tin cá nhân (SEC-07)
- **Mã Bug:** `BUG_FR04_03`
- **Mức độ nghiêm trọng (Severity):** High
- **Độ ưu tiên (Priority):** P1
- **Vị trí trong mã nguồn:** `eshop-sut/backend/server.js` (dòng 113)
  ```javascript
  app.get("/api/users/me", authenticateToken, (req, res) => {
    db.get("SELECT * FROM users WHERE id = ?", [req.user.id], (err, user) => {
      res.json(user);
    });
  });
  ```
- **Các bước tái hiện (Steps to Reproduce):**
  1. Đăng nhập và lấy Bearer Token.
  2. Gửi request `GET /api/users/me`.
  3. Kiểm tra payload JSON trả về.
- **Kết quả thực tế (Actual Result):** Response trả về chứa nguyên trường `password: "$2a$10$..."` (hoặc plain password).
- **Kết quả kỳ vọng (Expected Result):** Câu truy vấn phải loại bỏ trường mật khẩu (`SELECT id, name, email, phone, shipping_address, role, created_at FROM users ...`) để tránh rò rỉ dữ liệu nhạy cảm.

---

## 5. KẾT LUẬN & MINH CHỨNG

- Bộ kiểm thử tự động đã thực hiện thành công trên localhost với thời gian chạy trung bình 8ms/request.
- Báo cáo chi tiết dạng đồ thị HTML tương tác đã được lưu tại [reports/FR04_Newman_Report.html](../../reports/FR04_Newman_Report.html).
- Báo cáo cấu trúc dữ liệu JSON đã được lưu tại [reports/FR04_Newman_Report.json](../../reports/FR04_Newman_Report.json).
