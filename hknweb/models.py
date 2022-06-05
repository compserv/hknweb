import re
from typing import Dict

from django.db import models
from django.db.models import QuerySet
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils import timezone

from hknweb.coursesemester.models import Semester, Course

from hknweb.utils import view_url


MAX_STRLEN = 85  # default max length for char fields
MAX_TXTLEN = 2000  # default max length for text fields

# Pretty sure this is terrible coding practice but hey it works
# Sorry Daddy DeNero
User.__str__ = lambda self: "{} ({} {})".format(
    self.username, self.first_name, self.last_name
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    date_of_birth = models.DateField(null=True, blank=True)
    picture = models.CharField(max_length=500, blank=True)
    private = models.BooleanField(default=True, verbose_name="Private profile?")
    phone_regex = RegexValidator(
        regex=r"^([^\d]*\d){10}$", message="Phone number must be ten digits."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
    resume = models.FileField(blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    candidate_semester = models.ForeignKey(
        Semester, on_delete=models.SET_NULL, null=True, blank=True
    )
    google_calendar_id = models.CharField(max_length=255, null=True, blank=True)
    preferred_courses = models.ManyToManyField(Course, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def clean(self):
        if self.phone_number:
            self.phone_number = re.sub("[^0-9]", "", self.phone_number)
            self.phone_number = (
                "("
                + self.phone_number[0:3]
                + ") "
                + self.phone_number[3:6]
                + "-"
                + self.phone_number[6:]
            )

    def picture_display_url(self) -> str:  # pragma: no cover
        return view_url(self.picture)

    def __str__(self):  # pragma: no cover
        return "Profile of: " + str(self.user)

    def preferred_courses_str(self) -> str:  # pragma: no cover
        if self.preferred_courses.exists():
            return ", ".join(map(str, self.preferred_courses.all()))
        return "No preferred courses, but any lower division courses (61A, 61B, 70, 16A, 16B) welcome!"


class Announcement(models.Model):
    """
    Model for an announcement. Created by VP or some other superuser.
    Displayed on the candidate portal. The title will be displayed in bold,
    and the text will follow that in normal font, with a space in between.
    """

    title = models.CharField(max_length=MAX_STRLEN, default="")
    text = models.TextField(max_length=MAX_TXTLEN, blank=True, default="")
    # if visible == False, then admins can see announcement but it's not displayed on portal
    visible = models.BooleanField(default=False)
    release_date = models.DateTimeField(default=timezone.now)

    def __str__(self):  # pragma: no cover
        return self.title if self.title != "" else self.text


class CandidateProvisioningPassword(models.Model):
    password = models.CharField(max_length=30)


class Committee(models.Model):
    name = models.CharField(max_length=30)
    is_exec = models.BooleanField(default=False)

    def __str__(self):  # pragma: no cover
        return self.name


class Election(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        return f"{self.semester} Election"


class Committeeship(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    officers = models.ManyToManyField(User, related_name="officerships", blank=True)
    assistant_officers = models.ManyToManyField(
        User, related_name="ao_ships", blank=True
    )
    committee_members = models.ManyToManyField(
        User, related_name="cmemberships", blank=True
    )

    def __str__(self):  # pragma: no cover
        return f"{self.committee}, {self.election.semester}"

    def people(self) -> Dict[str, "QuerySet[User]"]:
        if self.committee.is_exec:
            return {self.committee.name: self.officers.all()}

        return {
            "Officer": self.officers.all(),
            "Assistant Officer": self.assistant_officers.all(),
            "Committee Member": self.committee_members.all(),
        }
