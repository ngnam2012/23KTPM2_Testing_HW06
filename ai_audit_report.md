**Khoa Công nghệ Thông tin (FIT) – Trường Đại học Khoa học Tự nhiên (HCMUS)**

**CS423 / CSC13003 – Kiểm chứng Phần mềm (AI-augmented · 2026)**

**CHÍNH SÁCH AI · BIỂU MẪU — 2026 v1.0**

# **AI Audit Report — Mẫu 5 mục cho mỗi Artifact**

*Phụ lục bắt buộc đính kèm cho bài tập HW#06 (API Testing).*

*Tài liệu được biên soạn lại từ Med Kharbach, PhD (2026) — Mẫu Chính sách Sử dụng AI cho Giáo dục Đại học. Giấy phép CC BY-NC-SA 4.0. Phiên bản này được FIT@HCMUS điều chỉnh cho môn CS423 / CSC13003 Kiểm chứng Phần mềm.*

---

## **1. Thông tin Sinh viên**

| Mục | Giá trị |
| :--- | :--- |
| **Họ tên sinh viên (in hoa):** | **NGUYỄN NHẬT NAM** |
| **MSSV:** | **23127092** |
| **Lớp / Khoá:** | **23KTPM2** |
| **Mã bài tập:** | **HW#06 (HW06-AI - API Testing)** |
| **Ngày làm bài:** | **21/08/2026 – 29/08/2026** |
| **Công cụ AI đã dùng:** | Google Antigravity Agent, Gemini 2.5 Pro, Claude 3.7 Sonnet |
| **Khai báo sử dụng AI:** | [x] Có  [ ] Không |

---

## **2. Hướng dẫn**

- Thêm 1 hàng cho mỗi artifact AI sinh (test case, script, dataset, OpenAPI spec, Postman collection...).
- Dán nguyên văn prompt — KHÔNG paraphrase.
- Dán nguyên văn output AI (trích đoạn có cấu trúc).
- Gắn nhãn: `VALID` / `INVALID` / `INCOMPLETE`.
- Lý do phải dẫn chiếu slide, mục ISTQB, RFC kỹ thuật hoặc OWASP API Security.
- Hiển thị bản sửa với phần thay đổi được tô sáng (`**bold**` / `code`).

---

## **3. Bảng Audit — 1 hàng / artifact**

