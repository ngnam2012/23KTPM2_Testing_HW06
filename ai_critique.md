# BÀI PHẢN BIỆN NĂNG LỰC & HẠN CHẾ CỦA AI TRONG KIỂM THỬ API (AI CRITIQUE)

> **Mã bài tập:** HW06-AI | **Môn học:** Software Testing (CS423 / CSC13003)  
> **Sinh viên:** Nguyễn Nhật Nam | **MSSV:** `23127092` | **Lớp:** `23KTPM2`

---

### Phản Biện Học Thuật Về Vai Trò và Giới Hạn Của AI Trong Kiểm Thử Tự Động Hóa API

Trong quá trình thực hiện kiểm thử trên hệ thống EShop SUT, mô hình ngôn ngữ lớn (LLM) đã bộc lộ rõ cả ưu thế lẫn những điểm mù nguy hiểm. Về mặt **sai sót và thiên kiến (Bias & Incompleteness)**, AI có xu hướng tạo ra các kịch bản kiểm thử "tự xoa dịu" bằng các assertion mơ hồ `oneOf([200, 400])`, bỏ qua kiểm thử phân quyền âm (Negative Access Control) trên các route Admin, và không nhận diện được lỗi máy trạng thái ở các bước chuyển trung gian (`shipping` ➔ `canceled`).

**Nguyên nhân gốc rễ** khiến AI thất bại nằm ở bản chất dự đoán xác suất token: AI nhìn nhận API như một chiếc hộp đen thuần túy dựa trên các mẫu văn bản phổ biến, thiếu khả năng phân tích luồng dữ liệu tĩnh trong mã nguồn Node.js/SQLite, và thiếu tư duy đa chiều về chuỗi tấn công leo thang đặc quyền. Chẳng hạn, AI không thể tự suy luận rằng câu lệnh `SELECT *` sẽ phơi bày `reset_token`, hay phép trừ `1 - discount_value` sẽ gây lỗi tràn số âm tiền giảm giá.

**Bài học cốt lõi rút ra:** AI là một trợ thủ đắc lực giúp tăng tốc 70% công việc soạn thảo boilerplate, nhưng **tuyệt đối không thể thay thế kỹ sư QA con người (Human-in-the-Loop)**. Để đảm bảo chất lượng, con người bắt buộc phải giữ vai trò nhạc trưởng: trực tiếp rà soát mã nguồn, thực thi phân tích giá trị biên (BVA) nghiêm ngặt, và áp đặt các bất biến nghiệp vụ tất định mà không trao quyền phán quyết cuối cùng cho AI.
