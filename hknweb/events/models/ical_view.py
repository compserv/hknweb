import random
import uuid
from datetime import datetime, timedelta

import icalendar
from django.conf import settings
from django.db import models
from django.urls import reverse

from hknweb.events.models import Event
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

        cal.add_component(self.dummy_event())
        return cal

    def dummy_event(self):
        # Google Calendar doesn't let you configure how often to sync iCal feeds
        # like Apple's Calendar app does. They say this can take up to 24 hours.

        # According to https://webapps.stackexchange.com/a/66686, they probably
        # look at how often the iCal feed itself changes and syncs more or less
        # frequently based on that.

        # So we add a dummy event in the far future that's randomized every time
        # the feed is requested in hopes of making Google Calendar sync faster.

        dt = datetime(3000, 1, 1) + timedelta(days=random.randrange(365))

        event = icalendar.Event()
        event.add("uid", "dummy")
        event.add("summary", "Dummy Event")
        event.add(
            "description",
            "Randomized dummy event to make Google Calendar sync faster",
        )
        event.add("dtstart", dt)
        event.add("dtend", dt)
        event.add("dtstamp", dt)
        return event
