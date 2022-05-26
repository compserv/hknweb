from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils import timezone
from django.contrib.auth.models import User

from hknweb.coursesemester.models import Semester


class Room(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name


class TutoringLogistics(models.Model):
    class Meta:
        verbose_name_plural = "TutoringLogistics"

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    one_hour_tutors = models.ManyToManyField(User, blank=True, related_name="one_hour_tutoring")
    two_hour_tutors = models.ManyToManyField(User, blank=True, related_name="two_hour_tutoring")

    def __str__(self) -> str:
        return str(self.semester)


class Slot(models.Model):
    logistics = models.ForeignKey(TutoringLogistics, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    num_tutors = models.IntegerField()
    tutors = models.ManyToManyField(User, blank=True, related_name="tutoring_slots")
    tutor_prefs = models.ManyToManyField(User, blank=True, related_name="tutoring_slotprefs")

    def __str__(self) -> str:
        return f"{self.logistics} {self.room}"

    def _convert_datetime(self) -> timezone.datetime:
        return self.datetime + timezone.timedelta(weeks=(self.offset - self.datetime).days // 7)

    def start_time(self) -> timezone.datetime:
        return self._convert_datetime()

    def end_time(self) -> timezone.datetime:
        return self._convert_datetime() + timezone.timedelta(hours=1)

    def tutor_names(self) -> str:
        tutors = self.tutors \
            .annotate(full_name=Concat("first_name", Value(" "), "last_name")) \
            .values_list("full_name", flat=True)
        return "\n".join(tutors)
