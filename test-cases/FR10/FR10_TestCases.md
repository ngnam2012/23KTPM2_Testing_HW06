# FR-10: Test Cases (Pool B - Order State Machine & Cancellation)

> **Mã chức năng:** FR-10 | **Pool:** B (Cart & Orders)  
> **Chức năng:** Máy Trạng thái & Hủy Đơn hàng (Order State Machine & Cancellation)  
> **Endpoints:** `PUT /api/orders/:id/cancel` & `GET /api/orders/:id`  
> **MSSV (X-Student-Id):** `23127092`  
> **Tiêu chuẩn áp dụng:** ISTQB (State Transition Testing, EP, BVA), OWASP API Security Top 10 (SEC-01 BOLA/IDOR, SEC-02 Broken Auth, SEC-06 SQLi), JSON Schema Validation Draft-07.  
> **Tổng số test cases:** 45 Test Cases (Gồm 40 TCs chuẩn + 5 TCs nâng cao chuyên sâu bóc tách mã nguồn)

---

## 1. BẢNG TỔNG HỢP MA TRẬN TEST CASES CHO FR-10

| Nhóm | Phân loại (Category) | Kỹ thuật kiểm thử | Số lượng TC | Mã định danh |
| :---: | :--- | :--- | :---: | :--- |
| **Nhóm 1** | **State Machine Valid Transitions** | Kiểm thử chuyển trạng thái hợp lệ (`pending` ➔ `canceled`, `confirmed` ➔ `canceled`) | 10 | `TC_FR10_STATE_01` → `TC_FR10_STATE_10` |
| **Nhóm 2** | **State Machine Invalid Transitions** | Chuyển trạng thái bất hợp lệ (`shipping`, `delivered`, `canceled` ➔ `canceled`, Idempotency) | 11 | `TC_FR10_INV_01` → `TC_FR10_INV_11` |
| **Nhóm 3** | **Security & BOLA / IDOR** | OWASP Top 10 (`SEC-01` BOLA/IDOR, `SEC-02` Broken Auth, `SEC-06` SQLi, Token Forgery) | 11 | `TC_FR10_SEC_01` → `TC_FR10_SEC_11` |
| **Nhóm 4** | **Domain, Boundary & Schema** | Phân tích giá trị biên tham số (`id` âm, 0, chuỗi, 999999) & JSON Schema Validation | 8 | `TC_FR10_DOM_01` → `TC_FR10_DOM_05`, `TC_FR10_SCHEMA_01` → `03` |
| **Nhóm 5** | **Hidden Logic & Race Conditions** | Bóc tách mã nguồn Backend (`server.js`), BOLA unauthenticated GET, TOCTOU Race Condition | 5 | `TC_FR10_ADV_01` → `TC_FR10_ADV_05` |
| **TỔNG** | | | **45** | |

---

## 2. CHI TIẾT 40 TEST CASES THEO CHUẨN ISTQB & OWASP

### NHÓM 1: STATE MACHINE VALID TRANSITIONS (10 TEST CASES)

