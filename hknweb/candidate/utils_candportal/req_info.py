from django.conf import settings
from django.db.models import Q

from hknweb.coursesemester.models import Semester

from hknweb.candidate.models import (
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
)
from hknweb.candidate.utils_candportal.utils import (
    create_title,
    get_requirement_colors,
)
from hknweb.candidate.utils_candportal.check_requirements import (
    check_interactivity_requirements,
)


class ReqInfo:
    def __init__(self,
        confirmed_events: dict,
        unconfirmed_events: dict,
    ):
        self.confirmed_events = confirmed_events
        self.unconfirmed_events = unconfirmed_events

        self.lst: dict = None
        self.statuses: dict = None
        self.remaining: dict = None
        self.titles: dict = None
        self.colors: dict = None

    def set_list(self, candidate_semester: Semester, required_events: dict):
        lst = {
            settings.HANGOUT_EVENT: {
                settings.HANGOUT_ATTRIBUTE_NAME: 0,
                settings.CHALLENGE_ATTRIBUTE_NAME: 0,
                settings.EITHER_ATTRIBUTE_NAME: 0,
            },
            settings.BITBYTE_ACTIVITY: 0,
        }
        if not candidate_semester:
            return lst

        for r in RequriementEvent.objects.filter(
            Q(enable=True) | Q(eventType__type__in=required_events),
            candidateSemesterActive=candidate_semester.id,
        ):
            lst[r.eventType.type] = r.numberRequired

        num_required_hangouts = lst[settings.HANGOUT_EVENT]
        for r in RequirementHangout.objects.filter(
            candidateSemesterActive=candidate_semester.id,
            enable=True,
        ):
            num_required_hangouts[r.eventType] = r.numberRequired

        bitbyte_requirement = RequirementBitByteActivity.objects.filter(
            candidateSemesterActive=candidate_semester,
            enable=True,
        ).first()
        if bitbyte_requirement:
            lst[settings.BITBYTE_ACTIVITY] = bitbyte_requirement.numberRequired

        self.lst = lst

    def set_statuses_and_remaining(self, num_challenges: int, num_bitbytes: int):
        """Checks which requirements have been fulfilled by a candidate."""
        statuses = dict.fromkeys(self.lst.keys(), False)
        remaining = {**self.lst}  # Makes deep copy of "req_list"

        for req_type, minimum in self.lst.items():
            num_confirmed = 0
            if req_type == settings.BITBYTE_ACTIVITY:
                num_confirmed = num_bitbytes
            elif req_type in self.confirmed_events:
                num_confirmed = len(self.confirmed_events[req_type])
            # officer hangouts and mandatory events are special cases
            if req_type == settings.HANGOUT_EVENT:
                # TODO: Hardcoded-ish for now, allow for choice of Hangout events
                if "Hangout" in self.confirmed_events:
                    num_confirmed = len(self.confirmed_events["Hangout"])
                interactivities = {
                    settings.HANGOUT_ATTRIBUTE_NAME: num_confirmed,
                    settings.CHALLENGE_ATTRIBUTE_NAME: num_challenges,
                    settings.EITHER_ATTRIBUTE_NAME: num_confirmed + num_challenges,
                }
                (
                    statuses[req_type],
                    remaining[req_type],
                ) = check_interactivity_requirements(
                    interactivities, self.lst[settings.HANGOUT_EVENT]
                )
            elif (minimum < 0) or (minimum is None):
                remaining[req_type] = len(self.unconfirmed_events[req_type])
                statuses[req_type] = remaining[req_type] == 0
            else:
                statuses[req_type] = num_confirmed >= minimum
                remaining[req_type] = max(minimum - num_confirmed, 0)

        self.statuses = statuses
        self.remaining = remaining

    def set_titles(self, required_events: dict):
        titles = {}
        for req_type in self.statuses:
            name = required_events.get(req_type, {}).get("title", req_type)
            if not name:
                name = req_type

            titles[req_type] = create_title(
                req_type,
                self.remaining[req_type],
                name,
                self.lst[req_type],
                self.lst.get(settings.HANGOUT_EVENT, {}),
            )

        self.titles = titles

    def set_colors(self, event_types: list, merger_nodes):
        colors = get_requirement_colors(event_types)
        colors.update(
            get_requirement_colors(
                merger_nodes,
                lambda view_key: view_key,
                lambda get_key: get_key.get_events_str(),
            )
        )

        self.colors = colors
