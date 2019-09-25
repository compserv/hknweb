from django.contrib import admin
from django.shortcuts import redirect
from .models import EventType, Event, Rsvp

class EventAdmin(admin.ModelAdmin):

    fields = ['name', 'slug', 'start_time', 'end_time', 'location', 'event_type', 'description', 'rsvp_limit', 'rsvps', 'created_by', 'created_at']
    # NOTE: created_by should be read only, but I don't know how to set it to default to current user
    readonly_fields = ['created_at']
    list_display = ('name', 'start_time', 'location', 'event_type', 'rsvps', 'created_by', 'created_at')
    list_filter = ['start_time', 'created_at', 'event_type', 'location', 'created_by']
    search_fields = ['name', 'created_by__username', 'created_by__first_name', 'created_by__last_name']


class RsvpAdmin(admin.ModelAdmin):

    fields = ['event', 'user', 'confirmed', 'comment', 'created_at']
    readonly_fields = ['created_at']
    list_display = ('event', 'user', 'full_name', 'confirmed', 'created_at')
    list_filter = ['confirmed', 'created_at', 'event']
    search_fields = ['event__name', 'user__username', 'user__first_name', 'user__last_name']

    actions = ["mark_confirmed", "mark_unconfirmed", "cute_animal"]

    def full_name(self, rsvp):
        return rsvp.user.get_full_name()

    def mark_confirmed(self, request, queryset):
        queryset.update(confirmed=True)

    def mark_unconfirmed(self, request, queryset):
        queryset.update(confirmed=False)

    def cute_animal(self, request, queryset):
        return redirect("http://stackoverflow.com/") # yes cute animals I swear

    mark_confirmed.short_description = "Mark selected as confirmed"
    mark_unconfirmed.short_description = "Mark selected as unconfirmed"
    cute_animal.short_description = "I wanna see a cute animal"

admin.site.register(EventType)
admin.site.register(Event, EventAdmin)
admin.site.register(Rsvp, RsvpAdmin)
