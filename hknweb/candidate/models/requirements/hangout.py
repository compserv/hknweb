from django.db import models

from hknweb.coursesemester.models import Semester

from hknweb.candidate.constants import EVENT_NAMES


class RequirementHangout(models.Model):
    eventType = models.CharField(
        max_length=255,
        choices=[
            (EVENT_NAMES.HANGOUT, "Officer Hangouts"),
            (EVENT_NAMES.CHALLENGE, "Officer Challenges"),
            (EVENT_NAMES.EITHER, "Either"),
        ],
    )
    numberRequired = models.IntegerField(default=0)
    enable = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True
    )
    hangoutsDateStart = models.DateTimeField(null=True, blank=True)
    hangoutsDateEnd = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} {} - Number Required: {}{}".format(
            self.candidateSemesterActive,
            self.eventType,
            self.numberRequired,
            "" if self.enable else " [Off]",
        )
