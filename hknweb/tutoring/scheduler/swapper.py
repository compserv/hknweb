import random

from typing import List, Union

from itertools import product

from hknweb.tutoring.scheduler.weighting import Weighting
from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.tutoring import Slot, Tutor
from hknweb.tutoring.scheduler.evaluator import Evaluator


class Swapper:
    ITERATIONS_MULTIPLIER: int = 10000  # Originally 100000 * 5 (for removed Q value)
    Ks = list(range(5, 2-1, -1))

    @staticmethod
    def stabilize(
        data: Data,
        weighting: Weighting,
        iterations_mul: Union[int, None]=None,
        print_output: bool=True,
    ) -> None:
        iterations_mul: int = iterations_mul if iterations_mul else Swapper.ITERATIONS_MULTIPLIER
        iterations: int = len(data.tutors) * iterations_mul
        curr_best: float = Evaluator.evaluate(data, weighting)[1]

        nonempty_tutors: List[Tutor] = [t for t in data.tutors if t.slots]

        total = len(Swapper.Ks) * iterations
        # Do k-way swaps iter times
        for i, (k, _) in enumerate(product(Swapper.Ks, range(iterations))):
            # Choose k distinct tutors with nonempty slots
            to_swap: List[Tutor] = random.sample(nonempty_tutors, k)

            # Choose a random slot within each tutor
            slots = [random.choice(list(t.slots)) for t in to_swap]
            slots_rotated_right = slots[1:] + slots[:1]

            Swapper._circular_swap(to_swap, slots, slots_rotated_right)

            cost: float = Evaluator.evaluate(data, weighting)[1]
            if cost > curr_best:
                curr_best = cost
            else:  # Undo changes otherwise
                Swapper._circular_swap(to_swap, slots_rotated_right, slots)

            pct = (i + 1) * 100
            if print_output and pct % total == 0:  # Print every 1%
                print(f"Swapping {pct // total}%\r", end="", flush=True)
        if print_output: print()

    @staticmethod
    def _circular_swap(tutors: List[Tutor], slots_from: List[Slot], slots_to: List[Slot]) -> None:
        for tutor, slot_from, slot_to in zip(tutors, slots_from, slots_to):
            # Remove slot_from from tutor
            slot_from.unassign(tutor)
            tutor.unassign(slot_from)

            # Assign slot_to to tutor
            slot_to.assign(tutor)
            tutor.assign(slot_to)
