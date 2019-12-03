from django.db import models

# Create your models here.
class Course(models.Model):
	course_number = models.CharField(max_length=5, null=True)
	department = models.CharField(max_length=8, null=True)
	name = models.CharField(max_length=255, null=False)
	description = models.TextField()
	prerequisites = models.TextField()
	workload = models.TextField()
	topic_covered = models.TextField()

class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    semester = models.CharField(max_length=12, null=False)

class Instructor(models.Model):
    name = models.CharField(max_length=255, null=False)

class InstructorRating(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
    effectiveness = models.DecimalField(max_digits=2, decimal_places=1)
    worthwhile = models.DecimalField(max_digits=2, decimal_places=1)
    respondent_count = models.PositiveIntegerField()
