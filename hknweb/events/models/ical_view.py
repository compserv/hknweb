import uuid

import icalendar
from django.conf import settings
from django.db import models

from hknweb.events.utils import get_events


class ICalView(models.Model):
    class Meta:
        verbose_name = "iCal view"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    show_rsvpd = models.BooleanField(default=True)
    show_not_rsvpd = models.BooleanField(default=False)

