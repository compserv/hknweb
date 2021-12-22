from django.db import models
from django.contrib.auth.models import User

from hknweb.events.models.event import Event


class Rsvp(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name="rsvp'd by")
    event = models.ForeignKey(Event, models.CASCADE)
    confirmed = models.BooleanField(default=False)
    comment = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="rsvp time")

    def __repr__(self):
        return "Rsvp(event={}, user={})".format(self.event, self.user.username)

    def __str__(self):
        return self.event.name

    @classmethod
    def has_not_rsvpd(cls, user, event):
        return cls.objects.filter(user=user, event=event).first() is None
