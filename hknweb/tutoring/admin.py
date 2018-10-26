from django.contrib import admin

from .models import Course
from .models import Slot
from .models import Tutor

admin.site.register(Course)
admin.site.register(Slot)
admin.site.register(Tutor)
