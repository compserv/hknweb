import itertools
from typing import Union

from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from hknweb.utils import get_access_level, get_semester_bounds

from hknweb.events.models import Event, Rsvp, EventType

from hknweb.candidate.constants import (
    ATTR,
    REQUIREMENT_TITLES_ALL,
    REQUIREMENT_TITLES_TEMPLATE,
)
from hknweb.candidate.models import (
    Announcement,
    BitByteActivity,
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
    OffChallenge,
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
    RequirementMandatory,
    RequirementMergeRequirement,
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

MANDATORY = "Mandatory"


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


def sort_rsvps_into_events(rsvps, required_events):
    """Takes in all confirmed rsvps and sorts them into types."""
    # Events in admin are currently in a readable format, must convert them to callable keys for Django template
    # sorted_events = dict.fromkeys(map_event_vars.keys())
    sorted_events = {}
    for event_type in required_events:
        temp = []
        event_time_range = required_events[event_type]
        query = Q(event__event_type__type=event_type)
        if event_time_range is not None:
            if event_time_range["eventsDateStart"] is not None:
                query = query & Q(
                    event__start_time__gt=event_time_range["eventsDateStart"]
                )
            if event_time_range["eventsDateEnd"] is not None:
                query = query & Q(event__end_time__lt=event_time_range["eventsDateEnd"])
        for rsvp in rsvps.filter(query):
            temp.append(rsvp.event)
        sorted_events[event_type] = temp
    return sorted_events


def get_events(
    rsvps, date, required_events, candidateSemester, requirement_mandatory, confirmed
):
    rsvp_models = rsvps.filter(confirmed=confirmed)
    events = sort_rsvps_into_events(rsvp_models, required_events)

    # We want to show all mandatory events, not just the events the candidate has RSVP'd to
    # Get all mandatory events i.e. events with event type "Mandatory"
    if candidateSemester and requirement_mandatory:
        mandatory_events = requirement_mandatory.events.all()
        if (
            requirement_mandatory.eventsDateStart
            and requirement_mandatory.eventsDateEnd
        ):
            mandatory_events = itertools.chain(
                mandatory_events,
                Event.objects.filter(
                    event_type__type=MANDATORY,
                    start_time__gt=requirement_mandatory.eventsDateStart,
                    end_time__lt=requirement_mandatory.eventsDateEnd,
                ),
            )
    else:
        curr_sem_start, curr_sem_end = get_semester_bounds(date)
        mandatory_events = Event.objects.filter(
            event_type__type=MANDATORY,
            start_time__gt=curr_sem_start,
            end_time__lt=curr_sem_end,
        )

    # Initialize events[MANDATORY] if hasn't
    if MANDATORY not in events:
        events[MANDATORY] = []

    # Can assume Mandatory Events where user RSVPed to is SEPARATE from those that they don't RSVP to
    if not confirmed:
        # Only add the non-rsvped Mandatory events to the Not Confirmed list
        mandatorySet = {}
        for mandatory_event in mandatory_events:
            # If no rsvps are found, add this mandatory event to the list of unconfirmed events
            if rsvps.filter(event__id=mandatory_event.id).count() == 0:
                mandatorySet[mandatory_event.id] = mandatory_event
        events[MANDATORY].extend(mandatorySet.values())

    events[MANDATORY].sort(key=lambda x: x.start_time)

    return events


def count_challenges(requested_user, candidateSemester):
    challenges = OffChallenge.objects.filter(requester__exact=requested_user)
    req_challenges_models = RequirementHangout.objects.filter(
        eventType=settings.CHALLENGE_ATTRIBUTE_NAME,
        candidateSemesterActive=candidateSemester,
    ).first()
    if req_challenges_models is not None:
        if req_challenges_models.hangoutsDateStart is not None:
            challenges = challenges.filter(
                request_date__gt=req_challenges_models.hangoutsDateStart,
            )
        if req_challenges_models.hangoutsDateEnd is not None:
            challenges = challenges.filter(
                request_date__lt=req_challenges_models.hangoutsDateEnd,
            )
    # if either one is waiting, challenge is still being reviewed

    ## Count number of confirmed
    challenges_confirmed = challenges.filter(
        Q(officer_confirmed=True) & Q(csec_confirmed=True)
    )
    num_challenges_confirmed = challenges_confirmed.count()
    ##

    ## Count number of rejected
    challenges_rejected = challenges.filter(
        Q(officer_confirmed=False) | Q(csec_confirmed=False)
    )
    num_challenges_rejected = challenges_rejected.count()
    ##

    num_pending = (
        challenges.count() - num_challenges_confirmed - num_challenges_rejected
    )

    return num_challenges_confirmed, num_challenges_rejected, num_pending


def count_num_bitbytes(requested_user, bitbyte_requirement):
    bitbyte_models = BitByteActivity.objects.filter(
        participants__exact=requested_user, confirmed=True
    )
    if bitbyte_requirement is not None:
        if bitbyte_requirement.bitByteDateStart is not None:
            bitbyte_models = bitbyte_models.filter(
                request_date__gt=bitbyte_requirement.bitByteDateStart,
            )
        if bitbyte_requirement.bitByteDateEnd is not None:
            bitbyte_models = bitbyte_models.filter(
                request_date__lt=bitbyte_requirement.bitByteDateEnd,
            )
    num_bitbytes = bitbyte_models.count()
    return num_bitbytes


def check_requirements(
    confirmed_events, unconfirmed_events, num_challenges, num_bitbytes, req_list
):
    """Checks which requirements have been fulfilled by a candidate."""
    req_statuses = dict.fromkeys(req_list.keys(), False)
    req_remaining = {**req_list}  # Makes deep copy of "req_list"

    for req_type, minimum in req_list.items():
        num_confirmed = 0
        if req_type == settings.BITBYTE_ACTIVITY:
            num_confirmed = num_bitbytes
        elif req_type in confirmed_events:
            num_confirmed = len(confirmed_events[req_type])
        # officer hangouts and mandatory events are special cases
        if req_type == settings.HANGOUT_EVENT:
            # TODO: Hardcoded-ish for now, allow for choice of Hangout events
            if "Hangout" in confirmed_events:
                num_confirmed = len(confirmed_events["Hangout"])
            interactivities = {
                settings.HANGOUT_ATTRIBUTE_NAME: num_confirmed,
                settings.CHALLENGE_ATTRIBUTE_NAME: num_challenges,
                settings.EITHER_ATTRIBUTE_NAME: num_confirmed + num_challenges,
            }
            (
                req_statuses[req_type],
                req_remaining[req_type],
            ) = check_interactivity_requirements(
                interactivities, req_list[settings.HANGOUT_EVENT]
            )
        elif (minimum < 0) or (minimum is None):  # settings.MANDATORY_EVENT:
            req_remaining[req_type] = len(
                unconfirmed_events[req_type]
            )  # len(unconfirmed_events[settings.MANDATORY_EVENT])
            req_statuses[req_type] = req_remaining[req_type] == 0
        else:
            req_statuses[req_type] = num_confirmed >= minimum
            req_remaining[req_type] = max(minimum - num_confirmed, 0)

    return req_statuses, req_remaining


def check_interactivity_requirements(interactivities, interactivity_requirements):
    """Returns whether officer interactivities are satisfied."""
    req_remaining = {}
    for req_type, num_required in interactivity_requirements.items():
        req_remaining[req_type] = max(num_required - interactivities[req_type], 0)

    req_status = not any(req_remaining.values())

    return req_status, req_remaining


# INTERACTIVITY_REQUIREMENTS = req_list[settings.HANGOUT_EVENT]
INTERACTIVITY_NAMES = {
    settings.EITHER_ATTRIBUTE_NAME: "Interactivities",
    settings.HANGOUT_ATTRIBUTE_NAME: "Officer Hangouts",
    settings.CHALLENGE_ATTRIBUTE_NAME: "Officer Challenges",
}


def create_title(
    req_type: str,
    req_remaining: Union[dict, int],
    name: str,
    num_required: int,
    num_required_hangouts: dict,
) -> str:
    if type(num_required) == int and (
        num_required < 0 or (num_required is None)
    ):  # settings.MANDATORY_EVENT:
        return REQUIREMENT_TITLES_ALL.format(name=name)
    elif req_type == settings.HANGOUT_EVENT:
        return {
            name: create_title(
                name,
                req_remaining[name],
                INTERACTIVITY_NAMES[name],
                num_required_hangouts[name],
                None,
            )
            for name in num_required_hangouts
        }
    else:
        return REQUIREMENT_TITLES_TEMPLATE.format(
            name=name,
            num_required=num_required,
            num_remaining=req_remaining,
        )


def get_requirement_colors(
    required_events,
    color_source=lambda view_key: EventType.objects.get(type=view_key),
    get_key=lambda x: x,
) -> dict:
    req_colors = {}
    for event in required_events:
        view_key = get_key(event)
        event_type = color_source(event)
        if event_type:
            req_colors[view_key] = event_type.color
        else:
            req_colors[view_key] = "grey"

    return req_colors


class MergedEvents:
    def __init__(
        self,
        merger_node: RequirementMergeRequirement,
        candidateSemester,
        seen_merger_nodes=set(),
    ):
        assert merger_node.enable, "The first Merger Node must be enabled"

        seen_merger_nodes.clear()
        current_merger_node = merger_node

        self.multiplier_event = {}
        self.all_required = False
        self.color = merger_node.color
        self.title = ""
        if merger_node.enableTitle:
            self.title = merger_node.title
        self.grand_total = None
        if merger_node.enableGrandTotal:
            self.grand_total = merger_node.grandTotal

        while current_merger_node is not None:
            if current_merger_node.id in seen_merger_nodes:
                self.all_required = True
                break
            seen_merger_nodes.add(current_merger_node.id)
            eventTypeKey = current_merger_node.event1.type
            self.multiplier_event[eventTypeKey] = (
                self.multiplier_event.get(eventTypeKey, 0)
                + current_merger_node.multiplier1
            )
            if current_merger_node.event2 is not None:
                eventTypeKey2 = current_merger_node.event2.type
                self.multiplier_event[eventTypeKey2] = (
                    self.multiplier_event.get(eventTypeKey2, 0)
                    + current_merger_node.multiplier2
                )
            if current_merger_node.linkedRequirement:
                current_merger_node = RequirementMergeRequirement.objects.filter(
                    candidateSemesterActive=candidateSemester.id,
                    id=current_merger_node.linkedRequirement.id,
                ).first()
            else:
                current_merger_node = None

    def __str__(self):
        text = self.get_events_str()
        all_required_text = "self.all_required = {}".format(self.all_required)
        all_color_text = "self.color = {}".format(self.color)
        return "{}, {}, {}".format(text, all_required_text, all_color_text)

    def get_events_str(self):
        if self.title:
            return self.title
        text = []
        for event, multiplier in zip(self.events(), self.multiplier()):
            if multiplier != 1.0:
                text.append(str(multiplier) + " x " + event)
            else:
                text.append(event)
        self.title = " + ".join(text)
        return self.title

    def get_counts(self, req_remaining, req_list):
        remaining_count = 0
        grand_total = 0
        for event, multiplier in zip(self.events(), self.multiplier()):
            remaining_count += multiplier * req_remaining.get(event, 0)
            grand_total += multiplier * req_list.get(event, 0)
        if self.grand_total is not None:
            grand_total = self.grand_total
        return remaining_count, grand_total

    def events(self):
        return self.multiplier_event.keys()

    def multiplier(self):
        return self.multiplier_event.values()
