from typing import Dict

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

def schedule(data: Data, output_readable=True, weighting_str: str="gardener") -> float:
    weighting: Weighting = WEIGHTINGS.get(weighting_str, Gardener)
    matcher: Matcher = Matcher(data, weighting)

    print("Matching...")
    score = float("-inf")
    while score < 0:
        # data.clear_assignments()  # TODO
        matcher.match()
        std, score = Evaluator.evaluate(data, weighting)
        print(f"Initial score: {score}, Stddev: {std}")

    # Now do some random swapping to make it stable
    Swapper.stabilize(data, weighting)

    if output_readable:
        print(data.readable_formatted_assignments())
    std, score = Evaluator.evaluate(data, weighting)
    print(f"Score: {score}, Stddev: {std}")

    return score
