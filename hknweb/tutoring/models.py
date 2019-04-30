from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import DO_NOTHING, CASCADE

from hknweb.alumni.models import max_strlen


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)


class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course)
    adjacency = models.IntegerField()
    user = models.OneToOneField(User, on_delete=CASCADE, related_name="tutor")
    # course_preferences = models.ManyToManyField()


class Slot(models.Model):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    DAY_CHOICES = [
        (MON, 'Mon'),
        (TUE, 'Tue'),
        (WED, 'Wed'),
        (THU, 'Thu'),
        (FRI, 'Fri'),
    ]

    CORY = 0
    SODA = 1
    ROOM_CHOICES = [
        (CORY, 'Cory'),
        (SODA, 'Soda'),
    ]

    HOUR_CHOICES = [
        (11, '11am'),
        (12, '12pm'),
        (13, '1pm'),
        (14, '2pm'),
        (15, '3pm'),
        (16, '4pm'),
    ]

    id = models.AutoField(primary_key=True)
    hour = models.IntegerField(choices=HOUR_CHOICES)
    day = models.IntegerField(choices=DAY_CHOICES)
    room = models.IntegerField(choices=ROOM_CHOICES)
    tutors = models.ManyToManyField(Tutor)

    @staticmethod
    def time(hour):
        if hour < 12:
            return '{}am'.format(hour)
        else:
            return '{}pm'.format(hour)

    def start_time(self):
        return self.time(self.hour)

    def end_time(self):
        return self.time(self.hour + 1)

    def adjacent_to(self, other_slot):
        return other_slot.day == self.day and abs((other_slot.hour - self.hour)) == 1


class CoursePreference(models.Model):
    current = 1
    completed = 2
    preferred = 3
    COURSE_PERFS = [
        (current, 'Current'),
        (completed, 'Completed'),
        (preferred, 'Preferred')
    ]
    id = models.AutoField(primary_key=True)
    courses = models.ForeignKey(Course, on_delete=CASCADE)
    level = models.IntegerField(choices=COURSE_PERFS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tutor = models.OneToOneField(Tutor, on_delete=CASCADE, related_name="coursepreference")


class Availability(models.Model):
    preferred = 1
    available = 2
    unavailable = 3

    PREFERENCES_CHOICES = [
        (preferred, 'Preferred'),
        (available, 'Available'),
        (unavailable, 'Not Available')
    ]
    id = models.AutoField(primary_key=True)
    tutor = models.OneToOneField(Tutor, on_delete=CASCADE, related_name="availabilities")
    slot = models.ManyToManyField(Slot)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    preference_level = models.IntegerField(choices=PREFERENCES_CHOICES)
    room_strength = models.IntegerField()
    semester = models.CharField(max_length=max_strlen, blank=True, default='')

    @property
    def preferred_room(self):
        return self.slot.room

    @property
    def hour(self):
        return self.slot.hour

    @property
    def wday(self):
        return self.slot.day


class Properties(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.CharField(max_length=max_strlen, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tutoring_enabled = models.BooleanField()
    tutoring_message = models.CharField(max_length=max_strlen, blank=True, default='')
    coursesurveys_active = models.BooleanField()

    @property
    def tutoring_start(self):
        return Slot.HOUR_CHOICES[0]

    @property
    def tutoring_end(self):
        return Slot.HOUR_CHOICES[-1]
