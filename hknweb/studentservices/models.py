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
    is_title = models.BooleanField(default=False)
    x_0 = models.IntegerField(blank=True, null=True)
    y_0 = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class CourseGuideAdjacencyList(models.Model):
    source = models.ForeignKey(CourseGuideNode, models.CASCADE, related_name="adjacency_list_source")
    targets = models.ManyToManyField(CourseGuideNode, related_name="adjacency_list_target")

    def __str__(self):
        source = str(self.source)
        targets = ", ".join(str(t) for t in self.targets.all())
        return f"{source}: [{targets}]"


class CourseGuideGroup(models.Model):
    nodes = models.ManyToManyField(CourseGuideNode)

    def __str__(self):
        return ", ".join(str(n) for n in self.nodes.all())


class CourseGuideParam(models.Model):
    link_distance = models.IntegerField()
    circle_radius = models.IntegerField()
    force_strength = models.IntegerField()
    marker_width = models.IntegerField()
    marker_height = models.IntegerField()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            "link_distance": self.link_distance,
            "circle_radius": self.circle_radius,
            "force_strength": self.force_strength,
            "marker_width": self.marker_width,
            "marker_height": self.marker_height,
        }
