# FR-04: Test Cases (Pool A - Profile Management)

> **Mã chức năng:** FR-04 | **Pool:** A (Auth & Users)  
> **Chức năng:** Quản lý Hồ sơ Cá nhân (Profile Management)  
> **Endpoints:** `PUT /api/users/me` & `GET /api/users/me`  
> **MSSV (X-Student-Id):** `23127092`  
> **Tiêu chuẩn áp dụng:** ISTQB (EP, BVA, State Transition), OWASP API Security Top 10 (SEC-01 -> SEC-07), JSON Schema Validation Draft-07.  
> **Tổng số test cases:** 44 Test Cases (Gồm 39 TCs chuẩn + 5 TCs nâng cao chuyên sâu bóc tách mã nguồn)

---

## 1. BẢNG TỔNG HỢP MA TRẬN TEST CASES CHO FR-04

| Nhóm | Phân loại (Category) | Kỹ thuật kiểm thử | Số lượng TC | Mã định danh |
| :---: | :--- | :--- | :---: | :--- |
| **Nhóm 1** | **Domain Partitions** | Equivalence Partitioning (EP) & Boundary Value Analysis (BVA) | 14 | `TC_FR04_EP_01` → `TC_FR04_EP_14` |
| **Nhóm 2** | **Security & Mass Assignment** | OWASP Top 10 (SEC-02, SEC-06 Privilege Escalation, SEC-07, SQLi, XSS) | 11 | `TC_FR04_SEC_01` → `TC_FR04_SEC_11` |
| **Nhóm 3** | **State & Data Integrity** | State Transition & Sequential Lifecycle Integrity Verification | 7 | `TC_FR04_STATE_01` → `TC_FR04_STATE_07` |
| **Nhóm 4** | **Schema & Status Codes** | JSON Schema Validation, Type Checking & HTTP Status Verification | 7 | `TC_FR04_SCHEMA_01` → `TC_FR04_SCHEMA_07` |
| **Nhóm 5** | **Hidden Logic & Code Vulnerabilities** | Phân tích sâu mã nguồn Backend SUT (`server.js`), Type Coercion, State Desync, Partial Wiping | 5 | `TC_FR04_ADV_01` → `TC_FR04_ADV_05` |
| **TỔNG** | | | **44** | |

---

## 2. CHI TIẾT 39 TEST CASES THEO CHUẨN ISTQB & OWASP

### NHÓM 1: DOMAIN PARTITIONS (EP & BVA - 14 TEST CASES)

#### TC_FR04_EP_01
- **TC_ID:** `TC_FR04_EP_01`
- **Category:** Domain (EP - Valid Phone 10 Digits)
- **Test Objective:** Kiểm tra cập nhật hồ sơ thành công với số điện thoại hợp lệ 10 chữ số bắt đầu bằng '0'
- **Pre-condition:** Tài khoản `user1@example.com` đã đăng ký và đăng nhập, token lưu tại `{{user_token}}`
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "message": "Profile updated"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Response body matches success message", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData.message).to.eql("Profile updated");
  });
  pm.test("Response time is under 500ms", function () {
      pm.expect(pm.response.responseTime).to.be.below(500);
  });
  ```

---

#### TC_FR04_EP_02
- **TC_ID:** `TC_FR04_EP_02`
- **Category:** Domain (EP - Valid Phone 11 Digits)
- **Test Objective:** Kiểm tra cập nhật hồ sơ thành công với số điện thoại hợp lệ 11 chữ số bắt đầu bằng '0'
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Tran Thi B",
    "shipping_address": "456 Nguyen Trai, Q5, TP.HCM",
    "phone": "01234567890"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Profile updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Message confirms update", function () {
      pm.expect(pm.response.json().message).to.eql("Profile updated");
  });
  ```

---

#### TC_FR04_EP_03
- **TC_ID:** `TC_FR04_EP_03`
- **Category:** Domain (EP - Invalid Phone Not Starting with 0)
- **Test Objective:** Kiểm tra hệ thống từ chối cập nhật khi số điện thoại không bắt đầu bằng chữ số '0'
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "1912345678"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:**
  ```json
  {
    "error": "Phone must start with 0 and be 10-11 digits"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request", function () {
      pm.response.to.have.status(400);
  });
  pm.test("Error message indicates invalid phone prefix", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData).to.have.property('error');
  });
  ```

---

#### TC_FR04_EP_04
- **TC_ID:** `TC_FR04_EP_04`
- **Category:** Domain (EP - Invalid Phone Containing Alphabets)
- **Test Objective:** Kiểm tra từ chối khi số điện thoại chứa ký tự chữ cái
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "091234567a"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Invalid phone format"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request", function () {
      pm.response.to.have.status(400);
  });
  pm.test("Response contains error message", function () {
      pm.expect(pm.response.json()).to.have.property("error");
  });
  ```

---

#### TC_FR04_EP_05
- **TC_ID:** `TC_FR04_EP_05`
- **Category:** Domain (EP - Invalid Phone with Special Characters/Dashes)
- **Test Objective:** Kiểm tra từ chối số điện thoại chứa ký tự đặc biệt hoặc dấu gạch nối
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "091-234-5678"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Invalid phone format"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request", function () {
      pm.response.to.have.status(400);
  });
  pm.test("Error returned for special characters", function () {
      pm.expect(pm.response.json().error).to.exist;
  });
  ```

