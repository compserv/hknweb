from copy import deepcopy

from django.conf import settings
from django.db.models import Q, QuerySet

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
from hknweb.candidate.utils_candportal.get_events import (
    MANDATORY,
    get_required_hangouts,
    get_required_events,
    get_mandatory_events,
    sort_rsvps_by_event_type,
)


class ReqInfo:
    EMPTY_REQ_LIST = {
        settings.HANGOUT_EVENT: {
            settings.HANGOUT_ATTRIBUTE_NAME: 0,
            settings.CHALLENGE_ATTRIBUTE_NAME: 0,
            settings.EITHER_ATTRIBUTE_NAME: 0,
        },
        settings.BITBYTE_ACTIVITY: 0,
    }

    TYPE_TO_TITLE_MAPPING = {
        settings.BITBYTE_ACTIVITY: "Bit-Byte",
    }

    def __init__(self):
        self.required_events: dict = None
        self.confirmed_events: dict = None
        self.unconfirmed_events: dict = None
        self.lst: dict = None
        self.confirmed: dict = None
        self.remaining: dict = None
        self.statuses: dict = None
        self.titles: dict = None
        self.colors: dict = None

    def set_confirmed_unconfirmed_events(
        self,
        rsvps: QuerySet,
        candidate_semester: Semester,
        required_events_merger: set,
    ):
        required_events = {
            **get_required_events(candidate_semester, required_events_merger),
            **get_required_hangouts(candidate_semester),
        }

        confirmed_rsvps = rsvps.filter(confirmed=True)
        unconfirmed_rsvps = rsvps.filter(confirmed=False)

        confirmed_events = sort_rsvps_by_event_type(confirmed_rsvps, required_events)
        unconfirmed_events = sort_rsvps_by_event_type(unconfirmed_rsvps, required_events)

        confirmed_events[MANDATORY], unconfirmed_events[MANDATORY] = \
            get_mandatory_events(candidate_semester, confirmed_rsvps)

        self.required_events = required_events
        self.confirmed_events = confirmed_events
        self.unconfirmed_events = unconfirmed_events

    def set_list(self, candidate_semester: Semester):
        lst = deepcopy(self.EMPTY_REQ_LIST)
        if not candidate_semester:
            return lst

        for r in RequriementEvent.objects.filter(
            Q(enable=True) | Q(eventType__type__in=self.required_events),
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

        lst[MANDATORY] =\
            len(self.confirmed_events[MANDATORY]) \
            + len(self.unconfirmed_events[MANDATORY])

        self.lst = lst

    def set_confirmed_reqs(self, num_challenges: int, num_bitbytes: int):
        # TODO: Hardcoded-ish for now, allow for choice of Hangout events
        confirmed_hangouts = len(self.confirmed_events.get("Hangout", []))
        confirmed = {
            settings.HANGOUT_EVENT: {
                settings.HANGOUT_ATTRIBUTE_NAME: confirmed_hangouts,
                settings.CHALLENGE_ATTRIBUTE_NAME: num_challenges,
                settings.EITHER_ATTRIBUTE_NAME: confirmed_hangouts + num_challenges,
            },
            settings.BITBYTE_ACTIVITY: num_bitbytes,
            **{r: len(self.confirmed_events[r]) for r in self.confirmed_events},
        }

        self.confirmed = confirmed

    def set_remaining(self):
        remaining = deepcopy(self.lst)

        def apply(d1: dict, d2: dict, output_d: dict):
            for r in d1:
                if isinstance(d1[r], dict):
                    apply(d1[r], d2[r], output_d[r])
                else:
                    output_d[r] = max(d1[r] - d2[r], 0)

        apply(self.lst, self.confirmed, remaining)

        self.remaining = remaining

    def set_statuses(self):
        statuses = dict()

        for k, v in self.remaining.items():
            if isinstance(v, int):
                statuses[k] = v == 0
            else:
                statuses[k] = all(v.values())

        self.statuses = statuses

    def set_titles(self):
        titles = {}
        for req_type in self.statuses:
            name = self.required_events.get(req_type, {}).get("title", None)
            if not name:
                name = self.TYPE_TO_TITLE_MAPPING.get(req_type, req_type)

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
