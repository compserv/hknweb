from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.weighting import Weighting, Butler
from hknweb.tutoring.scheduler.matching import Matcher
from hknweb.tutoring.scheduler.evaluator import Evaluator
from hknweb.tutoring.scheduler.swapper import Swapper


def schedule(data: Data) -> None:
    weighting: Weighting = Butler()

    print("Matching...")
    score = float("-inf")
    while score < 0:
        # data.clear_assignments()  # TODO
        Matcher.match(data, weighting)
        std, score = Evaluator.evaluate(data, weighting)
        print(f"Score: {score}, Stddev: {std}")

    print("\nSwapping...")
    # Now do some random swapping to make it stable
    Swapper.stabilize(data, weighting)

    print("\nFinished!")
    print(data.readable_formatted_assignments())  # TODO
    std, score = Evaluator.evaluate(data, weighting)
    print(f"Score: {score}, Stddev: {std}")
