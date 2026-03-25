"""CLI demo: generate a static exam by subject and difficulty mix."""
from typing import List, Dict
import random

from question_bank import load_questions, filter_questions, Question


def sample_by_difficulty(
    questions: List[Question],
    target_counts: Dict[str, int],
) -> List[Question]:
    selected: List[Question] = []
    for diff, count in target_counts.items():
        pool = [q for q in questions if q.difficulty_label == diff]
        if not pool:
            continue
        if len(pool) <= count:
            selected.extend(pool)
        else:
            selected.extend(random.sample(pool, count))
    seen = set()
    unique: List[Question] = []
    for q in selected:
        if q.question_id in seen:
            continue
        seen.add(q.question_id)
        unique.append(q)
    return unique

def deduplicate_by_question_id(questions):
    seen = set()
    unique = []
    for q in questions:
        if q.question_id not in seen:
            seen.add(q.question_id)
            unique.append(q)
    return unique


def generate_exam(
    csv_path: str,
    subject: str,
    total_questions: int,
    easy_ratio: float = 0.3,
    medium_ratio: float = 0.5,
    hard_ratio: float = 0.2,
):
    questions = load_questions(csv_path)
    subject_qs = filter_questions(questions, subject=subject)
    
    if not subject_qs:
        raise ValueError(f"No questions for subject {subject}")

    easy_n = int(total_questions * easy_ratio)
    med_n = int(total_questions * medium_ratio)
    hard_n = total_questions - easy_n - med_n
    targets = {'easy': easy_n, 'medium': med_n, 'hard': hard_n}

    picked = sample_by_difficulty(subject_qs, targets)

    if len(picked) < total_questions:
        remaining = [q for q in subject_qs if q not in picked]
        extra = random.sample(remaining, min(len(remaining), total_questions - len(picked)))
        picked.extend(extra)

    # Khử trùng theo question_id
    picked = deduplicate_by_question_id(picked)

    # Nếu sau khi khử trùng mà vẫn thiếu câu thì bổ sung tiếp
    if len(picked) < total_questions:
        used_ids = {q.question_id for q in picked}
        extra_pool = [q for q in subject_qs if q.question_id not in used_ids]
        extra_needed = total_questions - len(picked)
        picked.extend(random.sample(extra_pool, min(len(extra_pool), extra_needed)))

    return picked[:total_questions]



def print_exam(questions: List[Question]):
    for idx, q in enumerate(questions, start=1):
        print(f"Q{idx}. {q.text}")
        print(f"  A. {q.options['option_a']}")
        print(f"  B. {q.options['option_b']}")
        print(f"  C. {q.options['option_c']}")
        print(f"  D. {q.options['option_d']}")
        print()


if __name__ == '__main__':
    exam = generate_exam('questions.csv', 'Intro Python', 10)
    print_exam(exam)
