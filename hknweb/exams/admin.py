from django.contrib import admin
from .models import Course, CourseSemester, Department, Instructor, Exam, Semester

admin.site.register(Course)
admin.site.register(CourseSemester)
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Exam)
admin.site.register(Semester)