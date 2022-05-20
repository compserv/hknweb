from django.contrib import admin

from hknweb.models import Profile
from hknweb.events.models import Event, GCalAccessLevelMapping
import hknweb.events.google_calendar_utils as gcal


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    fields = [
        "name",
        "start_time",
        "end_time",
        "location",
        "event_type",
        "description",
        "rsvp_limit",
        "created_by",
        "created_at",
        "access_level",
        "google_calendar_event_id",
        "photographer",
    ]
    # NOTE: created_by should be read only, but I don't know how to set it to default to current user
    readonly_fields = ["created_at"]
    list_display = (
        "name",
        "start_time",
        "location",
        "event_type",
        "created_by",
        "created_at",
        "access_level",
    )
    list_filter = [
        "start_time",
        "created_at",
        "event_type",
        "location",
        "created_by",
        "access_level",
    ]
    search_fields = [
        "name",
        "created_by__username",
        "created_by__first_name",
        "created_by__last_name",
    ]
    ordering = ["-created_at"]
    autocomplete_fields = ["event_type", "created_by"]

    def delete_queryset(self, request, queryset):
        for e in queryset:
            calendar_id = GCalAccessLevelMapping.get_calendar_id(e.access_level)
            gcal.delete_event(e.google_calendar_event_id, calendar_id=calendar_id)

            for r in e.rsvp_set.all():
                profile = Profile.objects.filter(user=request.user).first()
                gcal.delete_event(
                    r.google_calendar_event_id, calendar_id=profile.google_calendar_id
                )

        super().delete_queryset(request, queryset)
