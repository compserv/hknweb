import uuid

import icalendar
from django.conf import settings
from django.db import models
from django.urls import reverse

from hknweb.events.utils import get_events


class ICalView(models.Model):
    class Meta:
        verbose_name = "iCal view"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show_rsvpd = models.BooleanField(default=True)
    show_not_rsvpd = models.BooleanField(default=False)

    @property
    def url(self):
        return reverse("events:ical", args=[self.id])

    def to_ical_obj(self):
        cal = icalendar.Calendar()
        cal.add("prodid", "-//Eta Kappa Nu, Mu Chapter//Calendar//EN")
        cal.add("version", "2.0")
        cal.add("summary", f"HKN Personal Calendar for {self.user}")

        events = get_events(self.user, self.show_rsvpd, self.show_not_rsvpd)
        for event in events:
            cal.add_component(event.to_ical_obj())

        return cal
