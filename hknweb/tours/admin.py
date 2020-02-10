from django.contrib import admin
from .models import DepTour

class ToursAdmin(admin.ModelAdmin):

    fields = ['name', 'desired_date', 'email', 'confirm_email', 'phone', 'comments', 'confirmed']
    # readonly_fields = ['desired_date']
    list_display = ('name', 'email', 'phone', 'comments', 'confirmed')
    # list_filter = ['requester', 'officer', 'request_date']
    # search_fields = ['requester', 'officer', 'name']

admin.site.register(DepTour,ToursAdmin)