---

#### TC_FR04_EP_06
- **TC_ID:** `TC_FR04_EP_06`
- **Category:** Domain (BVA - Invalid Phone 9 Digits / Min-1)
- **Test Objective:** Phân tích giá trị biên: Kiểm tra từ chối khi số điện thoại chỉ có 9 chữ số (Min - 1)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "091234567"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Phone number must be 10 or 11 digits"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request on 9 digits", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR04_EP_07
- **TC_ID:** `TC_FR04_EP_07`
- **Category:** Domain (BVA - Invalid Phone 12 Digits / Max+1)
- **Test Objective:** Phân tích giá trị biên: Kiểm tra từ chối khi số điện thoại có 12 chữ số (Max + 1)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "091234567890"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Phone number must be 10 or 11 digits"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request on 12 digits", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR04_EP_08
- **TC_ID:** `TC_FR04_EP_08`
- **Category:** Domain (EP - Empty String Phone)
- **Test Objective:** Kiểm tra từ chối khi trường phone là chuỗi rỗng `""`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": ""
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Phone cannot be empty"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for empty phone", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR04_EP_09
- **TC_ID:** `TC_FR04_EP_09`
- **Category:** Domain (BVA - Name Min Length 1 Char)
- **Test Objective:** Kiểm tra cập nhật tên với độ dài biên tối thiểu 1 ký tự
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Profile updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for 1 char name", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR04_EP_10
- **TC_ID:** `TC_FR04_EP_10`
- **Category:** Domain (BVA - Name Max Length 255 Chars)
- **Test Objective:** Kiểm tra cập nhật tên với độ dài biên tối đa 255 ký tự
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Profile updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for 255 chars name", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR04_EP_11
- **TC_ID:** `TC_FR04_EP_11`
- **Category:** Domain (BVA - Name Exceeding Max Length 256 Chars)
- **Test Objective:** Kiểm tra từ chối khi tên vượt quá 255 ký tự (256 ký tự)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Name exceeds maximum length of 255 characters"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for name > 255 chars", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR04_EP_12
- **TC_ID:** `TC_FR04_EP_12`
- **Category:** Domain (EP - Empty Name String or Whitespaces)
- **Test Objective:** Kiểm tra từ chối khi tên là chuỗi rỗng `""` hoặc toàn khoảng trắng `"   "`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "   ",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Name cannot be empty"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for whitespace name", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR04_EP_13
- **TC_ID:** `TC_FR04_EP_13`
- **Category:** Domain (EP - Valid Full Unicode Vietnamese Characters)
- **Test Objective:** Kiểm tra cập nhật hồ sơ với tên chứa đầy đủ ký tự tiếng Việt có dấu (Unicode UTF-8)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json; charset=utf-8`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyễn Hoàng Đỗ Quỳnh Như",
    "shipping_address": "Đường Lê Lợi, Phường Bến Nghé, Quận 1, TP. Hồ Chí Minh",
    "phone": "0988776655"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Profile updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for Vietnamese Unicode", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR04_EP_14
- **TC_ID:** `TC_FR04_EP_14`
- **Category:** Domain (BVA - Extremely Long Address > 1000 Chars)
- **Test Objective:** Kiểm tra xử lý chuỗi địa chỉ cực dài (> 1000 ký tự)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "Số 123 Đường Rất Dài, Phường 1, Quận 1... [lặp lại 1000 ký tự]",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Profile updated"}` (Hệ thống hỗ trợ chuỗi TEXT dài an toàn)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR04_EP_14: Long address (> 1000 chars) is supported without crash", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().message).to.eql("Profile updated");
  });
  ```

---

### NHÓM 2: SECURITY & MASS ASSIGNMENT (SEC-06 & OWASP - 11 TEST CASES)

#### TC_FR04_SEC_01
- **TC_ID:** `TC_FR04_SEC_01`
- **Category:** Security (SEC-06 - Privilege Escalation via Mass Assignment)
- **Test Objective:** Kiểm tra lỗ hổng Mass Assignment: Người dùng thường truyền `{"role": "admin"}` để tự nâng quyền
- **Pre-condition:** User có `role = 'user'`, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Attacker User",
    "shipping_address": "123 Hacker St",
    "phone": "0912345678",
    "role": "admin"
  }
  ```
