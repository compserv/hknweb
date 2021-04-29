from django.contrib import admin
from .models import Course, Department, Instructor, Semester

admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Semester)
