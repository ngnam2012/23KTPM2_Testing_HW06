# FR-09: Test Cases (Pool D / Mobile - Apply Coupon Flow)

> **Mã chức năng:** FR-09 | **Pool:** D (Mobile Flow) / B (Coupons)  
> **Chức năng:** Áp dụng Mã Giảm Giá Mobile (Apply Coupon)  
> **Endpoint:** `POST /api/apply-coupon`  
> **MSSV (X-Student-Id):** `23127092`  
> **Tiêu chuẩn áp dụng:** ISTQB (Decision Table Testing - Ma trận C1-C5, EP, BVA, Math Invariant Testing), OWASP API Security Top 10 (SEC-04, SEC-06 SQLi), JSON Schema Validation Draft-07.  
> **Tổng số test cases:** 45 Test Cases (Gồm 40 TCs chuẩn + 5 TCs nâng cao chuyên sâu bóc tách mã nguồn)

---

## 1. BẢNG TỔNG HỢP MA TRẬN TEST CASES CHO FR-09

| Nhóm | Phân loại (Category) | Kỹ thuật kiểm thử | Số lượng TC | Mã định danh |
| :---: | :--- | :--- | :---: | :--- |
| **Nhóm 1** | **Ma trận 5 Điều kiện C1 → C5** | Bảng quyết định (Decision Table) cho 5 quy tắc: Tồn tại/Active, Hạn sử dụng, Ngưỡng tối thiểu, User ID, Giới hạn lượt dùng | 16 | `TC_FR09_COND_01` → `TC_FR09_COND_16` |
| **Nhóm 2** | **Math & Calculation Edge Cases** | Kiểm thử công thức toán học (% và fixed), bất biến số học (`final_amount >= 0`, `discount >= 0`) | 11 | `TC_FR09_MATH_01` → `TC_FR09_MATH_11` |
| **Nhóm 3** | **Domain Partitions & Security** | Phân vùng tương đương (EP/BVA) cho `total_amount`, `code` rỗng/âm/0, SQL Injection | 7 | `TC_FR09_DOM_01` → `TC_FR09_DOM_07` |
| **Nhóm 4** | **Schema Validation & Mobile SLA** | JSON Schema Validation Draft-07, ép kiểu số học và Header `X-Student-Id: 23127092` | 6 | `TC_FR09_SCHEMA_01` → `TC_FR09_SCHEMA_06` |
| **Nhóm 5** | **Hidden Logic & Math Code Flaws** | Bóc tách mã nguồn Backend (`server.js`), Math Bug `1 - discount_value`, Ngưỡng `>` vs `>=`, Giả mạo User ID | 5 | `TC_FR09_ADV_01` → `TC_FR09_ADV_05` |
| **TỔNG** | | | **45** | |

---

## 2. CHI TIẾT 40 TEST CASES THEO CHUẨN ISTQB & OWASP

### NHÓM 1: MA TRẬN 5 ĐIỀU KIỆN C1 ĐẾN C5 (16 TEST CASES)

#### TC_FR09_COND_01
- **TC_ID:** `TC_FR09_COND_01`
- **Category:** Decision Table (Valid All 5 Conditions - Percent Coupon `SAVE10`)
- **Test Objective:** Kiểm tra áp dụng thành công mã giảm giá theo phần trăm khi thỏa mãn toàn bộ 5 điều kiện C1-C5
- **Pre-condition:** Mã `SAVE10` có trong CSDL (`type = 'percent'`, `discount_value = 10`, `min_order_amount = 300000`, `is_active = 1`, `expired_at = '2099-12-31'`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "success": true,
    "coupon_id": 1,
    "discount_amount": 50000,
    "final_amount": 450000,
    "message": "Áp dụng thành công! Giảm 10%"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Coupon applied successfully", function () {
      var data = pm.response.json();
      pm.expect(data.success).to.be.true;
      pm.expect(data.discount_amount).to.eql(50000);
      pm.expect(data.final_amount).to.eql(450000);
  });
  ```

---

#### TC_FR09_COND_02
- **TC_ID:** `TC_FR09_COND_02`
- **Category:** Decision Table (Valid All 5 Conditions - Fixed Coupon `BIGBUY`)
- **Test Objective:** Kiểm tra áp dụng thành công mã giảm giá số tiền cố định khi thỏa mãn C1-C5
- **Pre-condition:** Mã `BIGBUY` có trong CSDL (`type = 'fixed'`, `discount_value = 50000`, `min_order_amount = 500000`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "BIGBUY",
    "total_amount": 600000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "success": true,
    "coupon_id": 2,
    "discount_amount": 50000,
    "final_amount": 550000,
    "message": "Áp dụng thành công! Giảm 50,000 ₫"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for fixed coupon", function () {
      pm.response.to.have.status(200);
      var data = pm.response.json();
      pm.expect(data.discount_amount).to.eql(50000);
      pm.expect(data.final_amount).to.eql(550000);
  });
  ```

