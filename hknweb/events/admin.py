from django.contrib import admin
from .models import EventType, Event, Rsvp

admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(Rsvp)
