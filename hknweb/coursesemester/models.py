from django.db import models


# Create your models here.
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
        return "{}".format(self.name)  # "Instructor(name={}, department={})".format(


class Course(models.Model):
    name = models.CharField(max_length=255, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    number = models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department.abbreviated_name, self.number)


class Semester(models.Model):
    semester = models.CharField(max_length=10)
    year = models.IntegerField()

    def __str__(self):
        return "{} {}".format(self.semester, self.year)

    # Assuming latest semester is always the current one, otherwise either rename the function to latest semester
    # or change functionality to be smarter.
    @staticmethod
    def get_current_semester():
        latest_year = Semester.objects.order_by("-year").first().year
        latest_year_semesters = Semester.objects.filter(year=latest_year)
        latest_fall = latest_year_semesters.filter(semester="Fall")
        if latest_fall.exists():
            return latest_fall.first()

        # Add summer?
        latest_spring = latest_year_semesters.filter(semester="Spring")
        if latest_spring.exists():
            return latest_spring.first()

        # Should never get here.
        return latest_year_semesters.first()