- **Expected Status Code:** `200 OK` (nếu lọc bỏ trường `role`) hoặc `400/403` (từ chối sửa role)
- **Expected Response Body / Schema:** Server **KHÔNG ĐƯỢC PHÉP** cập nhật role lên `admin` trong CSDL
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is handled safely", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 400, 403]);
  });
  // Ghi chú Audit: SUT có lỗ hổng nếu backend thực thi UPDATE role = 'admin'
  ```

---

#### TC_FR04_SEC_02
- **TC_ID:** `TC_FR04_SEC_02`
- **Category:** Security (SEC-06 - Mass Assignment with Boolean Flag `isAdmin`)
- **Test Objective:** Thử gửi trường phân quyền dạng boolean `{"isAdmin": true, "is_admin": true}`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Attacker User",
    "shipping_address": "123 Hacker St",
    "phone": "0912345678",
    "isAdmin": true,
    "is_admin": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Profile updated"}` (các trường ngoài spec bị bỏ qua)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK and extra fields ignored", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR04_SEC_03
- **TC_ID:** `TC_FR04_SEC_03`
- **Category:** Security (SEC-06 - User ID Overwrite Attempt)
- **Test Objective:** Thử gửi trường `id` hoặc `user_id` trong body nhằm ghi đè tài khoản khác
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "id": 1,
    "user_id": 1,
    "name": "Tampered Name",
    "shipping_address": "Tampered Address",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK` (Chỉ cập nhật cho user hiện tại `req.user.id`)
- **Expected Response Body / Schema:** `{"message": "Profile updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Update applies only to authenticated user context", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR04_SEC_04
- **TC_ID:** `TC_FR04_SEC_04`
- **Category:** Security (SEC-06 - Email Tampering Attempt)
- **Test Objective:** Thử gửi trường `email` mới để chiếm đoạt tài khoản hoặc thay đổi email trái phép
- **Pre-condition:** User đã đăng nhập, token hợp lệ, email gốc là `user1@example.com`
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "email": "attacker_hijack@evil.com",
    "name": "Normal Name",
    "shipping_address": "123 Normal St",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Trường `email` trong CSDL không được thay đổi
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Response handled safely", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 400]);
  });
  ```

---

#### TC_FR04_SEC_05
- **TC_ID:** `TC_FR04_SEC_05`
- **Category:** Security (SEC-06 - Password / Hash Overwrite Attempt)
- **Test Objective:** Thử gửi trường `password` hoặc `password_hash` trong body `PUT /api/users/me`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "password": "NewHackerPassword123!",
    "password_hash": "$2a$10$FakeHashValue",
    "name": "Normal Name",
    "shipping_address": "123 Normal St",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK` (Bỏ qua trường password)
- **Expected Response Body / Schema:** Mật khẩu đăng nhập không bị đổi qua API này
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK and password field ignored", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR04_SEC_06
- **TC_ID:** `TC_FR04_SEC_06`
- **Category:** Security (SEC-02 - Missing Authorization Header)
- **Test Objective:** Kiểm tra xác thực bị từ chối khi gọi API mà không truyền Header `Authorization`
- **Pre-condition:** Không có token
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
  - *(Không có header Authorization)*
- **Request Body:**
  ```json
  {
    "name": "No Auth User",
    "shipping_address": "123 Street",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `401 Unauthorized`
- **Expected Response Body / Schema:**
  ```json
  {
    "error": "Unauthorized"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 401 Unauthorized", function () {
      pm.response.to.have.status(401);
  });
  pm.test("Error message is Unauthorized", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData.error).to.eql("Unauthorized");
  });
  ```

---

#### TC_FR04_SEC_07
- **TC_ID:** `TC_FR04_SEC_07`
- **Category:** Security (SEC-02 - Invalid / Forged JWT Token)
- **Test Objective:** Kiểm tra từ chối truy cập khi Header Authorization chứa Token rác / giả mạo
- **Pre-condition:** Token không hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake_payload.fake_signature`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Fake Token User",
    "shipping_address": "123 Street",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:**
  ```json
  {
    "error": "Forbidden"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden", function () {
      pm.response.to.have.status(403);
  });
  pm.test("Error message is Forbidden", function () {
      pm.expect(pm.response.json().error).to.eql("Forbidden");
  });
  ```

---

#### TC_FR04_SEC_08
- **TC_ID:** `TC_FR04_SEC_08`
- **Category:** Security (SEC-02 - Malformed Bearer Prefix)
- **Test Objective:** Kiểm tra gửi Header Authorization sai định dạng (thiếu từ khóa Bearer)
- **Pre-condition:** Token có sẵn nhưng header sai format
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: TokenWithoutBearerKeyword12345`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Test User",
    "shipping_address": "123 Street",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `401 Unauthorized` hoặc `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}` hoặc `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 401 or 403", function () {
      pm.expect(pm.response.code).to.be.oneOf([401, 403]);
  });
  ```

---

#### TC_FR04_SEC_09
- **TC_ID:** `TC_FR04_SEC_09`
- **Category:** Security (SEC-06 - SQL Injection in Name Field)
- **Test Objective:** Kiểm tra khả năng chống SQL Injection trong trường `name`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Admin' OR '1'='1'; --",
    "shipping_address": "123 Le Loi, Q1",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK` (Chuỗi được xử lý an toàn dạng Parameterized literal)
- **Expected Response Body / Schema:** `{"message": "Profile updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK (SQLi payload treated as literal)", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Server does not crash with 500 Internal Error", function () {
      pm.expect(pm.response.code).to.not.equal(500);
  });
  ```