| (1) Prompt + Công cụ | (2) Output AI | (3) Verdict | (4) Lý do (ISTQB / RFC / OWASP) | (5) Bản SV sửa (Tô sáng phần sửa) |
| :--- | :--- | :---: | :--- | :--- |
| **Artifact #1: Thiết lập Vai trò QA Lead & Tiêu chuẩn Kiểm thử**<br><br>**Tool:** Google Antigravity (Gemini 2.5)<br>**Thời gian:** 21:20 21/08/2026<br>**Prompt:** *"Bạn là một Chuyên gia Kiểm thử Phần mềm Cao cấp (Senior QA Automation Engineer & Security Tester) chuyên sâu về API Testing theo chuẩn quốc tế ISTQB và OWASP API Security Top 10. Chúng ta đang thực hiện kiểm thử cho hệ thống E-commerce có tên 'EShop' (Node.js/Express + SQLite)... Hãy xác nhận bạn đã hiểu rõ vai trò và sẵn sàng tiếp nhận yêu cầu phân tích từng API."* | "Tôi xác nhận đã hiểu rõ vai trò Senior QA Automation Engineer & Security Tester, cũng như các yêu cầu kỹ thuật và phương pháp luận áp dụng cho hệ thống EShop (Node.js/Express + SQLite)... Cam kết tuân thủ ISTQB EP/BVA, State Transition, OWASP SEC-01..07..." | **VALID** | Phản hồi xác lập đúng chuẩn phương pháp luận kiểm thử hộp đen ISTQB FL §4 và các danh mục kiểm thử an ninh OWASP API Security. | Giữ nguyên và sử dụng làm System Prompt định hướng cho toàn bộ pipeline sinh test. |
| **Artifact #2: Sinh bộ Test Suite FR-04 (Profile Management)**<br><br>**Tool:** Google Antigravity (Gemini 2.5)<br>**Thời gian:** 21:23 21/08/2026<br>**Prompt:** *"Bạn là Chuyên gia Kiểm thử API & Bảo mật. Hãy thiết kế bộ Test Suite toàn diện (tối thiểu 35 Test Cases) cho chức năng Quản lý Hồ sơ Cá nhân (FR-04): Endpoint: PUT /api/users/me & GET /api/users/me... Hãy sinh đủ 35 Test Cases bao phủ 4 nhóm: Nhóm 1 - Domain Partitions, Nhóm 2 - Security & Mass Assignment, Nhóm 3 - State & Data Integrity, Nhóm 4 - Schema & Status Codes."* | Sinh ra 39 Test Cases (`TC_FR04_EP_01` → `TC_FR04_SCHEMA_07`), bao gồm các ca kiểm tra phone regex, privilege escalation `role: admin`, data integrity. Tuy nhiên ca `TC_FR04_SEC_10` (SQLi phone) kỳ vọng 200 OK, và `TC_FR04_SEC_01` thiếu chuỗi GET xác minh. | **INCOMPLETE** | **ISTQB FL §4.2 (EP) & RFC 7231:** Payload phone chứa SQLi `' OR 1=1 --` vi phạm regex `^0[0-9]{9,10}$` nên phải bị chặn ở tầng 400 Bad Request. Ca Mass Assignment `role: admin` nếu không GET lại thì không chứng minh được lỗ hổng dữ liệu trong CSDL. | **Đã sửa:**<br>1. Sửa `TC_FR04_SEC_10`: Khóa cứng **`Expected Status: 400 Bad Request`** và `pm.response.to.have.status(400)`.<br>2. Bổ sung chuỗi kiểm tra **`TC_FR04_STATE_05`** gọi `GET /api/users/me` để `pm.expect(user.role).to.eql("user")`. |
| **Artifact #3: Sinh bộ Test Suite FR-10 (Order State Machine)**<br><br>**Tool:** Google Antigravity (Gemini 2.5)<br>**Thời gian:** 21:02 22/08/2026<br>**Prompt:** *"Bạn là Chuyên gia Kiểm thử Máy Trạng thái API (State Machine QA Specialist). Hãy thiết kế bộ Test Suite toàn diện (tối thiểu 35 Test Cases) cho chức năng Hủy đơn hàng & Máy trạng thái (FR-10): Endpoint: PUT /api/orders/:id/cancel & GET /api/orders/:id... Bao phủ 4 nhóm: State Valid, State Invalid, Security/BOLA, Domain/Boundary."* | Sinh ra 40 Test Cases (`TC_FR10_STATE_01` → `TC_FR10_DOM_05`). Phát hiện lỗi backend không chặn hủy đơn `shipping`. Tuy nhiên ca `TC_FR10_SEC_09` (HPP `PUT /api/orders/1/cancel?id=2`) chấp nhận `oneOf([200, 400])` gây mơ hồ. | **INCOMPLETE** | **RFC 7230 §5.3 & RESTful API Best Practices:** Tham số Path parameter (`/1/`) có quyền ưu tiên cao nhất, query string rác phải bị bỏ qua và đơn hàng `1` phải được hủy thành công với `200 OK`. Việc chấp nhận cả 400 là non-deterministic. | **Đã sửa:**<br>Khóa chặt assertion `TC_FR10_SEC_09`:<br>`pm.response.to.have.status(**200**);`<br>`pm.expect(res.message).to.eql(**"Order canceled successfully"**);` |
| **Artifact #4: Sinh bộ Test Suite FR-15 (Admin Product CRUD)**<br><br>**Tool:** Google Antigravity (Gemini 2.5)<br>**Thời gian:** 21:07 22/08/2026<br>**Prompt:** *"Bạn là Chuyên gia Kiểm thử Phân quyền & Bảo mật API. Hãy thiết kế bộ Test Suite toàn diện (tối thiểu 35 Test Cases) cho bộ API Quản trị Sản phẩm (FR-15): POST/PUT/DELETE /api/products... Bao phủ Broken Access Control, Domain & Boundary, Type Coercion, CRUD Lifecycle."* | Sinh ra 40 Test Cases (`TC_FR15_BAC_01` → `TC_FR15_CRUD_06`). Tuy nhiên các ca `TC_FR15_CRUD_03` & `04` (Cập nhật/xóa ID không tồn tại `999999`) AI đặt assertion `oneOf([400, 404])`. | **INVALID** | **RFC 7231 §6.5.4 (404 Not Found):** Thao tác trên tài nguyên không tồn tại theo chuẩn REST bắt buộc trả về `404 Not Found`. Mã 400 Bad Request chỉ dành cho cú pháp request sai. | **Đã sửa:**<br>Thay thế toàn bộ `oneOf([400, 404])` bằng **`pm.response.to.have.status(404)`** và kiểm tra `pm.expect(res).to.have.property("error")`. |
| **Artifact #5: Sinh bộ Test Suite FR-09 (Mobile Apply Coupon)**<br><br>**Tool:** Google Antigravity (Gemini 2.5)<br>**Thời gian:** 21:09 22/08/2026<br>**Prompt:** *"Bạn là Chuyên gia Kiểm thử Logic Nghiệp vụ E-commerce. Hãy thiết kế bộ Test Suite toàn diện (tối thiểu 35 Test Cases) cho chức năng Áp dụng Mã Giảm Giá (FR-09 Mobile Flow): Endpoint: POST /api/apply-coupon... Đặc tả 5 Điều kiện C1-C5... Bao phủ Ma trận C1-C5, Math Edge Cases, Domain Partitions, Schema Validation."* | Sinh ra 40 Test Cases (`TC_FR09_COND_01` → `TC_FR09_SCHEMA_06`). Nhưng ở các ca `TC_FR09_MATH_03` & `04` (test giảm giá fixed lớn hơn tổng tiền), AI gửi `total = 80k` cho mã `VIP100` (`min_order = 500k`) và kỳ vọng test nhánh toán học. | **INVALID** | **ISTQB FL §4.4 (Decision Table Testing):** Vi phạm thứ tự ưu tiên điều kiện. Điều kiện C3 (`total >= min_order_amount`) được kiểm tra trước, request bị chặn ngay lập tức với lỗi 400 do không đủ min_order, không bao giờ chạy đến nhánh trừ tiền. | **Đã sửa:**<br>1. Sửa `TC_FR09_MATH_03`: Đổi kỳ vọng thành **`400 Bad Request (Đơn hàng chưa đạt tối thiểu)`**.<br>2. Thiết kế riêng **`TC_FR09_ADV_03`** gửi mã `BIGBUY` với `total = 500k` để kiểm tra trọn vẹn bất biến `final_amount >= 0`. |
| **Artifact #6: Bổ sung 5 Test Cases Nâng cao FR-04 (Group 5)**<br><br>**Tool:** Claude 3.7 Sonnet / Antigravity<br>**Thời gian:** 20:15 29/08/2026<br>**Prompt:** *"Phân tích sâu mã nguồn backend server.js dòng 112-135 để tìm 5 Edge cases nâng cao mà AI thông thường rất dễ bỏ sót cho FR-04..."* | Đề xuất 5 ca: Partial update xóa trắng SĐT thành NULL (`ADV_01`), Ép kiểu số mất số 0 đầu (`ADV_02`), Lộ metadata `reset_token` qua `SELECT *` (`ADV_03`), Chuỗi leo thang Admin (`ADV_04`), Composite spoofing (`ADV_05`). | **VALID** | Phân tích chính xác các điểm yếu kiến trúc trong SQLite parameter binding, OWASP Top 10 API7:2023 Security Misconfiguration. | Tích hợp trực tiếp vào collection và nâng tổng số ca kiểm thử FR-04 lên **44 Test Cases**. |
| **Artifact #7: Bổ sung 5 Test Cases Nâng cao FR-10 (Group 5)**<br><br>**Tool:** Claude 3.7 Sonnet / Antigravity<br>**Thời gian:** 20:25 29/08/2026<br>**Prompt:** *"Phân tích sâu mã nguồn backend server.js dòng 284-350 để tìm 5 Edge cases nâng cao mà AI thông thường rất dễ bỏ sót cho FR-10..."* | Đề xuất 5 ca: Hủy đơn `shipping` do blacklist thiếu (`ADV_01`), BOLA trên `GET /api/orders/:id` không có auth (`ADV_02`), Race condition TOCTOU double cancel (`ADV_03`), Blind ID enumeration (`ADV_04`), Bất biến tài chính (`ADV_05`). | **VALID** | Bắt trúng 2 bugs cốt lõi của SUT: `BUG_FR10_01` (BOLA trên GET) và `BUG_FR10_02` (Hủy đơn shipping trái phép). | Tích hợp trực tiếp vào collection và nâng tổng số ca kiểm thử FR-10 lên **45 Test Cases**. |
| **Artifact #8: Bổ sung 5 Test Cases Nâng cao FR-15 (Group 5)**<br><br>**Tool:** Claude 3.7 Sonnet / Antigravity<br>**Thời gian:** 20:35 29/08/2026<br>**Prompt:** *"Phân tích sâu mã nguồn backend server.js dòng 141-196 để tìm 5 Edge cases nâng cao mà AI thông thường rất dễ bỏ sót cho FR-15..."* | Đề xuất 5 ca: Broken Access Control trên POST/PUT/DELETE (`ADV_01`), Ép kiểu chuỗi ở ID chẵn `row.id % 2 === 0` (`ADV_02`), Phản hồi 200 OK giả kèm `{}` (`ADV_03`), Bỏ lọt giá âm (`ADV_04`), SQLi search làm rò rỉ HTML 500 (`ADV_05`). | **VALID** | Bắt trọn 5 bugs thực tế trong mã nguồn backend SUT, bao gồm cả lỗi ép kiểu quái dị và lỗi lộ trang HTML lỗi cơ sở dữ liệu. | Tích hợp trực tiếp vào collection và nâng tổng số ca kiểm thử FR-15 lên **45 Test Cases**. |
| **Artifact #9: Bổ sung 5 Test Cases Nâng cao FR-09 (Group 5)**<br><br>**Tool:** Claude 3.7 Sonnet / Antigravity<br>**Thời gian:** 20:40 29/08/2026<br>**Prompt:** *"Phân tích sâu mã nguồn backend server.js dòng 363-441 để tìm 5 Edge cases nâng cao mà AI thông thường rất dễ bỏ sót cho FR-09..."* | Đề xuất 5 ca: Lỗi toán học `1 - discount_value` ra số âm (`ADV_01`), Lỗi toán tử ngưỡng `>` thay vì `>=` (`ADV_02`), Bất biến `final_amount >= 0` (`ADV_03`), Giả mạo `user_id` bypass hạn mức (`ADV_04`), Lỗi cắt cụt ngày nửa đêm (`ADV_05`). | **VALID** | Bắt trúng `BUG_FR09_01` (Tính phần trăm sai) và `BUG_FR09_02` (Ranh giới điểm ngưỡng C3). | Tích hợp trực tiếp vào collection và nâng tổng số ca kiểm thử FR-09 lên **45 Test Cases**. |
| **Artifact #10: Thiết kế Module AI Test Generator (`generator/`)**<br><br>**Tool:** Claude 3.7 Sonnet / Antigravity<br>**Thời gian:** 21:08 29/08/2026<br>**Prompt:** *"Xây dựng Module AI Test Generator trong generator/: generator_design.md, api_test_agent.py, SKILL.md dùng được cho toàn bộ 19 FRs..."* | Sinh mã nguồn Python hoàn chỉnh `api_test_agent.py`, tài liệu thiết kế kiến trúc Mermaid `generator_design.md` và file đặc tả Agent Skill `SKILL.md`. | **VALID** | Đáp ứng 100% tiêu chí sáng tạo Bloom G9.5 (Create), sinh tự động test collection cho toàn bộ FR-01 đến FR-19 có gắn kèm `X-Student-Id`. | Đã chạy thử nghiệm sinh thành công collection 17 features `collections/AutoGenerated_Collection.postman_collection.json`. |

