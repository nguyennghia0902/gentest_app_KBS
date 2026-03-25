"""Difficulty estimation based on item statistics."""
from typing import Tuple


def estimate_difficulty(correct_count: int, wrong_count: int, avg_time: float) -> float:
    """Estimate difficulty in [0, 1]. Higher means more difficult.

    Simple heuristic combining error rate and normalized time.
    """
    total = correct_count + wrong_count
    if total <= 0:
        return 0.5
    error_rate = wrong_count / total
    time_term = min(avg_time / 60.0, 1.0)
    d = 0.7 * error_rate + 0.3 * time_term
    return max(0.0, min(1.0, d))


def label_from_score(score: float) -> str:
    if score < 0.33:
        return 'easy'
    if score < 0.66:
        return 'medium'
    return 'hard'


def estimate_and_label(correct_count: int, wrong_count: int, avg_time: float) -> Tuple[float, str]:
    s = estimate_difficulty(correct_count, wrong_count, avg_time)
    return s, label_from_score(s)
