from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.weighting import Weighting, Butler
from hknweb.tutoring.scheduler.matching import Matcher
from hknweb.tutoring.scheduler.evaluator import Evaluator
from hknweb.tutoring.scheduler.swapper import Swapper


def schedule(data: Data, output_readable=True) -> float:
    weighting: Weighting = Butler()
    matcher: Matcher = Matcher(data, weighting)

    print("Matching...")
    score = float("-inf")
    while score < 0:
        # data.clear_assignments()  # TODO
        matcher.match()
        std, score = Evaluator.evaluate(data, weighting)
        print(f"Score: {score}, Stddev: {std}")

    print("\nSwapping...")
    # Now do some random swapping to make it stable
    Swapper.stabilize(data, weighting)

    print("\nFinished!")
    if output_readable:
        print(data.readable_formatted_assignments())
    std, score = Evaluator.evaluate(data, weighting)
    print(f"Score: {score}, Stddev: {std}")

    return score
