from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from hknweb.utils import markdownify

from hknweb.utils import allow_public_access
from hknweb.events.constants import (
    ACCESSLEVEL_TO_DESCRIPTION,
    ATTR,
    RSVPS_PER_PAGE,
)
from hknweb.events.models import Event, Rsvp, AttendanceForm
from hknweb.events.utils import format_url
from hknweb.utils import get_access_level


@allow_public_access
def show_details(request, id):
    return show_details_helper(request, id, reverse("events:index"), True)


def show_details_helper(request, id, back_link: str, can_edit: bool):
    event = get_object_or_404(Event, pk=id)
    if event.access_level < get_access_level(request.user):
        messages.warning(request, "Insufficent permission to access event.")
        return redirect(back_link)

    context = {
        "event": event,
        "event_description": markdownify(event.description),
        "event_location": format_url(event.location),
        "user_access_level": ACCESSLEVEL_TO_DESCRIPTION[get_access_level(request.user)],
        "event_access_level": ACCESSLEVEL_TO_DESCRIPTION[event.access_level],
        "back_link": back_link,
        "can_edit": can_edit and request.user.has_perm("events.change_event"),
    }

    if not request.user.is_authenticated:
        return render(request, "events/show_details.html", context)

    rsvps = Rsvp.objects.filter(event=event)
    waitlisted = False
    waitlist_position = 0

    rsvp = None
    user_rsvps = rsvps.filter(user=request.user)
    if user_rsvps.exists():
        # Gets the rsvp object for the user
        rsvp = user_rsvps.first()
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

    rsvps_page = Paginator(rsvps, RSVPS_PER_PAGE).get_page(
        request.GET.get("rsvps_page")
    )
    waitlists_page = Paginator(waitlists, RSVPS_PER_PAGE).get_page(
        request.GET.get("waitlists_page")
    )

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
        **context,
        ATTR.DATA: data,
        "rsvp": rsvp,
        "attendance_form": AttendanceForm.objects.filter(event=event).first(),
        "waitlisted": waitlisted,
        "waitlist_position": waitlist_position,
    }
    return render(request, "events/show_details.html", context)
