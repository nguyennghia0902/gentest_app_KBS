import time
import random
import streamlit as st

import question_bank
import exam_generator


def get_subjects(questions):
    return sorted({q.subject for q in questions})


def map_diff_to_ratios(diff_mode: str):
    if diff_mode == 'dễ':
        return 1.0, 0.0, 0.0
    if diff_mode == 'trung bình':
        return 0.0, 1.0, 0.0
    if diff_mode == 'khó':
        return 0.0, 0.0, 1.0
    # xáo trộn
    return 0.3, 0.5, 0.2


def generate_from_dataset(subject: str, num_questions: int, diff_mode: str):
    er, mr, hr = map_diff_to_ratios(diff_mode)
    exam = exam_generator.generate_exam(
        'questions_vi.csv',
        subject,
        num_questions,
        easy_ratio=er,
        medium_ratio=mr,
        hard_ratio=hr,
    )
    return exam


def generate_from_llm(subject: str, num_questions: int, diff_mode: str):
    # Placeholder: hiện tại dùng lại dataset
    return generate_from_dataset(subject, num_questions, diff_mode)


@st.cache_data(show_spinner=False)
def load_all_questions(path: str = 'questions_vi.csv'):
    return question_bank.load_questions(path)


def main():
    st.set_page_config(page_title='Hệ thống sinh đề tự động', layout='wide')

    st.title('Hệ thống sinh đề & làm bài trắc nghiệm')

    all_questions = load_all_questions()
    subjects = get_subjects(all_questions)

    if 'exam' not in st.session_state:
        st.session_state.exam = []
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'finished' not in st.session_state:
        st.session_state.finished = False

    with st.sidebar:
        st.header('Cấu hình đề thi')
        subject = st.selectbox('Môn học', subjects if subjects else ['(chưa có dữ liệu)'])
        diff_mode = st.selectbox('Độ khó', ['dễ', 'trung bình', 'khó', 'xáo trộn'], index=3)
        num_q = st.number_input('Số câu hỏi', min_value=1, max_value=50, value=10, step=1)
        source = st.radio('Nguồn câu hỏi', ['Dataset', 'LLM'], horizontal=True)

        if st.button('Tạo đề và bắt đầu làm bài', type='primary'):
            if not subjects:
                st.error('Chưa có ngân hàng câu hỏi.')
            else:
                try:
                    if source == 'Dataset':
                        exam = generate_from_dataset(subject, num_q, diff_mode)
                    else:
                        exam = generate_from_llm(subject, num_q, diff_mode)
                except Exception as e:
                    st.error(f'Lỗi sinh đề: {e}')
                else:
                    if not exam:
                        st.warning('Không tìm thấy câu hỏi phù hợp trong ngân hàng.')
                    else:
                        st.session_state.exam = exam
                        st.session_state.answers = {}
                        st.session_state.start_time = time.time()
                        st.session_state.finished = False
                        st.experimental_rerun()

        if st.session_state.start_time and not st.session_state.finished:
            elapsed = int(time.time() - st.session_state.start_time)
            m, s = divmod(elapsed, 60)
            st.info(f'Thời gian làm bài: {m:02d}:{s:02d}')

    exam = st.session_state.exam

    if not exam:
        st.warning('Hãy cấu hình và bấm "Tạo đề và bắt đầu làm bài" ở thanh bên.')
        return

    st.subheader('ĐỀ THI')

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

            st.write(prompt)
            if code:
                st.code(code, language='python')

            opt_items = list(q.options.items())
            random.shuffle(opt_items)

            labels = ['A', 'B', 'C', 'D']
            options_text = [f"{label}. {opt_text}" for (key, opt_text), label in zip(opt_items, labels)]

            correct_key = q.correct_option

            # Map each option text back to key
            option_key_map = {}
            for (key, opt_text), label in zip(opt_items, labels):
                label_text = f"{label}. {opt_text}"
                option_key_map[label_text] = key

            default = None
            if idx in st.session_state.answers:
                prev_key = st.session_state.answers[idx]
                for label_text, k in option_key_map.items():
                    if k == prev_key:
                        default = label_text
                        break

            choice = st.radio(
                'Chọn đáp án',
                options=options_text,
                index=options_text.index(default) if default in options_text else 0,
                key=f'q_{idx}',
            )

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
                st.experimental_rerun()
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
            st.session_state.exam = []
            st.session_state.answers = {}
            st.session_state.start_time = None
            st.session_state.finished = False
            st.experimental_rerun()


if __name__ == '__main__':
    main()