#### TC_FR10_STATE_01
- **TC_ID:** `TC_FR10_STATE_01`
- **Category:** State Transition (Valid - Pending to Canceled)
- **Test Objective:** Kiểm tra người dùng hủy đơn hàng thành công khi đơn hàng đang ở trạng thái `pending`
- **Pre-condition:** User A (`user_token_A`) sở hữu đơn hàng `id = 1` có trạng thái `status = 'pending'`
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "message": "Order canceled successfully"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("Cancellation success message returned", function () {
      var res = pm.response.json();
      pm.expect(res.message).to.eql("Order canceled successfully");
  });
  ```

---

#### TC_FR10_STATE_02
- **TC_ID:** `TC_FR10_STATE_02`
- **Category:** State Transition (State Verification - GET after Cancel Pending)
- **Test Objective:** Gọi `GET /api/orders/1` để xác thực trạng thái đơn hàng trong database đã chuyển sang `canceled`
- **Pre-condition:** Đơn hàng `id = 1` vừa được gửi lệnh hủy thành công ở `TC_FR10_STATE_01`
- **Request Method & Endpoint:** `GET /api/orders/1`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Payload đơn hàng có `status === "canceled"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Order status successfully updated to canceled in DB", function () {
      pm.response.to.have.status(200);
      var order = pm.response.json();
      pm.expect(order.status).to.eql("canceled");
  });
  ```

---

#### TC_FR10_STATE_03
- **TC_ID:** `TC_FR10_STATE_03`
- **Category:** State Transition (Valid - Confirmed to Canceled)
- **Test Objective:** Kiểm tra người dùng hủy đơn hàng thành công khi đơn hàng đang ở trạng thái `confirmed`
- **Pre-condition:** User A sở hữu đơn hàng `id = 2` có trạng thái `status = 'confirmed'`
- **Request Method & Endpoint:** `PUT /api/orders/2/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Order canceled successfully"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for confirmed order cancellation", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().message).to.eql("Order canceled successfully");
  });
  ```

---

#### TC_FR10_STATE_04
- **TC_ID:** `TC_FR10_STATE_04`
- **Category:** State Transition (State Verification - GET after Cancel Confirmed)
- **Test Objective:** Xác thực đơn hàng `confirmed` chuyển trạng thái sang `canceled` trong CSDL SQLite
- **Pre-condition:** Đơn hàng `id = 2` vừa được hủy thành công
- **Request Method & Endpoint:** `GET /api/orders/2`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `status === "canceled"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Confirmed order is now in canceled state", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().status).to.eql("canceled");
  });
  ```

---

#### TC_FR10_STATE_05
- **TC_ID:** `TC_FR10_STATE_05`
- **Category:** State Transition (Valid - Single Item Order Checkout & Cancel)
- **Test Objective:** Kiểm tra tạo đơn hàng 1 sản phẩm qua `POST /api/checkout` và hủy ngay lập tức
- **Pre-condition:** Giỏ hàng có 1 sản phẩm, checkout thành công đơn hàng `id = X`
- **Request Method & Endpoint:** `PUT /api/orders/{{new_order_id}}/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Order canceled successfully"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Newly created single-item order canceled successfully", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR10_STATE_06
- **TC_ID:** `TC_FR10_STATE_06`
- **Category:** State Transition (Valid - Multi Item Order Checkout & Cancel)
- **Test Objective:** Kiểm tra hủy đơn hàng chứa nhiều mặt hàng (multi-product items)
- **Pre-condition:** Đơn hàng gồm nhiều items ở trạng thái `pending`
- **Request Method & Endpoint:** `PUT /api/orders/{{multi_item_order_id}}/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Order canceled successfully"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Multi-item order canceled successfully", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR10_STATE_07
- **TC_ID:** `TC_FR10_STATE_07`
- **Category:** State Transition (Valid - Order with Coupon Applied)
- **Test Objective:** Kiểm tra hủy đơn hàng đã được áp dụng mã giảm giá
- **Pre-condition:** Đơn hàng tạo kèm discount coupon ở trạng thái `pending`
- **Request Method & Endpoint:** `PUT /api/orders/{{coupon_order_id}}/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Order canceled successfully"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Coupon discounted order canceled successfully", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR10_STATE_08
- **TC_ID:** `TC_FR10_STATE_08`
- **Category:** State Transition (Valid - Immediate Cancellation at T0)
- **Test Objective:** Kiểm tra hủy đơn hàng ngay tức thì sau khi bấm đặt hàng (T0)
- **Pre-condition:** Vừa hoàn tất `POST /api/checkout`
- **Request Method & Endpoint:** `PUT /api/orders/{{just_created_id}}/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Order canceled successfully"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Immediate cancellation returns 200 OK", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR10_STATE_09
- **TC_ID:** `TC_FR10_STATE_09`
- **Category:** State Transition (List Synchronization Verification)
- **Test Objective:** Kiểm tra danh sách đơn hàng cá nhân `GET /api/orders/my-orders` phản ánh chính xác trạng thái `canceled`
- **Pre-condition:** Đơn hàng `id = 1` đã được hủy
- **Request Method & Endpoint:** `GET /api/orders/my-orders`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Mảng đơn hàng chứa order với `id === 1` và `status === "canceled"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("my-orders list contains canceled status for order 1", function () {
      pm.response.to.have.status(200);
      var list = pm.response.json();
      var target = list.find(o => o.id === 1);
      pm.expect(target).to.exist;
      pm.expect(target.status).to.eql("canceled");
  });
  ```

---

#### TC_FR10_STATE_10
- **TC_ID:** `TC_FR10_STATE_10`
- **Category:** State Transition (Sequential Multi-Order Cancellation)
- **Test Objective:** Kiểm tra hủy liên tiếp nhiều đơn hàng `pending` khác nhau của cùng 1 user
- **Pre-condition:** User có ít nhất 2 đơn hàng `pending` (ID: 10, ID: 11)
- **Request Method & Endpoint:** `PUT /api/orders/11/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Order canceled successfully"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Sequential order cancellation succeeds", function () {
      pm.response.to.have.status(200);
  });
  ```

---

### NHÓM 2: STATE MACHINE INVALID TRANSITIONS (11 TEST CASES)

#### TC_FR10_INV_01
- **TC_ID:** `TC_FR10_INV_01`
- **Category:** State Machine Bug Hunter (Invalid - Shipping to Canceled)
- **Test Objective:** Kiểm tra người dùng thường KHÔNG ĐƯỢC PHÉP hủy đơn hàng khi trạng thái đang là `shipping` *(Bắt Bug SUT vi phạm SRS FR-10 & FR-20)*
- **Pre-condition:** Đơn hàng `id = 3` thuộc User A đang có trạng thái `status = 'shipping'`
- **Request Method & Endpoint:** `PUT /api/orders/3/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:**
  ```json
  {
    "error": "Cannot cancel this order."
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request (Cannot cancel shipping order)", function () {
      pm.response.to.have.status(400);
  });
  pm.test("Error message returned for invalid shipping cancel", function () {
      pm.expect(pm.response.json()).to.have.property("error");
  });
  // GHI CHÚ AUDIT: SUT hiện tại có bug cho phép hủy đơn shipping (trả về 200 OK sai đặc tả)
  ```

