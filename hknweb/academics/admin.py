from django.contrib import admin

from hknweb.academics.models import (
    Question,
    Rating,
    Survey,
    ICSR,
    Course,
    Department,
    Instructor,
    Semester,
)


admin.site.register(Question)
admin.site.register(Rating)
admin.site.register(Survey)
admin.site.register(ICSR)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Instructor)
admin.site.register(Semester)
