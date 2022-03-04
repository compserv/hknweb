from django.http import Http404, HttpResponseForbidden, HttpResponse
from hknweb.events.models import Rsvp
from hknweb.utils import get_access_level


def confirm_rsvp(request, id, operation):
    if request.method != "POST":
        raise Http404()

    access_level = get_access_level(request.user)
    if access_level > 0:
        return HttpResponseForbidden()

    rsvp = Rsvp.objects.get(id=id)
    rsvp.confirmed = operation == 0  # { confirmed: 0, unconfirmed: 1 }
    rsvp.save()

    return HttpResponse()
