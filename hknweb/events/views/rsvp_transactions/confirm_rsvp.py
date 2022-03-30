from django.http import Http404, HttpResponse
from hknweb.events.models import Rsvp
from hknweb.utils import login_and_access_level


@login_and_access_level(0)
def confirm_rsvp(request, id, operation):
    if request.method != "POST":
        raise Http404()

    rsvp = Rsvp.objects.get(id=id)
    rsvp.confirmed = operation == 0  # { confirmed: 0, unconfirmed: 1 }
    rsvp.save()

    if operation == 1:  # unconfirm
        rsvp.attendanceresponse_set.all().delete()

    return HttpResponse()
