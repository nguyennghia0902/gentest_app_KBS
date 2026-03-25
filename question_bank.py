"""Question bank loading and filtering."""
import csv
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Question:
    question_id: int
    subject: str
    topic: str
    concept: str
    text: str
    options: Dict[str, str]
    correct_option: str
    difficulty_label: str
    correct_count: int
    wrong_count: int
    avg_time: float


def load_questions(path: str) -> List[Question]:
    questions: List[Question] = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            options = {
                'option_a': row['option_a'],
                'option_b': row['option_b'],
                'option_c': row['option_c'],
                'option_d': row['option_d'],
            }
            q = Question(
                question_id=int(row['question_id']),
                subject=row['subject'],
                topic=row['topic'],
                concept=row['concept'],
                text=row['text'],
                options=options,
                correct_option=row['correct_option'],
                difficulty_label=row['difficulty_label'],
                correct_count=int(row['correct_count']),
                wrong_count=int(row['wrong_count']),
                avg_time=float(row['avg_time']),
            )
            questions.append(q)
    return questions


def filter_questions(
    questions: List[Question],
    subject: Optional[str] = None,
    topics: Optional[List[str]] = None,
    difficulty_labels: Optional[List[str]] = None,
) -> List[Question]:
    result: List[Question] = []
    for q in questions:
        if subject and q.subject != subject:
            continue
        if topics and q.topic not in topics:
            continue
        if difficulty_labels and q.difficulty_label not in difficulty_labels:
            continue
        result.append(q)
    return result
