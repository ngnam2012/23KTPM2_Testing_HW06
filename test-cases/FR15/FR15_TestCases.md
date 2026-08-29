# FR-15: Test Cases (Pool C - Admin Product CRUD)

> **Mã chức năng:** FR-15 | **Pool:** C (Web Admin & Product Management)  
> **Chức năng:** Quản lý Sản phẩm Admin (Admin Product CRUD)  
> **Endpoints:** `POST /api/products`, `PUT /api/products/:id`, `DELETE /api/products/:id`, `GET /api/products/:id`  
> **MSSV (X-Student-Id):** `23127092`  
> **Tiêu chuẩn áp dụng:** ISTQB (EP, BVA, CRUD Lifecycle), OWASP API Security Top 10 (SEC-03 Broken Access Control, SEC-05 BFLA, SEC-06 SQLi, Type Coercion), JSON Schema Validation Draft-07.  
> **Tổng số test cases:** 45 Test Cases (Gồm 40 TCs chuẩn + 5 TCs nâng cao chuyên sâu bóc tách mã nguồn)

---

## 1. BẢNG TỔNG HỢP MA TRẬN TEST CASES CHO FR-15

| Nhóm | Phân loại (Category) | Kỹ thuật kiểm thử | Số lượng TC | Mã định danh |
| :---: | :--- | :--- | :---: | :--- |
| **Nhóm 1** | **Broken Access Control** | Kiểm thử phân quyền RBAC & BFLA (`admin` vs `user` vs vãng lai, SEC-03) | 13 | `TC_FR15_BAC_01` → `TC_FR15_BAC_13` |
| **Nhóm 2** | **Domain & Boundary Values** | Phân tích giá trị biên (BVA) & Phân vùng tương đương (EP) cho `name`, `price`, `category_id` | 13 | `TC_FR15_DOM_01` → `TC_FR15_DOM_13` |
| **Nhóm 3** | **Type Coercion & Schema** | Kiểm thử ép kiểu (Type Coercion `price: number` vs `string`), JSON Schema Validation | 8 | `TC_FR15_TYPE_01` → `02`, `TC_FR15_SCHEMA_01` → `06` |
| **Nhóm 4** | **CRUD Lifecycle & Integrity** | Vòng đời CRUD (Create ➔ Read ➔ Update ➔ Read ➔ Delete ➔ Read 404), SQLi Protection | 6 | `TC_FR15_CRUD_01` → `TC_FR15_CRUD_06` |
| **Nhóm 5** | **Hidden Logic & Code Vulnerabilities**| Bóc tách mã nguồn Backend (`server.js`), Type Coercion chẵn lẻ, Missing Auth, SQLi HTML Leak | 5 | `TC_FR15_ADV_01` → `TC_FR15_ADV_05` |
| **TỔNG** | | | **45** | |

---

## 2. CHI TIẾT 40 TEST CASES THEO CHUẨN ISTQB & OWASP

### NHÓM 1: BROKEN ACCESS CONTROL (SEC-03 / BFLA - 13 TEST CASES)

#### TC_FR15_BAC_01
- **TC_ID:** `TC_FR15_BAC_01`
- **Category:** Broken Access Control Bug Hunter (SEC-03 - Unauthenticated POST Product)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi không có Header `Authorization` *(Bắt Bug SUT: thiếu `authenticateToken`)*
- **Pre-condition:** Khách vãng lai chưa đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Tai nghe Bluetooth Sony",
    "price": 2500000,
    "description": "Chống ồn chủ động",
    "imageUrl": "https://example.com/sony.jpg",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `401 Unauthorized`
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 401 Unauthorized for unauthenticated product creation", function () {
      pm.response.to.have.status(401);
  });
  // GHI CHÚ AUDIT: SUT hiện tại trả về 200 OK do POST /api/products không gắn authenticateToken
  ```

---

#### TC_FR15_BAC_02
- **TC_ID:** `TC_FR15_BAC_02`
- **Category:** Broken Access Control Bug Hunter (SEC-03 - Unauthenticated PUT Product)
- **Test Objective:** Kiểm tra từ chối cập nhật sản phẩm khi không có token
- **Pre-condition:** Khách vãng lai
- **Request Method & Endpoint:** `PUT /api/products/1`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Hacked Product Name",
    "price": 1000,
    "description": "Hacked",
    "imageUrl": "https://example.com/hacked.jpg",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `401 Unauthorized`
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 401 Unauthorized for unauthenticated product update", function () {
      pm.response.to.have.status(401);
  });
  ```

---

