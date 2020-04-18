from django.contrib import admin
from .models import Course, Department, Instructor, Exam, Semester, ExamChoice

admin.site.register(Course)
# admin.site.register(CourseSemester)
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Exam)
admin.site.register(Semester)
admin.site.register(ExamChoice)

