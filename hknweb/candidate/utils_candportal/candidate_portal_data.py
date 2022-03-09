from typing import Tuple

from django.conf import settings
from django.contrib.auth.models import User

from hknweb.coursesemester.models import Semester
from hknweb.events.models import Rsvp

from hknweb.candidate.constants import ATTR
from hknweb.candidate.models import (
    Announcement,
    RequirementMergeRequirement,
)

from hknweb.candidate.utils_candportal.utils import create_title
from hknweb.candidate.utils_candportal.merged_events import MergedEvents
from hknweb.candidate.utils_candportal.count import (
    count_challenges,
    count_num_bitbytes,
)
from hknweb.candidate.utils_candportal.get_events import (
    MANDATORY,
    get_required_events,
    get_upcoming_events,
)
from hknweb.candidate.utils_candportal.process_misc_req import (
    CandidateFormProcessor,
    CommitteeProjectProcessor,
    DuePaymentProjectProcessor,
)
from hknweb.candidate.utils_candportal.req_info import ReqInfo


""" What the event types are called on admin site.
    Code will not work if they're called something else!! """
# map_event_vars = {
#     settings.MANDATORY_EVENT: 'Mandatory',
#     settings.FUN_EVENT: 'Fun',
#     settings.BIG_FUN_EVENT: 'Big Fun',
#     settings.SERV_EVENT: 'Serv',
#     settings.PRODEV_EVENT: 'Prodev',
#     settings.HANGOUT_EVENT: 'Hangout',
#     settings.BITBYTE_ACTIVITY: "Bit-Byte",
# }


