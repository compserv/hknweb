from django.db import models

from hknweb.events.models.rsvp import Rsvp
from hknweb.events.models.attendance.attendance_form import AttendanceForm


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
