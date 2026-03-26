import streamlit as st
import time
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

def unique_questions_by_content(questions):
    seen = set()
    unique = []

    for q in questions:
        signature = (
            q.subject.strip(),
            q.topic.strip(),
            q.text.strip(),
            q.options['option_a'].strip(),
            q.options['option_b'].strip(),
            q.options['option_c'].strip(),
            q.options['option_d'].strip(),
        )
        if signature in seen:
            continue
        seen.add(signature)
        unique.append(q)

    return unique


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

@st.fragment(run_every=1)
def show_timer():
    if st.session_state.start_time and not st.session_state.finished:
        elapsed = int(time.time() - st.session_state.start_time)
        m, s = divmod(elapsed, 60)
        st.info(f'⏱ Thời gian làm bài: {m:02d}:{s:02d}')


def init_session_state():
    if 'exam' not in st.session_state:
        st.session_state.exam = []
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'finished' not in st.session_state:
        st.session_state.finished = False
    # Lưu thứ tự phương án cho từng câu để không bị nhảy lung tung mỗi lần rerun
    if 'option_orders' not in st.session_state:
        st.session_state.option_orders = {}