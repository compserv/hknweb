from django.db import models

class Department(models.Model):
    abbreviated_name = models.CharField(unique=True, max_length=4, null=True) #short form (e.g. 'EE')
    long_name = models.CharField(max_length=255) #long form (e.g. 'Electrical Engineering')

    def getAbbrName(self):
        return self.abbreviated_name

    def __str__(self):
        return "{} ({})".format(self.long_name, self.abbreviated_name)

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return "{}".format(self.name) #"Instructor(name={}, department={})".format(self.name, self.department)

class Course(models.Model):
    name        = models.CharField(max_length=255, null=False)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    number 		= models.CharField(max_length=10, null=False)

    def __str__(self):
        return "{} {}".format(self.department.getAbbrName(), self.number)

class Semester(models.Model):
     semester = models.CharField(max_length=255)

     def __str__(self):
         return "Test {}".format(self.semester)

"""
class CourseSemester(models.Model):
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester    = models.ForeignKey(Semester, on_delete=models.CASCADE)
    instructor  = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=False)
    release     = models.BooleanField()
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
"""

class ExamChoice(models.Model):
    exam_Choice = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.examChoices)

# department (EE, CS, or EECS), Course (Number), Instructor (Name), Exam Type(Midterm1, Midterm2, Final)
class Exam(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    exam_type = models.ForeignKey(ExamChoice, on_delete=models.CASCADE)
    solution = models.BooleanField(default=False)
    # FIXME - Add file container

