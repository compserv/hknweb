from django.db import models
from django.utils import timezone
from hknweb.coursesemester.models import Semester

from hknweb.candidate.models.constants import MAX_STRLEN


class CandidateForm(models.Model):
    name = models.CharField(max_length=MAX_STRLEN, default="")
    duedate = models.DateTimeField(default=timezone.now)
    link = models.CharField(max_length=MAX_STRLEN, default="")
    # if visible == False, then admins can see candiate form but it's not displayed on portal
    visible = models.BooleanField(default=False)
    candidateSemesterActive = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return "{} - {}".format(self.name, self.candidateSemesterActive)
