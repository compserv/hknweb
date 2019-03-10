from django.db import models

class Course(models.Model):
    id          = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=255, null=False)
    department  = models.CharField(max_length=2, choices=(('CS', 'Computer Science'), ('EE', 'Electrical Engineering')), null=False)
    number 		= models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department, self.number)

class CourseSemester(models.Model):
    id          = models.IntegerField(primary_key=True)
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester    = models.CharField(max_length=255)
    instructor  = models.CharField(max_length=255)
    midterm1    = models.FileField(blank=True)
    midterm1_sol = models.FileField(blank=True)
    midterm2    = models.FileField(blank=True)
    midterm2_sol = models.FileField(blank=True)
    midterm3    = models.FileField(blank=True)
    midterm3_sol = models.FileField(blank=True)
    final       = models.FileField(blank=True)
    final_sol   = models.FileField(blank=True)

    def __str__(self):
        return "CourseSemester(course={}, semester={})".format(self.course, self.semester)