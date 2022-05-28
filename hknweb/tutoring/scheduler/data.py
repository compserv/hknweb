from typing import List

from hknweb.tutoring.models import TutoringLogistics

from hknweb.tutoring.scheduler.tutoring import Slot, Tutor


class Data:
    def __init__(self, logistics: TutoringLogistics) -> None:
        self.slots: List[Slot] = []
        self.tutors: List[Tutor] = []
