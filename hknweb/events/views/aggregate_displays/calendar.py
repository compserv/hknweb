from django.shortcuts import render

from hknweb.models import Profile
from hknweb.events.models import Event, EventType, GCalAccessLevelMapping
from hknweb.events.models.constants import ACCESS_LEVELS
from hknweb.utils import get_access_level
from hknweb.events.google_calendar_utils import get_calendar_link


def index(request):
    context = dict()

    user_access_level = get_access_level(request.user)
    events = Event.objects.order_by("-start_time").filter(access_level__gte=user_access_level)
    event_types = EventType.objects.order_by("type")

    calendars = []
    for access_level, name in ACCESS_LEVELS:
        if user_access_level > access_level:
            continue

        calendar_id = GCalAccessLevelMapping.get_calendar_id(access_level)  # Link
        calendars.append({
            "name": name,
            "link": get_calendar_link(calendar_id=calendar_id),
        })

    profiles = Profile.objects.filter(user=request.user)
    if profiles.exists():
        profile = profiles.first()
        if profile.google_calendar_id:
            calendars.append({
                "name": "personal",
                "link": get_calendar_link(calendar_id=profile.google_calendar_id),
            })

    for calendar in calendars[:-1]:
        calendar["separator"] = "/"
    calendars[-1]["separator"] = ""

    context = {
        "events": events,
        "event_types": event_types,
        "calendars": calendars,
    }
    return render(request, "events/index.html", context)