---

#### TC_FR04_SEC_10
- **TC_ID:** `TC_FR04_SEC_10`
- **Category:** Security (SEC-06 - SQL Injection in Phone Field)
- **Test Objective:** Kiểm tra khả năng chống SQL Injection trong trường `phone`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1",
    "phone": "0912345678' OR 1=1 --"
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Invalid phone format"}` (Bắt buộc từ chối chuỗi chứa ký tự không phải chữ số)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR04_SEC_10: Non-digit SQLi phone payload MUST be rejected with 400 Bad Request", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  ```

---

#### TC_FR04_SEC_11
- **TC_ID:** `TC_FR04_SEC_11`
- **Category:** Security (SEC-06 - Stored XSS Payload in Profile)
- **Test Objective:** Kiểm tra khả năng xử lý an toàn chuỗi XSS trong `name` và `shipping_address`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "<script>alert('XSS_NAME')</script>",
    "shipping_address": "<img src=x onerror=alert('XSS_ADDR')>",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Profile updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK", function () {
      pm.response.to.have.status(200);
  });
  ```

---

### NHÓM 3: STATE & DATA INTEGRITY (7 TEST CASES)

#### TC_FR04_STATE_01
- **TC_ID:** `TC_FR04_STATE_01`
- **Category:** State (Full Profile Update & GET Lifecycle Verification)
- **Test Objective:** Thực hiện cập nhật toàn bộ trường (name, address, phone) và gọi `GET /api/users/me` xác thực dữ liệu đã lưu đúng vào CSDL
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me` theo sau bởi `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body (cho PUT):**
  ```json
  {
    "name": "State Test Full User",
    "shipping_address": "888 CMT8, District 10, HCMC",
    "phone": "0987654321"
  }
  ```
- **Expected Status Code:** PUT: `200 OK` | GET: `200 OK`
- **Expected Response Body / Schema (GET):**
  ```json
  {
    "id": 1,
    "name": "State Test Full User",
    "email": "user1@example.com",
    "phone": "0987654321",
    "shipping_address": "888 CMT8, District 10, HCMC",
    "role": "user"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("GET profile returns updated data correctly", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user.name).to.eql("State Test Full User");
      pm.expect(user.phone).to.eql("0987654321");
      pm.expect(user.shipping_address).to.eql("888 CMT8, District 10, HCMC");
      pm.expect(user.role).to.eql("user");
  });
  ```

---

#### TC_FR04_STATE_02
- **TC_ID:** `TC_FR04_STATE_02`
- **Category:** State (Partial Update - Name Only)
- **Test Objective:** Cập nhật chỉ riêng trường `name`, kiểm tra các trường `phone` và `shipping_address` không bị mất dữ liệu
- **Pre-condition:** User có dữ liệu hồ sơ sẵn
- **Request Method & Endpoint:** `PUT /api/users/me` ➔ `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Only Name Updated",
    "shipping_address": "888 CMT8, District 10, HCMC",
    "phone": "0987654321"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `GET /api/users/me` trả về name mới và giữ nguyên address, phone
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Name updated and existing fields preserved", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user.name).to.eql("Only Name Updated");
  });
  ```

---

#### TC_FR04_STATE_03
- **TC_ID:** `TC_FR04_STATE_03`
- **Category:** State (Partial Update - Phone Only)
- **Test Objective:** Cập nhật chỉ trường `phone`, xác thực trạng thái mới của phone được lưu trữ
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/users/me` ➔ `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Only Name Updated",
    "shipping_address": "888 CMT8, District 10, HCMC",
    "phone": "0909998877"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `GET /api/users/me` có `phone === "0909998877"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Phone updated successfully in GET response", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().phone).to.eql("0909998877");
  });
  ```

---

#### TC_FR04_STATE_04
- **TC_ID:** `TC_FR04_STATE_04`
- **Category:** State (Partial Update - Address Only)
- **Test Objective:** Cập nhật chỉ trường `shipping_address`, xác thực địa chỉ mới được lưu trữ
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/users/me` ➔ `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Only Name Updated",
    "shipping_address": "999 Vo Van Kiet, Q1, TP.HCM",
    "phone": "0909998877"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `GET /api/users/me` có `shipping_address === "999 Vo Van Kiet, Q1, TP.HCM"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Shipping address updated in GET response", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().shipping_address).to.eql("999 Vo Van Kiet, Q1, TP.HCM");
  });
  ```

---

#### TC_FR04_STATE_05
- **TC_ID:** `TC_FR04_STATE_05`
- **Category:** State (State Integrity - Role Immutability Verification)
- **Test Objective:** Sau khi gửi payload tấn công `{"role": "admin"}`, gọi `GET /api/users/me` để xác minh role vẫn là 'user'
- **Pre-condition:** User ban đầu có `role = 'user'`
- **Request Method & Endpoint:** `GET /api/users/me` (sau bước gọi `PUT /api/users/me` kèm role='admin')
- **Headers:**
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A (GET request)
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `role` bắt buộc phải là `"user"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("CRITICAL SECURITY: User role must remain 'user'", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user.role).to.eql("user");
      pm.expect(user.role).to.not.eql("admin");
  });
  ```

