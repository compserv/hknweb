from django.contrib import admin

from hknweb.events.models import EventType


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ["type"]
    ordering = ["type"]