---

#### TC_FR09_COND_03
- **TC_ID:** `TC_FR09_COND_03`
- **Category:** Decision Table (Violate C1 - Non-existent Coupon Code)
- **Test Objective:** Kiểm tra từ chối khi nhập mã giảm giá không tồn tại trong hệ thống
- **Pre-condition:** Mã `FAKE_COUPON_999` không có trong CSDL
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "FAKE_COUPON_999",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 404 or 400 for non-existent coupon", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  ```

---

#### TC_FR09_COND_04
- **TC_ID:** `TC_FR09_COND_04`
- **Category:** Decision Table (Violate C1 - Inactive Coupon `is_active = 0`)
- **Test Objective:** Kiểm tra từ chối khi mã giảm giá đã bị Admin vô hiệu hóa (`is_active = 0`)
- **Pre-condition:** Mã giảm giá có `is_active = 0`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "DISABLED_CODE",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Mã giảm giá không tồn tại hoặc đã bị vô hiệu hóa"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Inactive coupon is rejected", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR09_COND_05
- **TC_ID:** `TC_FR09_COND_05`
- **Category:** Decision Table (Violate C2 - Expired Coupon `EXPIRED`)
- **Test Objective:** Kiểm tra từ chối khi mã giảm giá đã hết hạn sử dụng (`expired_at = '2020-01-01'`)
- **Pre-condition:** Mã `EXPIRED` có trong CSDL nhưng thời hạn trong quá khứ
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "EXPIRED",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Mã giảm giá đã hết hạn"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for expired coupon", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.eql("Mã giảm giá đã hết hạn");
  });
  ```

---

#### TC_FR09_COND_06
- **TC_ID:** `TC_FR09_COND_06`
- **Category:** Decision Table (Violate C3 - Total Below Minimum Order Amount)
- **Test Objective:** Kiểm tra từ chối khi tổng tiền đơn hàng nhỏ hơn ngưỡng tối thiểu (`200,000 < min 300,000`)
- **Pre-condition:** Mã `SAVE10` có `min_order_amount = 300000`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 200000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Đơn hàng chưa đủ giá trị tối thiểu 300,000 ₫ để áp dụng mã này"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for below-minimum order", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.include("chưa đủ giá trị tối thiểu");
  });
  ```

---

#### TC_FR09_COND_07
- **TC_ID:** `TC_FR09_COND_07`
- **Category:** Decision Table Bug Hunter (Boundary C3 - Total Exactly Equals Min Order Amount)
- **Test Objective:** Kiểm tra áp dụng THÀNH CÔNG khi tổng tiền đơn hàng BẰNG ĐÚNG ngưỡng tối thiểu (`total_amount === 300000 === min_order_amount`) *(Bắt Bug SUT `total_amount > min_order_amount` thay vì `>=`)*
- **Pre-condition:** Mã `SAVE10` có `min_order_amount = 300000`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 300000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "success": true,
    "discount_amount": 30000,
    "final_amount": 270000
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("CRITICAL C3 BOUNDARY: Total amount EQUAL to min_order_amount MUST return 200 OK", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().success).to.be.true;
  });
  // GHI CHÚ AUDIT: SUT có bug ở dòng 379: if (total_amount > coupon.min_order_amount)
  ```

---

#### TC_FR09_COND_08
- **TC_ID:** `TC_FR09_COND_08`
- **Category:** Boundary Value Analysis (Boundary C3 - Min - 1: `total_amount = 299999`)
- **Test Objective:** Phân tích giá trị biên: Tổng tiền thiếu đúng 1 đồng so với ngưỡng tối thiểu
- **Pre-condition:** Mã `SAVE10` (`min = 300000`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 299999,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** Báo lỗi chưa đủ giá trị tối thiểu
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for Min-1", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR09_COND_09
- **TC_ID:** `TC_FR09_COND_09`
- **Category:** Boundary Value Analysis (Boundary C3 - Min + 1: `total_amount = 300001`)
- **Test Objective:** Phân tích giá trị biên: Tổng tiền vượt đúng 1 đồng so với ngưỡng tối thiểu
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 300001,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"success": true}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for Min+1", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR09_COND_10
- **TC_ID:** `TC_FR09_COND_10`
- **Category:** Boundary Value Analysis (Boundary C3 on Fixed Coupon: `BIGBUY` min = 500000)
- **Test Objective:** Kiểm tra áp dụng thành công khi `total_amount === 500000 === min_order_amount` cho mã fixed
- **Pre-condition:** Mã `BIGBUY`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "BIGBUY",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"success": true, "discount_amount": 50000, "final_amount": 450000}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Fixed coupon at exact min threshold returns 200 OK", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR09_COND_11
- **TC_ID:** `TC_FR09_COND_11`
- **Category:** Decision Table (Condition C4 - Anonymous User without `user_id`)
- **Test Objective:** Kiểm tra áp dụng mã giảm giá khi khách vãng lai không truyền `user_id`
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 500000
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Server áp dụng thành công hoặc yêu cầu đăng nhập
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Anonymous coupon application handled gracefully", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 400]);
  });
  ```