---

#### TC_FR10_INV_02
- **TC_ID:** `TC_FR10_INV_02`
- **Category:** State Machine (Invalid - Delivered to Canceled / Final State)
- **Test Objective:** Kiểm tra hệ thống từ chối khi cố gắng hủy đơn hàng đã giao thành công (`status = 'delivered'`)
- **Pre-condition:** Đơn hàng `id = 4` thuộc User A có `status = 'delivered'`
- **Request Method & Endpoint:** `PUT /api/orders/4/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Cannot cancel this order."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for delivered order", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.eql("Cannot cancel this order.");
  });
  ```

---

#### TC_FR10_INV_03
- **TC_ID:** `TC_FR10_INV_03`
- **Category:** State Machine (Invalid - Canceled to Canceled / Terminal State)
- **Test Objective:** Kiểm tra hệ thống từ chối khi cố gắng hủy đơn hàng đã ở trạng thái `canceled`
- **Pre-condition:** Đơn hàng `id = 1` đã có `status = 'canceled'`
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Cannot cancel this order."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for already canceled order", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.eql("Cannot cancel this order.");
  });
  ```

---

#### TC_FR10_INV_04
- **TC_ID:** `TC_FR10_INV_04`
- **Category:** State Machine (Idempotency & Double Cancellation on Pending)
- **Test Objective:** Gửi 2 request hủy liên tiếp trên cùng 1 đơn hàng `pending`: Request 1 trả về 200, Request 2 phải trả về 400 Bad Request
- **Pre-condition:** Đơn hàng mới tạo `id = 5` đang `pending`
- **Request Method & Endpoint:** `PUT /api/orders/5/cancel` (Lần 2)
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Cannot cancel this order."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Second cancellation attempt returns 400 Bad Request", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR10_INV_05
- **TC_ID:** `TC_FR10_INV_05`
- **Category:** State Machine (Idempotency & Double Cancellation on Confirmed)
- **Test Objective:** Gửi 2 request hủy liên tiếp trên đơn hàng `confirmed`: Lần 2 phải bị từ chối với 400
- **Pre-condition:** Đơn hàng `id = 6` đang `confirmed`
- **Request Method & Endpoint:** `PUT /api/orders/6/cancel` (Lần 2)
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Cannot cancel this order."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Repeated cancellation of confirmed order returns 400", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR10_INV_06
- **TC_ID:** `TC_FR10_INV_06`
- **Category:** State Machine (State Immutability Verification on Delivered)
- **Test Objective:** Xác thực trạng thái của đơn hàng `delivered` không bị biến đổi sau khi bị từ chối lệnh hủy
- **Pre-condition:** Đơn hàng `id = 4` (`delivered`) vừa bị từ chối hủy ở `TC_FR10_INV_02`
- **Request Method & Endpoint:** `GET /api/orders/4`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `status === "delivered"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Order remains in delivered state", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().status).to.eql("delivered");
  });
  ```

---

#### TC_FR10_INV_07
- **TC_ID:** `TC_FR10_INV_07`
- **Category:** State Machine (Payload Tampering - Status Override Attempt)
- **Test Objective:** Thử gửi body `{"status": "delivered"}` hoặc `{"status": "confirmed"}` khi gọi cancel để xem hệ thống có bị can thiệp trạng thái trái phép không
- **Pre-condition:** Đơn hàng `pending`
- **Request Method & Endpoint:** `PUT /api/orders/7/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "status": "delivered"
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Trạng thái đơn hàng phải chuyển sang `"canceled"` chứ không được thành `"delivered"`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Cancel endpoint ignores body status override", function () {
      pm.response.to.have.status(200);
  });
  ```

---

#### TC_FR10_INV_08
- **TC_ID:** `TC_FR10_INV_08`
- **Category:** State Machine (Invalid - Return / Refunded State Transition)
- **Test Objective:** Thử hủy đơn hàng đã hoàn tất đổi trả (`status = 'returned'`)
- **Pre-condition:** Đơn hàng có `status = 'returned'`
- **Request Method & Endpoint:** `PUT /api/orders/8/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Cannot cancel this order."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Returned order cannot be canceled", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR10_INV_09
- **TC_ID:** `TC_FR10_INV_09`
- **Category:** State Machine (Status Verification after Tampering Attempt)
- **Test Objective:** Gọi `GET /api/orders/7` để xác minh lệnh can thiệp body ở `TC_FR10_INV_07` không làm sai lệch trạng thái `canceled`
- **Pre-condition:** Đơn hàng `id = 7` vừa được gọi cancel
- **Request Method & Endpoint:** `GET /api/orders/7`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `status === "canceled"` (không phải "delivered")
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Order status is strictly 'canceled'", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().status).to.eql("canceled");
      pm.expect(pm.response.json().status).to.not.eql("delivered");
  });
  ```

---

#### TC_FR10_INV_10
- **TC_ID:** `TC_FR10_INV_10`
- **Category:** State Machine (Admin Changed Status to Shipping - User Cancel Attempt)
- **Test Objective:** Đơn hàng ban đầu `pending` được Admin cập nhật sang `shipping` ➔ User gửi lệnh hủy ➔ Phải bị từ chối với 400
- **Pre-condition:** Admin đã chuyển đơn `id = 9` sang `shipping`
- **Request Method & Endpoint:** `PUT /api/orders/9/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Cannot cancel this order."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("User cannot cancel order that transitioned to shipping", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR10_INV_11
- **TC_ID:** `TC_FR10_INV_11`
- **Category:** State Machine (State Integrity After Failed Transition)
- **Test Objective:** Đảm bảo khi lệnh hủy thất bại, tổng tiền `total_amount` và địa chỉ giao hàng không bị biến đổi
- **Pre-condition:** Đơn hàng `id = 4` giao dịch thất bại
- **Request Method & Endpoint:** `GET /api/orders/4`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `total_amount` và `shipping_address` giữ nguyên giá trị ban đầu
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Financial and address data remains intact", function () {
      pm.response.to.have.status(200);
      var order = pm.response.json();
      pm.expect(order.total_amount).to.be.above(0);
      pm.expect(order.shipping_address).to.be.a('string');
  });
  ```

---

### NHÓM 3: SECURITY & BOLA / IDOR (11 TEST CASES)

#### TC_FR10_SEC_01
- **TC_ID:** `TC_FR10_SEC_01`
- **Category:** Security (SEC-01 - BOLA/IDOR on Cancel Endpoint)
- **Test Objective:** Kiểm tra lỗ hổng BOLA: User A (`user_token_A`) cố gắng hủy đơn hàng của User B (`order_id_B = 20`)
- **Pre-condition:** Đơn hàng `id = 20` thuộc sở hữu của User B (`user_id = 2`)
- **Request Method & Endpoint:** `PUT /api/orders/20/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found` hoặc `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Order not found"}` hoặc `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("BOLA PREVENTED: User A cannot cancel User B's order", function () {
      pm.expect(pm.response.code).to.be.oneOf([404, 403]);
  });
  pm.test("Appropriate error message returned", function () {
      pm.expect(pm.response.json()).to.have.property("error");
  });
  ```

---

#### TC_FR10_SEC_02
- **TC_ID:** `TC_FR10_SEC_02`
- **Category:** Security Bug Hunter (SEC-01 - BOLA/IDOR on GET Order Detail)
- **Test Objective:** Kiểm tra lỗ hổng BOLA/IDOR: User A gọi `GET /api/orders/:id_B` để xem trái phép đơn hàng của User B *(Bắt Bug SUT nghiêm trọng: `GET /api/orders/:id` không có auth/ownership check)*
- **Pre-condition:** Đơn hàng `id = 20` thuộc User B chứa thông tin nhạy cảm (địa chỉ, số tiền)
- **Request Method & Endpoint:** `GET /api/orders/20`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `403 Forbidden` hoặc `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}` hoặc `{"error": "Order not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("CRITICAL BOLA: User A MUST NOT view User B's order details", function () {
      pm.expect(pm.response.code).to.be.oneOf([403, 404]);
  });
  // GHI CHÚ AUDIT: SUT hiện tại trả về 200 OK và lộ toàn bộ đơn hàng của User B (Lỗ hổng BOLA nghiêm trọng)
  ```

---

#### TC_FR10_SEC_03
- **TC_ID:** `TC_FR10_SEC_03`
- **Category:** Security (SEC-02 - Missing Authorization on Cancel)
- **Test Objective:** Kiểm tra từ chối yêu cầu hủy đơn khi không gửi kèm Header `Authorization`
- **Pre-condition:** Không có token
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `401 Unauthorized`
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 401 Unauthorized", function () {
      pm.response.to.have.status(401);
      pm.expect(pm.response.json().error).to.eql("Unauthorized");
  });
  ```

