from django.shortcuts import render

from hknweb.models import Profile
from hknweb.events.models import Event, EventType
from hknweb.utils import get_access_level
from hknweb.events.google_calendar_utils import get_calendar_link


def index(request):
    context = dict()

    events = Event.objects.order_by("-start_time").filter(
        access_level__gte=get_access_level(request.user)
    )
    event_types = EventType.objects.order_by("type")
    context = {
        **context,
        "events": events,
        "event_types": event_types,
    }

    if request.user.is_authenticated:
        gcal_all_add_link = get_calendar_link()

        profile = Profile.objects.filter(user=request.user).first()
        gcal_personal_add_link = None
        if profile.google_calendar_id:
            gcal_personal_add_link = get_calendar_link(calendar_id=profile.google_calendar_id)

        context = {
            **context,
            "gcal_all_add_link": gcal_all_add_link,
            "gcal_personal_add_link": gcal_personal_add_link,
        }

    return render(request, "events/index.html", context)
