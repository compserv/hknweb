from hknweb.tutoring.models import TutoringLogistics

from hknweb.tutoring.scheduler.data import Data
from hknweb.tutoring.scheduler.weighting import Weighting, Butler
from hknweb.tutoring.scheduler.matching import Matcher
from hknweb.tutoring.scheduler.evaluator import Evaluator
from hknweb.tutoring.scheduler.swapper import Swapper


class Scheduler:
    def __init__(self, logistics: TutoringLogistics) -> None:
        self.logistics = logistics

    def run(self):
        data: Data = Data(self.logistics)
        weighting: Weighting = Butler()

        print("Matching...")
        score = float("-inf")
        while score < 0:
            self.data.clear_assignments()  # TODO
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