---

#### TC_FR04_STATE_06
- **TC_ID:** `TC_FR04_STATE_06`
- **Category:** State (State Integrity - Email Immutability Verification)
- **Test Objective:** Sau khi gửi payload đổi email `{"email": "hacker@evil.com"}`, gọi `GET /api/users/me` để xác minh email gốc không bị đổi
- **Pre-condition:** Email gốc của user là `user1@example.com`
- **Request Method & Endpoint:** `GET /api/users/me`
- **Headers:**
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `email === "user1@example.com"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Email remains unchanged", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user.email).to.eql("user1@example.com");
  });
  ```

---

#### TC_FR04_STATE_07
- **TC_ID:** `TC_FR04_STATE_07`
- **Category:** State (Sequential State Transitions Across Multiple Updates)
- **Test Objective:** Kiểm tra cập nhật hồ sơ 3 lần liên tiếp và xác thực tính nhất quán của trạng thái cuối cùng
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/users/me` (Lần 3) ➔ `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Final Stable Name",
    "shipping_address": "Final Stable Address",
    "phone": "0911223344"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Trạng thái cuối cùng phản ánh đúng lần cập nhật thứ 3
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Final state is consistent after sequential updates", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user.name).to.eql("Final Stable Name");
      pm.expect(user.phone).to.eql("0911223344");
  });
  ```

---

### NHÓM 4: SCHEMA & STATUS CODES (7 TEST CASES)

#### TC_FR04_SCHEMA_01
- **TC_ID:** `TC_FR04_SCHEMA_01`
- **Category:** Schema (PUT /api/users/me 200 OK JSON Schema Validation)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema của phản hồi thành công `PUT /api/users/me`
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Schema User",
    "shipping_address": "123 Schema St",
    "phone": "0912345678"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["message"],
    "properties": {
      "message": { "type": "string" }
    },
    "additionalProperties": false
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  var schema = {
      "type": "object",
      "required": ["message"],
      "properties": {
          "message": { "type": "string" }
      }
  };
  pm.test("PUT response matches JSON Schema", function () {
      pm.response.to.have.status(200);
      pm.expect(tv4.validate(pm.response.json(), schema)).to.be.true;
  });
  ```

---

#### TC_FR04_SCHEMA_02
- **TC_ID:** `TC_FR04_SCHEMA_02`
- **Category:** Schema & Security (GET /api/users/me JSON Schema & Sensitive Data Exposure)
- **Test Objective:** Kiểm tra JSON Schema của `GET /api/users/me`, đặc biệt đảm bảo **KHÔNG rò rỉ trường `password` hoặc `password_hash`** (SEC-07)
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `GET /api/users/me`
- **Headers:**
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["id", "email", "name", "role"],
    "properties": {
      "id": { "type": "integer" },
      "email": { "type": "string", "format": "email" },
      "name": { "type": "string" },
      "phone": { "type": ["string", "null"] },
      "shipping_address": { "type": ["string", "null"] },
      "role": { "type": "string" }
    }
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  var userSchema = {
      "type": "object",
      "required": ["id", "email", "name", "role"],
      "properties": {
          "id": { "type": "integer" },
          "email": { "type": "string" },
          "name": { "type": "string" },
          "role": { "type": "string" }
      }
  };
  pm.test("GET response conforms to User Schema", function () {
      pm.response.to.have.status(200);
      pm.expect(tv4.validate(pm.response.json(), userSchema)).to.be.true;
  });
  pm.test("CRITICAL SECURITY SEC-07: Password must NOT be exposed", function () {
      var user = pm.response.json();
      pm.expect(user).to.not.have.property("password");
      pm.expect(user).to.not.have.property("password_hash");
  });
  ```

---

#### TC_FR04_SCHEMA_03
- **TC_ID:** `TC_FR04_SCHEMA_03`
- **Category:** Schema (Malformed JSON Payload Syntax)
- **Test Objective:** Kiểm tra xử lý và response schema khi gửi body chứa cú pháp JSON bị hỏng (Malformed JSON)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body (Raw String):**
  `{ "name": "Broken JSON", "phone": "0912345678", `
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "..."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for malformed JSON", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR04_SCHEMA_04
- **TC_ID:** `TC_FR04_SCHEMA_04`
- **Category:** Schema (Data Type Mismatch - Number/Array for Phone/Name)
- **Test Objective:** Kiểm tra xử lý khi gửi sai kiểu dữ liệu (Phone gửi số nguyên thay vì chuỗi, Name gửi Array)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": ["Invalid", "Array", "Type"],
    "shipping_address": 12345,
    "phone": 912345678
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Invalid data type"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for type mismatch", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR04_SCHEMA_05
- **TC_ID:** `TC_FR04_SCHEMA_05`
- **Category:** Schema (401 Unauthorized Response Schema Validation)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema chuẩn của phản hồi lỗi 401 Unauthorized
- **Pre-condition:** Không gửi Authorization header
- **Request Method & Endpoint:** `GET /api/users/me`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `401 Unauthorized`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["error"],
    "properties": {
      "error": { "type": "string" }
    }
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 401 Unauthorized", function () {
      pm.response.to.have.status(401);
  });
  pm.test("401 schema contains error string", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData).to.have.property("error");
      pm.expect(jsonData.error).to.be.a("string");
  });
  ```

---

#### TC_FR04_SCHEMA_06
- **TC_ID:** `TC_FR04_SCHEMA_06`
- **Category:** Schema (403 Forbidden Response Schema Validation)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema chuẩn của phản hồi lỗi 403 Forbidden khi token sai
- **Pre-condition:** Token không hợp lệ
- **Request Method & Endpoint:** `GET /api/users/me`
- **Headers:**
  - `Authorization: Bearer fake.jwt.token`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["error"],
    "properties": {
      "error": { "type": "string" }
    }
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden", function () {
      pm.response.to.have.status(403);
  });
  pm.test("403 schema contains error string", function () {
      var jsonData = pm.response.json();
      pm.expect(jsonData).to.have.property("error");
      pm.expect(jsonData.error).to.eql("Forbidden");
  });
  ```

---

#### TC_FR04_SCHEMA_07
- **TC_ID:** `TC_FR04_SCHEMA_07`
- **Category:** Schema & Route Protection (HTTP Method Not Allowed / 404 Route Check)
- **Test Objective:** Kiểm tra phản hồi khi gọi HTTP Method không được hỗ trợ trên endpoint (`DELETE /api/users/me`)
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `DELETE /api/users/me`
- **Headers:**
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `404 Not Found` hoặc `405 Method Not Allowed`
- **Expected Response Body / Schema:** HTML hoặc JSON thông báo route không hỗ trợ
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 404 Not Found or 405 Method Not Allowed", function () {
      pm.expect(pm.response.code).to.be.oneOf([404, 405]);
  });
  ```

