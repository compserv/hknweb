from typing import Any, Dict, List
import requests
import json

from hknweb.tutoring.models import TutoringLogistics

from hknweb.tutoring.scheduler.tutoring import Slot, Tutor


class Data:
    DAY_SORT_MAPPING: Dict[str, str] = {
        "Monday": "0",
        "Tuesday": "1",
        "Wednesday": "2",
        "Thursday": "3",
        "Friday": "4",
    }

    def __init__(self) -> None:
        self.slots: List[Slot] = []
        self.tutors: List[Tutor] = []

    def readable_formatted_assignments(self) -> str:  # pragma: no cover
        slot_sort = lambda s: Data.DAY_SORT_MAPPING[s.day] + str(s.hour)
        slots = sorted(self.slots, key=slot_sort)

        res = ""
        for slot in slots:
            tutors = ", ".join(map(repr, slot.tutors))
            res += f"{slot}: {tutors}\n"

        return res


class DjangoData(Data):
    def __init__(self, logistics: TutoringLogistics) -> None:
        super().__init__()


class JSONData(Data):
    def __init__(self) -> None:
        super().__init__()

        json_str = self.get_json_str()
        clean = lambda s: s.replace("\n", "").replace("\r", "").replace("'", '"')
        data: Dict[str, Any] = json.loads(clean(json_str))

        self.post_init(data)

    def get_json_str(self) -> str:  # pragma: no cover
        raise NotImplementedError()

    def post_init(self, data: Dict[str, Any]):
        for t_dto in data["tutors"]:
            self.tutors.append(
                Tutor(
                    tutor_id=t_dto["tid"],
                    slot_prefs=t_dto["timeSlots"],
                    office_prefs=t_dto["officePrefs"],
                    adjacent_pref=t_dto["adjacentPref"],
                    num_assignments=t_dto["numAssignments"],
                )
            )

        for s_dto in data["slots"]:
            self.slots.append(
                Slot(
                    slot_id=s_dto["sid"],
                    day=s_dto["day"],
                    hour=s_dto["hour"],
                    office=s_dto["office"],
                )
            )


class RemoteJSONData(JSONData):  # pragma: no cover
    def __init__(self, url: str) -> None:
        self.url = url

        super().__init__()

    def get_json_str(self) -> str:
        return requests.get(self.url).content.decode()


class LocalJSONData(JSONData):  # pragma: no cover
    def __init__(self, path: str) -> None:
        self.path = path

        super().__init__()

    def get_json_str(self) -> str:
        return open(self.path).read()
