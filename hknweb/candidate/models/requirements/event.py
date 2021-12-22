from django.db import models
from hknweb.coursesemester.models import Semester

from hknweb.candidate.models.constants import MAX_STRLEN


class RequriementEvent(models.Model):
    enableTitle = models.BooleanField(default=False)
    title = models.CharField(max_length=MAX_STRLEN, default="", blank=True)

    eventType = models.ForeignKey("events.EventType", on_delete=models.CASCADE)
    numberRequired = models.IntegerField(
        default=0,
        help_text="Number of events needed to satisfy this requirement (set to -1 for ALL events of evenType and between the eventsDateStart and eventsDateEnd, if filled)",
    )
    enable = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True
    )
    eventsDateStart = models.DateTimeField(null=True, blank=True)
    eventsDateEnd = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        numReqText = self.numberRequired
        if self.numberRequired < 0 or (self.numberRequired is None):
            numReqText = "All"
        eventTypeText = self.eventType
        if self.enableTitle:
            eventTypeText = "{} ({})".format(self.title, self.eventType)
        return "{} {} Event - Number Required: {}{}".format(
            self.candidateSemesterActive,
            eventTypeText,
            numReqText,
            "" if self.enable else " [Off]",
        )