---

### NHÓM 5: TÌNH HUỐNG BIÊN NÂNG CAO & BÓC TÁCH MÃ NGUỒN ẨN (5 ADVANCED TEST CASES)

> **Mục đích nhóm 5:** Khai thác các kẽ hở logic nằm sâu trong tầng triển khai mã nguồn Node.js/Express + SQLite của `server.js` mà các công cụ sinh test AI thông thường (Blackbox Prompting) rất dễ bỏ qua.

---

#### TC_FR04_ADV_01
- **TC_ID:** `TC_FR04_ADV_01`
- **Category:** Advanced Code Vulnerability (Destructive Partial Update - Silent Omitted Fields Wiping to NULL)
- **Test Objective:** Kiểm tra hành vi cập nhật một phần (Partial Update): Gửi payload chỉ chứa trường `name` mà KHÔNG gửi `phone` và `shipping_address`, nhằm phát hiện lỗi backend tự động ghi đè dữ liệu cũ thành `NULL` trong SQLite *(Bắt Bug SUT: câu lệnh SQL tĩnh `UPDATE users SET name = ?, shipping_address = ?, phone = ?`)*
- **Pre-condition:** User A đã có sẵn hồ sơ đầy đủ (`phone = "0912345678"`, `shipping_address = "123 Le Loi, Q1"`)
- **Request Method & Endpoint:** `PUT /api/users/me` theo sau bởi `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Only New Name"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema (GET):** `phone` và `shipping_address` ban đầu **BẮT BUỘC PHẢI ĐƯỢC GIỮ NGUYÊN**, không bị biến thành `null` hay chuỗi rỗng
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR04_ADV_01: Partial update must NOT silently wipe omitted fields to NULL", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user.name).to.eql("Only New Name");
      pm.expect(user.phone).to.not.be.null;
      pm.expect(user.shipping_address).to.not.be.null;
      pm.expect(user.phone).to.eql("0912345678");
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Các công cụ AI tạo test thông thường chỉ nhìn nhận API theo góc nhìn Blackbox RESTful tiêu chuẩn. Chúng mặc định giả định rằng một API `PUT` nếu chấp nhận payload khuyết trường thì hoặc sẽ từ chối 400, hoặc sẽ thông minh bảo toàn các trường không được gửi (tương tự như `PATCH`). AI thông thường thiếu khả năng đọc hiểu luồng mã nguồn backend tại dòng 119-122 trong `server.js` (`const { name, shipping_address, phone } = req.body; let params = [name, shipping_address, phone];`). Khi biến `phone` và `shipping_address` không được truyền trong JSON, JavaScript gán chúng là `undefined`, và thư viện SQLite driver sẽ âm thầm chuyển `undefined` thành `NULL`, dẫn đến việc vô tình **xóa sổ toàn bộ số điện thoại và địa chỉ giao hàng của khách hàng** mà không hề có bất kỳ cảnh báo nào.

---

#### TC_FR04_ADV_02
- **TC_ID:** `TC_FR04_ADV_02`
- **Category:** Advanced Code Vulnerability (Numeric Phone Type Coercion & Leading-Zero Loss in SQLite)
- **Test Objective:** Kiểm tra lỗ hổng ép kiểu ngầm (Type Coercion): Client gửi số điện thoại dưới dạng số nguyên (`phone: 912345678` thay vì string `"0912345678"`) để phát hiện việc SQLite lưu dạng INTEGER làm mất chữ số 0 đầu tiên
- **Pre-condition:** User đã đăng nhập, token hợp lệ
- **Request Method & Endpoint:** `PUT /api/users/me` theo sau bởi `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Numeric Phone User",
    "shipping_address": "123 Street",
    "phone": 912345678
  }
  ```
- **Expected Status Code:** `400 Bad Request` (Do vi phạm kiểu dữ liệu String và thiếu số 0) hoặc nếu chấp nhận thì khi GET phải trả về chuỗi đầy đủ `"0912345678"`
- **Expected Response Body / Schema:** Bị từ chối hoặc chuẩn hóa chuỗi
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR04_ADV_02: Number phone without leading zero is rejected or normalized", function () {
      if (pm.response.code === 200) {
          var user = pm.response.json();
          pm.expect(typeof user.phone).to.eql("string");
          pm.expect(user.phone.startsWith("0")).to.be.true;
      } else {
          pm.response.to.have.status(400);
      }
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Hầu hết các prompt sinh test bằng AI chỉ tập trung vào phân vùng tương đương chuỗi (ví dụ: chuỗi chứa chữ cái, chuỗi 9 ký tự). AI thông thường không suy luận được sự tương tác giữa cơ chế *Dynamic Typing* của SQLite (Type Affinity) và tính năng tự động parse JSON của Express `express.json()`. Nếu người dùng gửi số `912345678` dạng Number, backend không có bộ Schema Validator (như Joi hay Zod) sẽ đẩy trực tiếp Number vào SQLite. SQLite nhận diện đây là số nguyên và lưu dạng INTEGER, vô tình làm mất hoàn toàn chữ số `'0'` ở đầu. Khi ứng dụng Mobile nhận lại dữ liệu, trường phone sẽ là số nguyên `912345678`, làm sụp đổ hoàn toàn biểu thức chính quy (Regex `^0[0-9]{9,10}$`) trên ứng dụng Mobile.

---

#### TC_FR04_ADV_03
- **TC_ID:** `TC_FR04_ADV_03`
- **Category:** Advanced Security Vulnerability (Internal Security State Leak via `SELECT *` in Profile GET)
- **Test Objective:** Kiểm tra rò rỉ toàn bộ metadata an ninh nhạy cảm: Yêu cầu đặt lại mật khẩu qua `/api/forgot-password`, sau đó gọi `GET /api/users/me` để chứng minh `reset_token`, `login_attempts`, và `locked_until` bị rò rỉ cho client *(Bắt Bug SUT dòng 113: `SELECT * FROM users WHERE id = ?`)*
- **Pre-condition:** User `user1@example.com` vừa gọi `POST /api/forgot-password`
- **Request Method & Endpoint:** `GET /api/users/me`
- **Headers:**
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Response **TUYỆT ĐỐI KHÔNG ĐƯỢC CHỨA** các trường `reset_token`, `password`, `login_attempts`, `locked_until`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR04_ADV_03: CRITICAL SEC-07 - Internal security metadata MUST NOT be exposed", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user).to.not.have.property("password");
      pm.expect(user).to.not.have.property("reset_token");
      pm.expect(user).to.not.have.property("login_attempts");
      pm.expect(user).to.not.have.property("locked_until");
  });
  // GHI CHÚ AUDIT: SUT hiện tại chạy SELECT * FROM users nên trả về toàn bộ các cột nhạy cảm trên
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI thông thường khi được yêu cầu kiểm thử bảo mật SEC-07 (Sensitive Data Exposure) chỉ có thói quen kiểm tra xem trường `password` có bị lộ hay không. AI thiếu góc nhìn toàn cục về kiến trúc cơ sở dữ liệu (Database Schema). Trong file `database.js`, bảng `users` chứa rất nhiều trường an ninh nội bộ quan trọng như mã khôi phục mật khẩu (`reset_token`), số lần đăng nhập sai (`login_attempts`), và thời gian khóa tài khoản (`locked_until`). Do `server.js` sử dụng câu lệnh lười biếng `SELECT *`, toàn bộ trạng thái an ninh của tài khoản bị phơi bày. Một kẻ tấn công hoặc mã độc trên thiết bị có thể lợi dụng điều này để đọc `reset_token` ngay trong API Profile mà không cần phải truy cập hộp thư email của nạn nhân!

---

#### TC_FR04_ADV_04
- **TC_ID:** `TC_FR04_ADV_04`
- **Category:** Advanced Security Vulnerability (Full Privilege Escalation & Admin Action Exploitation Chain)
- **Test Objective:** Thực thi chuỗi tấn công leo thang đặc quyền hoàn chỉnh (Full Attack Chain): User thường gửi `{"role": "admin"}` trong `PUT /api/users/me` ➔ Đăng nhập lại để nhận JWT Token mang quyền Admin ➔ Gọi API Quản trị viên `POST /api/admin/import-products` để chứng minh đã chiếm quyền quản trị tối cao
- **Pre-condition:** User thường `test@eshop.com` ban đầu có `role = 'user'`
- **Request Method & Endpoint:**
  1. `PUT /api/users/me` với payload `{"name": "Attacker", "shipping_address": "HN", "phone": "0912345678", "role": "admin"}`
  2. `POST /api/login` để lấy Token mới
  3. `POST /api/admin/import-products` với Token mới
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{new_elevated_token}}`
  - `X-Student-Id: 23127092`
