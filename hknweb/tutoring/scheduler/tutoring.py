from typing import Dict, List, Set, Union


class Slot:
    def __init__(
        self,
        slot_id: int,
        day: str,
        hour: int,
        office: str,
    ):
        self.slot_id = slot_id
        self.day = day
        self.hour = hour
        self.office = office

        self.tutors: "Set[Tutor]" = []

    def assign(self, t: "Tutor") -> None:
        self.tutors.add(t)

    def unassign(self, t: "Tutor") -> None:
        self.tutors.remove(t)

    def simultaneous(self, other: "Slot") -> bool:
        return (self.hour == other.hour) and (self.day == other.day)

    def adjacent(self, other: "Slot") -> bool:
        is_same_office: bool = self.office == other.office
        is_same_day: bool = self.day == other.day
        is_hour_before: bool = self.hour == other.hour - 1
        is_hour_after: bool = self.hour == other.hour + 1
        return is_same_office and is_same_day and (is_hour_before or is_hour_after)

    def __repr__(self) -> Dict[str, Union[int, str]]:
        return {
            "slot_id": self.slot_id,
            "day": self.day,
            "hour": self.hour,
            "office": self.office,
        }

    def __eq__(self, other: "Slot") -> bool:
        return repr(self) == repr(other)

    def __str__(self):
        return f"Slot({repr(self)})"


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

        self.slots: "Set[Slot]" = set()

    def conflict(self, s1: "Slot") -> bool:
        return any(map(lambda s2: s1.simultaneous(s2), self.slots))

    def assign(self, s: "Slot") -> None:
        self.slots.add(s)

    def unassign(self, s: "Slot") -> None:
        self.slots.remove(s)

    def __repr__(self) -> Dict[str, Union[str, int]]:
        return {
            "tutor_id": self.tutor_id,
            "name": self.name,
        }

    def __str__(self) -> str:
        return f"Tutor({repr(self)})"
