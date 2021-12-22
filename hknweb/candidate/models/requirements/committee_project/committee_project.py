from django.db import models
from django.utils import timezone
from hknweb.coursesemester.models import Semester

from hknweb.candidate.models.constants import MAX_STRLEN


class CommitteeProject(models.Model):
    name = models.CharField(max_length=MAX_STRLEN, default="")
    duedate = models.DateTimeField(default=timezone.now)
    instructions = models.CharField(max_length=MAX_STRLEN, default="", blank=True)
    # if visible == False, then admins can see candiate form but it's not displayed on portal
    visible = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return "{} - {}".format(self.name, self.candidateSemesterActive)