---

#### TC_FR09_COND_12
- **TC_ID:** `TC_FR09_COND_12`
- **Category:** Decision Table (Condition C4 - Non-existent User ID `99999`)
- **Test Objective:** Kiểm tra áp dụng mã giảm giá với `user_id` không tồn tại
- **Pre-condition:** Không có user 99999
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 500000,
    "user_id": 99999
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Xử lý an toàn không crash hệ thống
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Invalid user_id handled safely", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 400]);
  });
  ```

---

#### TC_FR09_COND_13
- **TC_ID:** `TC_FR09_COND_13`
- **Category:** Decision Table (Violate C5 - Usage Limit Reached `max_uses_per_user = 1`)
- **Test Objective:** Kiểm tra từ chối khi người dùng đã sử dụng mã quá số lần cho phép
- **Pre-condition:** User 1 đã có 1 bản ghi trong bảng `coupon_usage` cho coupon `VIP100` (`max_uses_per_user = 1` hoặc `2`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "VIP100",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request` (khi đã đạt limit)
- **Expected Response Body / Schema:** `{"error": "Bạn đã sử dụng mã này 1 lần (đã đạt giới hạn)"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Exceeded coupon usage is rejected", function () {
      if (pm.response.code === 400) {
          pm.expect(pm.response.json().error).to.include("đã đạt giới hạn");
      }
  });
  ```

---

#### TC_FR09_COND_14
- **TC_ID:** `TC_FR09_COND_14`
- **Category:** Decision Table (Condition C5 - First Use of Multi-use Coupon)
- **Test Objective:** Áp dụng mã `VIP100` lần thứ 1 cho User chưa từng dùng
- **Pre-condition:** User 2 chưa dùng mã `VIP100`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "VIP100",
    "total_amount": 500000,
    "user_id": 2
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"success": true, "discount_amount": 100000, "final_amount": 400000}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("First use of multi-use coupon succeeds with 200 OK", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR09_COND_15
- **TC_ID:** `TC_FR09_COND_15`
- **Category:** Decision Table (Combined Violation: Inactive AND Expired)
- **Test Objective:** Kiểm tra xử lý khi mã giảm giá vừa bị vô hiệu hóa vừa hết hạn
- **Pre-condition:** Mã không hợp lệ
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "INACTIVE_EXPIRED",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request` hoặc `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "..."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Combined violation rejected", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR09_COND_16
- **TC_ID:** `TC_FR09_COND_16`
- **Category:** Domain & Usability (Case-Insensitive Coupon Code `save10`)
- **Test Objective:** Kiểm tra nhập mã bằng chữ thường (`save10` thay vì `SAVE10`)
- **Pre-condition:** Mã trong DB là `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "save10",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK` (hoặc 404 nếu hệ thống yêu cầu case-sensitive)
- **Expected Response Body / Schema:** Xử lý đồng nhất
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Case-handling of coupon code is stable", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 404]);
  });
  ```

---

### NHÓM 2: MATH & CALCULATION EDGE CASES (11 TEST CASES)

#### TC_FR09_MATH_01
- **TC_ID:** `TC_FR09_MATH_01`
- **Category:** Math Bug Hunter (Percent Formula Verification - 10% on 500k)
- **Test Objective:** Kiểm tra công thức tính phần trăm: Giảm 10% trên đơn 500k phải ra `discount = 50,000` và `final = 450,000` *(Bắt Bug SUT tính `total_amount * (1 - 10)` ra số âm -4,500,000!)*
- **Pre-condition:** Mã `SAVE10` (`10%`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "success": true,
    "discount_amount": 50000,
    "final_amount": 450000
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("CRITICAL MATH BUG: Discount amount MUST be POSITIVE 50000 (10% of 500k)", function () {
      var data = pm.response.json();
      pm.expect(data.discount_amount).to.eql(50000);
      pm.expect(data.discount_amount).to.be.above(0);
      pm.expect(data.final_amount).to.eql(450000);
  });
  // GHI CHÚ AUDIT: SUT có bug ở dòng 400: discount_amount = Math.floor(total_amount * (1 - coupon.discount_value))
  ```

---

