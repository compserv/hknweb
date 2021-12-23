from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404, reverse
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from hknweb.utils import (
    login_and_permission,
    get_rand_photo,
)
from hknweb.events.models import Event, Rsvp


@login_and_permission("events.delete_rsvp")
def unrsvp(request, id):
    if request.method != "POST":
        raise Http404()

    event = get_object_or_404(Event, pk=id)
    rsvp = get_object_or_404(Rsvp, user=request.user, event=event)
    if rsvp.confirmed:
        messages.error(request, "Cannot un-rsvp from event you have gone to.")
    else:
        old_admitted = set(event.admitted_set())
        rsvp.delete()
        for off_waitlist_rsvp in event.newly_off_waitlist_rsvps(old_admitted):
            send_off_waitlist_email(request, off_waitlist_rsvp.user, event)
    next_page = request.POST.get("next", "/")
    return redirect(next_page)


def send_off_waitlist_email(request, user, event):
    subject = "[HKN] You have gotten off the waitlist for your event"

    event_link = request.build_absolute_uri(
        reverse("events:detail", kwargs={"id": event.id})
    )
    html_content = render_to_string(
        "events/off_waitlist_email.html",
        {
            "subject": subject,
            "event_name": event.name,
            "event_link": event_link,
            "img_link": get_rand_photo(),
        },
    )
    msg = EmailMultiAlternatives(
        subject, subject, settings.NO_REPLY_EMAIL, [user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
