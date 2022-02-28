from django.db import models
from django.contrib.auth.models import User

from markdownx.models import MarkdownxField

from hknweb.utils import get_semester
import hknweb.events.google_calendar_utils as gcal

from hknweb.events.models.event_type import EventType


class Event(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    event_type = models.ForeignKey(EventType, models.CASCADE)
    description = MarkdownxField()
    rsvp_limit = models.PositiveIntegerField(null=True, blank=True)
    access_level = models.IntegerField(
        choices=[
            (0, "internal"),
            (1, "candidate"),
            (2, "external"),
        ],
        default=0,
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    google_calendar_event_id = models.CharField(max_length=255, null=True, blank=True)

    @property
    def semester(self):
        """A string representation of the candidate semester of this event.
        Assumes that there are only spring and fall semesters, separated at 07/01.
        Example: "Spring 2020" """
        return get_semester(self.start_time)

    def get_absolute_url(self):
        return "/events/{}".format(self.id)

    def __repr__(self):
        return "Event(name={}, location={})".format(self.name, self.location)

    def __str__(self):
        return "{} - {} to {}".format(self.name, self.start_time, self.end_time)

    def admitted_set(self):
        return self.rsvp_set.order_by("created_at")[: self.rsvp_limit]

    def waitlist_set(self):
        if not self.rsvp_limit:
            return self.rsvp_set.none()
        return self.rsvp_set.order_by("created_at")[self.rsvp_limit :]

    def on_waitlist(self, user):
        if not self.rsvp_limit:
            return False
        return (
            list(
                self.rsvp_set.order_by("created_at").values_list("user", flat=True)
            ).index(user.id)
            >= self.rsvp_limit
        )

    def newly_off_waitlist_rsvps(self, old_admitted):
        """old_admitted must be a set, not a QuerySet. QuerySets are mutable views into the database."""
        new_admitted = set(self.admitted_set())
        return new_admitted - old_admitted

    def save(self, *args, **kwargs):
        if self.google_calendar_event_id is None:
            self.google_calendar_event_id = gcal.create_event(
                self.name,
                self.location,
                self.description,
                self.start_time.isoformat(),
                self.end_time.isoformat(),
            )
        else:
            gcal.update_event(
                self.google_calendar_event_id,
                summary=self.name,
                location=self.location,
                description=self.description,
                start=self.start_time.isoformat(),
                end=self.end_time.isoformat(),
            )

        super().save(*args, **kwargs)