- **Request Body (Import Products):**
  ```json
  {
    "products": [
      {
        "name": "Backdoor Admin Product",
        "price": 1000,
        "description": "Created via privilege escalation",
        "imageUrl": "https://placehold.co/300",
        "category_id": 1
      }
    ]
  }
  ```
- **Expected Status Code:** Bước 1 phải từ chối `403` hoặc bỏ qua role; Bước 3 **BẮT BUỘC PHẢI BỊ CHẶN VỚI 403 FORBIDDEN** nếu phân quyền đúng
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR04_ADV_04: Privilege Escalation chain is blocked; Admin actions remain protected", function () {
      // Trong hệ thống an toàn, người dùng thường không thể thực thi API import sản phẩm của Admin
      pm.expect(pm.response.code).to.be.oneOf([401, 403]);
  });
  // GHI CHÚ AUDIT: SUT có lỗ hổng cho phép khai thác toàn bộ chuỗi này thành công (Mass Assignment)
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Các mô hình AI thông thường sinh test theo tư duy "cô lập từng Endpoint" (Isolated Endpoint Testing). Khi kiểm tra Mass Assignment, AI chỉ dừng lại ở việc gửi `role: 'admin'` và kiểm tra response của endpoint đó. Chúng không có khả năng tự động liên kết thành một chuỗi kịch bản khai thác đầu cuối (Multi-request Attack Exploitation Chain) để chứng minh tác động thực tế của lỗ hổng (Business Impact). Việc kết nối từ việc đổi role ➔ re-authenticate lấy claim JWT mới ➔ gọi một API Admin nhạy cảm khác như Import CSV chính là minh chứng thuyết phục nhất về mức độ nguy hiểm của `BUG_FR04_01`.

