from django.contrib import admin
from django.shortcuts import redirect

from hknweb.models import Profile
from hknweb.events.models import Rsvp
import hknweb.events.google_calendar_utils as gcal


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
