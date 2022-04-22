from typing import Tuple
from functools import reduce

from django.contrib.auth.models import User

from hknweb.coursesemester.models import Semester
from hknweb.events.models import Rsvp

from hknweb.candidate.constants import ATTR, EVENT_NAMES, REQUIREMENT_TITLES_TEMPLATE
from hknweb.candidate.models import (
    Announcement,
    RequirementMergeRequirement,
)

from hknweb.candidate.utils_candportal.merged_events import MergedEvents
from hknweb.candidate.utils_candportal.count import (
    count_challenges,
    count_num_bitbytes,
)
from hknweb.candidate.utils_candportal.get_events import (
    get_required_events,
    get_upcoming_events,
)
from hknweb.candidate.utils_candportal.process_misc_req import (
    CandidateFormProcessor,
    CommitteeProjectProcessor,
    DuePaymentProjectProcessor,
)
from hknweb.candidate.utils_candportal.req_info import ReqInfo


class CandidatePortalData:
    def __init__(self, user: User):
        self.user = user

    def get_merge_info(self, candidate_semester: Semester) -> Tuple[set, list]:
        if not candidate_semester:
            return set(), []

        merger_reqs = RequirementMergeRequirement.objects.filter(
            candidateSemesterActive=candidate_semester.id,
            enable=True,
        )
        if not merger_reqs:
            return set(), []

        merged_events = [MergedEvents(m, candidate_semester) for m in merger_reqs]
        required_events_merger = reduce(set.__or__, (set(n.events()) for n in merged_events))
        return required_events_merger, merged_events

    def process_merged_events(self, merge_event, req_info: ReqInfo) -> str:
        merge_event_string = merge_event.get_events_str()

        key = merge_event_string
        if key in req_info.titles:
            key = f"{key} {sum(s.startswith(key) for s in req_info.titles) + 1}"
            req_info.colors[key] = req_info.colors[merge_event_string]

        remaining_count, grand_total, missing_event_reqs_text = merge_event.get_counts(req_info)
        req_info.statuses[key] = round(remaining_count, 2) < 0.05

        req_info.titles[key] = REQUIREMENT_TITLES_TEMPLATE.format(
            merge_event_string, grand_total, remaining_count
        )
        
        if missing_event_reqs_text:
            req_info.titles[key] += " - " + missing_event_reqs_text

        events = merge_event.events()
        confirmed, unconfirmed = req_info.confirmed_events, req_info.unconfirmed_events
        EMPTY_LIST = []
        confirmed[key] = reduce(list.__add__, (confirmed.get(e, EMPTY_LIST) for e in events), EMPTY_LIST)
        unconfirmed[key] = reduce(list.__add__, (unconfirmed.get(e, EMPTY_LIST) for e in events), EMPTY_LIST)

        return key

    def get_user_cand_data(self) -> dict:
        candidate_semester = self.user.profile.candidate_semester

        required_events_merger, merged_events = self.get_merge_info(candidate_semester)

        challenges = count_challenges(self.user, candidate_semester)
        num_bitbytes = count_num_bitbytes(self.user, candidate_semester)

        event_types = list(get_required_events(candidate_semester, set()))
        rsvps = Rsvp.objects.filter(user__exact=self.user)

        req_info = ReqInfo()
        req_info.set_confirmed_unconfirmed_events(
            rsvps, candidate_semester, required_events_merger
        )
        req_info.set_list(candidate_semester)
        req_info.set_confirmed_reqs(challenges[ATTR.NUM_CONFIRMED], num_bitbytes)
        req_info.set_remaining()
        req_info.set_statuses()
        req_info.set_titles()
        req_info.set_colors(event_types, merged_events)

        merge_names = [self.process_merged_events(merged_e, req_info) for merged_e in merged_events]

        return {
            "req_statuses": {e: req_info.statuses[e] for e in event_types},
            **self._get_interactivities_context(req_info, challenges),
            **self._get_bitbyte_context(req_info, num_bitbytes),
            **self._get_misc_context(self.user, candidate_semester),
            **self._get_event_related_context(
                self.user, req_info, event_types + merge_names
            ),
            **self._get_misc_req_related_context(self.user, candidate_semester),
        }

    @staticmethod
    def _get_interactivities_context(req_info: ReqInfo, challenges: dict) -> dict:
        req_info_titles = req_info.titles
        interactivities_req_info_titles = req_info_titles[EVENT_NAMES.INTERACTIVITIES]
        req_info_statuses = req_info.statuses
        return {
            EVENT_NAMES.INTERACTIVITIES: {
                EVENT_NAMES.CHALLENGE: {
                    ATTR.TITLE: interactivities_req_info_titles[EVENT_NAMES.CHALLENGE],
                    **challenges,
                    ATTR.STATUS: req_info_statuses[EVENT_NAMES.CHALLENGE],
                },
                EVENT_NAMES.HANGOUT: {
                    ATTR.TITLE: interactivities_req_info_titles[EVENT_NAMES.HANGOUT],
                    ATTR.STATUS: req_info_statuses[EVENT_NAMES.HANGOUT],
                },
                EVENT_NAMES.EITHER: {
                    ATTR.TITLE: interactivities_req_info_titles[EVENT_NAMES.EITHER],
                    ATTR.STATUS: req_info_statuses[EVENT_NAMES.EITHER],
                },
            }
        }

    @staticmethod
    def _get_bitbyte_context(req_info: ReqInfo, num_bitbytes: int) -> dict:
        return {
            "bitbyte": {
                ATTR.TITLE: req_info.titles[EVENT_NAMES.BITBYTE],
                ATTR.STATUS: req_info.statuses[EVENT_NAMES.BITBYTE],
                ATTR.NUM_BITBYTES: num_bitbytes,
            }
        }

    @staticmethod
    def _get_misc_context(user: User, candidate_semester: Semester) -> dict:
        announcements = Announcement.objects.filter(visible=True).order_by(
            "-release_date"
        )

        return {
            "announcements": announcements,
            "username": user.username,
            "user_self": True,
            "candidate_semester": candidate_semester
            or "Please set your candidate semester in your Account Settings",
        }

    @staticmethod
    def _get_event_related_context(user: User, r: ReqInfo, event_types: list) -> dict:
        info = (
            r.titles,
            r.statuses,
            r.colors,
            r.confirmed_events,
            r.unconfirmed_events,
        )
        attrs = (ATTR.TITLE, ATTR.STATUS, ATTR.COLOR, ATTR.CONFIRMED, ATTR.UNCONFIRMED)
        events = [dict(zip(attrs, (i[t] for i in info))) for t in event_types]

        return {
            "events": events,
            "confirmed_events": r.confirmed_events,
            "unconfirmed_events": r.unconfirmed_events,
            "upcoming_events": get_upcoming_events(user),
        }

    @staticmethod
    def _get_misc_req_related_context(user: User, candidate_semester: Semester) -> dict:
        return {
            "committee_project": CommitteeProjectProcessor.process_status(
                user, candidate_semester
            ),
            "candidate_forms": CandidateFormProcessor.process_status(
                user, candidate_semester
            ),
            "due_payments": DuePaymentProjectProcessor.process_status(
                user, candidate_semester
            ),
        }
