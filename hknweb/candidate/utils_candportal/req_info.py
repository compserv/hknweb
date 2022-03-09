from copy import deepcopy

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
        num_required_hangouts[settings.EITHER_ATTRIBUTE_NAME] =\
            num_required_hangouts[settings.HANGOUT_ATTRIBUTE_NAME] \
            + num_required_hangouts[settings.CHALLENGE_ATTRIBUTE_NAME]

        bitbyte_requirement = RequirementBitByteActivity.objects.filter(
            candidateSemesterActive=candidate_semester,
            enable=True,
        ).first()
        if bitbyte_requirement:
            lst[settings.BITBYTE_ACTIVITY] = bitbyte_requirement.numberRequired

        self.lst = lst

    def set_remaining(self, num_challenges: int, num_bitbytes: int):
        """Checks which requirements have been fulfilled by a candidate."""
        # TODO: Hardcoded-ish for now, allow for choice of Hangout events
        confirmed_hangouts = len(self.confirmed_events.get("Hangout", []))
        confirmed = {
            settings.HANGOUT_EVENT: {
                settings.HANGOUT_ATTRIBUTE_NAME: confirmed_hangouts,
                settings.CHALLENGE_ATTRIBUTE_NAME: num_challenges,
                settings.EITHER_ATTRIBUTE_NAME: confirmed_hangouts + num_challenges,
            },
            settings.BITBYTE_ACTIVITY: num_bitbytes,
            **{r: len(self.confirmed_events[r]) for r in self.confirmed_events}
        }
        remaining = deepcopy(self.lst)

        def apply(d1: dict, d2: dict, output_d: dict):
            for r in d1:
                if isinstance(d1[r], dict):
                    apply(d1[r], d2[r], output_d[r])
                else:
                    output_d[r] = max(d1[r] - d2[r], 0)

        apply(self.lst, confirmed, remaining)

        self.remaining = remaining

    def set_statuses(self):
        statuses = dict()

        for k, v in self.remaining.items():
            if isinstance(v, int):
                statuses[k] = v == 0
            else:
                statuses[k] = all(v.values())

        self.statuses = statuses

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
