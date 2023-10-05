from django.contrib import admin

from hknweb.events.admin.attendance import AttendanceFormAdmin, AttendanceResponseAdmin
from hknweb.events.admin.event import EventAdmin
from hknweb.events.admin.event_type import EventTypeAdmin
from hknweb.events.admin.google_calendar import (
    GCalAccessLevelMappingAdmin,
    GoogleCalendarCredentialsAdmin,
)
from hknweb.events.admin.ical_view import ICalViewAdmin
from hknweb.events.admin.rsvp import RsvpAdmin
from hknweb.events.models import EventPhoto

admin.site.register(EventPhoto)
