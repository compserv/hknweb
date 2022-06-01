from typing import Dict, Union

from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.weighting import Weighting, Butler, Gardener, OldGardener
from hknweb.tutoring.scheduler.matching import Matcher
from hknweb.tutoring.scheduler.evaluator import Evaluator
from hknweb.tutoring.scheduler.swapper import Swapper


WEIGHTINGS: Dict[str, Weighting] = {
    "butler": Butler,
    "gardener": Gardener,
    "old_gardener": OldGardener,
}

def schedule(
    data: Data,
    print_output: bool=True,
    weighting_str: str="gardener",
    iterations_mul: Union[int, None]=None,
) -> float:
    weighting: Weighting = WEIGHTINGS.get(weighting_str, Gardener)
    matcher: Matcher = Matcher(data, weighting)

    if print_output: print("Matching...")
    score = float("-inf")
    while score < 0:
        # data.clear_assignments()  # TODO
        matcher.match()
        _, score = Evaluator.evaluate(data, weighting)

    # Now do some random swapping to make it stable
    Swapper.stabilize(data, weighting, iterations_mul=iterations_mul, print_output=print_output)

    std, score = Evaluator.evaluate(data, weighting)
    if print_output:
        print(data.readable_formatted_assignments())
        print(f"Score: {score}, Stddev: {std}")

    return score