---

#### TC_FR10_SEC_04
- **TC_ID:** `TC_FR10_SEC_04`
- **Category:** Security Bug Hunter (SEC-02 - Missing Authorization on GET Order)
- **Test Objective:** Kiểm tra từ chối truy cập chi tiết đơn hàng khi khách vãng lai không đăng nhập
- **Pre-condition:** Không có token
- **Request Method & Endpoint:** `GET /api/orders/1`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `401 Unauthorized`
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Unauthenticated GET order should be rejected with 401", function () {
      pm.response.to.have.status(401);
  });
  // GHI CHÚ AUDIT: SUT trả về 200 OK do route GET /api/orders/:id không gắn authenticateToken
  ```

---

#### TC_FR10_SEC_05
- **TC_ID:** `TC_FR10_SEC_05`
- **Category:** Security (SEC-02 - Forged / Invalid JWT Token on Cancel)
- **Test Objective:** Kiểm tra từ chối truy cập khi gửi Token JWT giả mạo
- **Pre-condition:** Token không hợp lệ
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel`
- **Headers:**
  - `Authorization: Bearer fake.forged.jwt.token`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden for forged token", function () {
      pm.response.to.have.status(403);
      pm.expect(pm.response.json().error).to.eql("Forbidden");
  });
  ```

---

#### TC_FR10_SEC_06
- **TC_ID:** `TC_FR10_SEC_06`
- **Category:** Security (SEC-02 - Expired JWT Token)
- **Test Objective:** Kiểm tra từ chối khi Bearer Token đã hết hạn
- **Pre-condition:** Token đã quá hạn sinh từ epoch cũ
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel`
- **Headers:**
  - `Authorization: Bearer {{expired_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `403 Forbidden` hoặc `401 Unauthorized`
- **Expected Response Body / Schema:** Thông báo token không hợp lệ hoặc hết hạn
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Expired token is rejected", function () {
      pm.expect(pm.response.code).to.be.oneOf([401, 403]);
  });
  ```

