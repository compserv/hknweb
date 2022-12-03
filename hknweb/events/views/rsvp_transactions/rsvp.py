from django.http import Http404, HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from hknweb.utils import login_and_permission
from hknweb.events.models import Event, Rsvp


@login_and_permission("events.add_rsvp")
def rsvp(request, id):
    if request.method != "POST":
        raise Http404()

    event = get_object_or_404(Event, pk=id)

    if Rsvp.has_not_rsvpd(request.user, event):
        Rsvp.objects.create(user=request.user, event=event, confirmed=False)
    else:
        messages.error(request, "You have already RSVP'd.")

    return HttpResponse()
