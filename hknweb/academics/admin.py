from django.contrib import admin

from .models.course_surveys import Question, Rating, Survey
from .models.icsr import ICSR
from .models.logistics import Course, Department, Instructor, Semester


admin.site.register(Question)
admin.site.register(Rating)
admin.site.register(Survey)
admin.site.register(ICSR)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Semester)
