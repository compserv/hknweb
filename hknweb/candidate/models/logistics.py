from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from hknweb.events.models import EventType, Rsvp
from hknweb.coursesemester.models import Semester

from hknweb.candidate.models import OffChallenge, BitByteActivity
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

    def populate(self, user: User):
        date_start = timezone.make_aware(datetime.combine(self.date_start, datetime.min.time()))
        date_end = timezone.make_aware(datetime.combine(self.date_end, datetime.min.time()))

        rsvps = Rsvp.objects \
            .filter(user=user, event__start_time__range=[date_start, date_end])

        self.event_req_objs = self.event_reqs.all()
        for event_req in self.event_req_objs:
            event_req_rsvps = rsvps.filter(event__event_type__in=event_req.event_types.all())
            event_req.confirmed = [r.event for r in event_req_rsvps.filter(confirmed=True)]
            event_req.unconfirmed = [r.event for r in event_req_rsvps.filter(confirmed=False)]
            event_req.n_finished = len(event_req.confirmed)
        self.event_reqs_finished = all(e.n_finished >= e.n for e in self.event_req_objs)

        self.forms_confirmed = self.form_reqs.filter(completed__in=[user])
        self.forms_unconfirmed = self.form_reqs.exclude(completed__in=[user])
        self.misc_confirmed = self.misc_reqs.filter(completed__in=[user])
        self.misc_unconfirmed = self.misc_reqs.exclude(completed__in=[user])

        self.challenges = OffChallenge.objects \
            .filter(requester=user, request_date__range=[date_start, date_end])
        self.n_challenges_confirmed = sum(c.confirmed for c in self.challenges)
        self.n_challenges_rejected = sum(c.rejected for c in self.challenges)
        self.n_challenges_pending = \
            self.challenges.count() - self.n_challenges_confirmed - self.n_challenges_rejected

        hangouts = rsvps.filter(event__event_type__type="Hangout")
        self.hangouts_confirmed = [r.event for r in hangouts.filter(confirmed=True)]
        self.hangouts_unconfirmed = [r.event for r in hangouts.filter(confirmed=False)]

        self.n_interactivities = len(self.hangouts_confirmed) + self.n_challenges_confirmed

        self.bitbytes = BitByteActivity.objects \
            .filter(
                participants__exact=user,
                request_date__range=[date_start, date_end],
            ) \
            .order_by("-request_date")
        self.n_bitbyte = self.bitbytes.filter(confirmed=True).count()
