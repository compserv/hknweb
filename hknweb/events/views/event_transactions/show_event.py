from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from hknweb.utils import markdownify

from hknweb.utils import login_and_permission
from hknweb.events.constants import (
    ACCESSLEVEL_TO_DESCRIPTION,
    ATTR,
    GCAL_INVITE_TEMPLATE_ATTRIBUTE_NAME,
    RSVPS_PER_PAGE,
)
from hknweb.events.models import Event, Rsvp
from hknweb.events.utils import (
    create_gcal_link,
    format_url,
)
from hknweb.utils import get_access_level


@login_and_permission("events.view_event")
def show_details(request, id):
    event = get_object_or_404(Event, pk=id)
    if event.access_level < get_access_level(request.user):
        messages.warning(request, "Insufficent permission to access event.")
        return redirect("/events")
    rsvps = Rsvp.objects.filter(event=event)
    rsvpd = Rsvp.objects.filter(user=request.user, event=event).exists()
    waitlisted = False
    waitlist_position = 0

    if rsvpd:
        # Gets the rsvp object for the user
        rsvp = Rsvp.objects.filter(user=request.user, event=event)[:1].get()
        # Check if waitlisted
        if event.rsvp_limit:
            rsvps_before = rsvps.filter(created_at__lt=rsvp.created_at).count()
            waitlisted = rsvps_before >= event.rsvp_limit

    # Get waitlist position
    if waitlisted:
        position = rsvps.filter(created_at__lt=rsvp.created_at).count()
        waitlist_position = position - event.rsvp_limit + 1
    # Render only non-waitlisted rsvps
    rsvps = event.admitted_set()
    waitlists = event.waitlist_set()
    limit = event.rsvp_limit
    gcal_link = create_gcal_link(event)

    event_location = format_url(event.location)

    rsvps_page = Paginator(rsvps, RSVPS_PER_PAGE).get_page(
        request.GET.get("rsvps_page")
    )
    waitlists_page = Paginator(waitlists, RSVPS_PER_PAGE).get_page(
        request.GET.get("waitlists_page")
    )

    user_access_level = ACCESSLEVEL_TO_DESCRIPTION[get_access_level(request.user)]
    event_access_level = ACCESSLEVEL_TO_DESCRIPTION[event.access_level]

    data = [
        {
            ATTR.TITLE: "RSVPs",
            ATTR.DATA: rsvps_page if len(rsvps_page) > 0 else None,
            ATTR.PAGE_PARAM: "rsvps_page",
            ATTR.COUNT: str(rsvps.count()) + " / {limit}".format(limit=limit),
        },
    ]
    if limit:
        data.append(
            {
                ATTR.TITLE: "Waitlist",
                ATTR.DATA: waitlists_page if len(waitlists_page) > 0 else None,
                ATTR.PAGE_PARAM: "waitlists_page",
                ATTR.COUNT: str(waitlists.count()),
            }
        )

    context = {
        ATTR.DATA: data,
        "event": event,
        "event_description": markdownify(event.description),
        "event_location": event_location,
        "user_access_level": user_access_level,
        "event_access_level": event_access_level,
        "rsvpd": rsvpd,
        "waitlisted": waitlisted,
        "waitlist_position": waitlist_position,
        "can_edit": request.user.has_perm("events.change_event"),
        GCAL_INVITE_TEMPLATE_ATTRIBUTE_NAME: gcal_link,
    }
    return render(request, "events/show_details.html", context)
