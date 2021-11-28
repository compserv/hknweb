from django.db import models
from hknweb.coursesemester.models import Semester


class RequirementBitByteActivity(models.Model):
    enable = models.BooleanField(default=False)
    candidateSemesterActive = models.OneToOneField(
        Semester, on_delete=models.SET_NULL, null=True
    )
    numberRequired = models.IntegerField(default=0)
    bitByteDateStart = models.DateTimeField(null=True, blank=True)
    bitByteDateEnd = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} - Number Required: {}{}".format(
            self.candidateSemesterActive,
            self.numberRequired,
            "" if self.enable else " [Off]",
        )
