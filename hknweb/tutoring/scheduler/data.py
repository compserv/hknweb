from typing import List
import requests
import json

from hknweb.tutoring.models import TutoringLogistics

from hknweb.tutoring.scheduler.tutoring import Slot, Tutor


class Data:
    def __init__(self) -> None:
        self.slots: List[Slot] = []
        self.tutors: List[Tutor] = []


class DjangoData(Data):
    def __init__(self, logistics: TutoringLogistics) -> None:
        super().__init__()


class OldJSONTestData(Data):
    def __init__(self, url: str) -> None:
        super().__init__()

        content = requests.get(url).content
        clean = lambda s: s.replace(b"\n", b"").replace(b"\r", b"").replace(b"\'", b"\"")
        data = json.loads(clean(content))

        for t_dto in data["tutors"]:
            self.tutors.append(Tutor(
                tutor_id=t_dto["tid"],
                slot_prefs=t_dto["timeSlots"],
                office_prefs=t_dto["officePrefs"],
                adjacent_pref=t_dto["adjacentPref"],
                num_assignments=t_dto["numAssignments"],
            ))

        for s_dto in data["slots"]:
            self.slots.append(Slot(
                slot_id=s_dto["sid"],
                day=s_dto["day"],
                hour=s_dto["hour"],
                office=s_dto["office"],
            ))
