from django.conf import settings
from django.utils import timezone

from hknweb.utils import get_access_level

from hknweb.events.models import Event, Rsvp, EventType

from hknweb.candidate.constants import ATTR
from hknweb.candidate.models import (
    Announcement,
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
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
from hknweb.candidate.utils_candportal.get_events import get_events


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

    def get_event_types_and_times_map(
        self, candidateSemester, required_events_merger=None
    ):
        if candidateSemester is not None:
            for requirementEvent in RequriementEvent.objects.filter(
                candidateSemesterActive=candidateSemester.id
            ):
                if requirementEvent.enable or (
                    (required_events_merger is not None)
                    and (requirementEvent.eventType.type in required_events_merger)
                ):
                    title = None
                    if requirementEvent.enableTitle:
                        title = requirementEvent.title
                    yield (
                        requirementEvent.eventType.type,
                        requirementEvent.eventsDateStart,
                        requirementEvent.eventsDateEnd,
                        title,
                    )

    def get_event_types_map(self, candidateSemester):
        for eventType, _, _, _ in self.get_event_types_and_times_map(candidateSemester):
            yield eventType

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
        # Confirmed (confirmed=True)
        confirmed_events = get_events(
            rsvps,
            today,
            required_events,
            candidateSemester,
            requirement_mandatory,
            confirmed=True,
        )

        # Unconfirmed (confirmed=False)
        unconfirmed_events = get_events(
            rsvps,
            today,
            required_events,
            candidateSemester,
            requirement_mandatory,
            confirmed=False,
        )

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

    def process_status(
        self,
        title,
        requirements,
        completed_roster_model,
        completed_process,
        all_done_processor=lambda all_done, other_bool: all_done and other_bool,
        all_done=True,
    ):
        """
        requriements - the QuerySet of the requirements
        completed_roster - the Model of the entire entires of those who completed requirements
        user - the current User (as the User Model type)
        completed_process - function or lambda function to check if the requirement is completed,
                            with two parameters with the "requirement" and "completed_roster" of
                            the current user
        """
        completed_roster = completed_roster_model.objects.all()
        resulting_statuses = []
        if requirements is not None:
            for requirement in requirements:
                is_completed = completed_process(requirement, completed_roster)
                all_done = all_done_processor(all_done, is_completed)
                resulting_statuses.append(
                    {"requirement": requirement, "status": is_completed}
                )
        result = {
            "title": title,
            "resulting_statuses": resulting_statuses,
            "all_done": all_done,
        }
        return result

    def check_due(self, due_required, completed_roster):
        entry = completed_roster.filter(duePayment=due_required.id).first()
        if entry is None:
            return False
        return self.user in entry.users.all()

    def check_form(self, form_required, completed_roster):
        entry = completed_roster.filter(form=form_required.id).first()
        if entry is None:
            return False
        return self.user in entry.users.all()

    def check_committee_project(self, committee_project_required, completed_roster):
        entry = completed_roster.filter(
            committeeProject=committee_project_required.id
        ).first()
        if entry is None:
            return False
        return self.user in entry.users.all()

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

        required_events = {}
        for (
            eventType,
            eventsDateStart,
            eventsDateEnd,
            title,
        ) in self.get_event_types_and_times_map(
            candidateSemester, required_events_merger
        ):
            required_events[eventType] = {
                "eventsDateStart": eventsDateStart,
                "eventsDateEnd": eventsDateEnd,
                "title": title,
            }

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

        ### Candidate Forms
        candidate_forms = candidateSemester and CandidateForm.objects.filter(
            visible=True, candidateSemesterActive=candidateSemester.id
        ).order_by("duedate")

        candidate_forms_with_completed = self.process_status(
            "Complete all required forms",
            candidate_forms,
            CandidateFormDoneEntry,
            lambda form_required, completed_roster: self.check_form(
                form_required, completed_roster
            ),
        )
        ###

        ### Due Payments
        due_payments = candidateSemester and DuePayment.objects.filter(
            visible=True, candidateSemesterActive=candidateSemester.id
        ).order_by("duedate")

        due_payments_with_completed = self.process_status(
            "Pay dues",
            due_payments,
            DuePaymentPaidEntry,
            lambda due_required, completed_roster: self.check_due(
                due_required, completed_roster
            ),
        )
        ###

        ### Committee Projects
        committee_project = candidateSemester and CommitteeProject.objects.filter(
            visible=True, candidateSemesterActive=candidateSemester.id
        ).order_by("name")

        committee_project_with_completed = self.process_status(
            "Complete a Committee Project",
            committee_project,
            CommitteeProjectDoneEntry,
            lambda committee_project_required, completed_roster: self.check_committee_project(
                committee_project_required, completed_roster
            ),
            all_done_processor=lambda all_done, other_bool: all_done or other_bool,
            all_done=False,
        )
        ###

        # miscellaneous_requirements = [due_payments_with_completed, candidate_forms_with_completed]

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

        req_colors = get_requirement_colors(self.get_event_types_map(candidateSemester))

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

        upcoming_events = (
            Event.objects.filter(
                start_time__range=(today, today + timezone.timedelta(days=7))
            )
            .order_by("start_time")
            .filter(access_level__gte=get_access_level(self.user))
        )

        events = []
        for req_event in self.get_event_types_map(candidateSemester):
            events.append(
                {
                    ATTR.TITLE: req_titles[req_event],
                    ATTR.STATUS: req_statuses[req_event],
                    ATTR.COLOR: req_colors[req_event],
                    ATTR.CONFIRMED: confirmed_events[req_event],
                    ATTR.UNCONFIRMED: unconfirmed_events[req_event],
                }
            )
        for req_event in merge_names:
            events.append(
                {
                    ATTR.TITLE: req_titles[req_event],
                    ATTR.STATUS: req_statuses[req_event],
                    ATTR.COLOR: req_colors[req_event],
                    ATTR.CONFIRMED: confirmed_events[req_event],
                    ATTR.UNCONFIRMED: unconfirmed_events[req_event],
                }
            )

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
                **{event_key: confirmed_events[event_key]
                for event_key in self.get_event_types_map(candidateSemester)},
                "hangout": confirmed_events["Hangout"],
            },
            "unconfirmed_events": {
                **{event_key: unconfirmed_events[event_key]
                for event_key in self.get_event_types_map(candidateSemester)},
                "hangout": unconfirmed_events["Hangout"],
            },
            "req_statuses": {
                event_key: req_statuses[event_key]
                for event_key in self.get_event_types_map(candidateSemester)
            },
            "upcoming_events": upcoming_events,
            "committee_project": committee_project_with_completed,
            "candidate_forms": candidate_forms_with_completed,
            "due_payments": due_payments_with_completed,
            "events": events,
            "interactivities": interactivities,
            "bitbyte": bitbyte,
            "candidate_semester": candidateSemester
            or "Please set your candidate semester in your Account Settings",
            "username": self.user.username,
            "user_self": True,
        }
        return context