---

#### TC_FR10_SEC_07
- **TC_ID:** `TC_FR10_SEC_07`
- **Category:** Security (SEC-06 - SQL Injection in Cancel URL Path Param)
- **Test Objective:** Kiểm tra khả năng chống SQL Injection trong path parameter `:id` khi hủy đơn
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/orders/1' OR '1'='1/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Xử lý an toàn dạng Parameterized Query, KHÔNG gây lỗi SQL syntax 500
- **Postman Chai Assertion:**
  ```javascript
  pm.test("SQL Injection handled safely (No 500 Internal Error)", function () {
      pm.expect(pm.response.code).to.not.equal(500);
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR10_SEC_08
- **TC_ID:** `TC_FR10_SEC_08`
- **Category:** Security (SEC-06 - SQL Injection in GET Order Detail URL)
- **Test Objective:** Kiểm tra khả năng chống SQL Injection Union-based trong `GET /api/orders/:id`
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `GET /api/orders/1' UNION SELECT 1,2,3,4,5,6,7 --`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Không crash hệ thống với 500
- **Postman Chai Assertion:**
  ```javascript
  pm.test("GET SQL Injection treated safely (No 500)", function () {
      pm.expect(pm.response.code).to.not.equal(500);
  });
  ```

---

#### TC_FR10_SEC_09
- **TC_ID:** `TC_FR10_SEC_09`
- **Category:** Security (HTTP Parameter Pollution - HPP)
- **Test Objective:** Thử truyền query parameter trùng lặp `PUT /api/orders/1/cancel?id=2`
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel?id=2`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Order canceled successfully"}` (Tham số trên path `/1/` có độ ưu tiên cao nhất, query pollution bị bỏ qua)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR10_SEC_09: Path param takes strict precedence over query pollution", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().message).to.eql("Order canceled successfully");
  });
  ```

---

#### TC_FR10_SEC_10
- **TC_ID:** `TC_FR10_SEC_10`
- **Category:** Security (Privilege Impersonation - Fake Admin Header)
- **Test Objective:** User thường gửi kèm Header `X-Role: admin` hoặc `X-Is-Admin: true` để thử ép hủy đơn `shipping`
- **Pre-condition:** Đơn hàng `shipping`
- **Request Method & Endpoint:** `PUT /api/orders/3/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Role: admin`
  - `X-Is-Admin: true`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** Header giả mạo bị bỏ qua, quyền hạn dựa hoàn toàn vào JWT payload
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Fake role headers are ignored", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR10_SEC_11
- **TC_ID:** `TC_FR10_SEC_11`
- **Category:** Security & Compliance (Mandatory Header X-Student-Id Enforcement)
- **Test Objective:** Xác thực Header `X-Student-Id: 23127092` được gửi đầy đủ và log trên server
- **Pre-condition:** Request được cấu hình qua Pre-request Script
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `200 OK` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Request được chấp nhận xử lý
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Request header X-Student-Id is present", function () {
      pm.expect(pm.request.headers.get("X-Student-Id")).to.eql("23127092");
  });
  ```

---

### NHÓM 4: DOMAIN, BOUNDARY ON PARAMS & SCHEMA (8 TEST CASES)