class CandidatePortalData:
    def __init__(self, user: User):
        self.user = user

    def process_events(
        self,
        rsvps,
        candidate_semester: Semester,
        num_challenges_confirmed: int,
        num_bitbytes: int,
        event_types: list,
        merger_nodes,
        required_events_merger,
    ) -> ReqInfo:
        req_info = ReqInfo()

        req_info.set_confirmed_unconfirmed_events(rsvps, candidate_semester, required_events_merger)
        req_info.set_list(candidate_semester)
        req_info.set_confirmed_reqs(num_challenges_confirmed, num_bitbytes)
        req_info.set_remaining()
        req_info.set_statuses()
        req_info.set_titles()
        req_info.set_colors(event_types, merger_nodes)

        return req_info

    def get_merge_info(self, candidate_semester: Semester) -> Tuple[set, list]:
        required_events_merger = set()

        seen_merger_nodes = set()
        merger_nodes = []
        if candidate_semester is not None:
            for merger in RequirementMergeRequirement.objects.filter(
                candidateSemesterActive=candidate_semester.id
            ):
                if merger.enable:
                    merger_nodes.append(
                        MergedEvents(merger, candidate_semester, seen_merger_nodes)
                    )

        for node in merger_nodes:
            for eventType in node.events():
                required_events_merger.add(eventType)

        return required_events_merger, merger_nodes

    def process_merge_node(self, node, req_info) -> str:
        node_string = node.get_events_str()
        remaining_count, grand_total = 0, 0

        node_string_key = node_string
        count = 2
        if node_string_key in req_info.titles:
            while node_string_key in req_info.titles:
                node_string_key = "{} {}".format(node_string, count)
                count += 1
            req_info.colors[node_string_key] = req_info.colors[node_string]

        req_info.statuses[node_string_key] = True
        if node.all_required:
            grand_total = -1
            for event in node.events():
                req_info.statuses[node_string_key] = (
                    req_info.statuses[node_string_key] and req_info.statuses[event]
                )
                if not req_info.statuses[node_string_key]:
                    break
        else:
            remaining_count, grand_total = node.get_counts(req_info.remaining, req_info.lst)
            req_info.statuses[node_string_key] = round(remaining_count, 2) < 0.05

        # num_required_hangouts is None, since Merger nodes should not use it
        if node.all_required:
            # TODO Support for All Required for Merged Requirement (probably not a huge priority)
            req_info.titles[node_string_key] = (
                node_string
                + " - Looped Merged Requirements for all required currently unsupported"
            )
        else:
            req_info.titles[node_string_key] = create_title(
                "", remaining_count, node_string, grand_total, None
            )

        req_info.confirmed_events[node_string_key] = []
        req_info.unconfirmed_events[node_string_key] = []
        for event in node.events():
            req_info.confirmed_events[node_string_key].extend(req_info.confirmed_events[event])
            req_info.unconfirmed_events[node_string_key].extend(req_info.unconfirmed_events[event])

        return node_string_key

    def get_user_cand_data(self) -> dict:
        candidate_semester = self.user.profile.candidate_semester

        required_events_merger, merger_nodes = self.get_merge_info(candidate_semester)

        (
            num_challenges_confirmed,
            num_challenges_rejected,
            num_challenges_pending,
        ) = count_challenges(self.user, candidate_semester)
        num_bitbytes = count_num_bitbytes(self.user, candidate_semester)

        event_types = list(get_required_events(candidate_semester, set())) + [MANDATORY]
        req_info = self.process_events(
            Rsvp.objects.filter(user__exact=self.user),
            candidate_semester,
            num_challenges_confirmed,
            num_bitbytes,
            event_types,
            merger_nodes,
            required_events_merger,
        )

        merge_names = [self.process_merge_node(node, req_info) for node in merger_nodes]

        return {
            "req_statuses": {e: req_info.statuses[e] for e in event_types},
            **self._get_interactivities_context(
                req_info,
                num_challenges_confirmed,
                num_challenges_rejected,
                num_challenges_pending,
            ),
            **self._get_bitbyte_context(req_info, num_bitbytes),
            **self._get_misc_context(self.user, candidate_semester),
            **self._get_event_related_context(self.user, req_info, event_types + merge_names),
            **self._get_misc_req_related_context(self.user, candidate_semester),
        }

    @staticmethod
    def _get_interactivities_context(
        req_info: ReqInfo,
        num_challenges_confirmed: int,
        num_challenges_rejected: int,
        num_challenges_pending: int,
    ) -> dict:
        return {
            "interactivities": {
                ATTR.TITLE: req_info.titles[settings.HANGOUT_EVENT][
                    settings.EITHER_ATTRIBUTE_NAME
                ],
                ATTR.STATUS: req_info.statuses[settings.HANGOUT_EVENT],
                settings.CHALLENGE_ATTRIBUTE_NAME: {
                    ATTR.TITLE: req_info.titles[settings.HANGOUT_EVENT][
                        settings.CHALLENGE_ATTRIBUTE_NAME
                    ],
                    ATTR.NUM_PENDING: num_challenges_pending,
                    ATTR.NUM_REJECTED: num_challenges_rejected,
                    # anything not pending or rejected is confirmed
                    ATTR.NUM_CONFIRMED: num_challenges_confirmed,
                },
                settings.HANGOUT_ATTRIBUTE_NAME: {
                    ATTR.TITLE: req_info.titles[settings.HANGOUT_EVENT][
                        settings.HANGOUT_ATTRIBUTE_NAME
                    ],
                },
            }
        }

    @staticmethod
    def _get_bitbyte_context(req_info: ReqInfo, num_bitbytes: int) -> dict:
        return {
            "bitbyte": {
                ATTR.TITLE: req_info.titles[settings.BITBYTE_ACTIVITY],
                ATTR.STATUS: req_info.statuses[settings.BITBYTE_ACTIVITY],
                ATTR.NUM_BITBYTES: num_bitbytes,
            }
        }

    @staticmethod
    def _get_misc_context(user: User, candidate_semester: Semester) -> dict:
        announcements = Announcement.objects \
            .filter(visible=True) \
            .order_by("-release_date")

        return {
            "announcements": announcements,
            "username": user.username,
            "user_self": True,
            "candidate_semester": candidate_semester
            or "Please set your candidate semester in your Account Settings",
        }

    @staticmethod
    def _get_event_related_context(
        user: User,
        req_info: ReqInfo,
        event_types: list,
    ) -> dict:
        events = [
            {
                ATTR.TITLE: req_info.titles[t],
                ATTR.STATUS: req_info.statuses[t],
                ATTR.COLOR: req_info.colors[t],
                ATTR.CONFIRMED: req_info.confirmed_events[t],
                ATTR.UNCONFIRMED: req_info.unconfirmed_events[t]
            }
        for t in event_types]

        def helper(events):
            return {
                **{e: events[e] for e in event_types},
                "hangout": events.get("Hangout", []),
            }

        return {
            "events": events,
            "confirmed_events": helper(req_info.confirmed_events),
            "unconfirmed_events": helper(req_info.unconfirmed_events),
            "upcoming_events": get_upcoming_events(user),
        }

    @staticmethod
    def _get_misc_req_related_context(user: User, candidate_semester: Semester) -> dict:
        return {
            "committee_project": CommitteeProjectProcessor.process_status(user, candidate_semester),
            "candidate_forms": CandidateFormProcessor.process_status(user, candidate_semester),
            "due_payments": DuePaymentProjectProcessor.process_status(user, candidate_semester),
        }
