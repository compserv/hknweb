from django.shortcuts import render

from hknweb.models import Profile
from hknweb.events.models import Event, EventType, GCalAccessLevelMapping
from hknweb.events.models.constants import ACCESS_LEVELS
from hknweb.utils import allow_public_access, get_access_level
from hknweb.events.google_calendar_utils import get_calendar_link


@allow_public_access
def index(request):
    return calendar_helper(request)


def calendar_helper(request, event_type: str = None):
    user_access_level = get_access_level(request.user)

    events = Event.objects.order_by("-start_time").filter(
        access_level__gte=user_access_level
    )
    event_types = EventType.objects.order_by("type")
    if event_type is not None:
        events = events.filter(event_type__type=event_type)
        event_types = event_types.filter(type=event_type)

    context = {
        "events": events,
        "event_types": event_types,
        "calendars": get_calendars(request, user_access_level),
    }
    return render(request, "events/index.html", context)


def get_calendars(request, user_access_level: int):
    calendars = []
    for access_level, name in ACCESS_LEVELS:
        if user_access_level > access_level:
            continue

        calendar_id = GCalAccessLevelMapping.get_calendar_id(access_level)  # Link
        if not calendar_id:
            continue

        calendars.append(
            {
                "name": name,
                "link": get_calendar_link(calendar_id=calendar_id),
            }
        )

    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile.google_calendar_id:
            calendars.append(
                {
                    "name": "personal",
                    "link": get_calendar_link(calendar_id=profile.google_calendar_id),
                }
            )

    for calendar in calendars[:-1]:
        calendar["separator"] = "/"
    if len(calendars) > 0:
        calendars[-1]["separator"] = ""

    return calendars
