from django.contrib import admin
from django.utils import timezone

from hknweb.utils import get_access_level

from hknweb.models import Profile
from hknweb.events.models import (
    Event,
    Rsvp,
    GoogleCalendarCredentials,
    GCalAccessLevelMapping,
)
from hknweb.events.models.constants import ACCESS_LEVELS
from hknweb.events.utils import SingleThreadWrapper
import hknweb.events.google_calendar_utils as gcal


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
            calendar_id = GCalAccessLevelMapping.get_calendar_id(
                access_level=access_level
            )
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

    provision_calendar.short_description = (
        "Provision the events Google calendar and all personalized GCals"
    )
