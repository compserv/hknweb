from django.contrib import admin

from hknweb.events.models import AttendanceResponse


@admin.register(AttendanceResponse)
class AttendanceResponseAdmin(admin.ModelAdmin):
    fields = ["attendance_form", "rsvp", "feedback"]
    list_display = ["attendance_form", "rsvp", "feedback"]