#### TC_FR15_BAC_03
- **TC_ID:** `TC_FR15_BAC_03`
- **Category:** Broken Access Control Bug Hunter (SEC-03 - Unauthenticated DELETE Product)
- **Test Objective:** Kiểm tra từ chối xóa sản phẩm khi không có token
- **Pre-condition:** Khách vãng lai
- **Request Method & Endpoint:** `DELETE /api/products/1`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `401 Unauthorized`
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 401 Unauthorized for unauthenticated product deletion", function () {
      pm.response.to.have.status(401);
  });
  ```

---

#### TC_FR15_BAC_04
- **TC_ID:** `TC_FR15_BAC_04`
- **Category:** Broken Function Level Authorization (SEC-05 / BFLA - Regular User POST)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi User thường (`role = 'user'`) gọi API Admin
- **Pre-condition:** Đăng nhập với User thường `test@eshop.com` (`user_token`)
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Unauthorized Product",
    "price": 500000,
    "description": "Created by user",
    "imageUrl": "https://example.com/item.jpg",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}` hoặc `{"error": "Admin role required"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden for regular user attempting product creation", function () {
      pm.response.to.have.status(403);
  });
  ```

---

#### TC_FR15_BAC_05
- **TC_ID:** `TC_FR15_BAC_05`
- **Category:** Broken Function Level Authorization (SEC-05 / BFLA - Regular User PUT)
- **Test Objective:** Kiểm tra từ chối cập nhật sản phẩm khi User thường gọi API
- **Pre-condition:** User thường đăng nhập
- **Request Method & Endpoint:** `PUT /api/products/1`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Tampered Name",
    "price": 1000,
    "description": "Desc",
    "imageUrl": "https://example.com/item.jpg",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden for regular user attempting product update", function () {
      pm.response.to.have.status(403);
  });
  ```

---

#### TC_FR15_BAC_06
- **TC_ID:** `TC_FR15_BAC_06`
- **Category:** Broken Function Level Authorization (SEC-05 / BFLA - Regular User DELETE)
- **Test Objective:** Kiểm tra từ chối xóa sản phẩm khi User thường gọi API
- **Pre-condition:** User thường đăng nhập
- **Request Method & Endpoint:** `DELETE /api/products/1`
- **Headers:**
  - `Authorization: Bearer {{user_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden for regular user attempting product deletion", function () {
      pm.response.to.have.status(403);
  });
  ```

---

#### TC_FR15_BAC_07
- **TC_ID:** `TC_FR15_BAC_07`
- **Category:** Access Control (Valid Admin - POST Product)
- **Test Objective:** Kiểm tra tài khoản Quản trị viên (`role = 'admin'`) tạo sản phẩm thành công
- **Pre-condition:** Đăng nhập tài khoản `admin@eshop.com` lấy `{{admin_token}}`
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Tai nghe Bluetooth Sony WH-1000XM5",
    "price": 8490000,
    "description": "Tai nghe chống ồn đỉnh cao",
    "imageUrl": "https://placehold.co/300x300/png?text=Sony+XM5",
    "category_id": 3
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `201 Created`
- **Expected Response Body / Schema:**
  ```json
  {
    "message": "Product created",
    "id": 6
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK or 201 Created for Admin", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
  });
  pm.test("Response contains product ID and success message", function () {
      var data = pm.response.json();
      pm.expect(data.message).to.eql("Product created");
      pm.expect(data).to.have.property("id");
  });
  ```

---

#### TC_FR15_BAC_08
- **TC_ID:** `TC_FR15_BAC_08`
- **Category:** Access Control (Valid Admin - PUT Product)
- **Test Objective:** Kiểm tra tài khoản Quản trị viên cập nhật thông tin sản phẩm thành công
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `PUT /api/products/1`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "iPhone 15 Pro Max 256GB - VN/A",
    "price": 29990000,
    "description": "Điện thoại Apple chính hãng",
    "imageUrl": "https://placehold.co/300x300/png?text=iPhone+15",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Product updated"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for Admin product update", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().message).to.eql("Product updated");
  });
  ```

---

#### TC_FR15_BAC_09
- **TC_ID:** `TC_FR15_BAC_09`
- **Category:** Access Control (Valid Admin - DELETE Product)
- **Test Objective:** Kiểm tra tài khoản Quản trị viên xóa sản phẩm thành công
- **Pre-condition:** Đã tạo sản phẩm nháp `id = 6`
- **Request Method & Endpoint:** `DELETE /api/products/6`
- **Headers:**
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Product deleted"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK for Admin product deletion", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().message).to.eql("Product deleted");
  });
  ```

---

#### TC_FR15_BAC_10
- **TC_ID:** `TC_FR15_BAC_10`
- **Category:** Access Control (Invalid JWT Token on POST)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi Bearer Token bị giả mạo
- **Pre-condition:** Token không hợp lệ
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer fake.jwt.admin.token`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"name": "Fake Item", "price": 100000, "category_id": 1}`
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden for forged token", function () {
      pm.response.to.have.status(403);
  });
  ```

---

#### TC_FR15_BAC_11
- **TC_ID:** `TC_FR15_BAC_11`
- **Category:** Access Control (Invalid JWT Token on PUT)
- **Test Objective:** Kiểm tra từ chối sửa sản phẩm khi Bearer Token bị giả mạo
- **Pre-condition:** Token không hợp lệ
- **Request Method & Endpoint:** `PUT /api/products/1`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer fake.jwt.admin.token`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"name": "Fake Item", "price": 100000, "category_id": 1}`
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden for forged token on PUT", function () {
      pm.response.to.have.status(403);
  });
  ```

---

#### TC_FR15_BAC_12
- **TC_ID:** `TC_FR15_BAC_12`
- **Category:** Access Control (Invalid JWT Token on DELETE)
- **Test Objective:** Kiểm tra từ chối xóa sản phẩm khi Bearer Token bị giả mạo
- **Pre-condition:** Token không hợp lệ
- **Request Method & Endpoint:** `DELETE /api/products/1`
- **Headers:**
  - `Authorization: Bearer fake.jwt.admin.token`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 403 Forbidden for forged token on DELETE", function () {
      pm.response.to.have.status(403);
  });
  ```

