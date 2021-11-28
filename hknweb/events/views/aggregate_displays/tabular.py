from django.shortcuts import reverse
from django.views.generic import TemplateView
from django.utils import timezone

from hknweb.utils import (
    method_login_and_permission,
    get_semester_bounds,
)
from hknweb.events.constants import ATTR
from hknweb.events.models import Event, EventType, Rsvp
from hknweb.events.utils import (
    format_url,
    get_padding,
)
from hknweb.utils import get_access_level


@method_login_and_permission("events.add_rsvp")
class AllRsvpsView(TemplateView):
    """List of rsvp'd and not rsvp'd events."""

    template_name = "events/all_rsvps.html"

    def get_context_data(self):
        view_option = self.request.GET.get("option")
        semester_start, semester_end = get_semester_bounds(timezone.now())
        all_events = (
            Event.objects.filter(start_time__gte=semester_start)
            .filter(start_time__lte=semester_end)
            .filter(access_level__gte=get_access_level(self.request.user))
            .order_by("start_time")
        )
        if view_option == "upcoming":
            all_events = all_events.filter(start_time__gte=timezone.now())
        rsvpd_event_ids = Rsvp.objects.filter(
            user__exact=self.request.user
        ).values_list("event", flat=True)
        rsvpd_events = all_events.filter(pk__in=rsvpd_event_ids)
        not_rsvpd_events = all_events.exclude(pk__in=rsvpd_event_ids)

        for event in rsvpd_events:
            event.waitlisted = event.on_waitlist(
                self.request.user
            )  # Is this bad practice? idk

        event_types = EventType.objects.order_by("type").all()
        event_types = sorted(event_types, key=lambda e: not (e.type == ATTR.MANDATORY))

        rsvpd_data, not_rsvpd_data = [], []
        for event_type in event_types:
            typed_rsvpd_events = rsvpd_events.filter(event_type=event_type)
            typed_not_rsvpd_events = not_rsvpd_events.filter(event_type=event_type)

            rsvpd_padding, not_rsvpd_padding = get_padding(
                len(typed_not_rsvpd_events), len(typed_rsvpd_events)
            )

            rsvpd_data.append(
                {
                    ATTR.EVENT_TYPE: event_type,
                    ATTR.EVENTS: [
                        [
                            event,
                            reverse("events:unrsvp", args=[event.id]),
                            format_url(event.location),
                        ]
                        for event in typed_rsvpd_events
                    ],
                    ATTR.PADDING: rsvpd_padding,
                }
            )
            not_rsvpd_data.append(
                {
                    ATTR.EVENT_TYPE: event_type,
                    ATTR.EVENTS: [
                        [
                            event,
                            reverse("events:rsvp", args=[event.id]),
                            format_url(event.location),
                        ]
                        for event in typed_not_rsvpd_events
                    ],
                    ATTR.PADDING: not_rsvpd_padding,
                }
            )

        data = [
            {
                ATTR.CLASS: "right-half",
                ATTR.TITLE: "RSVP'd / Waitlist",
                ATTR.EVENTS_DATA: rsvpd_data,
                ATTR.DISPLAY_VALUE: "un-RSVP",
            },
            {
                ATTR.CLASS: "left-half",
                ATTR.TITLE: "Not RSVP'd",
                ATTR.EVENTS_DATA: not_rsvpd_data,
                ATTR.DISPLAY_VALUE: "RSVP",
            },
        ]

        context = {
            ATTR.DATA: data,
        }
        return context
