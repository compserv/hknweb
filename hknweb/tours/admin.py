from django.contrib import admin
from .models import DepTour

class ToursAdmin(admin.ModelAdmin):

    fields = ['name', 'confirmed', 'datetime', 'email', 'phone', \
    	'comments', 'deprel_comments']
    readonly_fields = ('name', 'email', 'phone', 'comments')
    list_display = ('name','confirmed', 'email', 'datetime', \
    	'date_submitted', 'phone', 'comments', 'deprel_comments')

admin.site.register(DepTour,ToursAdmin)
