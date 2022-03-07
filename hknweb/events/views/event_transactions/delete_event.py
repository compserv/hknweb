from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from hknweb.utils import method_login_and_permission
from hknweb.events.models import Event


@method_login_and_permission("events.delete_event")
class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy("events:index")