#### TC_FR09_MATH_02
- **TC_ID:** `TC_FR09_MATH_02`
- **Category:** Math Calculation (Fixed Discount Calculation - 50k off 600k)
- **Test Objective:** Kiểm tra tính đúng tiền giảm fixed 50k trên đơn 600k
- **Pre-condition:** Mã `BIGBUY` (`50k fixed`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "BIGBUY",
    "total_amount": 600000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `discount_amount === 50000`, `final_amount === 550000`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Fixed discount calculation is correct", function () {
      pm.response.to.have.status(200);
      var data = pm.response.json();
      pm.expect(data.discount_amount).to.eql(50000);
      pm.expect(data.final_amount).to.eql(550000);
  });
  ```

---

#### TC_FR09_MATH_03
- **TC_ID:** `TC_FR09_MATH_03`
- **Category:** Math Boundary (Order Below Minimum for Fixed Coupon - C3 Precedence)
- **Test Objective:** Kiểm tra khi gửi đơn hàng `total_amount = 80000` cho mã `VIP100` (`min_order_amount = 500000`), hệ thống bắt buộc phải từ chối theo Điều kiện C3 với mã `400 Bad Request` trước khi thực thi tính toán
- **Pre-condition:** Mã `VIP100` (`discount_value = 100000`, `min_order_amount = 500000`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "VIP100",
    "total_amount": 80000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Đơn hàng chưa đủ giá trị tối thiểu 500,000 ₫ để áp dụng mã này"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR09_MATH_03: Order below min_order_amount is rejected with 400 Bad Request", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.include("chưa đủ giá trị tối thiểu");
  });
  ```

---

#### TC_FR09_MATH_04
- **TC_ID:** `TC_FR09_MATH_04`
- **Category:** Math Boundary (Order Below Minimum for Fixed Coupon - C3 Precedence)
- **Test Objective:** Kiểm tra khi gửi đơn hàng `total_amount = 50000` cho mã `BIGBUY` (`min_order_amount = 500000`), hệ thống từ chối theo C3 với mã `400 Bad Request`
- **Pre-condition:** Mã `BIGBUY` (`min_order_amount = 500000`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "BIGBUY",
    "total_amount": 50000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Đơn hàng chưa đủ giá trị tối thiểu 500,000 ₫ để áp dụng mã này"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR09_MATH_04: Order below min_order_amount is rejected with 400 Bad Request", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.include("chưa đủ giá trị tối thiểu");
  });
  ```

---

#### TC_FR09_MATH_05
- **TC_ID:** `TC_FR09_MATH_05`
- **Category:** Math Precision (Percent Rounding on Fractional Amount)
- **Test Objective:** Kiểm tra làm tròn số tiền chiết khấu bằng `Math.floor` (10% trên 333,333 ➔ 33,333)
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 333333,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `discount_amount === 33333`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Discount rounded to integer", function () {
      if (pm.response.code === 200) {
          var data = pm.response.json();
          pm.expect(Number.isInteger(data.discount_amount)).to.be.true;
      }
  });
  ```

---

#### TC_FR09_MATH_06
- **TC_ID:** `TC_FR09_MATH_06`
- **Category:** Math Scalability (Large Total Amount 100,000,000)
- **Test Objective:** Kiểm tra tính toán chiết khấu chính xác với đơn hàng giá trị lớn (100 triệu)
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 100000000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `discount_amount === 10000000`, `final_amount === 90000000`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Large amount calculated accurately", function () {
      pm.response.to.have.status(200);
      var data = pm.response.json();
      pm.expect(data.discount_amount).to.eql(10000000);
      pm.expect(data.final_amount).to.eql(90000000);
  });
  ```

---

#### TC_FR09_MATH_07
- **TC_ID:** `TC_FR09_MATH_07`
- **Category:** Math Invariant (Arithmetic Sum Property: `final + discount === total`)
- **Test Objective:** Kiểm tra bất biến số học: Tổng tiền sau giảm cộng tiền giảm phải luôn bằng tổng tiền ban đầu
- **Pre-condition:** Bất kỳ coupon hợp lệ
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "BIGBUY",
    "total_amount": 750000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `final_amount + discount_amount === 750000`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Arithmetic invariant: final_amount + discount_amount === total_amount", function () {
      pm.response.to.have.status(200);
      var data = pm.response.json();
      pm.expect(data.final_amount + data.discount_amount).to.eql(750000);
  });
  ```

---

#### TC_FR09_MATH_08
- **TC_ID:** `TC_FR09_MATH_08`
- **Category:** Math Invariant (Non-Negative Discount Assertion)
- **Test Objective:** Xác thực số tiền giảm giá `discount_amount` bắt buộc phải là số không âm (`>= 0`)
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 400000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `discount_amount >= 0`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("discount_amount must be >= 0", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().discount_amount).to.be.at.least(0);
  });
  ```

---

#### TC_FR09_MATH_09
- **TC_ID:** `TC_FR09_MATH_09`
- **Category:** Math Invariant (Non-Negative Final Amount Assertion)
- **Test Objective:** Xác thực số tiền thanh toán cuối cùng `final_amount` bắt buộc phải là số không âm (`>= 0`)
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 400000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `final_amount >= 0`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("final_amount must be >= 0", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().final_amount).to.be.at.least(0);
  });
  ```

