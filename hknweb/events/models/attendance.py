from django.db import models

from hknweb.events.models.event import Event


class AttendanceForm(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    secret_word = models.CharField(max_length=255)

    def __repr__(self):
        return f"AttendanceForm(event={str(self.event)}, secret_word={self.secret_word}"

    def __str__(self):
        return str(repr(self))
