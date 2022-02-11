from django.contrib.auth.models import User
from django.db import models

from hknweb.candidate.models.requirements.committee_project.committee_project import (
    CommitteeProject,
)


class CommitteeProjectDoneEntry(models.Model):
    users = models.ManyToManyField(User, blank=True)
    committeeProject = models.OneToOneField(CommitteeProject, models.CASCADE)
    notes = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Committee Project Done Entries"

    def __str__(self):
        return "Committee Project completed for: {}".format(self.committeeProject)
