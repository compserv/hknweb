from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)

    def __repr__(self):
        return "Course(name={})".format(self.name)

    def __str__(self):
        return str(self.name)

class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    user  = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    adjacent_pref = models.IntegerField(default=0)
    def get_course_preferences(self):
        return CoursePreference.objects.filter(tutor=self)
    def get_slot_preferences(self):
        return SlotPreference.objects.filter(tutor=self)
    def __repr__(self):
        return "Tutor(name={})".format(self.name)
    def __str__(self):
        return str(self.name)

class TimeSlot(models.Model):
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
    HOUR_CHOICES = [
        (11, '11am'),
        (12, '12pm'),
        (13, '1pm'),
        (14, '2pm'),
        (15, '3pm'),
        (16, '4pm'),
    ]
    hour = models.IntegerField(choices=HOUR_CHOICES)
    day = models.IntegerField(choices=DAY_CHOICES)
    timeslot_id = models.IntegerField(default=0)

    @staticmethod
    def time(hour):
        if hour < 12:
            return '{}am'.format(hour)
        else:
            return '{}pm'.format(hour)

    def get_day(self):
        for day in self.DAY_CHOICES:
            if day[0] == self.day:
                return day[1]

    def start_time(self):
        return self.time(self.hour)

    def end_time(self):
        return self.time(self.hour + 1)

    def __repr__(self):
        return "TimeSlot(day={}, start={}, end={})".format(self.get_day(), self.start_time(), self.end_time())
    def __str__(self):
        return str(self.get_day()) + ' ' + str(self.start_time()) + ' to ' + str(self.end_time())

class Slot(models.Model):
    CORY = 0
    SODA = 1
    ROOM_CHOICES = [
        (CORY, 'Cory'),
        (SODA, 'Soda'),
    ]
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True)
    room = models.IntegerField(choices=ROOM_CHOICES)
    slot_id = models.IntegerField(default=0)
    tutors = models.ManyToManyField(Tutor)

    def __repr__(self):
        tutor_string = ""
        for tutor in self.tutors.all():
            tutor_string += str(tutor) + ", "
        return "Slot(room={}, day = {}, start = {}, end = {}, tutors = {})".format(self.room, self.timeslot.get_day(), self.timeslot.start_time(), self.timeslot.end_time(), tutor_string)

    def __str__(self):
        return str(self.room) + ' ' + str(self.timeslot.get_day()) + ' ' + str(self.timeslot.start_time()) + ' ' + str(self.timeslot.end_time())

class CoursePreference(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

class TimeSlotPreference(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    time_preference = models.IntegerField(default=1)
    office_preference = models.IntegerField(default=2)





