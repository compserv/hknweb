from django.shortcuts import reverse
from django.views.generic import TemplateView
from django.utils import timezone

from hknweb.utils import (
    method_login_and_permission,
    get_semester_bounds,
)
from hknweb.events.constants import ATTR
from hknweb.events.models import Event, EventType
from hknweb.events.utils import format_url
from hknweb.utils import get_access_level


@method_login_and_permission("events.add_rsvp")
class AllRsvpsView(TemplateView):
    """List of rsvp'd and not rsvp'd events."""

    template_name = "events/all_rsvps.html"

    def get_context_data(self):
        # Get the start and end time for event filtering
        start_time, end_time = get_semester_bounds(timezone.now())
        if self.request.GET.get("option") == "upcoming":
            start_time = timezone.now()

        # Get the current event type
        event_types = EventType.objects.order_by("type").all()
        event_types = sorted(event_types, key=lambda e: not (e.type == ATTR.MANDATORY))

        event_type = self.request.GET.get("event_type", None)
        event_type = event_types[0].type if ((event_type is None) and event_types) else event_type
        event_type = EventType.objects.filter(type=event_type).first()

        # Get all events
        all_events = Event.objects.filter(
            start_time__gte=start_time,
            start_time__lte=end_time,
            access_level__gte=get_access_level(self.request.user),
            event_type=event_type,
        ).order_by("start_time")

        rsvpd_data, not_rsvpd_data = [], []
        for event in all_events:
            if event.rsvp_set.filter(user=self.request.user):
                data, url = rsvpd_data, "events:unrsvp"
                waitlisted = event.on_waitlist(self.request.user)
            else:
                data, url = not_rsvpd_data, "events:rsvp"
                waitlisted = False

            data.append(
                {
                    "event": event,
                    "action": reverse(url, args=[event.id]),
                    "location": format_url(event.location),
                    "waitlisted": waitlisted,
                }
            )

        data = [
            {
                ATTR.CLASS: "right-half",
                ATTR.TITLE: "RSVP'd / Waitlist",
                ATTR.EVENTS: rsvpd_data,
                ATTR.DISPLAY_VALUE: "un-RSVP",
            },
            {
                ATTR.CLASS: "left-half",
                ATTR.TITLE: "Not RSVP'd",
                ATTR.EVENTS: not_rsvpd_data,
                ATTR.DISPLAY_VALUE: "RSVP",
            },
        ]

        context = {
            "data": data,
            "event_types": event_types,
            "event_type": event_type,
        }
        return context
