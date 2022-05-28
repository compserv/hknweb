import random

from typing import List

from hknweb.tutoring.scheduler.weighting import Weighting
from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.tutoring import Slot, Tutor
from hknweb.tutoring.scheduler.evaluator import Evaluator


class Swapper:
    ITERATIONS_MULTIPLIER: int = 100  # Originally 100000
    THRESHOLD: float = 1e-10
    Q = 5
    K_high = 5
    K_low = 2

    @staticmethod
    def stabilize(data: Data, weighting: Weighting) -> None:
        iterations: int = len(data.tutors) * Swapper.ITERATIONS_MULTIPLIER
        curr_best: float = Evaluator.evaluate(data, weighting)[1]

        i, total = 0, Swapper.Q * (Swapper.K_high - Swapper.K_low + 1) * iterations
        for q in range(Swapper.Q):
            # Less movement the more iterations we go
            cthresh: float = Swapper.THRESHOLD / ((10 - q) ** 2)

            for k in range(Swapper.K_high, Swapper.K_low - 1, -1):
                # Do k-way swaps iter times
                for _ in range(iterations):
                    # Choose k distinct tutors with nonempty slots
                    nonempty_tutors: List[Tutor] = [t for t in data.tutors if t.slots]
                    to_swap: List[Tutor] = random.sample(nonempty_tutors, k)

                    # Choose a random slot within each tutor
                    slots = [random.choice(list(t.slots)) for t in to_swap]
                    slots_rotated_right = slots[1:] + slots[:1]

                    # Now do a circular swap
                    for swap in zip(to_swap, slots, slots_rotated_right):
                        Swapper._swap(*swap)

                    # Only move up if at least thresh improvement
                    cost: float = Evaluator.evaluate(data, weighting)[1]
                    if cost > (curr_best + cthresh):
                        print(f"Moved up by {cost - curr_best:.6f}")
                        curr_best = cost
                    else:   # Undo changes otherwise
                        for swap in zip(to_swap, slots_rotated_right, slots):
                            Swapper._swap(*swap)

                    i += 1
                    print(f"Swapping {i * 100 // total}%\r", end="", flush=True)
        print()

    @staticmethod
    def _swap(tutor: Tutor, slot1: Slot, slot2: Slot) -> None:
        """
        Swap tutor from slot1 to slot2
        """
        # Remove slot1 from tutor
        slot1.unassign(tutor)
        tutor.unassign(slot1)

        # Assign slot2 to tutor
        slot2.assign(tutor)
        tutor.assign(slot2)
