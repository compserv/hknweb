from django.db import models

from hknweb.events.models.event import Event
from hknweb.events.models.rsvp import Rsvp


class AttendanceForm(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    secret_word = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __repr__(self):
        event = f"event={str(self.event)}"
        secret_word = f"secret_word={self.secret_word}"
        description = f"description={self.description}"

        attrs = ", ".join((event, secret_word, description))
        return f"AttendanceForm({attrs})"

    def __str__(self):
        return str(repr(self))


class AttendanceResponse(models.Model):
    attendance_form = models.ForeignKey(AttendanceForm, on_delete=models.CASCADE)
    rsvp = models.ForeignKey(Rsvp, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True)

    def __repr__(self):
        return f"AttendanceResponse(attendance_form={str(self.attendance_form)}, rsvp={str(self.rsvp)})"

    def __str__(self):
        return str(repr(self))

    def save(self, *args, **kwargs):
        self.rsvp.confirmed = True
        self.rsvp.save()

        super().save(*args, **kwargs)