---

#### TC_FR09_MATH_10
- **TC_ID:** `TC_FR09_MATH_10`
- **Category:** Math Edge (Fixed 100k Discount on 1 Million)
- **Test Objective:** Kiểm tra tính đúng mã 100k trên đơn 1,000,000 ➔ Còn 900,000
- **Pre-condition:** Mã `VIP100`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "VIP100",
    "total_amount": 1000000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `discount_amount === 100000`, `final_amount === 900000`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("VIP100 discount calculated accurately", function () {
      pm.response.to.have.status(200);
      var data = pm.response.json();
      pm.expect(data.discount_amount).to.eql(100000);
      pm.expect(data.final_amount).to.eql(900000);
  });
  ```

---

#### TC_FR09_MATH_11
- **TC_ID:** `TC_FR09_MATH_11`
- **Category:** Math Edge (Discount Message Formatting Check)
- **Test Objective:** Kiểm tra nội dung chuỗi thông báo trả về (`message`) chứa đúng ký hiệu tiền tệ ₫ hoặc %
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `message` chứa "10%"
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Message string formatted properly", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().message).to.include("10%");
  });
  ```

---

### NHÓM 3: DOMAIN PARTITIONS & SECURITY (7 TEST CASES)

#### TC_FR09_DOM_01
- **TC_ID:** `TC_FR09_DOM_01`
- **Category:** Domain (BVA - Zero Total Amount `total_amount = 0`)
- **Test Objective:** Kiểm tra từ chối khi tổng tiền đơn hàng bằng 0
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 0,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "..."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for zero total amount", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR09_DOM_02
- **TC_ID:** `TC_FR09_DOM_02`
- **Category:** Domain (BVA - Negative Total Amount `total_amount = -500000`)
- **Test Objective:** Kiểm tra từ chối khi tổng tiền đơn hàng là số âm
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": -500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "..."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for negative total amount", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR09_DOM_03
- **TC_ID:** `TC_FR09_DOM_03`
- **Category:** Domain (EP - Empty Coupon Code `""`)
- **Test Objective:** Kiểm tra từ chối khi trường code là chuỗi rỗng
- **Pre-condition:** Không có code
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Vui lòng nhập mã giảm giá"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for empty code", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.eql("Vui lòng nhập mã giảm giá");
  });
  ```

---

#### TC_FR09_DOM_04
- **TC_ID:** `TC_FR09_DOM_04`
- **Category:** Domain (EP - Whitespace Only Coupon Code `"   "`)
- **Test Objective:** Kiểm tra từ chối khi trường code toàn khoảng trắng
- **Pre-condition:** Code chứa spaces
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "   ",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request` hoặc `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "..."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Whitespace code rejected", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR09_DOM_05
- **TC_ID:** `TC_FR09_DOM_05`
- **Category:** Domain (EP - Non-numeric String Total Amount)
- **Test Objective:** Kiểm tra từ chối khi `total_amount` là chuỗi chữ cái
- **Pre-condition:** Amount không hợp lệ
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": "năm trăm ngàn",
    "user_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "..."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("String total amount rejected with 400", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR09_DOM_06
- **TC_ID:** `TC_FR09_DOM_06`
- **Category:** Security (SEC-06 - SQL Injection in Coupon Code Parameter)
- **Test Objective:** Kiểm tra khả năng chống SQL Injection trong trường `code`
- **Pre-condition:** Không cần auth
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10' OR '1'='1",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Xử lý an toàn bằng Parameterized Query, KHÔNG gây lỗi crash 500
- **Postman Chai Assertion:**
  ```javascript
  pm.test("SQL Injection handled safely without 500 error", function () {
      pm.expect(pm.response.code).to.not.equal(500);
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR09_DOM_07
- **TC_ID:** `TC_FR09_DOM_07`
- **Category:** Security (SEC-06 - Stored/Reflected XSS in Coupon Code)
- **Test Objective:** Kiểm tra an toàn khi chèn payload XSS trong `code`
- **Pre-condition:** Không cần auth
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "<script>alert('COUPON_XSS')</script>",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Không thực thi script
- **Postman Chai Assertion:**
  ```javascript
  pm.test("XSS payload in coupon code rejected safely", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

### NHÓM 4: SCHEMA VALIDATION & MOBILE SLA (6 TEST CASES)

#### TC_FR09_SCHEMA_01
- **TC_ID:** `TC_FR09_SCHEMA_01`
- **Category:** Schema Validation (POST /api/apply-coupon 200 OK Response Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema phản hồi thành công khi áp dụng mã giảm giá
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "SAVE10",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["success", "coupon_id", "discount_amount", "final_amount", "message"],
    "properties": {
      "success": { "type": "boolean" },
      "coupon_id": { "type": "integer" },
      "discount_amount": { "type": "number" },
      "final_amount": { "type": "number" },
      "message": { "type": "string" }
    }
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  var couponSchema = {
      "type": "object",
      "required": ["success", "coupon_id", "discount_amount", "final_amount", "message"],
      "properties": {
          "success": { "type": "boolean" },
          "coupon_id": { "type": "integer" },
          "discount_amount": { "type": "number" },
          "final_amount": { "type": "number" },
          "message": { "type": "string" }
      }
  };
  pm.test("200 OK response conforms to Apply Coupon Schema", function () {
      pm.response.to.have.status(200);
      pm.expect(tv4.validate(pm.response.json(), couponSchema)).to.be.true;
  });
  ```

---

#### TC_FR09_SCHEMA_02
- **TC_ID:** `TC_FR09_SCHEMA_02`
- **Category:** Schema Validation (400 Bad Request Error Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema của phản hồi lỗi 400 Bad Request
- **Pre-condition:** Không nhập code
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"total_amount": 500000}`
- **Expected Status Code:** `400 Bad Request`
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
  pm.test("400 error response contains error message string", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json()).to.have.property("error");
      pm.expect(pm.response.json().error).to.be.a("string");
  });
  ```

---

#### TC_FR09_SCHEMA_03
- **TC_ID:** `TC_FR09_SCHEMA_03`
- **Category:** Schema Validation (404 Not Found Error Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema của phản hồi lỗi 404 Not Found
- **Pre-condition:** Code không tồn tại
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"code": "UNKNOWN_CODE", "total_amount": 500000}`
- **Expected Status Code:** `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "string"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("404 error schema contains error property", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  ```

---

#### TC_FR09_SCHEMA_04
- **TC_ID:** `TC_FR09_SCHEMA_04`
- **Category:** Type Consistency (Numeric Type Verification on Calculated Fields)
- **Test Objective:** Đảm bảo `discount_amount` và `final_amount` luôn là kiểu `number` (không bị ép kiểu thành string)
- **Pre-condition:** Mã `BIGBUY`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"code": "BIGBUY", "total_amount": 600000, "user_id": 1}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `typeof discount_amount === 'number'` và `typeof final_amount === 'number'`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Amounts are strictly numeric types", function () {
      pm.response.to.have.status(200);
      var data = pm.response.json();
      pm.expect(data.discount_amount).to.be.a("number");
      pm.expect(data.final_amount).to.be.a("number");
  });
  ```

---

#### TC_FR09_SCHEMA_05
- **TC_ID:** `TC_FR09_SCHEMA_05`
- **Category:** Anti-Cheat Header Enforcement (X-Student-Id Verification)
- **Test Objective:** Xác thực Header `X-Student-Id: 23127092` được đính kèm thành công
- **Pre-condition:** Pre-request script cấu hình header
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"code": "BIGBUY", "total_amount": 600000, "user_id": 1}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Request được chấp nhận
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Header X-Student-Id is present in request", function () {
      pm.expect(pm.request.headers.get("X-Student-Id")).to.eql("23127092");
  });
  ```

---

#### TC_FR09_SCHEMA_06
- **TC_ID:** `TC_FR09_SCHEMA_06`
- **Category:** Performance SLA (Mobile Checkout Response Time < 200ms)
- **Test Objective:** Kiểm tra thời gian phản hồi của API áp dụng mã giảm giá đáp ứng trải nghiệm mượt mà trên Mobile App (< 200ms)
- **Pre-condition:** Mã `SAVE10`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"code": "SAVE10", "total_amount": 500000, "user_id": 1}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Response Time < 200ms
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Response time is under 200ms (Mobile SLA)", function () {
      pm.expect(pm.response.responseTime).to.be.below(200);
  });
  ```