---

#### TC_FR15_BAC_13
- **TC_ID:** `TC_FR15_BAC_13`
- **Category:** Access Control (Privilege Escalation via Custom Admin Headers)
- **Test Objective:** User thường gửi kèm các Header đặc quyền giả lập (`X-Admin-Role: true`, `X-Role: admin`) để cố gắng tạo sản phẩm
- **Pre-condition:** User thường đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{user_token}}`
  - `X-Admin-Role: true`
  - `X-Role: admin`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"name": "Hacked Item", "price": 100000, "category_id": 1}`
- **Expected Status Code:** `403 Forbidden`
- **Expected Response Body / Schema:** `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Spoofed admin headers are ignored, returning 403 Forbidden", function () {
      pm.response.to.have.status(403);
  });
  ```

---

### NHÓM 2: DOMAIN & BOUNDARY VALUES (EP & BVA - 13 TEST CASES)

#### TC_FR15_DOM_01
- **TC_ID:** `TC_FR15_DOM_01`
- **Category:** Domain (BVA - Zero Price: `price = 0`)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi đơn giá bằng 0
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Sản phẩm 0 đồng",
    "price": 0,
    "description": "Giá bằng 0",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Price must be greater than 0"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for zero price", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR15_DOM_02
- **TC_ID:** `TC_FR15_DOM_02`
- **Category:** Domain (BVA - Negative Price: `price = -10000`)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi đơn giá âm
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Sản phẩm giá âm",
    "price": -10000,
    "description": "Giá âm",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Price must be positive"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for negative price", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR15_DOM_03
- **TC_ID:** `TC_FR15_DOM_03`
- **Category:** Domain (EP - Price Non-numeric String)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi giá tiền là chuỗi chữ cái không phải số
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Chuỗi giá",
    "price": "hai triệu đồng",
    "description": "Giá dạng chuỗi",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Price must be a valid number"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for string price", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR15_DOM_04
- **TC_ID:** `TC_FR15_DOM_04`
- **Category:** Domain (BVA - Minimum Positive Price: `price = 1000`)
- **Test Objective:** Kiểm tra tạo sản phẩm với giá tối thiểu hợp lệ
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Túi vải nhỏ",
    "price": 1000,
    "description": "Giá nhỏ nhất",
    "imageUrl": "https://placehold.co/300",
    "category_id": 3
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `201 Created`
- **Expected Response Body / Schema:** `{"message": "Product created"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200/201 for minimum valid price", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
  });
  ```

---

#### TC_FR15_DOM_05
- **TC_ID:** `TC_FR15_DOM_05`
- **Category:** Domain (BVA - Extremely Large Price: `price = 999999999999`)
- **Test Objective:** Kiểm tra xử lý an toàn khi giá tiền cực lớn mà không gây tràn số CSDL
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Siêu du thuyền xa xỉ",
    "price": 999999999999,
    "description": "Giá siêu lớn",
    "imageUrl": "https://placehold.co/300",
    "category_id": 2
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `201 Created`
- **Expected Response Body / Schema:** Không gây crash hệ thống 500
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Extremely large price handled without server crash", function () {
      pm.expect(pm.response.code).to.not.equal(500);
  });
  ```

---

#### TC_FR15_DOM_06
- **TC_ID:** `TC_FR15_DOM_06`
- **Category:** Domain (EP - Empty Name String `""`)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi tên sản phẩm là chuỗi rỗng
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "",
    "price": 500000,
    "description": "Tên rỗng",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Name is required"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for empty product name", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR15_DOM_07
- **TC_ID:** `TC_FR15_DOM_07`
- **Category:** Domain (EP - Whitespace Only Name `"   "`)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi tên chỉ chứa khoảng trắng
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "      ",
    "price": 500000,
    "description": "Khoảng trắng",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Name cannot be whitespace only"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for whitespace name", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR15_DOM_08
- **TC_ID:** `TC_FR15_DOM_08`
- **Category:** Domain (BVA - Name Min Length 1 Char)
- **Test Objective:** Kiểm tra tạo sản phẩm với độ dài tên tối thiểu 1 ký tự (`"A"`)
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "A",
    "price": 500000,
    "description": "Tên 1 ký tự",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `201 Created`
- **Expected Response Body / Schema:** `{"message": "Product created"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200/201 for 1-char name", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
  });
  ```

---

#### TC_FR15_DOM_09
- **TC_ID:** `TC_FR15_DOM_09`
- **Category:** Domain (BVA - Name Max Length 255 Chars)
- **Test Objective:** Kiểm tra tạo sản phẩm với độ dài tên tối đa 255 ký tự
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "price": 500000,
    "description": "Tên 255 ký tự",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `201 Created`
- **Expected Response Body / Schema:** `{"message": "Product created"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200/201 for 255-char name", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
  });
  ```

---

#### TC_FR15_DOM_10
- **TC_ID:** `TC_FR15_DOM_10`
- **Category:** Domain (BVA - Name Exceeding Max Length 256 Chars)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi tên vượt quá 255 ký tự (256 ký tự)
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "price": 500000,
    "description": "Tên 256 ký tự",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Name exceeds max length of 255"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for name > 255 chars", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR15_DOM_11
- **TC_ID:** `TC_FR15_DOM_11`
- **Category:** Domain (Security - Stored XSS Injection in Product Name)
- **Test Objective:** Kiểm tra khả năng xử lý an toàn khi chèn script XSS trong tên sản phẩm
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "<script>alert('XSS_PRODUCT')</script>",
    "price": 500000,
    "description": "<img src=x onerror=alert(1)>",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `200 OK` hoặc `201 Created`
- **Expected Response Body / Schema:** Lưu an toàn dạng literal / escaped
- **Postman Chai Assertion:**
  ```javascript
  pm.test("XSS payload handled safely without 500 error", function () {
      pm.expect(pm.response.code).to.not.equal(500);
  });
  ```

---

#### TC_FR15_DOM_12
- **TC_ID:** `TC_FR15_DOM_12`
- **Category:** Domain (Foreign Key Constraint - Non-existent Category ID `9999`)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi `category_id` không tồn tại trong CSDL
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Sản phẩm sai danh mục",
    "price": 500000,
    "description": "Category 9999",
    "imageUrl": "https://placehold.co/300",
    "category_id": 9999
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Invalid category_id"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for non-existent category", function () {
      pm.response.to.have.status(400);
  });
  ```

