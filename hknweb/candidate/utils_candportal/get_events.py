from django.conf import settings
from django.db.models import Q, QuerySet
from django.utils import timezone
from django.contrib.auth.models import User

from hknweb.coursesemester.models import Semester
from hknweb.utils import get_semester_bounds, get_access_level

from hknweb.events.models import Event, EventType
from hknweb.candidate.models import RequriementEvent, RequirementHangout, RequirementMandatory


MANDATORY = "Mandatory"


def sort_rsvps_by_event_type(
    rsvps: QuerySet,
    required_events: dict,
) -> dict:
    """Takes in all confirmed rsvps and sorts them into types."""
    res = dict()
    for event_type, event_time_range in required_events.items():
        filtered = rsvps.filter(
            event__event_type__type=event_type,
            event__start_time__gt=event_time_range["eventsDateStart"],
            event__end_time__lt=event_time_range["eventsDateEnd"],
        )
        res[event_type] = [r.event for r in filtered]

    return res


def get_mandatory_events(candidate_semester: Semester, confirmed_rsvps: bool):
    # We want to show all mandatory events, not just the events the candidate has RSVP'd to

    r = candidate_semester \
        and RequirementMandatory.objects.filter(
            candidateSemesterActive=candidate_semester.id
        ).first()
    mandatory_events = QuerySet()
    start_time, end_time = get_semester_bounds(timezone.now())
    if r:
        mandatory_events = r.events.all()
        if r.eventsDateStart and r.eventsDateEnd:
            start_time, end_time = r.eventsDateStart, r.eventsDateEnd

    mandatory_events |= Event.objects.filter(
        event_type__type=MANDATORY,
        start_time__gt=start_time,
        end_time__lt=end_time,
    )
    mandatory_events = mandatory_events.distinct().order_by("start_time")

    confirmed_events = [r.event.id for r in confirmed_rsvps]
    confirmed = mandatory_events.filter(id__in=confirmed_events)
    unconfirmed = mandatory_events.exclude(id__in=confirmed_events)

    return confirmed, unconfirmed


def get_required_events(candidate_semester: Semester, required_events_merger: set) -> dict:
    required_events = {}
    if candidate_semester is None:
        return required_events

    semester_start, semester_end = get_semester_bounds(timezone.now())
    requirement_events = RequriementEvent.objects.filter(
        Q(enable=True) | Q(eventType__type__in=required_events_merger),
        candidateSemesterActive=candidate_semester.id,
    )
    for r in requirement_events:
        required_events[r.eventType.type] = {
            "eventsDateStart": r.eventsDateStart or semester_start,
            "eventsDateEnd": r.eventsDateEnd or semester_end,
            "title": r.title if r.enableTitle else None,
        }

    return required_events


def get_required_hangouts(candidate_semester: Semester) -> dict:
    required_hangout_events = {}
    if EventType.objects.filter(type="Hangout").count() == 0:
        return required_hangout_events

    semester_start, semester_end = get_semester_bounds(timezone.now())
    requirement_hangout = RequirementHangout.objects.filter(
        candidateSemesterActive=candidate_semester.id,
        eventType=settings.HANGOUT_ATTRIBUTE_NAME,
        enable=True,
    ).first()
    if not requirement_hangout:
        return required_hangout_events

    # TODO: Hardcoded-ish for now, allow for choice of Hangout events
    required_hangout_events["Hangout"] = {
        "eventsDateStart": requirement_hangout.hangoutsDateStart or semester_start,
        "eventsDateEnd": requirement_hangout.hangoutsDateEnd or semester_end,
        "title": "Hangout",
    }

    return required_hangout_events


def get_upcoming_events(user: User) -> QuerySet:
    today = timezone.now()
    return Event.objects.filter(
        start_time__range=(today, today + timezone.timedelta(days=7)),
        access_level__gte=get_access_level(user)
    ).order_by("start_time")
