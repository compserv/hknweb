from django.contrib import admin

from .models import Day
from .models import Course
from .models import Slot
from .models import Tutor

admin.site.register(Day)
admin.site.register(Course)
admin.site.register(Slot)
admin.site.register(Tutor)

# Register your models here.
