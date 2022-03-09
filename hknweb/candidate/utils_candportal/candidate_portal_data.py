from django.conf import settings
from django.utils import timezone

from hknweb.events.models import Rsvp, EventType

from hknweb.candidate.constants import ATTR
from hknweb.candidate.models import (
    Announcement,
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
    RequirementMandatory,
    RequirementMergeRequirement,
)

from hknweb.candidate.utils_candportal.utils import (
    create_title,
    get_requirement_colors,
)
from hknweb.candidate.utils_candportal.check_requirements import (
    check_requirements,
)
from hknweb.candidate.utils_candportal.merged_events import MergedEvents
from hknweb.candidate.utils_candportal.count import (
    count_challenges,
    count_num_bitbytes,
)
from hknweb.candidate.utils_candportal.get_events import (
    get_events,
    get_required_events,
    get_upcoming_events,
)
from hknweb.candidate.utils_candportal.process_misc_req import (
    CandidateFormProcessor,
    CommitteeProjectProcessor,
    DuePaymentProjectProcessor,
)


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
    user = None

    def __init__(self, user):
        self.user = user

    def process_events(
        self,
        rsvps,
        today,
        required_events,
        candidateSemester,
        requirement_mandatory,
        num_challenges_confirmed,
        num_bitbytes,
        req_list,
    ):
        def get_events_by_confirmed(confirmed):
            return get_events(
                rsvps,
                today,
                required_events,
                candidateSemester,
                requirement_mandatory,
                confirmed=confirmed,
            )

        confirmed_events = get_events_by_confirmed(True)
        unconfirmed_events = get_events_by_confirmed(False)

        req_statuses, req_remaining = check_requirements(
            confirmed_events,
            unconfirmed_events,
            num_challenges_confirmed,
            num_bitbytes,
            req_list,
        )

        return confirmed_events, unconfirmed_events, req_statuses, req_remaining

    def process_merge_node(
        self,
        node,
        req_titles,
        req_remaining,
        req_list,
        req_colors,
        req_statuses,
        confirmed_events,
        unconfirmed_events,
        merge_names,
    ):
        node_string = node.get_events_str()
        remaining_count, grand_total = 0, 0

        node_string_key = node_string
        count = 2
        if node_string_key in req_titles:
            while node_string_key in req_titles:
                node_string_key = "{} {}".format(node_string, count)
                count += 1
            req_colors[node_string_key] = req_colors[node_string]

        req_statuses[node_string_key] = True
        if node.all_required:
            grand_total = -1
            for event in node.events():
                req_statuses[node_string_key] = (
                    req_statuses[node_string_key] and req_statuses[event]
                )
                if not req_statuses[node_string_key]:
                    break
        else:
            remaining_count, grand_total = node.get_counts(req_remaining, req_list)
            req_statuses[node_string_key] = round(remaining_count, 2) < 0.05

        # num_required_hangouts is None, since Merger nodes should not use it
        if node.all_required:
            # TODO Support for All Required for Merged Requirement (probably not a huge priority)
            req_titles[node_string_key] = (
                node_string
                + " - Looped Merged Requirements for all required currently unsupported"
            )
        else:
            req_titles[node_string_key] = create_title(
                "", remaining_count, node_string, grand_total, None
            )

        confirmed_events[node_string_key] = []
        unconfirmed_events[node_string_key] = []
        for event in node.events():
            confirmed_events[node_string_key].extend(confirmed_events[event])
            unconfirmed_events[node_string_key].extend(unconfirmed_events[event])

        merge_names.append(node_string_key)
        # req_statuses, confirmed_events, unconfirmed_events

    def get_user_cand_data(self):
        candidateSemester = self.user.profile.candidate_semester

        (
            num_challenges_confirmed,
            num_challenges_rejected,
            num_pending,
        ) = count_challenges(self.user, candidateSemester)

        required_events_merger = set()

        seen_merger_nodes = set()
        merger_nodes = []
        if candidateSemester is not None:
            for merger in RequirementMergeRequirement.objects.filter(
                candidateSemesterActive=candidateSemester.id
            ):
                if merger.enable:
                    merger_nodes.append(
                        MergedEvents(merger, candidateSemester, seen_merger_nodes)
                    )

        for node in merger_nodes:
            for eventType in node.events():
                required_events_merger.add(eventType)

        required_events = get_required_events(candidateSemester, required_events_merger)

        req_list = {}
        # Can't use "get", since no guarantee that the Mandatory object of a semester always exist
        requirement_mandatory = (
            candidateSemester
            and RequirementMandatory.objects.filter(
                candidateSemesterActive=candidateSemester.id
            ).first()
        )

        if candidateSemester is not None:
            for requirementEvent in RequriementEvent.objects.filter(
                candidateSemesterActive=candidateSemester.id
            ):
                if requirementEvent.enable or (
                    requirementEvent.eventType.type in required_events
                ):
                    req_list[
                        requirementEvent.eventType.type
                    ] = requirementEvent.numberRequired

        req_list[settings.HANGOUT_EVENT] = {
            settings.HANGOUT_ATTRIBUTE_NAME: 0,
            settings.CHALLENGE_ATTRIBUTE_NAME: 0,
            settings.EITHER_ATTRIBUTE_NAME: 0,
        }

        num_required_hangouts = req_list[settings.HANGOUT_EVENT]
        if candidateSemester is not None:
            for requirementHangout in RequirementHangout.objects.filter(
                candidateSemesterActive=candidateSemester.id
            ):
                if requirementHangout.enable:
                    num_required_hangouts[
                        requirementHangout.eventType
                    ] = requirementHangout.numberRequired
                    if requirementHangout.eventType == settings.HANGOUT_ATTRIBUTE_NAME:
                        # TODO: Hardcoded-ish for now, allow for choice of Hangout events
                        if EventType.objects.filter(type="Hangout").count() > 0:
                            required_events["Hangout"] = {
                                "eventsDateStart": requirementHangout.hangoutsDateStart,
                                "eventsDateEnd": requirementHangout.hangoutsDateEnd,
                                "title": "Hangout",
                            }

        ### Bit Byte
        req_list[settings.BITBYTE_ACTIVITY] = 0
        # Can't use "get", since no guarantee that the object of this semester always exist
        bitbyte_requirement = (
            candidateSemester
            and RequirementBitByteActivity.objects.filter(
                candidateSemesterActive=candidateSemester
            ).first()
        )
        if bitbyte_requirement is not None and bitbyte_requirement.enable:
            req_list[settings.BITBYTE_ACTIVITY] = bitbyte_requirement.numberRequired

        num_bitbytes = count_num_bitbytes(self.user, bitbyte_requirement)

        announcements = Announcement.objects.filter(visible=True).order_by(
            "-release_date"
        )
        ###

        today = timezone.now()
        rsvps = Rsvp.objects.filter(user__exact=self.user)
        # Both confirmed and unconfirmed rsvps have been sorted into event types

        # Process Events here
        (
            confirmed_events,
            unconfirmed_events,
            req_statuses,
            req_remaining,
        ) = self.process_events(
            rsvps,
            today,
            required_events,
            candidateSemester,
            requirement_mandatory,
            num_challenges_confirmed,
            num_bitbytes,
            req_list,
        )

        event_types = list(get_required_events(candidateSemester, None))
        req_colors = get_requirement_colors(event_types)

        blank_dict = {}
        req_titles = {}
        for req_type in req_statuses:
            name = required_events.get(req_type, blank_dict).get("title", req_type)
            if (name is None) or (name == ""):
                name = req_type
            title_created = create_title(
                req_type,
                req_remaining[req_type],
                name,
                req_list[req_type],
                req_list.get(settings.HANGOUT_EVENT, blank_dict),
            )
            req_titles[req_type] = title_created

        # Process Merged Events here
        req_colors.update(
            get_requirement_colors(
                merger_nodes,
                lambda view_key: view_key,
                lambda get_key: get_key.get_events_str(),
            )
        )
        merge_names = []
        for node in merger_nodes:
            self.process_merge_node(
                node,
                req_titles,
                req_remaining,
                req_list,
                req_colors,
                req_statuses,
                confirmed_events,
                unconfirmed_events,
                merge_names,
            )

        events = [
            {
                ATTR.TITLE: req_titles[t],
                ATTR.STATUS: req_statuses[t],
                ATTR.COLOR: req_colors[t],
                ATTR.CONFIRMED: confirmed_events[t],
                ATTR.UNCONFIRMED: unconfirmed_events[t]
            }
        for t in (event_types + merge_names)]

        interactivities = {
            ATTR.TITLE: req_titles[settings.HANGOUT_EVENT][
                settings.EITHER_ATTRIBUTE_NAME
            ],
            ATTR.STATUS: req_statuses[settings.HANGOUT_EVENT],
            settings.CHALLENGE_ATTRIBUTE_NAME: {
                ATTR.TITLE: req_titles[settings.HANGOUT_EVENT][
                    settings.CHALLENGE_ATTRIBUTE_NAME
                ],
                ATTR.NUM_PENDING: num_pending,
                ATTR.NUM_REJECTED: num_challenges_rejected,
                # anything not pending or rejected is confirmed
                ATTR.NUM_CONFIRMED: num_challenges_confirmed,
            },
            settings.HANGOUT_ATTRIBUTE_NAME: {
                ATTR.TITLE: req_titles[settings.HANGOUT_EVENT][
                    settings.HANGOUT_ATTRIBUTE_NAME
                ],
            },
        }

        bitbyte = {
            ATTR.TITLE: "Bit-Byte",
            ATTR.STATUS: req_statuses[settings.BITBYTE_ACTIVITY],
            ATTR.NUM_BITBYTES: num_bitbytes,
        }

        context = {
            "announcements": announcements,
            "confirmed_events": {
                **{e: confirmed_events[e] for e in event_types},
                "hangout": confirmed_events["Hangout"],
            },
            "unconfirmed_events": {
                **{e: unconfirmed_events[e] for e in event_types},
                "hangout": unconfirmed_events["Hangout"],
            },
            "req_statuses": {e: req_statuses[e] for e in event_types},
            "upcoming_events": get_upcoming_events(self.user),
            "committee_project": CommitteeProjectProcessor.process_status(self.user, candidateSemester),
            "candidate_forms": CandidateFormProcessor.process_status(self.user, candidateSemester),
            "due_payments": DuePaymentProjectProcessor.process_status(self.user, candidateSemester),
            "events": events,
            "interactivities": interactivities,
            "bitbyte": bitbyte,
            "candidate_semester": candidateSemester
            or "Please set your candidate semester in your Account Settings",
            "username": self.user.username,
            "user_self": True,
        }
        return context
