from django.shortcuts import render

from hknweb.events.models import Event, EventType
from hknweb.utils import get_access_level


def index(request):
    events = Event.objects.order_by("-start_time").filter(
        access_level__gte=get_access_level(request.user)
    )
    event_types = EventType.objects.order_by("type")

    context = {
        "events": events,
        "event_types": event_types,
    }
    return render(request, "events/index.html", context)
