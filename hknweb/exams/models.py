from django.db import models

class Department(models.Model):
    name = models.CharField(unique=True, max_length=4, null=True) #short form (e.g. 'EE')
    subject = models.CharField(unique=True, max_length=255) #long form (e.g. 'Electrical Engineering')

    def __str__(self):
        return "{}".format(self.subject)

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    release = models.BooleanField()

    def __str__(self):
        return "Instructor(name={}, department={}, release={})".format(self.name, self.department, self.release)

class Course(models.Model):
    #id          = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=255, null=False)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    number 		= models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department, self.number)

class CourseSemester(models.Model):
    #id          = models.IntegerField(primary_key=True)
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester    = models.CharField(max_length=255)
    instructor  = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
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