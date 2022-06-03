from typing import List


class Slot:
    def __init__(self, slot_id: int, day: str, hour: int, office: str):
        self.slot_id = slot_id
        self.day = day
        self.hour = hour
        self.office = office

        self.tutors: "List[Tutor]" = []

    def assign(self, t: "Tutor") -> None:
        self.tutors.append(t)

    def unassign(self, t: "Tutor") -> None:
        self.tutors.remove(t)

    def simultaneous(self, other: "Slot") -> bool:
        return (self.hour == other.hour) and (self.day == other.day)

    def adjacent(self, other: "Slot") -> bool:
        return (
            (self.office == other.office)
            and (self.day == other.day)
            and (abs(self.hour - other.hour) == 1)
        )

    def __repr__(self):  # pragma: no cover
        return f"Slot({self.slot_id} on {self.day} at {self.hour} in {self.office})"


class Tutor:
    def __init__(
        self,
        tutor_id: int,
        slot_prefs: List[int],
        office_prefs: List[int],
        adjacent_pref: int,
        num_assignments: int,
    ):
        self.tutor_id = tutor_id

        self.slot_prefs = slot_prefs
        self.office_prefs = office_prefs
        self.adjacent_pref = adjacent_pref
        self.num_assignments = num_assignments

        self.slots: "List[Slot]" = []

    def conflict(self, s1: "Slot") -> bool:
        return any(map(lambda s2: s1.simultaneous(s2), self.slots))

    def assign(self, s: "Slot") -> None:
        self.slots.append(s)

    def unassign(self, s: "Slot") -> None:
        self.slots.remove(s)

    def clear_slots(self) -> "List[Slot]":
        res = self.slots.copy()
        self.slots = []

        return res

    def __repr__(self) -> str:  # pragma: no cover
        return f"Tutor({self.tutor_id})"