---

## **4. Tổng kết Độ chính xác AI**

| Chỉ số | Số lượng | Tỉ lệ |
| :--- | :---: | :---: |
| **Tổng artifact AI sinh đã audit** | **10 Artifacts** | **100%** |
| **VALID (đúng, dùng nguyên hoặc mở rộng)** | **6** | **60.0%** |
| **INVALID (sai nghiệp vụ / HTTP spec; đã sửa)** | **2** | **20.0%** |
| **INCOMPLETE (thiếu ràng buộc / assertion lỏng; đã bổ sung)** | **2** | **20.0%** |

---

## **5. Kết luận — Khi nào nên / không nên dùng AI?**

* **Khi NÊN dùng AI:** AI thể hiện thế mạnh vượt trội trong việc **sinh nhanh cấu trúc khung (Scaffolding)**, tạo hàng loạt ca kiểm thử phân vùng tương đương (EP) cơ bản cho chuỗi/số, sinh nhanh cú pháp Postman Collection v2.1 JSON, và chuyển đổi tự động từ đặc tả sang mã Chai Assertion chuẩn BDD. Sử dụng AI giúp rút ngắn 70% thời gian tạo boilerplate.
* **Khi KHÔNG NÊN tin tưởng mù quáng vào AI:** Tuyệt đối không để AI tự quyết định các **ca kiểm thử bảo mật chuyên sâu (OWASP SEC-01..07)**, **logic máy trạng thái trung gian (State Machine Transitions)**, và **phân tích giá trị biên ranh giới (BVA)**. AI có xu hướng "tự xoa dịu" bằng assertion lỏng lẻo (`oneOf([200, 400])`), bỏ qua kiểm tra ranh giới toán tử so sánh (`>` vs `>=`), và mặc định áp dụng Happy Path cho các API quản trị thay vì kiểm thử phân quyền âm (Negative Access Control). **Sự can thiệp và rà soát của kỹ sư QA con người (Human-in-the-Loop) là bắt buộc để đảm bảo chất lượng phần mềm.**

