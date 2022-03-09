import itertools

from django.db.models import Q
from django.utils import timezone

from hknweb.utils import get_semester_bounds, get_access_level

from hknweb.events.models import Event
from hknweb.candidate.models import RequriementEvent


MANDATORY = "Mandatory"


def sort_rsvps_into_events(rsvps, required_events):
    """Takes in all confirmed rsvps and sorts them into types."""
    # Events in admin are currently in a readable format, must convert them to callable keys for Django template
    # sorted_events = dict.fromkeys(map_event_vars.keys())
    sorted_events = {}
    for event_type, event_time_range in required_events.items():
        query = Q(event__event_type__type=event_type)
        if event_time_range is not None:
            if event_time_range["eventsDateStart"] is not None:
                query = query & Q(
                    event__start_time__gt=event_time_range["eventsDateStart"]
                )
            if event_time_range["eventsDateEnd"] is not None:
                query = query & Q(event__end_time__lt=event_time_range["eventsDateEnd"])

        sorted_events[event_type] = [r.event for r in rsvps.filter(query)]

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


def get_required_events(candidate_semester, required_events_merger):
    required_events = {}
    if candidate_semester is None:
        return required_events

    merger_enabled = required_events_merger is not None
    requirement_events = RequriementEvent.objects.filter(
        candidateSemesterActive=candidate_semester.id
    )
    for r in requirement_events:
        enabled = r.enable
        event_type = r.eventType.type
        merged = merger_enabled and (event_type in required_events_merger)
        if enabled or merged:
            required_events[event_type] = {
                "eventsDateStart": r.eventsDateStart,
                "eventsDateEnd": r.eventsDateEnd,
                "title": r.title if r.enableTitle else None,
            }

    return required_events


def get_upcoming_events(user):
    today = timezone.now()
    return Event.objects.filter(
        start_time__range=(today, today + timezone.timedelta(days=7)),
        access_level__gte=get_access_level(user)
    ).order_by("start_time")
