from copy import deepcopy

from django.db.models import Q, QuerySet

from hknweb.coursesemester.models import Semester

from hknweb.candidate.constants import EVENT_NAMES, REQUIREMENT_TITLES_TEMPLATE
from hknweb.candidate.models import (
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
)
from hknweb.candidate.utils_candportal.utils import get_requirement_colors
from hknweb.candidate.utils_candportal.get_events import (
    get_required_hangouts,
    get_required_events,
    get_mandatory_events,
    sort_rsvps_by_event_type,
)


class ReqInfo:
    EMPTY_REQ_LIST = {
        EVENT_NAMES.INTERACTIVITIES: {
            EVENT_NAMES.HANGOUT: 0,
            EVENT_NAMES.CHALLENGE: 0,
            EVENT_NAMES.EITHER: 0,
        },
        EVENT_NAMES.BITBYTE: 0,
    }

    TYPE_TO_TITLE_MAPPING = {
        EVENT_NAMES.BITBYTE: "Bit-Byte",
        EVENT_NAMES.INTERACTIVITIES: {
            EVENT_NAMES.EITHER: "Interactivities",
            EVENT_NAMES.HANGOUT: "Officer Hangouts",
            EVENT_NAMES.CHALLENGE: "Officer Challenges",
        },
        EVENT_NAMES.MANDATORY: "Mandatory",
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

        confirmed_events[EVENT_NAMES.MANDATORY], unconfirmed_events[EVENT_NAMES.MANDATORY] = \
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

        num_required_hangouts = lst[EVENT_NAMES.INTERACTIVITIES]
        for r in RequirementHangout.objects.filter(
            candidateSemesterActive=candidate_semester.id,
            enable=True,
        ):
            num_required_hangouts[r.eventType] = r.numberRequired
        num_required_hangouts[EVENT_NAMES.EITHER] =\
            num_required_hangouts[EVENT_NAMES.HANGOUT] \
            + num_required_hangouts[EVENT_NAMES.CHALLENGE]

        bitbyte_requirement = RequirementBitByteActivity.objects.filter(
            candidateSemesterActive=candidate_semester,
            enable=True,
        ).first()
        if bitbyte_requirement:
            lst[EVENT_NAMES.BITBYTE] = bitbyte_requirement.numberRequired

        lst[EVENT_NAMES.MANDATORY] =\
            len(self.confirmed_events[EVENT_NAMES.MANDATORY]) \
            + len(self.unconfirmed_events[EVENT_NAMES.MANDATORY])

        self.lst = lst

    def set_confirmed_reqs(self, num_challenges: int, num_bitbytes: int):
        # TODO: Hardcoded-ish for now, allow for choice of Hangout events
        confirmed_hangouts = len(self.confirmed_events.get("Hangout", []))
        confirmed = {
            EVENT_NAMES.INTERACTIVITIES: {
                EVENT_NAMES.HANGOUT: confirmed_hangouts,
                EVENT_NAMES.CHALLENGE: num_challenges,
                EVENT_NAMES.EITHER: confirmed_hangouts + num_challenges,
            },
            EVENT_NAMES.BITBYTE: num_bitbytes,
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
        names = {
            **{r: r for r in self.lst},
            **self.TYPE_TO_TITLE_MAPPING,
        }
        titles = deepcopy(names)

        def apply(d1: dict, d2: dict, d3: dict, d4: dict):
            for k, v in d1.items():
                if isinstance(v, dict):
                    apply(d1[k], d2[k], d3[k], d4[k])
                else:
                    d2[k] = REQUIREMENT_TITLES_TEMPLATE.format(
                        name=d1[k],
                        num_required=d3[k],
                        num_remaining=d4[k],
                    )

        apply(names, titles, self.lst, self.remaining)

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