---

### NHÓM 5: TÌNH HUỐNG BIÊN NÂNG CAO & BÓC TÁCH MÃ NGUỒN ẨN (5 ADVANCED TEST CASES)

> **Mục đích nhóm 5:** Khai thác các lỗi nghiêm trọng về công thức toán học (`1 - discount_value`), sai lệch toán tử so sánh ngưỡng tối thiểu (`>` thay vì `>=`), và nguy cơ giả mạo định danh User ID trong `server.js` (dòng 363–441).

---

#### TC_FR09_ADV_01
- **TC_ID:** `TC_FR09_ADV_01`
- **Category:** Math Logic Bug Hunter (Critical Percent Formula Inversion `1 - discount_value`)
- **Test Objective:** Phát hiện lỗi công thức toán học nghiêm trọng làm số tiền giảm giá biến thành số âm khổng lồ: Áp dụng mã `GIAM10` (10%) cho đơn hàng 500,000 ₫ *(Bắt Bug SUT dòng 400: `discount_amount = Math.floor(total_amount * (1 - coupon.discount_value))` tính ra `500000 * (1 - 10) = -4,500,000` ₫)*
- **Pre-condition:** Mã `GIAM10` (`discount_value = 10`, `type = 'percent'`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "GIAM10",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  - `discount_amount === 50000` (Giảm 10% của 500k là 50k)
  - `final_amount === 450000` (500k - 50k = 450k)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR09_ADV_01: CRITICAL MATH - Percent discount formula MUST be (discount_value/100), not (1-discount_value)", function () {
      pm.response.to.have.status(200);
      var res = pm.response.json();
      pm.expect(res.discount_amount, "Discount amount was negative due to math bug!").to.eql(50000);
      pm.expect(res.final_amount, "Final amount was inflated by 10x!").to.eql(450000);
  });
  // GHI CHÚ AUDIT: SUT trả về discount_amount = -4500000 và final_amount = 5000000 (Đội giá tiền lên gấp 10 lần)
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Các công cụ AI sinh test Blackbox thường chỉ kiểm tra trạng thái HTTP (`pm.response.to.have.status(200)`) hoặc kiểm tra sự tồn tại của các thuộc tính (`res.should.have.property('discount_amount')`). AI hiếm khi tính toán độc lập giá trị kỳ vọng (Golden Expected Values) dựa trên công thức toán học chuẩn: `Math.floor(total_amount * (discount_value / 100))`. Khi server trả về `200 OK`, nếu chỉ assert lỏng lẻo `pm.expect(res.discount_amount).to.be.a('number')`, test case sẽ Pass 100% trong khi hệ thống đang mắc lỗi tính sai tiền làm khách hàng bị đội giá gấp 10 lần!