---

#### TC_FR15_DOM_13
- **TC_ID:** `TC_FR15_DOM_13`
- **Category:** Domain (Foreign Key Constraint - Negative Category ID `-1`)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi `category_id` là số âm
- **Pre-condition:** Admin đã đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Sản phẩm category âm",
    "price": 500000,
    "description": "Category -1",
    "imageUrl": "https://placehold.co/300",
    "category_id": -1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Invalid category_id"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for negative category_id", function () {
      pm.response.to.have.status(400);
  });
  ```

---

### NHÓM 3: TYPE COERCION & SCHEMA VALIDATION (8 TEST CASES)

#### TC_FR15_TYPE_01
- **TC_ID:** `TC_FR15_TYPE_01`
- **Category:** Type Coercion Bug Hunter (Even ID Price String Coercion)
- **Test Objective:** Kiểm tra `GET /api/products/2` (ID chẵn) có trả về đúng kiểu `price: number` hay bị ép kiểu sai thành `string` *(Bắt Bug SUT `row.price = row.price.toString()`)*
- **Pre-condition:** Sản phẩm `id = 2` tồn tại trong database (Samsung Galaxy S24 Ultra)
- **Request Method & Endpoint:** `GET /api/products/2`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `price` bắt buộc phải là kiểu `number` (`typeof price === 'number'`)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 200 OK", function () {
      pm.response.to.have.status(200);
  });
  pm.test("CRITICAL: Price MUST be a number, NOT a string (Type Coercion Bug Check)", function () {
      var product = pm.response.json();
      pm.expect(product.price).to.be.a("number");
      pm.expect(typeof product.price).to.not.equal("string");
  });
  // GHI CHÚ AUDIT: SUT có bug ở dòng 162: if (row.id % 2 === 0) row.price = row.price.toString();
  ```

---

