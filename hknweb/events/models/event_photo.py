from django.db import models

from hknweb.events.models import Event

from hknweb.utils import view_url


class EventPhoto(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    photo = models.CharField(max_length=100)

    def __str__(self):
        return f"Photo(event={self.event.name}, photo={self.photo})"

    def photo_display_url(self):
        return view_url(self.photo)
