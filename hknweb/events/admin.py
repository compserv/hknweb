from django.contrib import admin
from django.shortcuts import redirect
from django.utils import timezone

from hknweb.utils import get_access_level

from hknweb.models import Profile
from hknweb.events.models import (
    EventType,
    Event,
    Rsvp,
    GoogleCalendarCredentials,
    GCalAccessLevelMapping,
    AttendanceForm,
    AttendanceResponse,
)
from hknweb.events.models.constants import ACCESS_LEVELS
from hknweb.events.utils import SingleThreadWrapper
import hknweb.events.google_calendar_utils as gcal


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ["type"]
    ordering = ["type"]


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
                gcal.delete_event(r.google_calendar_event_id, calendar_id=profile.google_calendar_id)

        super().delete_queryset(request, queryset)


@admin.register(Rsvp)
class RsvpAdmin(admin.ModelAdmin):

    fields = ["event", "user", "confirmed", "comment", "created_at"]
    readonly_fields = ["created_at"]
    list_display = ("event", "user", "full_name", "confirmed", "created_at")
    list_filter = ["confirmed", "created_at", "event"]
    search_fields = [
        "event__name",
        "user__username",
        "user__first_name",
        "user__last_name",
    ]
    ordering = ["-created_at"]
    autocomplete_fields = ["event", "user"]

    actions = ["mark_confirmed", "mark_unconfirmed", "cute_animal"]

    def full_name(self, rsvp):
        return rsvp.user.get_full_name()

    def mark_confirmed(self, request, queryset):
        queryset.update(confirmed=True)

    mark_confirmed.short_description = "Mark selected as confirmed"

    def mark_unconfirmed(self, request, queryset):
        queryset.update(confirmed=False)

    mark_unconfirmed.short_description = "Mark selected as unconfirmed"

    def cute_animal(self, request, queryset):
        return redirect("https://www.google.com/search?q=cute+cats&tbm=isch")

    cute_animal.short_description = "I wanna see a cute animal"

    def delete_queryset(self, request, queryset):
        for r in queryset:
            profile = Profile.objects.filter(user=r.user).first()
            gcal.delete_event(
                r.google_calendar_event_id,
                calendar_id=profile.google_calendar_id,
            )

        super().delete_queryset(request, queryset)


@admin.register(GoogleCalendarCredentials)
class GoogleCalendarCredentialsAdmin(admin.ModelAdmin):
    fields = ["file"]

    actions = ["provision_calendar"]

    def provision_calendar(self, request, queryset):
        thread = SingleThreadWrapper(lambda: self._provision_calendar(request))
        thread.start()

    @staticmethod
    def _provision_calendar(request):
        # Clear existing calendars
        for access_level, _ in ACCESS_LEVELS:
            calendar_id = GCalAccessLevelMapping.get_calendar_id(access_level=access_level)
            gcal.clear_calendar(calendar_id=calendar_id)

        for u in Profile.objects.all():
            if not u.google_calendar_id:
                continue

            gcal.clear_calendar(calendar_id=u.google_calendar_id)

        upcoming_events = Event.objects.filter(start_time__gte=timezone.now()).filter(
            access_level__gte=get_access_level(request.user)
        )

        for e in upcoming_events:
            e.google_calendar_event_id = None
            e.save()

            for r in Rsvp.objects.filter(event=e):
                r.google_calendar_event_id = None
                r.save()

    provision_calendar.short_description = "Provision the events Google calendar and all personalized GCals"


@admin.register(GCalAccessLevelMapping)
class GCalAccessLevelMappingAdmin(admin.ModelAdmin):
    fields = ["access_level", "calendar_id"]
    list_display = ["access_level", "calendar_id"]


@admin.register(AttendanceForm)
class AttendanceFormAdmin(admin.ModelAdmin):
    fields = ["event", "secret_word", "description"]
    list_display = ["event", "secret_word", "description"]


@admin.register(AttendanceResponse)
class AttendanceResponseAdmin(admin.ModelAdmin):
    fields = ["attendance_form", "rsvp", "feedback"]
    list_display = ["attendance_form", "rsvp", "feedback"]
