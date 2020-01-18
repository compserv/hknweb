from django.db import models

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
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course)

    def __repr__(self):
        return "Tutor(name={})".format(self.name)

    def __str__(self):
        return str(self.name)

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

    def __repr__(self):
        return "Slot(room={}, day = {}, start = {}, end = {})".format(self.room, self.day, self.start_time(), self.end_time())

    def __str__(self):
        return str(self.room) + ' ' + str(self.day) + ' ' + str(self.start_time()) + ' ' + str(self.end_time())



