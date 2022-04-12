from copy import deepcopy

from django.db.models import Q, QuerySet

from hknweb.coursesemester.models import Semester
from hknweb.events.models import EventType

from hknweb.candidate.constants import EVENT_NAMES, REQUIREMENT_TITLES_TEMPLATE
from hknweb.candidate.models import (
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
)
from hknweb.candidate.utils_candportal.utils import apply_to_dicts
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
        EVENT_NAMES.MANDATORY: 0,
    }

    TYPE_TO_TITLE_MAPPING = {
        EVENT_NAMES.BITBYTE: "Bit-Byte",
        EVENT_NAMES.INTERACTIVITIES: {
            EVENT_NAMES.EITHER: "Interactivities",
            EVENT_NAMES.HANGOUT: "Officer Hangouts",
            EVENT_NAMES.CHALLENGE: "Officer Challenges",
        },
    }

    def set_confirmed_unconfirmed_events(
        self,
        rsvps: QuerySet,
        candidate_semester: Semester,
        required_events_merger: set,
    ):
        self.required_events = {
            **get_required_events(candidate_semester, required_events_merger),
            **get_required_hangouts(candidate_semester),
        }

        confirmed_rsvps = rsvps.filter(confirmed=True)
        unconfirmed_rsvps = rsvps.filter(confirmed=False)

        confirmed_events = sort_rsvps_by_event_type(
            confirmed_rsvps, self.required_events
        )
        unconfirmed_events = sort_rsvps_by_event_type(
            unconfirmed_rsvps, self.required_events
        )

        (
            confirmed_events[EVENT_NAMES.MANDATORY],
            unconfirmed_events[EVENT_NAMES.MANDATORY],
        ) = get_mandatory_events(candidate_semester, confirmed_rsvps)
        confirmed_events.setdefault("Hangout", [])
        unconfirmed_events.setdefault("Hangout", [])

        self.confirmed_events = confirmed_events
        self.unconfirmed_events = unconfirmed_events

    def set_list(self, candidate_semester: Semester):
        self.lst = deepcopy(self.EMPTY_REQ_LIST)
        if not candidate_semester:
            return

        data = [
            (RequriementEvent, Q(eventType__type__in=self.required_events)),
            (RequirementHangout, Q()),
            (RequirementBitByteActivity, Q()),
        ]
        events, hangouts, bitbyte = [
            c.objects.filter(
                Q(enable=True) | q, candidateSemesterActive=candidate_semester.id
            )
            for c, q in data
        ]

        self.lst.update({r.eventType.type: r.numberRequired for r in events})

        d = self.lst[EVENT_NAMES.INTERACTIVITIES]
        d.update({r.eventType: r.numberRequired for r in hangouts})
        d[EVENT_NAMES.EITHER] += d[EVENT_NAMES.HANGOUT] + d[EVENT_NAMES.CHALLENGE]

        if bitbyte.exists():
            self.lst[EVENT_NAMES.BITBYTE] = bitbyte.first().numberRequired

        self.lst[EVENT_NAMES.MANDATORY] = len(
            self.confirmed_events[EVENT_NAMES.MANDATORY]
        ) + len(self.unconfirmed_events[EVENT_NAMES.MANDATORY])

    def set_confirmed_reqs(self, num_challenges: int, num_bitbytes: int):
        # TODO: Hardcoded-ish for now, allow for choice of Hangout events
        confirmed_hangouts = len(self.confirmed_events["Hangout"])
        self.confirmed = {
            EVENT_NAMES.INTERACTIVITIES: {
                EVENT_NAMES.HANGOUT: confirmed_hangouts,
                EVENT_NAMES.CHALLENGE: num_challenges,
                EVENT_NAMES.EITHER: confirmed_hangouts + num_challenges,
            },
            EVENT_NAMES.BITBYTE: num_bitbytes,
            **{r: len(self.confirmed_events[r]) for r in self.confirmed_events},
        }

    def set_remaining(self):
        def fn(k, v, d1, d2, d3):
            d1[k] = max(d2[k] - d3[k], 0)

        self.remaining = apply_to_dicts(
            fn, deepcopy(self.lst), self.lst, self.confirmed
        )

    def set_statuses(self):
        self.statuses = {}
        for k, v in self.remaining.items():
            if isinstance(v, int):
                self.statuses[k] = (v == 0)
            elif k == EVENT_NAMES.INTERACTIVITIES:
                for k_interactivities, v_interactivities in v.items():
                    self.statuses[k_interactivities] = (v_interactivities == 0)
            else:
                self.statuses[k] = not any(v.values())

    def set_titles(self):
        names = {
            **{r: r for r in self.lst},
            **self.TYPE_TO_TITLE_MAPPING,
        }

        def fn(k, v, d1, d2, d3, d4):
            d1[k] = REQUIREMENT_TITLES_TEMPLATE.format(d2[k], d3[k], d4[k])

        self.titles = apply_to_dicts(
            fn, deepcopy(names), names, self.lst, self.remaining
        )

    def set_colors(self, event_types: list, merger_nodes):
        self.colors = {
            **dict.fromkeys(event_types, "grey"),
            **{e.type: e.color for e in EventType.objects.filter(type__in=event_types)},
            **{e.get_events_str(): e.color for e in merger_nodes},
        }
