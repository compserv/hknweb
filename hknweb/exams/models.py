from django.db import models


class Department(models.Model):
    abbreviated_name = models.CharField(
        unique=True, max_length=8, null=True
    )  # short form (e.g. 'EE')
    long_name = models.CharField(
        max_length=255
    )  # long form (e.g. 'Electrical Engineering')

    def __str__(self):
        return "{} ({})".format(self.long_name, self.abbreviated_name)


class Instructor(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "{}".format(
            self.name
        )  # "Instructor(name={}, department={})".format(self.name, self.department)


class Course(models.Model):
    name = models.CharField(max_length=255, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    number = models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department.abbreviated_name, self.number)


class Semester(models.Model):
    semester = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.semester)


class CourseSemester(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
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
