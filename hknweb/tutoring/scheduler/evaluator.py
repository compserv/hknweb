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
        score: float = 0.0
        scores: List[float] = []

        for t in assignment.tutors:
            if len(t.slots) != t.num_assignments:
                continue

            if any(s1.simultaneous(s2) for s1, s2 in combinations(t.slots, 2)):
                score -= Evaluator.PENALTY
                continue

            # Reset slots
            old_slots: Set[Slot] = t.slots.copy()
            t.slots = set()

            # 0 means not available
            if any(t.slot_prefs[s.slot_id] == 0 for s in old_slots):
                score -= Evaluator.PENALTY
                continue

            # Simulate re-adding the slots in one by one
            # Order shouldn't matter when adding slots in
            d: float = 0.0
            for s in old_slots:
                d += weighting.weight(t, s)
                t.assign(s)

            d /= t.num_assignments
            scores.append(d)
            score += d

        mean: float = score / len(scores)
        std: float = sum((score - mean) ** 2 for score in scores)
        return sqrt(std), score
