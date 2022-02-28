from django.db import models

from hknweb.academics.models import Department, Semester


class Course(models.Model):
    name = models.CharField(max_length=255, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    number = models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department.abbreviated_name, self.number)


class CourseSemester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    release = models.BooleanField()
    midterm1 = models.FileField(blank=True)
    midterm1_sol = models.FileField(blank=True)
    midterm2 = models.FileField(blank=True)
    midterm2_sol = models.FileField(blank=True)
    midterm3 = models.FileField(blank=True)
    midterm3_sol = models.FileField(blank=True)
    final = models.FileField(blank=True)
    final_sol = models.FileField(blank=True)

    def __str__(self):
        return "CourseSemester(course={}, semester={})".format(
            self.course, self.semester
        )
