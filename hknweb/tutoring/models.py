from operator import mod
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TutorCourse(models.Model):
    course = models.ForeignKey("coursesemester.Course", on_delete=models.CASCADE)
    cory_preference = models.IntegerField(default=0, null=True)
    soda_preference = models.IntegerField(default=1, null=True)

    def __repr__(self):
        return "Course(name={})".format(self.name)

    def __str__(self):
        return str(self.course)


class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    adjacent_pref = models.IntegerField(default=0)
    num_assignments = models.IntegerField(default=2)

    def get_course_preferences(self):
        return CoursePreference.objects.filter(tutor=self).order_by("course__id")

    def get_timeslot_preferences(self):
        return TimeSlotPreference.objects.filter(tutor=self).order_by("timeslot__hour", "timeslot__day")

    def get_room_preferences(self):
        return RoomPreference.objects.filter(tutor=self).order_by("timeslot__hour", "timeslot__day", "room__id")

    def get_preferred_courses(self):
        preferences = self.get_course_preferences()
        courses = []
        for pref in preferences:
            if pref.preference == 2:
                courses.append(pref.course)
        return courses

    def __repr__(self):
        return "Tutor(name={})".format(self.name)

    def __str__(self):
        return str(self.name)


# Hour and day choices changed because of virtual semester, remember to change back when in person
class TimeSlot(models.Model):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    DAY_CHOICES = [
        (MON, "Mon"),
        (TUE, "Tue"),
        (WED, "Wed"),
        (THU, "Thu"),
        (FRI, "Fri"),
    ]
    HOUR_CHOICES = [
        (13, "1pm"),
        (14, "2pm"),
        (15, "3pm"),
        (16, "4pm"),
        (21, "9pm"),
    ]
    hour = models.IntegerField(choices=HOUR_CHOICES)
    day = models.IntegerField(choices=DAY_CHOICES)
    timeslot_id = models.IntegerField(default=0)

    @staticmethod
    def time(hour):
        if hour == 0:
            return "12am"
        elif hour < 12:
            return "{}am".format(hour)
        elif hour == 12:
            return "12pm"
        else:
            return "{}pm".format(hour - 12)

    DAYS_OF_WEEK = ["Sun", "Mon", "Tues", "Wed", "Thus", "Fri", "Sat"]

    def get_day(self):
        return self.DAYS_OF_WEEK[self.day]

    def start_time(self):
        return self.time(self.hour)

    def end_time(self):
        return self.time(self.hour + 1)

    def __repr__(self):
        return "TimeSlot(day={}, start={}, end={})".format(
            self.get_day(), self.start_time(), self.end_time()
        )

    def __str__(self):
        return (
            str(self.get_day())
            + " "
            + str(self.start_time())
            + " to "
            + str(self.end_time())
        )


class Room(models.Model):
    DEFAULT_ROOM_CHOICES = [
        (0, "Hybrid/Cory", "290"),
        (1, "Hybrid/Soda", "345"),
        (2, "Online", ""),
    ]
    building = models.CharField(max_length=255)
    room_num = models.CharField(max_length=255, blank=True)

    def get_num_building(self):
        to_display = self.building
        if self.room_num:
            to_display += " %s" % (self.room_num,)
        return to_display

    def __str__(self):
        return self.get_num_building()


class Slot(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    slot_id = models.IntegerField(default=0)
    tutors = models.ManyToManyField(Tutor)

    def get_office(self):
        return self.room.building
        # for room in self.ROOM_CHOICES:
        #     if room[0] == self.room:
        #         return room[1]

    def get_previous_hour_slot(self, hours_back=1):
        # Returns None if no slot exist
        return Slot.objects.filter(
            timeslot__day=self.timeslot.day,
            room=self.room.id,
            timeslot__hour=(self.timeslot.hour - hours_back),
        ).first()

    def get_after_hour_slot(self, hours_forward=1):
        # Returns None if no slot exist
        return Slot.objects.filter(
            timeslot__day=self.timeslot.day,
            room=self.room.id,
            timeslot__hour=(self.timeslot.hour + hours_forward),
        ).first()

    def __repr__(self):
        tutor_string = ""
        for tutor in self.tutors.all():
            tutor_string += str(tutor) + ", "
        return "Slot(room={}, day = {}, start = {}, end = {}, tutors = {})".format(
            self.room,
            self.timeslot.get_day(),
            self.timeslot.start_time(),
            self.timeslot.end_time(),
            tutor_string,
        )

    def __str__(self):
        return (
            str(self.room)
            + " "
            + str(self.timeslot.get_day())
            + " "
            + str(self.timeslot.start_time())
            + " "
            + str(self.timeslot.end_time())
        )


class CoursePreference(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    course = models.ForeignKey(TutorCourse, on_delete=models.CASCADE)
    preference = models.IntegerField(default=-1)


class TimeSlotPreference(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    preference = models.IntegerField(default=0)


class RoomPreference(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    preference = models.IntegerField(default=0)