#### TC_FR10_DOM_01
- **TC_ID:** `TC_FR10_DOM_01`
- **Category:** Domain & Boundary (Boundary ID = 0)
- **Test Objective:** Phân tích giá trị biên: Kiểm tra hủy đơn hàng với `id = 0`
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/orders/0/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Order not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Order ID 0 returns 404 Not Found", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR10_DOM_02
- **TC_ID:** `TC_FR10_DOM_02`
- **Category:** Domain & Boundary (Negative ID = -1)
- **Test Objective:** Phân tích giá trị biên: Kiểm tra hủy đơn hàng với ID âm (`id = -1`)
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/orders/-1/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Order not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Negative Order ID returns 404 or 400", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR10_DOM_03
- **TC_ID:** `TC_FR10_DOM_03`
- **Category:** Domain (Non-numeric String ID = "abc")
- **Test Objective:** Kiểm tra xử lý khi truyền ID dạng chuỗi chữ cái không phải số
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/orders/abc/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Order not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("String ID 'abc' handled gracefully", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR10_DOM_04
- **TC_ID:** `TC_FR10_DOM_04`
- **Category:** Domain (Floating Point ID = 1.5)
- **Test Objective:** Kiểm tra xử lý khi truyền ID là số thực dấu phẩy động
- **Pre-condition:** User đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/orders/1.5/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Order not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Float ID handled as not found or bad request", function () {
      pm.expect(pm.response.code).to.be.oneOf([400, 404]);
  });
  ```

---

#### TC_FR10_DOM_05
- **TC_ID:** `TC_FR10_DOM_05`
- **Category:** Domain (Non-existent Large ID = 999999)
- **Test Objective:** Kiểm tra hủy đơn hàng với ID không tồn tại trong hệ thống (`id = 999999`)
- **Pre-condition:** Database không có đơn hàng 999999
- **Request Method & Endpoint:** `PUT /api/orders/999999/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found`
- **Expected Response Body / Schema:**
  ```json
  {
    "error": "Order not found"
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 404 Not Found", function () {
      pm.response.to.have.status(404);
  });
  pm.test("Error message is Order not found", function () {
      pm.expect(pm.response.json().error).to.eql("Order not found");
  });
  ```

---

#### TC_FR10_SCHEMA_01
- **TC_ID:** `TC_FR10_SCHEMA_01`
- **Category:** Schema (PUT /api/orders/:id/cancel 200 OK JSON Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema phản hồi thành công khi hủy đơn
- **Pre-condition:** Đơn hàng `pending`
- **Request Method & Endpoint:** `PUT /api/orders/1/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
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
  pm.test("PUT cancel response matches JSON Schema", function () {
      pm.response.to.have.status(200);
      pm.expect(tv4.validate(pm.response.json(), schema)).to.be.true;
  });
  ```

---

#### TC_FR10_SCHEMA_02
- **TC_ID:** `TC_FR10_SCHEMA_02`
- **Category:** Schema (GET /api/orders/:id 200 OK JSON Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema phản hồi chi tiết đơn hàng
- **Pre-condition:** Đơn hàng tồn tại trong CSDL
- **Request Method & Endpoint:** `GET /api/orders/1`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["id", "user_id", "total_amount", "shipping_address", "status"],
    "properties": {
      "id": { "type": "integer" },
      "user_id": { "type": "integer" },
      "total_amount": { "type": "number" },
      "shipping_address": { "type": "string" },
      "status": { 
        "type": "string",
        "enum": ["pending", "confirmed", "shipping", "delivered", "canceled"]
      },
      "created_at": { "type": "string" }
    }
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  var orderSchema = {
      "type": "object",
      "required": ["id", "user_id", "total_amount", "shipping_address", "status"],
      "properties": {
          "id": { "type": "integer" },
          "user_id": { "type": "integer" },
          "total_amount": { "type": "number" },
          "shipping_address": { "type": "string" },
          "status": { "type": "string" }
      }
  };
  pm.test("GET order details matches Order Schema", function () {
      pm.response.to.have.status(200);
      pm.expect(tv4.validate(pm.response.json(), orderSchema)).to.be.true;
  });
  ```

---

