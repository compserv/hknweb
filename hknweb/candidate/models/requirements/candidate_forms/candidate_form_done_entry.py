from django.contrib.auth.models import User
from django.db import models

from hknweb.candidate.models.requirements.candidate_forms.candidate_form import (
    CandidateForm,
)


class CandidateFormDoneEntry(models.Model):
    users = models.ManyToManyField(User, blank=True)
    form = models.OneToOneField(CandidateForm, models.CASCADE)
    notes = models.TextField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Candidate Form Done Entries"

    def __str__(self):
        return "Forms filled for: {}".format(self.form)
