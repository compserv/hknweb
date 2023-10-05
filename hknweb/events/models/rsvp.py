from django.contrib.auth.models import User
from django.db import models

import hknweb.events.google_calendar_utils as gcal
from hknweb.events.models.event import Event
from hknweb.models import Profile


class Rsvp(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name="rsvp'd by")
    event = models.ForeignKey(Event, models.CASCADE)
    confirmed = models.BooleanField(default=False)
    comment = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="rsvp time")
    google_calendar_event_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = [["user", "event"]]

    def __repr__(self):
        return "Rsvp(event={}, user={})".format(self.event, self.user.username)

    def __str__(self):
        return self.event.name

    @classmethod
    def has_not_rsvpd(cls, user, event):
        return cls.objects.filter(user=user, event=event).first() is None

    def save(self, *args, **kwargs):
        profile = Profile.objects.filter(user=self.user).first()
        if not profile.google_calendar_id:
            # we no longer provision new personal google calendars
            # instead, we generate a ICalView and a route to view it
            # so they can add it to any calendar app
            return

        if self.google_calendar_event_id is None:
            self.google_calendar_event_id = gcal.create_event(
                self.event.name,
                self.event.location,
                self.event.description,
                self.event.start_time.isoformat(),
                self.event.end_time.isoformat(),
                calendar_id=profile.google_calendar_id,
            )
        else:
            gcal.update_event(
                self.google_calendar_event_id,
                summary=self.event.name,
                location=self.event.location,
                description=self.event.description,
                start=self.event.start_time.isoformat(),
                end=self.event.end_time.isoformat(),
                calendar_id=profile.google_calendar_id,
            )

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.google_calendar_event_id:
            profile = Profile.objects.filter(user=self.user).first()
            gcal.delete_event(
                self.google_calendar_event_id,
                calendar_id=profile.google_calendar_id,
            )

        super().delete(*args, **kwargs)
