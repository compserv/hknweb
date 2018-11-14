from django.contrib import admin

from .models import Committee
from .models import Officer

admin.site.register(Committee)
admin.site.register(Officer)
