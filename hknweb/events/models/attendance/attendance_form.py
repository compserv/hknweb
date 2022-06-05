from django.db import models

from hknweb.events.models.event import Event


class AttendanceForm(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    secret_word = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __repr__(self):  # pragma: no cover
        event = f"event={str(self.event)}"
        secret_word = f"secret_word={self.secret_word}"
        description = f"description={self.description}"

        attrs = ", ".join((event, secret_word, description))
        return f"AttendanceForm({attrs})"

    def __str__(self):  # pragma: no cover
        return str(repr(self))
