from django.conf import settings
from django.db import models
from hknweb.coursesemester.models import Semester


class RequirementHangout(models.Model):
    eventType = models.CharField(
        max_length=255,
        choices=[
            (settings.HANGOUT_ATTRIBUTE_NAME, "Officer Hangouts"),
            (settings.CHALLENGE_ATTRIBUTE_NAME, "Officer Challenges"),
            (settings.EITHER_ATTRIBUTE_NAME, "Either"),
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
