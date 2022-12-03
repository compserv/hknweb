from django.contrib import admin

from hknweb.events.models import AttendanceForm


@admin.register(AttendanceForm)
class AttendanceFormAdmin(admin.ModelAdmin):
    fields = ["event", "secret_word", "description"]
    list_display = ["event", "secret_word", "description"]
