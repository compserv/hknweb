from django.db import models

# Create your models here.
class Department(models.Model):
    abbreviated_name = models.CharField(unique=True, max_length=8, null=True) #short form (e.g. 'EE')
    long_name = models.CharField(max_length=255) #long form (e.g. 'Electrical Engineering')

    def __str__(self):
        return "{} ({})".format(self.long_name, self.abbreviated_name)

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "{}".format(self.name) #"Instructor(name={}, department={})".format(

class Course(models.Model):
    name        = models.CharField(max_length=255, null=False)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    number 		= models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department.abbreviated_name, self.number)

class Semester(models.Model):
    semester   = models.CharField(max_length=10)
    year = models.IntegerField()

    def __str__(self):
         return "{} {}".format(self.semester, self.year)


