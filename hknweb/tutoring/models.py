from django.db import models

# Create your models here.


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)


class Slot(models.Model):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    DAYS = [MON, TUE, WED, THU, FRI]
    DAY_CHOICES = [
        (MON, 'Monday'),
        (TUE, 'Tuesday'),
        (WED, 'Wednesday'),
        (THU, 'Thursday'),
        (FRI, 'Friday'),
    ]

    CORY = 0
    SODA = 1

    ROOM_CHOICES = [
        (CORY, 'Cory'),
        (SODA, 'Soda'),
    ]

    HOURS = [11, 12, 13, 14, 15, 16]
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


class Tutor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slots = models.ManyToManyField(Slot)
    courses = models.ManyToManyField(Course)
