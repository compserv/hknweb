from django.contrib import admin

from hknweb.events.models import GCalAccessLevelMapping


@admin.register(GCalAccessLevelMapping)
class GCalAccessLevelMappingAdmin(admin.ModelAdmin):
    fields = ["access_level", "calendar_id"]
    list_display = ["access_level", "calendar_id"]
