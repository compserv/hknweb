from django.contrib import admin

from hknweb.events.models import ICalView


@admin.register(ICalView)
class ICalViewAdmin(admin.ModelAdmin):
    fields = ["user", "show_rsvpd", "show_not_rsvpd"]
    list_display = ["id", "user"]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
    ]
