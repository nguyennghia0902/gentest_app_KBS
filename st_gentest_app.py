import time
import streamlit as st
from st_utilities import *
import uuid

st.set_page_config(page_title='Hệ thống sinh đề tự động', page_icon="📝", layout='wide')

def main():
    st.set_page_config(page_title='Hệ thống sinh đề tự động', layout='wide')

    st.title('HỆ THỐNG SINH ĐỀ VÀ LÀM BÀI TRẮC NGHIỆM')

    all_questions = load_all_questions()
    subjects = get_subjects(all_questions)

    if 'exam_id' not in st.session_state:
        st.session_state.exam_id = str(uuid.uuid4())
    if 'exam' not in st.session_state:
        st.session_state.exam = []

    init_session_state()

    with st.sidebar:
        st.header('Cấu hình đề thi')

        exam_in_progress = bool(st.session_state.get('exam')) and not st.session_state.get('finished')

        subject = st.selectbox('Môn học', subjects if subjects else ['(chưa có dữ liệu)'], disabled=exam_in_progress)
        diff_mode = st.selectbox('Độ khó', ['dễ', 'trung bình', 'khó', 'xáo trộn'], index=3, disabled=exam_in_progress)
        num_q = st.number_input('Số câu hỏi', min_value=1, max_value=50, value=10, step=1, disabled=exam_in_progress)
        source = st.radio('Nguồn câu hỏi', ['Dataset', 'LLM'], horizontal=True, disabled=exam_in_progress)

        if st.button('Tạo đề và bắt đầu làm bài', type='primary', disabled=exam_in_progress):
            if not subjects:
                st.error('Chưa có ngân hàng câu hỏi.')
            else:
                old_exam = st.session_state.get('exam', [])
                for i in range(1, len(old_exam) + 1):
                    widget_key = f'q_{i}'
                    if widget_key in st.session_state:
                        del st.session_state[widget_key]
                with st.spinner('Đang soạn đề thi, vui lòng đợi trong giây lát...'):
                    try:
                        if source == 'Dataset':
                            exam = generate_from_dataset(subject, num_q, diff_mode)
                        else:
                            exam = generate_from_llm(subject, num_q, diff_mode)
                    except Exception as e:
                        st.error(f'Lỗi sinh đề: {e}')
                    else:
                        if not exam:
                            st.warning('Không tìm thấy câu hỏi phù hợp.')
                        else:
                            st.session_state.exam = exam
                            st.session_state.answers = {}
                            st.session_state.start_time = time.time()
                            st.session_state.finished = False
                            st.session_state.exam_id = str(uuid.uuid4())
                            st.rerun()

        if st.session_state.start_time and not st.session_state.finished:
            elapsed = int(time.time() - st.session_state.start_time)
            m, s = divmod(elapsed, 60)
            show_timer()

    exam = st.session_state.exam

    if not exam:
        st.warning('Hãy cấu hình và bấm "Tạo đề và bắt đầu làm bài" ở thanh bên.')
        return

    st.subheader('Trắc nghiệm: Hãy chọn phương án đúng nhất trong các phương án A, B, C và D.')

    for idx, q in enumerate(exam, start=1):
        with st.container(border=True):
            st.markdown(f'**Câu {idx}.**')

            text = q.text or ''
            text = text.replace('\\n', '\n')

            if '\n' in text:
                parts = text.split('\n')
                prompt = parts[0]
                code = '\n'.join(parts[1:]).strip()
            else:
                prompt = text
                code = ''


            #st.markdown(f"<div class='question-text'>{prompt}</div>", unsafe_allow_html=True)
            st.write(prompt)
            if code:
                st.code(code, language='python')

            opt_items = st.session_state.option_orders.get(idx)
            if not opt_items:
                opt_items = list(q.options.items())
                st.session_state.option_orders[idx] = opt_items

            labels = ['A', 'B', 'C', 'D']
            option_key_map = {}
            options_text = []
            for (key, opt_text), label in zip(opt_items, labels):
                label_text = f"{label}. {opt_text}"
                options_text.append(label_text)
                option_key_map[label_text] = key

            correct_key = q.correct_option

            display_options = options_text

            # Nếu đã có đáp án trong session_state thì chọn lại đúng phương án đó
            prev_key = st.session_state.answers.get(idx)
            prev_label = None
            if prev_key is not None:
                for label_text, k in option_key_map.items():
                    if k == prev_key:
                        prev_label = label_text
                        break

            if prev_label and prev_label in display_options:
                default_index = display_options.index(prev_label)
            else:
                # Mặc định là "(Chưa chọn)"
                default_index = 0

            choice = st.radio(
                'Chọn đáp án',
                options=display_options,
                index=None,
                key=f"q_{st.session_state.exam_id}_{idx}",
            )

            if choice == None:
                # Chưa chọn gì hoặc bỏ chọn
                if idx in st.session_state.answers:
                    del st.session_state.answers[idx]
                chosen_key = None
            else:
                chosen_key = option_key_map[choice]
                st.session_state.answers[idx] = chosen_key

            if st.session_state.finished:
                is_correct = chosen_key == correct_key
                correct_label = None
                for label_text, k in option_key_map.items():
                    if k == correct_key:
                        correct_label = label_text
                        break
                if is_correct:
                    st.success(f'Kết quả: Đúng. Đáp án đúng: {correct_label}')
                else:
                    st.error(f'Kết quả: Sai. Đáp án đúng: {correct_label}')

    if not st.session_state.finished:
        if st.button('Nộp bài và chấm điểm', type='primary'):
            # kiểm tra đã trả lời hết
            if len(st.session_state.answers) < len(exam):
                st.warning('Vui lòng trả lời tất cả các câu hỏi trước khi nộp.')
            else:
                st.session_state.finished = True
                st.rerun()
    else:
        total = len(exam)
        correct = 0
        for idx, q in enumerate(exam, start=1):
            if st.session_state.answers.get(idx) == q.correct_option:
                correct += 1
        if st.session_state.start_time:
            elapsed = int(time.time() - st.session_state.start_time)
        else:
            elapsed = 0
        m, s = divmod(elapsed, 60)
        score_10 = 10 * correct / total if total > 0 else 0.0
        st.success(f'Điểm: {score_10:.2f}/10 | Đúng {correct}/{total} câu | Thời gian: {m:02d}:{s:02d}')
        if st.button('Làm lại đề mới'):
            old_exam = st.session_state.get('exam', [])
            for i in range(1, len(old_exam) + 1):
                widget_key = f'q_{i}'
                if widget_key in st.session_state:
                    del st.session_state[widget_key]
            st.session_state.exam = []
            st.session_state.answers = {}
            st.session_state.start_time = None
            st.session_state.finished = False
            st.session_state.exam_id = str(uuid.uuid4())
            st.rerun()

if __name__ == '__main__':
    main()