from typing import List

from hknweb.tutoring.scheduler.tutoring import Slot, Tutor


class Data:
    def __init__(self):
        self.slots: List[Slot] = []
        self.tutors: List[Tutor] = []
