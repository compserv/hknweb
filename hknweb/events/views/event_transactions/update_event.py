from django.contrib import messages
from django.views.generic.edit import UpdateView

from hknweb.utils import (
    method_login_and_permission,
    DATETIME_12_HOUR_FORMAT,
    PACIFIC_TIMEZONE,
)
from hknweb.events.models import Event
from hknweb.events.forms import EventUpdateForm


@method_login_and_permission("events.change_event")
class EventUpdateView(UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name_suffix = "_edit"

    def get_initial(self):
        """Override some prepopulated data with custom data; in this case, make times
        the right format."""
        initial = super().get_initial()
        initial["start_time"] = self.object.start_time.astimezone(
            PACIFIC_TIMEZONE
        ).strftime(DATETIME_12_HOUR_FORMAT)
        initial["end_time"] = self.object.end_time.astimezone(
            PACIFIC_TIMEZONE
        ).strftime(DATETIME_12_HOUR_FORMAT)
        return initial

    def form_valid(self, form):
        if "rsvp_limit" in form.changed_data:
            messages.success(
                self.request,
                "People who rsvp'd or are on the waitlist are not notified"
                " when you change the rsvp limit. Be sure to make an announcement!",
            )
        return super().form_valid(form)
