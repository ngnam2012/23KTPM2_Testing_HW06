# HW06: API TESTING VỚI AI & POSTMAN/NEWMAN (ESHOP SUT)

> **Môn học:** Software Testing (CS423 / CSC13003) | **Khoa:** Công nghệ Thông tin – FIT@HCMUS  
> **Sinh viên thực hiện:** Nguyễn Nhật Nam | **MSSV:** `23127092` | **Lớp:** `23KTPM2`  
> **Repository:** [https://github.com/ngnam2012/23KTPM2_Testing_HW06](https://github.com/ngnam2012/23KTPM2_Testing_HW06)  
> **Hệ thống SUT:** EShop Backend (`Node.js/Express + SQLite3`)  
> **Anti-Cheat Headers:** Bắt buộc gắn `X-Student-Id: 23127092` trên 100% Request  
> **Thang đo Bloom-AI đạt được:** **G9.2 (Apply) ➔ G9.3 (Analyse) ➔ G9.4 (Collaborate) ➔ G9.5 (Create)**  

---

## 1. THÔNG TIN SINH VIÊN & BẢNG TỰ ĐÁNH GIÁ (SELF-ASSESSMENT)

- **Họ và tên:** Nguyễn Nhật Nam
- **MSSV:** `23127092`
- **Lớp:** `23KTPM2`
- **Mã bài tập:** `HW06-AI`
- **Điểm tự đánh giá:** **`100 / 100`**

### Bảng Tự Đánh Giá Chi Tiết Theo Tiêu Chí Đề Bài (Rubric)

| STT | Tiêu chí đánh giá (Rubric) | Điểm tối đa | Điểm tự chấm | Minh chứng & Artifacts tương ứng |
| :---: | :--- | :---: | :---: | :--- |
| **1** | **API 1 — Full Pipeline (FR-04: Profile Management - Pool A)**<br>• AI Generation (≥ 35 TCs)<br>• Human Audit (Valid/Invalid/Incomplete)<br>• Extension (≥ 5 TCs AI bỏ sót)<br>• Newman Execution & HTML Report<br>• Phát hiện & Báo cáo Bug chi tiết | 30 | **30** | • **44 TCs** (39 TCs chuẩn + 5 TCs nâng cao)<br>• 44/44 TCs chạy độc lập trong Postman/Newman (47 Reqs, 59 Assertions)<br>• Bắt **5 Bugs** (Mass Assignment, Phone Regex, Password Leak...)<br>• [FR04_TestCases.md](test-cases/FR04/FR04_TestCases.md)<br>• [FR04_Newman_Report.html](reports/FR04_Newman_Report.html) |
| **2** | **API 2 — Full Pipeline (FR-10: Order State Machine - Pool B)**<br>• AI Generation (≥ 35 TCs)<br>• Human Audit (Valid/Invalid/Incomplete)<br>• Extension (≥ 5 TCs AI bỏ sót)<br>• Newman Execution & HTML Report<br>• Phát hiện & Báo cáo Bug chi tiết | 30 | **30** | • **45 TCs** (40 TCs chuẩn + 5 TCs nâng cao)<br>• 45/45 TCs chạy độc lập trong Postman/Newman (48 Reqs, 52 Assertions)<br>• Bắt **3 Bugs** (BOLA/IDOR on GET, Hủy đơn Shipping...)<br>• [FR10_TestCases.md](test-cases/FR10/FR10_TestCases.md)<br>• [FR10_Newman_Report.html](reports/FR10_Newman_Report.html) |
| **3** | **API 3 — Full Pipeline (FR-15: Admin Product CRUD - Pool C)**<br>• AI Generation (≥ 35 TCs)<br>• Human Audit (Valid/Invalid/Incomplete)<br>• Extension (≥ 5 TCs AI bỏ sót)<br>• Newman Execution & HTML Report<br>• Phát hiện & Báo cáo Bug chi tiết | 30 | **30** | • **45 TCs** (40 TCs chuẩn + 5 TCs nâng cao)<br>• 45/45 TCs chạy độc lập trong Postman/Newman (48 Reqs, 50 Assertions)<br>• Bắt **5 Bugs** (Thiếu Auth, Type Coercion ID chẵn, Price âm...)<br>• [FR15_TestCases.md](test-cases/FR15/FR15_TestCases.md)<br>• [FR15_Newman_Report.html](reports/FR15_Newman_Report.html) |
| **+** | **API 4 (Bonus Mở rộng) — FR-09: Mobile Apply Coupon (Pool D)**<br>• Hoàn thành trọn vẹn cả 4 Pools A, B, C, D | *Bonus* | *Bonus* | • **45 TCs** (Ma trận C1-C5, Bắt Math Bug `1 - discount_value`, C3 Boundary)<br>• 45/45 TCs chạy độc lập trong Postman/Newman (48 Reqs, 50 Assertions)<br>• [FR09_Mobile_TestCases.md](test-cases/FR09_Mobile/FR09_Mobile_TestCases.md)<br>• [FR09_Newman_Report.html](reports/FR09_Newman_Report.html) |
| **4** | **Agent Skill (AI-Driven API Test Generator - G9.5 Create)**<br>• Sơ đồ kiến trúc tự thiết kế (Self-drawn Diagram)<br>• Mã giả (Pseudocode) & Tài liệu thiết kế kiến trúc<br>• Mã nguồn thực thi Python sinh test cho toàn bộ 19 FRs | 10 | **10** | • Sơ đồ Mermaid & Mã giả: [generator/generator_design.md](generator/generator_design.md)<br>• Script Python: [generator/api_test_agent.py](generator/api_test_agent.py)<br>• Agent Skill Manifest: [generator/SKILL.md](generator/SKILL.md) |
| **TỔNG** | **TOÀN BỘ YÊU CẦU HW06 (G9.2 ➔ G9.5)** | **100** | **100** | **Xuất sắc, đầy đủ 100% tài liệu và bằng chứng thực thi 1-to-1** |

---

## 2. BẢNG TỔNG KẾT KIỂM THỬ (TEST SUMMARY REPORT)

```
┌─────────┬──────────────────────────────────┬──────────┬───────────┬──────────────┬───────────────┬─────────────────────────────────┐
│ Mã FR   │ Chức năng & Phân vùng (Pool)     │ Số TCs   │ Requests  │ Assertions   │ Bugs SUT      │ Báo cáo HTML & JSON             │
├─────────┼──────────────────────────────────┼──────────┼───────────┼──────────────┼───────────────┼─────────────────────────────────┤
│ FR-04   │ Quản lý Hồ sơ Cá nhân (Pool A)   │ 44 TCs   │ 47 Reqs   │ 21P / 38F    │ 5 Bugs        │ reports/FR04_Newman_Report.html │
│ FR-10   │ Máy Trạng thái & Hủy Đơn(Pool B) │ 45 TCs   │ 48 Reqs   │ 20P / 32F    │ 3 Bugs        │ reports/FR10_Newman_Report.html │
│ FR-15   │ Quản lý Sản phẩm Admin (Pool C)  │ 45 TCs   │ 48 Reqs   │ 22P / 28F    │ 5 Bugs        │ reports/FR15_Newman_Report.html │
│ FR-09   │ Áp dụng Mã Giảm Giá (Pool D)    │ 45 TCs   │ 48 Reqs   │ 22P / 28F    │ 3 Bugs        │ reports/FR09_Newman_Report.html │
├─────────┼──────────────────────────────────┼──────────┼───────────┼──────────────┼───────────────┼─────────────────────────────────┤
│ TỔNG    │ 4 POOLS HOÀN TẤT 100%            │ 179 TCs  │ 191 Reqs  │ 85P / 126F   │ 16 BUGS SUT   │ Đầy đủ 8 file HTML + JSON       │
└─────────┴──────────────────────────────────┴──────────┴───────────┴──────────────┴───────────────┴─────────────────────────────────┘
```

- **Tổng số APIs / Chức năng thực hiện:** 4 FRs (FR-04, FR-10, FR-15, FR-09).
- **Tổng số Test Cases thiết kế:** **179 Test Cases** (Trung bình 45 TCs / FR, vượt chuẩn yêu cầu ≥ 35 TCs/FR).
- **Tổng số Requests thực thi trong Newman:** **191 requests** (Bao gồm các bước nạp token xác thực tự động).
- **Số Test Cases mở rộng bởi con người (Human Extension):** **20 TCs nâng cao (Group 5)** đào sâu mã nguồn.
- **Tổng số lỗi thực tế phát hiện trong SUT:** **16 Bugs nghiêm trọng** (Mass Assignment, BOLA trên GET, Broken Access Control, Math Bug...).
- **Độ chính xác Anti-Cheat Header:** **100% requests** đều mang header `X-Student-Id: 23127092`.

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN (PROJECT REPOSITORY LAYOUT)

```
23KTPM2_Testing_HW06/
├── collections/                               # Bộ Postman Collections chuẩn v2.1.0 (179 TCs)
│   ├── FR04_Profile_Management.postman_collection.json
│   ├── FR10_Order_State_Machine.postman_collection.json
│   ├── FR15_Admin_Product_CRUD.postman_collection.json
│   ├── FR09_Mobile_Coupon.postman_collection.json
│   └── AutoGenerated_Collection.postman_collection.json
├── data/                                      # Dữ liệu kiểm thử JSON Data-driven
│   ├── fr04_test_data.json
│   ├── fr10_test_data.json
│   ├── fr15_test_data.json
│   └── fr09_test_data.json
├── test-cases/                                # Báo cáo đặc tả Test Cases và Kết quả thực thi
│   ├── EShop_TestCases_All.xlsx              # Bảng tính Excel 6 Sheets chứa 179 TCs & 16 Bugs
│   ├── FR04/                                  # FR04_TestCases.md & FR04_TestExecution_Results.md
│   ├── FR10/                                  # FR10_TestCases.md & FR10_TestExecution_Results.md
│   ├── FR15/                                  # FR15_TestCases.md & FR15_TestExecution_Results.md
│   └── FR09_Mobile/                           # FR09_Mobile_TestCases.md & FR09_TestExecution_Results.md
├── reports/                                   # Báo cáo đồ họa tương tác Newman HTML Extra & JSON
│   ├── FR04_Newman_Report.html & .json
│   ├── FR10_Newman_Report.html & .json
│   ├── FR15_Newman_Report.html & .json
│   └── FR09_Newman_Report.html & .json
├── generator/                                 # Module AI Test Generator (Agent Skill - G9.5)
│   ├── generator_design.md                    # Sơ đồ Mermaid tự thiết kế & Mã giả thuật toán
│   ├── api_test_agent.py                      # Script Python sinh test tự động cho toàn bộ 19 FRs
│   └── SKILL.md                               # Đặc tả Agent Skill tái sử dụng
├── openapi/                                   # Đặc tả chuẩn OpenAPI 3.0 YAML
│   └── eshop_openapi.yaml                     # Đặc tả 17+ Endpoints và Schemas
├── ci-cd/                                     # Báo cáo Tích hợp CI/CD Pipeline
│   └── ci_cd_report.md                        # Minh chứng 2 sample commits (Green All-Pass & Red Bug-Fail)
├── .github/workflows/                         # Cấu hình GitHub Actions
│   └── api-tests.yml
├── eshop-sut/                                 # Mã nguồn hệ thống backend SUT
├── main_report.md                             # BÁO CÁO TỔNG HỢP TOÀN DỰ ÁN
├── ai_audit_report.md                         # BÁO CÁO KIỂM TOÁN AI (Chuẩn mẫu FIT@HCMUS)
├── ai_critique.md                             # BÀI PHẢN BIỆN HỌC THUẬT AI (275 từ)
├── git_commit_log.txt                         # Nhật ký lịch sử Git commit
├── package.json                               # Cấu hình NPM scripts chạy test Newman
└── README.md                                  # Hướng dẫn tổng quan & Bảng tự chấm điểm
```

---

## 4. HƯỚNG DẪN CÀI ĐẶT & THỰC THI KIỂM THỬ (QUICK START)

### 4.1. Khởi động Backend SUT (Node.js/Express + SQLite)
```bash
# 1. Di chuyển vào thư mục backend
cd eshop-sut/backend

# 2. Cài đặt thư viện dependencies
npm install

# 3. Tái tạo database SQLite sạch sẽ & nạp dữ liệu mẫu
node database.js

# 4. Khởi động backend server (Cổng 3000)
node server.js
```

### 4.2. Chạy Kiểm Thử Tự Động Với Newman CLI
Tại thư mục gốc của repository:
```bash
# Cài đặt thư viện kiểm thử (Newman & Reporter HTML Extra)
npm install

# Chạy toàn bộ 4 Pool kiểm thử và xuất báo cáo
npm run test:fr04
npm run test:fr10
npm run test:fr15
npm run test:fr09
```

### 4.3. Chạy Module AI Test Generator (Sinh Test Tự Động)
```bash
# Sinh test cho toàn bộ 19 chức năng trong hệ thống EShop:
python generator/api_test_agent.py --target-fr ALL --student-id 23127092 --output-collection collections/AutoGenerated_Collection.postman_collection.json
```

---

## 5. MINH CHỨNG 16 LỖ HỔNG & BẢO MẬT PHÁT HIỆN TRONG SUT

1. `BUG_FR04_01` (Critical - SEC-06): Privilege Escalation qua Mass Assignment (`role: 'admin'`).
2. `BUG_FR04_02` (Medium - Domain): Thiếu kiểm tra regex và độ dài số điện thoại (`^0[0-9]{9,10}$`).
3. `BUG_FR04_03` (High - SEC-07): Rò rỉ thông tin mật khẩu `password` trong `GET /api/users/me`.
4. `BUG_FR04_04` (High - Data Integrity): Partial Update xóa trắng `phone` và `shipping_address` thành `NULL`.
5. `BUG_FR04_05` (High - SEC-07): Rò rỉ toàn bộ metadata an ninh (`reset_token`, `login_attempts`, `locked_until`).
6. `BUG_FR10_01` (Critical - SEC-01): Lỗ hổng BOLA/IDOR trên `GET /api/orders/:id` (hoàn toàn thiếu auth).
7. `BUG_FR10_02` (High - State Machine): Cho phép người dùng hủy đơn hàng đang giao `shipping`.
8. `BUG_FR10_03` (Medium - Info Disclosure): Dò quét ID đơn hàng qua phản hồi bất đối xứng PUT (404) và GET (200).
9. `BUG_FR15_01` (Critical - SEC-03): Broken Access Control trên cả 3 route `POST/PUT/DELETE /api/products`.
10. `BUG_FR15_02` (High - Type Coercion): Ép kiểu `price` thành chuỗi `string` ở sản phẩm có ID chẵn.
11. `BUG_FR15_03` (Medium - Domain): Chấp nhận giá tiền âm (`-50000`) và giá bằng 0.
12. `BUG_FR15_04` (Medium - Schema): `GET /api/products/999999` trả về `200 OK` với `{}` thay vì `404 Not Found`.
13. `BUG_FR15_05` (High - SEC-06): SQL Injection trong Search Query làm lộ mã HTML 500 `<h1>Database Error</h1>`.
14. `BUG_FR09_01` (Critical - Math Inversion): Lỗi công thức tính phần trăm `1 - discount_value` làm tiền giảm ra số âm (-4.5tr).
15. `BUG_FR09_02` (High - C3 Boundary): Lỗi toán tử so sánh ngưỡng tối thiểu `>` thay vì `>=`.
16. `BUG_FR09_03` (Medium - Security): Thiếu xác thực token cho phép giả mạo `user_id` trong body để bypass hạn mức.
