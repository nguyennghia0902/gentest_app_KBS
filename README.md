# 🎓 Hệ thống sinh đề & làm bài trắc nghiệm tự động

Ứng dụng web giúp **tự động sinh đề thi trắc nghiệm**, hỗ trợ sinh viên làm bài trực tuyến và **chấm điểm tức thì** dựa trên ngân hàng câu hỏi hai môn học: _Nhập môn Python_ và _Cấu trúc dữ liệu & Giải thuật_.

### Web demo:     [![](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bnn-genmctest-kbs.streamlit.app/)

---

## ✨ Tính năng nổi bật

- 📚 **Ngân hàng câu hỏi tiếng Việt** – 60+ câu, phân loại theo môn học, chủ đề, khái niệm và độ khó.
- 🎲 **Sinh đề linh hoạt** – chọn môn học, số câu, mức độ khó (dễ / trung bình / khó / xáo trộn).
- 🔀 **Xáo trộn phương án** – thứ tự A/B/C/D thay đổi mỗi lần sinh đề nhưng vẫn chấm đáp án chính xác.
- ⏱️ **Đồng hồ đếm thời gian** làm bài trực tiếp trên giao diện.
- ✅ **Chấm điểm tự động** – điểm thang 10, thống kê đúng/sai, hiển thị đáp án đúng cho từng câu.
- 🔒 **Bảo mật** – tắt copy nội dung đề thi ngay trên giao diện.

---

## 🗂️ Cấu trúc thư mục

```
.
├── app_streamlit.py      # Ứng dụng Streamlit chính
├── st_home.py            # Trang chủ giới thiệu 
├── st_gentest.py         # Trang sinh đề trắc nghiệm và làm bài
├── st_utilities.py       # Các hàm tiện ích cho ứng dụng
├── exam_generator.py     # Sinh đề theo môn & phân bố độ khó
├── question_bank.py      # Load & lọc ngân hàng câu hỏi
├── questions_vi.csv      # Ngân hàng câu hỏi tiếng Việt
├── requirements.txt      # Danh sách thư viện Python
└── README.md
```

---

## 🚀 Chạy ứng dụng trên máy

**1. Cài đặt thư viện**

```
$ pip install -r requirements.txt
```

**2. Chạy ứng dụng**

```
$ streamlit run app_streamlit.py
```

Trình duyệt sẽ tự mở tại `http://localhost:8501`.

---

## 🧪 Hướng dẫn sử dụng nhanh

1. Vào **sidebar**, chọn:
   - 📖 Môn học
   - ⚖️ Độ khó
   - 🔢 Số câu hỏi
   - 🤖 Nguồn câu hỏi _(Dataset hoặc LLM)_
2. Bấm **"Tạo đề và bắt đầu làm bài"**.
3. Trả lời các câu hỏi trắc nghiệm trong khung **ĐỀ THI**.
4. Bấm **"Nộp bài và chấm điểm"** để xem kết quả chi tiết.
5. Bấm **"Làm lại đề mới"** để thi lại với đề khác.

---

## 🔮 Hướng phát triển
- Tích hợp **LLM thật** (GPT/Gemini) để sinh câu hỏi mới theo ontology.
- Thêm **dashboard đánh giá năng lực** sinh viên theo chủ đề.
- Ghi log lịch sử làm bài, phân tích tiến bộ theo thời gian.
- Hỗ trợ mở rộng sang nhiều môn học khác.
