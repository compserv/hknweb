from django.db import models
from hknweb.coursesemester.models import Semester


class RequirementMandatory(models.Model):
    enable = models.BooleanField(default=False)
    events = models.ManyToManyField("events.Event")
    candidateSemesterActive = models.OneToOneField(
        Semester, on_delete=models.SET_NULL, null=True
    )
    eventsDateStart = models.DateTimeField(null=True, blank=True)
    eventsDateEnd = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} Mandatory - {} to {}{}".format(
            self.candidateSemesterActive,
            self.eventsDateStart,
            self.eventsDateEnd,
            "" if self.enable else " [Off]",
        )
