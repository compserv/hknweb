from django.contrib import admin
from .models import DepTour

class ToursAdmin(admin.ModelAdmin):

    fields = ['name', 'desired_date', 'email', 'phone', 'confirmed', 'comments']
    # readonly_fields = ['desired_date']
    list_display = ('name','confirmed', 'email', 'desired_date', 'phone', 'comments')
    # list_filter = ['requester', 'officer', 'request_date']
    # search_fields = ['requester', 'officer', 'name']

admin.site.register(DepTour,ToursAdmin)
