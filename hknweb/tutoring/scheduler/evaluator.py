from typing import List, Set, Tuple

from math import sqrt

from itertools import combinations

from hknweb.tutoring.scheduler.weighting import Weighting
from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.tutoring import Slot


class Evaluator:
    PENALTY: float = 10000000

    @staticmethod
    def evaluate(assignment: Data, weighting: Weighting) -> Tuple[float, float]:
        total_score: float = 0.0
        tutor_scores: List[float] = []

        has_correct_slots = lambda t: len(t.slots) == t.num_assignments
        for t in filter(has_correct_slots, assignment.tutors):
            if any(s1.simultaneous(s2) for s1, s2 in combinations(t.slots, 2)):
                total_score -= Evaluator.PENALTY
                continue

            # 0 means not available
            if any(t.slot_prefs[s.slot_id] == 0 for s in t.slots):
                total_score -= Evaluator.PENALTY
                continue

            # Simulate re-adding the slots in one by one
            # Order shouldn't matter when adding slots in
            d: float = 0.0
            old_slots: Set[Slot] = t.slots.copy()
            t.slots = set()
            for s in old_slots:
                d += weighting.weight(t, s)
                t.assign(s)

            d /= t.num_assignments
            tutor_scores.append(d)

        total_score += sum(tutor_scores)
        mean: float = total_score / len(tutor_scores)
        std: float = sum((s - mean) ** 2 for s in tutor_scores)
        return sqrt(std), total_score
