from django.db import models

# Create your models here.
class Course(models.Model):
	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 255, null=False)
	


class Day(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=255, null=False)

class Slot(models.Model):
	id = models.IntegerField(primary_key = True)
	starttime = models.IntegerField(null=False)
	endtime = models.IntegerField(null=False)
	day = models.ForeignKey(Day, on_delete=models.CASCADE)


class Tutor(models.Model):
	id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length=255, null=False)
	slots = models.ManyToManyField(Slot)
	courses = models.ManyToManyField(Course)