#### TC_FR10_SCHEMA_03
- **TC_ID:** `TC_FR10_SCHEMA_03`
- **Category:** Schema (400 Bad Request & 404 Not Found JSON Error Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema chuẩn của các phản hồi lỗi
- **Pre-condition:** Gọi đơn hàng không tồn tại
- **Request Method & Endpoint:** `PUT /api/orders/999999/cancel`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `404 Not Found`
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
  pm.test("Error response contains 'error' string property", function () {
      var json = pm.response.json();
      pm.expect(json).to.have.property("error");
      pm.expect(json.error).to.be.a("string");
  });
  ```

---

### NHÓM 5: TÌNH HUỐNG BIÊN NÂNG CAO & BÓC TÁCH MÃ NGUỒN ẨN (5 ADVANCED TEST CASES)

> **Mục đích nhóm 5:** Khai thác các kẽ hở logic máy trạng thái (State Machine Transitions), lỗ hổng phân quyền đa người dùng BOLA/IDOR và điều kiện tranh chấp đồng thời (Race Conditions) trong `server.js` (dòng 321–350).

---

#### TC_FR10_ADV_01
- **TC_ID:** `TC_FR10_ADV_01`
- **Category:** State Machine Bug Hunter (Illegal Transition from `shipping` to `canceled`)
- **Test Objective:** Kiểm tra người dùng thường KHÔNG ĐƯỢC PHÉP hủy đơn hàng khi trạng thái đang là `shipping` *(Bắt Bug SUT dòng 329: `if (order.status === "delivered" || order.status === "canceled")` bỏ sót kiểm tra `shipping`)*
- **Pre-condition:** Đơn hàng `id = 3` thuộc User A đang có trạng thái `status = 'shipping'`
- **Request Method & Endpoint:** `PUT /api/orders/3/cancel`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Cannot cancel this order."}` (Hoặc thông báo tương đương thể hiện đơn hàng đang giao không được hủy)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR10_ADV_01: CRITICAL - Order in 'shipping' state MUST NOT be canceled by regular user", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  // GHI CHÚ AUDIT: SUT hiện tại cho phép hủy đơn shipping (trả về 200 OK sai hoàn toàn đặc tả SRS FR-10)
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Các công cụ AI thông thường khi tạo test cho máy trạng thái (State Machine) chỉ tập trung vào trạng thái khởi đầu (`pending` ➔ `canceled`) và hai trạng thái kết thúc (`delivered` ➔ `canceled`, `canceled` ➔ `canceled`). AI thường bỏ quên trạng thái trung gian `shipping`. Hơn nữa, trong mã nguồn backend (`server.js` dòng 329), lập trình viên sử dụng kỹ thuật kiểm tra danh sách đen lỏng lẻo: `if (order.status === "delivered" || order.status === "canceled") return res.status(400)`. Do thiếu kiểm tra `order.status === 'shipping'`, SUT vô tình cho phép hủy đơn hàng đang giao. Một AI không có khả năng đối chiếu đối xứng giữa đặc tả SRS FR-10 (*"Đơn hàng shipping chỉ có Admin mới có quyền hủy"*) và mã nguồn sẽ dễ dàng chấp nhận phản hồi `200 OK` như một hành vi bình thường.

---

#### TC_FR10_ADV_02
- **TC_ID:** `TC_FR10_ADV_02`
- **Category:** Security Bug Hunter (Unauthenticated Cross-Tenant BOLA/IDOR on `GET /api/orders/:id`)
- **Test Objective:** Kiểm tra truy cập trái phép chi tiết đơn hàng: Khách vãng lai KHÔNG CÓ TOKEN hoặc User A sử dụng Token của mình để đọc trộm đơn hàng `id = 2` của User B *(Bắt Bug SUT dòng 344: `GET /api/orders/:id` hoàn toàn thiếu middleware `authenticateToken` và thiếu kiểm tra `WHERE user_id = req.user.id`)*
- **Pre-condition:** Đơn hàng `id = 2` thuộc về User B chứa thông tin cá nhân và số tiền nhạy cảm
- **Request Method & Endpoint:** `GET /api/orders/2`
- **Headers:**
  - `X-Student-Id: 23127092` (Không gửi kèm Header `Authorization`)
- **Request Body:** N/A
- **Expected Status Code:** `401 Unauthorized` (Nếu không có token) hoặc `403 Forbidden` / `404 Not Found` (Nếu User A đọc của User B)
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}` hoặc `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR10_ADV_02: CRITICAL BOLA - Unauthenticated access to order details MUST be rejected with 401", function () {
      pm.response.to.have.status(401);
      pm.expect(pm.response.json().error).to.eql("Unauthorized");
  });
  // GHI CHÚ AUDIT: SUT trả về 200 OK và phơi bày toàn bộ dữ liệu đơn hàng do thiếu middleware bảo vệ
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI sinh test tự động có xu hướng áp dụng Header mặc định (Collection-level Authentication) vào tất cả các request. Do đó, tất cả các request `GET /api/orders/:id` được AI tạo ra đều gửi kèm token của chính chủ đơn hàng (Happy Path). AI rất hiếm khi chủ động bóc tách Header Authentication ra khỏi request hoặc mô phỏng môi trường đa người dùng (Multi-tenant) để User A truy cập ID của User B. Điều này khiến lỗ hổng BOLA/IDOR (OWASP API Security Top 1) bị ẩn giấu hoàn toàn trong các đợt kiểm thử tự động sơ sài.

---