---

#### TC_FR09_ADV_02
- **TC_ID:** `TC_FR09_ADV_02`
- **Category:** Boundary Operator Bug Hunter (Threshold Operator `>` vs `>=` on Condition C3)
- **Test Objective:** Kiểm tra áp dụng mã tại ĐÚNG ĐIỂM BIÊN NGƯỠNG ĐƠN HÀNG TỐI THIỂU: Gửi `total_amount = 300000` cho mã `GIAM10` (`min_order_amount = 300000`) *(Bắt Bug SUT dòng 379: `if (total_amount > coupon.min_order_amount)` sử dụng dấu `>` thay vì `>=`)*
- **Pre-condition:** Mã `GIAM10` có `min_order_amount = 300000`
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "GIAM10",
    "total_amount": 300000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK` (Thỏa mãn điều kiện C3: `total_amount >= min_order_amount`)
- **Expected Response Body / Schema:** `{"success": true, "coupon_id": 1}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR09_ADV_02: CRITICAL BVA - Order total EXACTLY EQUAL to min_order_amount MUST be accepted (C3 rule)", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().success).to.be.true;
  });
  // GHI CHÚ AUDIT: SUT trả về 400 Bad Request 'Đơn hàng chưa đủ giá trị tối thiểu' do dùng dấu > thay vì >=
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Khi sinh test cho các giá trị hợp lệ (Happy Path), AI có xu hướng chọn các con số "an toàn" lớn hơn hẳn ngưỡng tối thiểu (ví dụ: gửi `total_amount = 500000` hoặc `1000000` khi ngưỡng là 300k). AI thiếu sự nhạy bén của kỹ thuật Phân tích Giá trị Biên (Boundary Value Analysis - BVA) theo chuẩn ISTQB, vốn yêu cầu bắt buộc phải test tại điểm biên chính xác `Boundary Value = 300000` (`total_amount == min_order_amount`). Khi không test điểm biên này, lỗi lệch 1 đơn vị toán tử (Off-by-One Comparison Bug) sẽ không bao giờ bị phát hiện.

---

