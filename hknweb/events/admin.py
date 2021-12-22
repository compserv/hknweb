from django.contrib import admin
from django.shortcuts import redirect
from .models import EventType, Event, Rsvp


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    search_fields = ["type"]
    ordering = ["type"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    fields = [
        "name",
        "slug",
        "start_time",
        "end_time",
        "location",
        "event_type",
        "description",
        "rsvp_limit",
        "created_by",
        "created_at",
        "access_level",
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
