import json
import streamlit as st
from huggingface_hub import InferenceClient

# (Tùy chọn) Khởi tạo một class đơn giản để chứa dữ liệu câu hỏi từ LLM
# Nó sẽ có cấu trúc giống với object lấy từ file question_bank
class LLMQuestion:
    def __init__(self, text, options, correct_option):
        self.text = text
        self.options = options
        self.correct_option = correct_option

def generate_from_llm(subject: str, num_questions: int, diff_mode: str):
    """
    Sử dụng Hugging Face Inference API để sinh câu hỏi.
    """
    # 1. Lấy token từ Streamlit Secrets
    try:
        hf_token = st.secrets["HF_TOKEN"]
    except FileNotFoundError:
        raise Exception("Chưa cấu hình HF_TOKEN trong cài đặt Secrets của Streamlit.")

    # 2. Khởi tạo Client. Sử dụng Qwen-2.5-72B (Mô hình rất thông minh của Qwen)
    repo_id = "Qwen/Qwen2.5-72B-Instruct"
    client = InferenceClient(model=repo_id, token=hf_token)

    # 3. Ép LLM trả về cấu trúc JSON nghiêm ngặt
    prompt = f"""
Bạn là một chuyên gia về Lập trình Python và Cấu trúc dữ liệu & Giải thuật.
Hãy tạo một bộ gồm đúng {num_questions} câu hỏi trắc nghiệm về chủ đề: "{subject}".
Độ khó yêu cầu: {diff_mode}.

QUAN TRỌNG: Chỉ trả về MỘT mảng JSON hợp lệ, KHÔNG kèm văn bản giải thích.
Cấu trúc JSON bắt buộc:
[
  {{
    "text": "Nội dung câu hỏi... (nếu có code hãy dùng dấu \\n để xuống dòng, ví dụ: Cho đoạn mã:\\nprint('Hello'))",
    "options": {{
      "A": "Lựa chọn 1",
      "B": "Lựa chọn 2",
      "C": "Lựa chọn 3",
      "D": "Lựa chọn 4"
    }},
    "correct_option": "A" 
  }}
]
"""
    messages = [{"role": "user", "content": prompt}]

    # 4. Gọi API
    response = client.chat_completion(
        messages, 
        max_tokens=2500, 
        temperature=0.7
    )
    raw_content = response.choices[0].message.content

    # 5. Làm sạch kết quả (Lọc bỏ các thẻ markdown ```json...``` nếu AI sinh ra dư thừa)
    clean_content = raw_content.strip()
    if clean_content.startswith("```json"):
        clean_content = clean_content.replace("```json", "", 1)
    if clean_content.endswith("```"):
        clean_content = clean_content[::-1].replace("```", "", 1)[::-1]
    clean_content = clean_content.strip()

    # 6. Parse JSON và đưa vào danh sách object
    try:
        data = json.loads(clean_content)
        exam = []
        for item in data:
            q = LLMQuestion(
                text=item.get("text", ""),
                options=item.get("options", {}),
                correct_option=item.get("correct_option", "A")
            )
            exam.append(q)
        return exam
    except json.JSONDecodeError:
        raise Exception("LLM trả về định dạng không chuẩn, vui lòng thử tạo lại đề!")