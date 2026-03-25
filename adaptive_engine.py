"""Simple adaptive testing engine."""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import math

from question_bank import Question
from difficulty_model import estimate_difficulty


@dataclass
class AdaptiveState:
    theta: float = 0.0
    responses: Dict[int, bool] = field(default_factory=dict)


def question_effective_difficulty(q: Question) -> float:
    d = estimate_difficulty(q.correct_count, q.wrong_count, q.avg_time)
    return 6.0 * d - 3.0


def update_theta(state: AdaptiveState, q: Question, is_correct: bool, step: float = 0.3) -> None:
    d = question_effective_difficulty(q)
    diff_gap = d - state.theta
    direction = 1.0 if not is_correct else -1.0
    state.theta += direction * step * (1.0 + 0.2 * abs(diff_gap))


def select_next_question(
    state: AdaptiveState,
    pool: List[Question],
    used_ids: Optional[List[int]] = None,
) -> Optional[Question]:
    used_set = set(used_ids or [])
    candidates = [q for q in pool if q.question_id not in used_set]
    if not candidates:
        return None
    best_q = None
    best_gap = None
    for q in candidates:
        d = question_effective_difficulty(q)
        gap = abs(d - state.theta)
        if best_gap is None or gap < best_gap:
            best_gap = gap
            best_q = q
    return best_q