#### TC_FR15_TYPE_02
- **TC_ID:** `TC_FR15_TYPE_02`
- **Category:** Type Coercion Consistency (Odd ID vs Even ID Price Comparison)
- **Test Objective:** So sánh kiểu dữ liệu của `price` giữa sản phẩm ID lẻ (`id = 1`) và ID chẵn (`id = 2`) đảm bảo nhất quán
- **Pre-condition:** Sản phẩm `id = 1` và `id = 2` có sẵn
- **Request Method & Endpoint:** `GET /api/products/1`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `typeof product.price === 'number'`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Odd ID product price is a number", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().price).to.be.a("number");
  });
  ```

---

#### TC_FR15_SCHEMA_01
- **TC_ID:** `TC_FR15_SCHEMA_01`
- **Category:** Schema Validation (POST /api/products 200/201 Response Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema phản hồi khi tạo sản phẩm thành công
- **Pre-condition:** Admin đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"name": "Item Schema", "price": 100000, "category_id": 1}`
- **Expected Status Code:** `200 OK` hoặc `201 Created`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["message", "id"],
    "properties": {
      "message": { "type": "string" },
      "id": { "type": "integer" }
    }
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  var schema = {
      "type": "object",
      "required": ["message", "id"],
      "properties": {
          "message": { "type": "string" },
          "id": { "type": "integer" }
      }
  };
  pm.test("POST response matches JSON Schema", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
      pm.expect(tv4.validate(pm.response.json(), schema)).to.be.true;
  });
  ```

---

#### TC_FR15_SCHEMA_02
- **TC_ID:** `TC_FR15_SCHEMA_02`
- **Category:** Schema Validation (GET /api/products/:id Response Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema đầy đủ của API lấy chi tiết sản phẩm
- **Pre-condition:** Sản phẩm `id = 1` tồn tại
- **Request Method & Endpoint:** `GET /api/products/1`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:**
  ```json
  {
    "type": "object",
    "required": ["id", "name", "price", "description", "imageUrl", "category_id"],
    "properties": {
      "id": { "type": "integer" },
      "name": { "type": "string" },
      "price": { "type": "number" },
      "description": { "type": "string" },
      "imageUrl": { "type": "string" },
      "category_id": { "type": "integer" }
    }
  }
  ```
- **Postman Chai Assertion:**
  ```javascript
  var productSchema = {
      "type": "object",
      "required": ["id", "name", "price", "category_id"],
      "properties": {
          "id": { "type": "integer" },
          "name": { "type": "string" },
          "price": { "type": "number" },
          "category_id": { "type": "integer" }
      }
  };
  pm.test("GET product details conforms to Product JSON Schema", function () {
      pm.response.to.have.status(200);
      pm.expect(tv4.validate(pm.response.json(), productSchema)).to.be.true;
  });
  ```

---

#### TC_FR15_SCHEMA_03
- **TC_ID:** `TC_FR15_SCHEMA_03`
- **Category:** Schema Validation (PUT /api/products/:id Response Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema phản hồi khi cập nhật sản phẩm
- **Pre-condition:** Admin đăng nhập
- **Request Method & Endpoint:** `PUT /api/products/1`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"name": "Updated Name", "price": 200000, "category_id": 1}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"type": "object", "required": ["message"], "properties": {"message": {"type": "string"}}}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("PUT response contains message string", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json()).to.have.property("message");
  });
  ```

---

#### TC_FR15_SCHEMA_04
- **TC_ID:** `TC_FR15_SCHEMA_04`
- **Category:** Schema Validation (DELETE /api/products/:id Response Schema)
- **Test Objective:** Kiểm tra cấu trúc JSON Schema phản hồi khi xóa sản phẩm
- **Pre-condition:** Admin đăng nhập, sản phẩm tồn tại
- **Request Method & Endpoint:** `DELETE /api/products/5`
- **Headers:**
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `{"message": "Product deleted"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("DELETE response contains message string", function () {
      pm.response.to.have.status(200);
      pm.expect(pm.response.json().message).to.eql("Product deleted");
  });
  ```

---