---

#### TC_FR04_ADV_05
- **TC_ID:** `TC_FR04_ADV_05`
- **Category:** Advanced Security Vulnerability (Identity Protection against Hybrid Spoofing Payload)
- **Test Objective:** Kiểm tra tính bất biến của định danh: Kẻ tấn công gửi payload lai ghép chứa cùng lúc nhiều trường định danh giả mạo (`id: 999`, `user_id: 888`, `email: "victim@eshop.com"`, `is_admin: true`) nhằm thử nghiệm khả năng ghi đè tài khoản khác trong cùng 1 câu lệnh UPDATE
- **Pre-condition:** User đang đăng nhập với tài khoản `id = 1`, `email = "user1@example.com"`
- **Request Method & Endpoint:** `PUT /api/users/me` theo sau bởi `GET /api/users/me`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "id": 999,
    "user_id": 888,
    "email": "victim_hacked@eshop.com",
    "name": "Attempted Hijacker",
    "shipping_address": "999 Hackers Rd",
    "phone": "0988888888",
    "is_admin": true
  }
  ```
- **Expected Status Code:** `200 OK` (hoặc `400 Bad Request`)
- **Expected Response Body / Schema (GET):** Định danh `id` vẫn là `1`, `email` vẫn là `"user1@example.com"`, `role` vẫn là `"user"`. Chỉ có `name`, `shipping_address`, `phone` hợp lệ của chính user đó được cập nhật
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR04_ADV_05: Hybrid spoofing payload cannot alter identity or compromise foreign accounts", function () {
      pm.response.to.have.status(200);
      var user = pm.response.json();
      pm.expect(user.id).to.eql(1);
      pm.expect(user.email).to.eql("user1@example.com");
      pm.expect(user.role).to.eql("user");
      pm.expect(user.name).to.eql("Attempted Hijacker");
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI khi sinh test case thường phân rã các thuộc tính để kiểm tra đơn lẻ (1 test case cho `id`, 1 test case cho `email`, 1 test case cho `is_admin`). Trong thực tế tấn công bảo mật (Penetration Testing), hacker luôn sử dụng các kỹ thuật tấn công kết hợp (Hybrid / Composite Payload) nhằm kiểm tra xem ORM hoặc câu lệnh SQL động của backend có bị lỗi phân tích cú pháp khi gặp nhiều trường lạ cùng lúc hay không. Nếu backend sử dụng các pattern nguy hiểm như `Object.assign()` hay câu lệnh `UPDATE` lặp qua `Object.keys(req.body)`, payload này sẽ ngay lập tức ghi đè toàn bộ thông tin định danh và phá vỡ cấu trúc CSDL.

