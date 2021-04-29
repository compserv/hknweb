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

