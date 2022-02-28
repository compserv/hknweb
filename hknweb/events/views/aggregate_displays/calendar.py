from django.shortcuts import render

from hknweb.events.models import Event, EventType
from hknweb.utils import get_access_level
from hknweb.events.google_calendar_utils import get_calendar_link


def index(request):
    events = Event.objects.order_by("-start_time").filter(
        access_level__gte=get_access_level(request.user)
    )
    event_types = EventType.objects.order_by("type")
    google_calendar_add_link = get_calendar_link()

    context = {
        "events": events,
        "event_types": event_types,
        "google_calendar_add_link": google_calendar_add_link,
    }
    return render(request, "events/index.html", context)
