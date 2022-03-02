import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import RegexValidator


MAX_STRLEN = 255
MAX_TXTLEN = 10000


class Resume(models.Model):
    name = models.CharField(max_length=MAX_STRLEN, blank=False)
    email = models.CharField(max_length=MAX_STRLEN, blank=False)
    notes = models.TextField(max_length=MAX_TXTLEN, blank=True)
    document = models.FileField(upload_to="resume/", blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    critiques = models.TextField(max_length=MAX_TXTLEN, blank=True)


class ReviewSession(models.Model):
    name = models.CharField(max_length=MAX_STRLEN)
    slug = models.CharField(max_length=MAX_STRLEN)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=MAX_STRLEN)
    description = models.TextField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return "/studentservices/reviewsessions/{}".format(self.id)

    def __repr__(self):
        return "Event(name={}, location={})".format(self.name, self.location)

    def __str__(self):
        return self.name


class DepTour(models.Model):
    """
    Model for a department tour
    """

    class Meta:
        verbose_name = "Department Tour"

    name = models.CharField(max_length=MAX_STRLEN, default="")
    email = models.EmailField(max_length=MAX_STRLEN, default="")
    datetime = models.DateTimeField(
        default=datetime.date.today, verbose_name="Desired Date and Time"
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{10}$",
        message="Enter a valid 10-digit phone number in the format: '9876543210'",
    )
    phone = models.CharField(validators=[phone_regex], max_length=15, default="")
    comments = models.TextField(
        max_length=MAX_TXTLEN,
        blank=True,
        default="",
        verbose_name="Additional comments",
    )
    date_submitted = models.DateTimeField(default=timezone.datetime.now)
    confirmed = models.BooleanField(default=False)
    deprel_comments = models.TextField(max_length=MAX_TXTLEN, blank=True, default="")

    def __str__(self):
        return self.name


class CourseGuideNode(models.Model):
    name = models.CharField(max_length=MAX_STRLEN, blank=False)


class CourseGuideAdjacencyList(models.Model):
    source = models.ForeignKey(CourseGuideNode, models.CASCADE)
    targets = models.ManyToManyField(CourseGuideNode)


class CourseGuideGroups(models.Model):
    nodes = models.ManyToManyField(CourseGuideNode)
