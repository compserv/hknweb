from django.contrib import admin
from .models import DepTour

class ToursAdmin(admin.ModelAdmin):

    fields = ['name', 'desired_date', 'desired_time', 'email', 'phone', 'confirmed', 'comments', 'rsec_comments']
    # readonly_fields = ['desired_date']
    list_display = ('name','confirmed', 'email', 'desired_date', 'desired_time', 'date_submitted', 'phone', 'comments', 'rsec_comments')
    # list_filter = ['requester', 'officer', 'request_date']
    # search_fields = ['requester', 'officer', 'name']

admin.site.register(DepTour,ToursAdmin)