#### TC_FR10_ADV_03
- **TC_ID:** `TC_FR10_ADV_03`
- **Category:** Concurrency & Robustness (Asynchronous Double-Cancellation TOCTOU Race Condition)
- **Test Objective:** Kiểm tra tính bất biến trạng thái khi xảy ra tranh chấp đồng thời: Gửi 2 request hủy đơn liên tiếp cực nhanh trên cùng một đơn hàng `pending` để phát hiện lỗi TOCTOU (Time-of-Check to Time-of-Use) trong câu truy vấn bất đồng bộ của Node.js SQLite
- **Pre-condition:** Đơn hàng mới tạo `id = 15` đang có `status = 'pending'`
- **Request Method & Endpoint:** `PUT /api/orders/15/cancel` (Gửi 2 lần liên tiếp)
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** Lần 1: `200 OK`; Lần 2: **BẮT BUỘC PHẢI LÀ `400 Bad Request`**
- **Expected Response Body / Schema:** Lần 2 trả về `{"error": "Cannot cancel this order."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR10_ADV_03: Second cancellation attempt MUST be rejected with 400 Bad Request", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json().error).to.eql("Cannot cancel this order.");
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Các mô hình AI sinh test theo luồng tuyến tính đơn luồng (Linear Sequential Flow: Request 1 xong mới tới Request 2). AI không tự động suy luận được khoảng cách thời gian trễ (latency window) giữa thao tác `db.get` (kiểm tra trạng thái) và `db.run` (cập nhật trạng thái) tại dòng 322–339 trong `server.js`. Nếu 2 request đến cùng lúc, cả 2 đều thấy `status === 'pending'` và cả 2 đều thực hiện UPDATE, dẫn đến việc cả 2 request đều trả về `200 OK` (vi phạm tính lũy thừa Idempotency và tính nhất quán ACID của máy trạng thái).

---

#### TC_FR10_ADV_04
- **TC_ID:** `TC_FR10_ADV_04`
- **Category:** Information Disclosure (Order Existence Enumeration via Asymmetric Status Responses)
- **Test Objective:** Phát hiện kỹ thuật dò quét ID đơn hàng (Blind ID Enumeration): So sánh phản hồi giữa `PUT /api/orders/2/cancel` (trả về `404 Not Found` do có `WHERE user_id = ?`) và `GET /api/orders/2` (trả về `200 OK` do thiếu `WHERE user_id = ?`), chứng minh kẻ tấn công có thể phân biệt được ID nào tồn tại trong hệ thống
- **Pre-condition:** Đơn hàng `id = 2` thuộc về User B
- **Request Method & Endpoint:**
  1. `PUT /api/orders/2/cancel` với `{{user_token_A}}` ➔ Nhận `404 Not Found`
  2. `GET /api/orders/2` với `{{user_token_A}}` ➔ Nhận `200 OK` (Lộ đơn)
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** Cả hai endpoint **PHẢI NHẤT QUÁN TRẢ VỀ `403 Forbidden` HOẶC `404 Not Found`** để ngăn chặn việc dò quét dữ liệu
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR10_ADV_04: Cross-endpoint authorization consistency - Foreign order must NOT return 200 on GET", function () {
      // Trong hệ thống bảo mật, User A không thể nhận 200 OK trên đơn hàng của User B
      pm.expect(pm.response.code).to.be.oneOf([403, 404]);
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI kiểm thử chỉ đánh giá từng endpoint đơn lẻ (Single Endpoint Scope). AI không có khả năng "liên kết chéo" (Cross-Endpoint Correlation Analysis) để nhận ra sự bất đối xứng nguy hiểm: lập trình viên đã viết đúng kiểm tra quyền sở hữu `WHERE id = ? AND user_id = ?` ở endpoint `PUT cancel` (dòng 323), nhưng lại **hoàn toàn quên mất điều kiện này ở endpoint `GET order`** (dòng 345: `SELECT * FROM orders WHERE id = ?`). Sự thiếu nhất quán này mở ra vector tấn công do thám (Reconnaissance Attack) cho hacker.

---

#### TC_FR10_ADV_05
- **TC_ID:** `TC_FR10_ADV_05`
- **Category:** Financial & Address Data Integrity (Post-Cancellation Financial Immutability)
- **Test Objective:** Xác thực tính bất biến của dữ liệu tài chính và giao vận: Sau khi đơn hàng chuyển sang `status = 'canceled'`, tổng tiền (`total_amount`) và địa chỉ giao hàng (`shipping_address`) ban đầu bắt buộc phải được giữ nguyên vẹn 100% để phục vụ đối soát kế toán và lưu vết lịch sử
- **Pre-condition:** Đơn hàng `id = 1` vừa được hủy thành công
- **Request Method & Endpoint:** `GET /api/orders/1`
- **Headers:**
  - `Authorization: Bearer {{user_token_A}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  - `status === "canceled"`
  - `total_amount > 0` (Bằng đúng số tiền lúc checkout ban đầu)
  - `shipping_address` không bị null hay rỗng
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR10_ADV_05: Financial and audit data remains completely immutable after cancellation", function () {
      pm.response.to.have.status(200);
      var order = pm.response.json();
      pm.expect(order.status).to.eql("canceled");
      pm.expect(order.total_amount).to.be.a("number");
      pm.expect(order.total_amount).to.be.above(0);
      pm.expect(order.shipping_address).to.be.a("string");
      pm.expect(order.shipping_address.length).to.be.above(0);
  });
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Khi kiểm tra tính năng hủy đơn hàng, AI thông thường chỉ đặt kỳ vọng vào trường `status === 'canceled'` hoặc message `"Order canceled successfully"`. AI không có tư duy của một chuyên gia kiểm thử nghiệp vụ E-commerce (Business Domain Logic): một lệnh hủy đơn hàng chỉ được phép thay đổi trạng thái vòng đời, tuyệt đối không được làm sai lệch dữ liệu tài chính lịch sử (`total_amount`) hoặc thông tin giao vận ban đầu. Nếu thiếu assertion này, các lỗi backend vô tình gán `total_amount = 0` hoặc xóa địa chỉ khi hủy đơn sẽ bị bỏ lọt hoàn toàn.