#### TC_FR15_SCHEMA_05
- **TC_ID:** `TC_FR15_SCHEMA_05`
- **Category:** Schema Bug Hunter (Non-existent Product GET Status 404)
- **Test Objective:** Kiểm tra gọi sản phẩm không tồn tại `GET /api/products/999999` phải trả về `404 Not Found` *(Bắt Bug SUT: trả về 200 OK kèm `{}`)*
- **Pre-condition:** Không có sản phẩm 999999
- **Request Method & Endpoint:** `GET /api/products/999999`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "Product not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Non-existent product MUST return 404 Not Found", function () {
      pm.response.to.have.status(404);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  // GHI CHÚ AUDIT: SUT có bug ở dòng 161: if (!row) return res.status(200).json({});
  ```

---

#### TC_FR15_SCHEMA_06
- **TC_ID:** `TC_FR15_SCHEMA_06`
- **Category:** Schema Validation (400 Bad Request Error Schema)
- **Test Objective:** Kiểm tra schema trả về khi gửi payload thiếu các trường bắt buộc
- **Pre-condition:** Admin đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{}`
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "..."}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Status code is 400 Bad Request for empty payload", function () {
      pm.response.to.have.status(400);
  });
  ```

---

### NHÓM 4: CRUD LIFECYCLE & DATA INTEGRITY (6 TEST CASES)

#### TC_FR15_CRUD_01
- **TC_ID:** `TC_FR15_CRUD_01`
- **Category:** CRUD Lifecycle (Full End-to-End Lifecycle Verification)
- **Test Objective:** Thực thi trọn vẹn luồng: Tạo mới ➔ Lấy chi tiết ➔ Cập nhật ➔ Lấy xác thực ➔ Xóa ➔ Lấy kiểm tra 404
- **Pre-condition:** Admin đăng nhập
- **Request Method & Endpoint:** `POST /api/products` ➔ `GET` ➔ `PUT` ➔ `GET` ➔ `DELETE` ➔ `GET`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body (POST):**
  ```json
  {
    "name": "Chuột Gaming Logitech G502",
    "price": 1290000,
    "description": "Cảm biến Hero 25K",
    "imageUrl": "https://placehold.co/300",
    "category_id": 3
  }
  ```
- **Expected Status Code:** Tất cả bước thành công theo đúng thứ tự
- **Expected Response Body / Schema:** Trạng thái sản phẩm nhất quán qua từng bước
- **Postman Chai Assertion:**
  ```javascript
  pm.test("CRUD Lifecycle step executed successfully", function () {
      pm.expect(pm.response.code).to.be.oneOf([200, 201]);
  });
  ```

---

#### TC_FR15_CRUD_02
- **TC_ID:** `TC_FR15_CRUD_02`
- **Category:** Data Integrity (Product Isolation Check)
- **Test Objective:** Cập nhật sản phẩm A không làm thay đổi giá và tên của sản phẩm B
- **Pre-condition:** Sản phẩm 1 và 2 có sẵn
- **Request Method & Endpoint:** `PUT /api/products/1` theo sau bởi `GET /api/products/2`
- **Headers:**
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"name": "iPhone Modified", "price": 99999, "category_id": 1}`
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** Sản phẩm 2 vẫn giữ nguyên giá 28,000,000
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Product 2 remains unchanged after updating Product 1", function () {
      pm.response.to.have.status(200);
      var p2 = pm.response.json();
      pm.expect(p2.id).to.eql(2);
      pm.expect(p2.name).to.include("Samsung");
  });
  ```

---

#### TC_FR15_CRUD_03
- **TC_ID:** `TC_FR15_CRUD_03`
- **Category:** CRUD (Update Non-existent Product ID `999999`)
- **Test Objective:** Kiểm tra cập nhật sản phẩm không tồn tại
- **Pre-condition:** Không có sản phẩm 999999
- **Request Method & Endpoint:** `PUT /api/products/999999`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** `{"name": "No Item", "price": 1000, "category_id": 1}`
- **Expected Status Code:** `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "Product not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR15_CRUD_03: Updating non-existent product MUST return 404 Not Found", function () {
      pm.response.to.have.status(404);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  ```

---

#### TC_FR15_CRUD_04
- **TC_ID:** `TC_FR15_CRUD_04`
- **Category:** CRUD (Delete Non-existent Product ID `999999`)
- **Test Objective:** Kiểm tra xóa sản phẩm không tồn tại
- **Pre-condition:** Không có sản phẩm 999999
- **Request Method & Endpoint:** `DELETE /api/products/999999`
- **Headers:**
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "Product not found"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR15_CRUD_04: Deleting non-existent product MUST return 404 Not Found", function () {
      pm.response.to.have.status(404);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  ```

---

#### TC_FR15_CRUD_05
- **TC_ID:** `TC_FR15_CRUD_05`
- **Category:** Security Bug Hunter (SQL Injection in Search Query String)
- **Test Objective:** Kiểm tra khả năng chống SQL Injection trong API tìm kiếm sản phẩm *(Bắt Bug SUT dòng 144: string interpolation `${searchQuery}`)*
- **Pre-condition:** Không cần auth
- **Request Method & Endpoint:** `GET /api/products?search=' OR '1'='1`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK` (Parameterized) hoặc `400 Bad Request`
- **Expected Response Body / Schema:** JSON Array, **KHÔNG ĐƯỢC trả về HTML 500 `<h1>Database Error</h1>`**
- **Postman Chai Assertion:**
  ```javascript
  pm.test("Search API handles SQLi safely without 500 HTML Error", function () {
      pm.expect(pm.response.code).to.not.equal(500);
      pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
  });
  ```

---

#### TC_FR15_CRUD_06
- **TC_ID:** `TC_FR15_CRUD_06`
- **Category:** Security (SQL Injection in Product ID Path Param)
- **Test Objective:** Kiểm tra chống SQL Injection khi xóa sản phẩm qua path parameter `:id`
- **Pre-condition:** Admin đăng nhập
- **Request Method & Endpoint:** `DELETE /api/products/1 OR 1=1`
- **Headers:**
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `404 Not Found` hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Không xóa toàn bộ bảng dữ liệu
- **Postman Chai Assertion:**
  ```javascript
  pm.test("SQL Injection in DELETE path param handled safely", function () {
      pm.expect(pm.response.code).to.not.equal(500);
  });
  ```

---

### NHÓM 5: TÌNH HUỐNG BIÊN NÂNG CAO & BÓC TÁCH MÃ NGUỒN ẨN (5 ADVANCED TEST CASES)

> **Mục đích nhóm 5:** Khai thác các kẽ hở phân quyền RBAC/BFLA, lỗi ép kiểu ngầm theo ID chẵn/lẻ (Type Coercion), và lỗi rò rỉ mã HTML 500 khi dính SQLi trong `server.js` (dòng 141–196).

---

#### TC_FR15_ADV_01
- **TC_ID:** `TC_FR15_ADV_01`
- **Category:** Broken Function Level Authorization (Unauthenticated Product Mutation Bug - SEC-03/SEC-05)
- **Test Objective:** Kiểm tra lỗ hổng phân quyền nghiêm trọng: Khách vãng lai KHÔNG CÓ TOKEN hoặc User thường (`role = 'user'`) gọi `POST /api/products` để thêm sản phẩm mới mà không bị chặn *(Bắt Bug SUT dòng 167: hoàn toàn thiếu middleware `authenticateToken`)*
- **Pre-condition:** Khách vãng lai chưa đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Hack Product Without Auth",
    "price": 1000,
    "description": "Created by unauthenticated user",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `401 Unauthorized` (Nếu không có token) hoặc `403 Forbidden` (Nếu là User thường)
- **Expected Response Body / Schema:** `{"error": "Unauthorized"}` hoặc `{"error": "Forbidden"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR15_ADV_01: CRITICAL BFLA - Product creation without admin token MUST be rejected", function () {
      pm.expect(pm.response.code).to.be.oneOf([401, 403]);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  // GHI CHÚ AUDIT: SUT hiện tại trả về 200 OK do POST/PUT/DELETE /api/products không gắn authenticateToken
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Khi sinh test cho nhóm chức năng "Quản trị Sản phẩm Admin (Admin CRUD)", các prompt AI thông thường tự động thiết lập kịch bản lý tưởng (Happy Path Pre-condition): Tạo token Admin trước, sau đó truyền Header `Authorization: Bearer {{admin_token}}` vào 100% các request POST, PUT, DELETE. AI hoàn toàn bỏ quên việc kiểm tra ranh giới phân quyền âm (Negative Access Control Testing) bằng cách thử gửi request *không có token* hoặc *dùng token của người dùng thông thường*. Điều này khiến lỗ hổng Broken Access Control nghiêm trọng bậc nhất hệ thống bị bỏ lọt hoàn toàn trong suốt quá trình kiểm thử.

---

#### TC_FR15_ADV_02
- **TC_ID:** `TC_FR15_ADV_02`
- **Category:** Type Coercion Bug Hunter (Modulo-Based Parity String Coercion on Even IDs)
- **Test Objective:** Kiểm tra tính toàn vẹn kiểu dữ liệu: Gọi `GET /api/products/2` (ID chẵn) để phát hiện trường `price` bị ép kiểu sai trái từ kiểu số (`number`) thành chuỗi ký tự (`string`) *(Bắt Bug SUT dòng 162: `if (row.id % 2 === 0) row.price = row.price.toString();`)*
- **Pre-condition:** Sản phẩm `id = 2` tồn tại trong database
- **Request Method & Endpoint:** `GET /api/products/2`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK`
- **Expected Response Body / Schema:** `typeof product.price === 'number'` (Bắt buộc là kiểu số học, không được là chuỗi string)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR15_ADV_02: CRITICAL - Product price MUST be a numeric type for both even and odd IDs", function () {
      pm.response.to.have.status(200);
      var product = pm.response.json();
      pm.expect(product.price).to.be.a("number");
      pm.expect(typeof product.price).to.not.equal("string");
  });
  // GHI CHÚ AUDIT: SUT có bug ở dòng 162 chuyển giá tiền của các sản phẩm có ID chẵn thành String
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* AI sinh test tự động thường chỉ chọn một mẫu dữ liệu đơn lẻ (ví dụ: `GET /api/products/1` hoặc lấy `id` vừa tạo ở bước POST đầu tiên). Nếu sản phẩm được kiểm tra tình cờ rơi vào ID lẻ (`id = 1`), assertion `typeof price === 'number'` sẽ luôn ĐẠT (Passed). AI không có khả năng tự động phân tích mã nguồn (Static Code Analysis) để nhận ra sự tồn tại của logic phân nhánh quái dị dựa trên tính chẵn lẻ của ID (`row.id % 2 === 0`). Khi ứng dụng Web/Mobile nhận giá tiền dạng chuỗi `"28000000"` cho ID chẵn, các phép tính cộng giỏ hàng sẽ bị lỗi ghép chuỗi (`"28000000" + 500000 = "28000000500000"`).

---

#### TC_FR15_ADV_03
- **TC_ID:** `TC_FR15_ADV_03`
- **Category:** Schema Bug Hunter (Silent 200 OK False-Positive with Empty Object on Non-Existent Entity)
- **Test Objective:** Kiểm tra mã trạng thái HTTP chuẩn RESTful khi truy vấn sản phẩm không tồn tại `GET /api/products/999999` *(Bắt Bug SUT dòng 161: `if (!row) return res.status(200).json({});`)*
- **Pre-condition:** Không có sản phẩm với `id = 999999` trong database
- **Request Method & Endpoint:** `GET /api/products/999999`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `404 Not Found`
- **Expected Response Body / Schema:** `{"error": "Product not found"}` (Tuyệt đối không được trả về `200 OK` kèm object rỗng `{}`)
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR15_ADV_03: Non-existent product query MUST return 404 Not Found, NOT 200 with {}", function () {
      pm.response.to.have.status(404);
      var data = pm.response.json();
      pm.expect(data).to.have.property("error");
      pm.expect(data).to.not.deep.equal({});
  });
  // GHI CHÚ AUDIT: SUT trả về 200 OK kèm {} làm sập logic xử lý lỗi Not Found trên Frontend
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Khi kiểm thử các mã lỗi Not Found, nếu một AI tạo assertion lỏng lẻo dạng `pm.expect(pm.response.code).to.be.oneOf([200, 404])` hoặc chỉ kiểm tra `pm.response.to.be.json`, test case sẽ vô tình bị coi là ĐẠT (False Positive). AI không nhận thức được tiêu chuẩn thiết kế RESTful API (RFC 7231): Việc trả về `200 OK` cho một tài nguyên không tồn tại làm cho các thư viện HTTP client (như Axios, Fetch) không thể bắt được lỗi trong khối `catch()`, khiến giao diện hiển thị sản phẩm rỗng không có tên và không có giá.

---

#### TC_FR15_ADV_04
- **TC_ID:** `TC_FR15_ADV_04`
- **Category:** Domain Constraint Enforcement (Negative and Zero Price Creation Bypass)
- **Test Objective:** Kiểm tra từ chối tạo sản phẩm khi đơn giá là số âm (`price = -50000`) hoặc bằng 0 *(Bắt Bug SUT dòng 167–176: hoàn toàn thiếu tầng Validation dữ liệu đầu vào)*
- **Pre-condition:** Admin đăng nhập
- **Request Method & Endpoint:** `POST /api/products`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer {{admin_token}}`
  - `X-Student-Id: 23127092`
- **Request Body:**
  ```json
  {
    "name": "Sản phẩm giá âm nguy hiểm",
    "price": -50000,
    "description": "Giá âm làm sập tổng tiền giỏ hàng",
    "imageUrl": "https://placehold.co/300",
    "category_id": 1
  }
  ```
- **Expected Status Code:** `400 Bad Request`
- **Expected Response Body / Schema:** `{"error": "Price must be greater than 0"}`
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR15_ADV_04: Negative price MUST be rejected with 400 Bad Request", function () {
      pm.response.to.have.status(400);
      pm.expect(pm.response.json()).to.have.property("error");
  });
  // GHI CHÚ AUDIT: SUT hiện tại chấp nhận lưu giá âm vào database và trả về 200 OK
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Các công cụ sinh test AI thông thường thường tập trung kiểm tra các trường kiểu chuỗi (như tên rỗng, tên quá dài) và giả định rằng kiểu số sẽ luôn được hệ thống bảo vệ tự nhiên. AI ít khi suy luận đến hệ quả domino trong nghiệp vụ E-commerce: Nếu một sản phẩm giá âm được lưu thành công vào CSDL, người dùng có thể thêm sản phẩm này vào giỏ hàng để trừ bớt tổng tiền thanh toán (Negative Price Exploit).