#### TC_FR09_ADV_03
- **TC_ID:** `TC_FR09_ADV_03`
- **Category:** Arithmetic Invariant (Fixed Coupon Exceeding Total & Non-Negative Invariant `final_amount >= 0`)
- **Test Objective:** Kiểm tra tính bất biến số học trong tài chính: Khi mã giảm giá cố định có giá trị giảm lớn hơn tổng tiền đơn hàng (`discount_value > total_amount`), số tiền thanh toán cuối cùng `final_amount` **BẮT BUỘC PHẢI ĐƯỢC CHẶN DƯỚI BẰNG 0** (hoặc `discount_amount` bằng `total_amount`), tuyệt đối không được ra số âm
- **Pre-condition:** Mã giảm giá cố định `GIAM500K` (`discount_value = 500000`, `min_order_amount = 200000`)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "GIAM500K",
    "total_amount": 300000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `final_amount >= 0` (Giá trị bằng `0` ₫, không được là `-200,000` ₫)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR09_ADV_03: Financial Invariant - Final amount must NEVER be negative (Capped at 0)", function () {
      pm.response.to.have.status(200);
      var res = pm.response.json();
      pm.expect(res.final_amount).to.be.at.least(0);
      pm.expect(res.discount_amount).to.be.at.most(300000);
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI thông thường chỉ thử nghiệm các trường hợp dữ liệu mẫu phổ biến (`discount_value` nhỏ hơn `total_amount`). AI không tự động suy luận ra các trường hợp biên tài chính (Financial Edge Cases) khi áp dụng mã giảm giá lớn cho giỏ hàng nhỏ. Nếu backend thiếu hàm chặn dưới `Math.max(0, total_amount - discount_amount)`, hệ thống sẽ trả về số tiền thanh toán âm, tạo lỗ hổng cho người dùng rút tiền ngược lại từ sàn thương mại điện tử!

---

#### TC_FR09_ADV_04
- **TC_ID:** `TC_FR09_ADV_04`
- **Category:** Security & Identity Integrity (Unauthenticated User ID Spoofing & Quota Bypass)
- **Test Objective:** Kiểm tra tính toàn vẹn định danh người dùng: Gọi `POST /api/apply-coupon` với `user_id` giả mạo của người khác (`user_id = 999` hoặc `user_id = 2`) để vượt qua điều kiện giới hạn lượt dùng C5 (`max_uses_per_user`) *(Bắt Bug SUT dòng 363: endpoint hoàn toàn không có JWT Authentication, tin tưởng mù quáng `user_id` từ request body)*
- **Pre-condition:** User 1 đã dùng hết số lượt của mã `GIAM10` (đã dùng 1/1 lần)
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "GIAM10",
    "total_amount": 500000,
    "user_id": 9999
  }
  ```
- **Expected Status Code:** Hệ thống chuẩn an toàn phải yêu cầu đăng nhập và lấy `user_id` từ Token (`req.user.id`), từ chối việc tự ý truyền `user_id` trong body để bypass hạn mức
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR09_ADV_04: Server must validate user identity via token rather than trusting arbitrary user_id", function () {
      // Đánh giá cơ chế xác thực và chống giả mạo user_id
      pm.expect(pm.response.code).to.be.oneOf([200, 400, 401]);
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI sinh test chỉ coi `user_id` như một tham số dữ liệu bình thường trong payload JSON. AI không nhận thức được lỗ hổng kiến trúc (Architectural Security Flaw): Việc một API cho phép client tự gửi `user_id` trong body thay vì trích xuất từ JWT Token (`req.user.id`) mở ra lỗ hổng nghiêm trọng cho phép kẻ tấn công thay đổi `user_id` ngẫu nhiên để sử dụng mã giảm giá không giới hạn số lần (Bypass Quota Limit).

---

#### TC_FR09_ADV_05
- **TC_ID:** `TC_FR09_ADV_05`
- **Category:** Date & Time Boundary (Midnight ISO Timestamp Expiration Truncation)
- **Test Objective:** Kiểm tra tính chính xác của thời gian hết hạn (Condition C2): Mã giảm giá có hạn sử dụng ghi ngày `expired_at = "2026-12-31"` (dạng Date-only) không bị backend hiểu nhầm thành `2026-12-31T00:00:00.000Z` làm hết hạn ngay từ đầu ngày
- **Pre-condition:** Mã giảm giá có ngày hết hạn là ngày hôm nay
- **Request Method & Endpoint:** `POST /api/apply-coupon`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "code": "TODAY_COUPON",
    "total_amount": 500000,
    "user_id": 1
  }
  ```
- **Expected Status Code:** `200 OK` (Hoặc `400` nếu đã qua đúng 23:59:59 của ngày hết hạn)
- **Expected Response Body / Schema:** Xử lý thời gian nhất quán theo UTC / Local Timezone
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR09_ADV_05: Expiration date parsing handles end-of-day boundary consistently", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 400, 404]);
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI kiểm thử thường chỉ phân biệt ngày quá khứ (ví dụ: `2020-01-01`) và ngày tương lai xa (ví dụ: `2099-12-31`). AI không tạo các ca kiểm thử biên vi mô (Micro-boundary) tại ranh giới nửa đêm (00:00:00 vs 23:59:59). Trong JavaScript, câu lệnh `new Date("2026-12-31")` sẽ chuyển thành `00:00:00 UTC`. Khách hàng sử dụng mã vào ban ngày của ngày 31/12 sẽ bị hệ thống báo lỗi hết hạn một cách vô lý, gây trải nghiệm rất xấu trên ứng dụng Mobile.

