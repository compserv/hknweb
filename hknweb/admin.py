from django.contrib import admin

from .models import Committee
from .models import Officer
from .models import Profile

admin.site.register(Profile)
admin.site.register(Committee)
admin.site.register(Officer)
