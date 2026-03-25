"""CLI demo: simulate an adaptive test session."""
from typing import List
import random

from question_bank import load_questions, filter_questions, Question
from adaptive_engine import AdaptiveState, select_next_question, update_theta


def simulate_student_answer(q: Question, true_theta: float) -> bool:
    from adaptive_engine import question_effective_difficulty
    d = question_effective_difficulty(q)
    gap = d - true_theta
    base_prob = 1.0 / (1.0 + 2.0 ** gap)
    noise = random.uniform(-0.1, 0.1)
    p = max(0.05, min(0.95, base_prob + noise))
    return random.random() < p


def run_adaptive_session(csv_path: str, subject: str, true_theta: float, max_questions: int = 10):
    qs = load_questions(csv_path)
    pool = filter_questions(qs, subject=subject)
    state = AdaptiveState(theta=0.0)
    used: List[int] = []
    for step in range(max_questions):
        q = select_next_question(state, pool, used_ids=used)
        if not q:
            break
        used.append(q.question_id)
        correct = simulate_student_answer(q, true_theta)
        update_theta(state, q, correct)
        difficulty = 'easy'
        print(f"Step {step+1}: Q{q.question_id} | correct={correct} | theta={state.theta:.2f}")
    print(f"Final estimated theta: {state.theta:.2f} (true {true_theta:.2f})")


if __name__ == '__main__':
    run_adaptive_session('questions.csv', 'Data Structures & Algorithms', true_theta=0.5)
