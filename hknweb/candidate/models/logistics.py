from django.db import models
from django.contrib.auth.models import User

from hknweb.events.models import EventType
from hknweb.coursesemester.models import Semester
from hknweb.candidate.models.constants import MAX_STRLEN, MAX_TXTLEN


class BaseReq(models.Model):
    title = models.CharField(max_length=MAX_STRLEN)


class EventReq(BaseReq):
    event_types = models.ManyToManyField(EventType)
    n = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.title} ({self.n})"


class ExternalReq(BaseReq):
    completed = models.ManyToManyField(User, blank=True)


class MiscReq(ExternalReq):
    description = models.TextField(max_length=MAX_TXTLEN, blank=True, default="")

    def __str__(self):
        return f"{self.title}: {self.description}"


class FormReq(ExternalReq):
    link = models.CharField(max_length=MAX_STRLEN)

    def __str__(self):
        return f"{self.title}: {self.link}"


class Logistics(models.Model):
    class Meta:
        verbose_name_plural = "Logistics"


    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()

    event_reqs = models.ManyToManyField(EventReq, blank=True)

    min_challenges = models.PositiveSmallIntegerField()
    min_hangouts = models.PositiveSmallIntegerField()
    num_interactivities = models.PositiveSmallIntegerField()

    num_bitbyte = models.PositiveSmallIntegerField()

    misc_reqs = models.ManyToManyField(MiscReq, blank=True)
    form_reqs = models.ManyToManyField(FormReq, blank=True)
