from django.shortcuts import redirect
from django.http import Http404
from django.shortcuts import get_object_or_404

from hknweb.utils import login_and_permission
from hknweb.events.models import Event


@login_and_permission("events.delete_event")
def delete_event(request, id):
    if request.method != "POST":
        raise Http404()

    event = get_object_or_404(Event, pk=id)
    event.delete()

    next_page = request.POST.get("next", "/")
    return redirect(next_page)