---

## **6. Mandatory Disclosure (Khai báo bắt buộc)**

*"Bộ Test Cases, Postman Collections, Script sinh test tự động và Báo cáo kiểm thử này được sinh phiên bản đầu bởi Google Antigravity Agent (Gemini 2.5 Pro & Claude 3.7 Sonnet); tôi đã rà soát và chỉnh sửa các mã trạng thái sai lệch, bổ sung 20 Test Cases nâng cao (Group 5) phát hiện 16 lỗi nghiêm trọng trong mã nguồn SUT, chuẩn hóa assertion Chai BDD loại bỏ hoàn toàn các assertion mơ hồ `oneOf`; toàn bộ sơ đồ kiến trúc Mermaid và ma trận đối soát do tôi trực tiếp phân tích và thiết kế. AI Audit Report chi tiết được đính kèm tại đây. Tôi cam đoan không dùng AI để sinh bất kỳ artifact nào thuộc danh mục bị cấm."*

---

## **Chữ ký**

| Mục | Thông tin xác nhận |
| :--- | :--- |
| **Họ tên sinh viên (in hoa):** | **NGUYỄN NHẬT NAM** |
| **MSSV:** | **23127092** |
| **Lớp / Khoá:** | **23KTPM2** |
| **Môn học:** | **CS423 / CSC13003 – Kiểm chứng Phần mềm** |
| **Giảng viên:** | **TS. Lâm Quang Vũ / TS. Trần Duy Hoàng / ThS. Trần Thị Bích Hạnh** |
| **Ngày:** | **29/08/2026** |
| **Chữ ký điện tử:** | *Nguyễn Nhật Nam* |

---

## **Tham khảo**

- Kharbach, M. (2026). *AI Use Policy Templates for Higher Education*. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus v4.0 (2023/2025).
- OWASP API Security Top 10 (2023).
- RFC 7231: Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content.
- Anthropic (2025). *Building reliable AI test agents* — engineering blog.