---

#### TC_FR15_ADV_05
- **TC_ID:** `TC_FR15_ADV_05`
- **Category:** Security Bug Hunter (SQL Injection in Search Query Causing Unhandled HTML 500 Leak)
- **Test Objective:** Kiểm tra khả năng chống SQL Injection trong tham số tìm kiếm: Gửi chuỗi inject `GET /api/products?search=' OR '1'='1` hoặc ký tự nháy đơn `'` để chứng minh backend bị lỗi cú pháp SQL và trả về trang HTML 500 thô *(Bắt Bug SUT dòng 144–149: nối chuỗi trực tiếp `${searchQuery}`)*
- **Pre-condition:** Không cần đăng nhập
- **Request Method & Endpoint:** `GET /api/products?search='`
- **Headers:**
  - `X-Student-Id: 23127092`
- **Request Body:** N/A
- **Expected Status Code:** `200 OK` (Xử lý an toàn bằng Parameterized Query) hoặc `400 Bad Request`
- **Expected Response Body / Schema:** Bắt buộc phải là JSON (`Content-Type: application/json`), **TUYỆT ĐỐI KHÔNG ĐƯỢC LÀ HTML 500 VỚI NỘI DUNG `<h1>Database Error</h1>`**
- **Postman Chai Assertion:**
  ```javascript
  pm.test("TC_FR15_ADV_05: CRITICAL SEC-06 - Search API must use Parameterized Query and NEVER return HTML 500", function () {
      pm.expect(pm.response.code).to.not.equal(500);
      pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json");
      pm.expect(pm.response.text()).to.not.include("Database Error");
  });
  // GHI CHÚ AUDIT: SUT trả về HTML 500 <h1>Database Error</h1> làm lộ lỗi cú pháp SQLite
  ```
- **TẠI SAO AI THÔNG THƯỜNG LẠI BỎ SÓT CA NÀY?**
  > *Phân tích kỹ thuật của QA Lead:* Khi kiểm tra tính năng tìm kiếm, AI thường chỉ gửi các từ khóa chữ cái thông thường (`?search=Sony`, `?search=Samsung`). Khi thực hiện kiểm thử bảo mật SQLi, AI thường chỉ kiểm tra assertion thụ động `pm.response.to.not.have.status(500)`. AI không kiểm tra Header `Content-Type` và không kiểm tra chuỗi trả về có chứa mã HTML rò rỉ cấu trúc database hay không. Trong kiến trúc RESTful API, việc một endpoint trả về HTML thay vì JSON khi gặp ký tự đặc biệt là một lỗi nghiêm trọng về cấu hình bảo mật (OWASP API Security Top 8: Security Misconfiguration / CWE-209).

