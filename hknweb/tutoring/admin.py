from django.contrib import admin

from hknweb.tutoring.models import Room, TutoringLogistics, Slot


@admin.register(TutoringLogistics)
class TutoringLogisticsAdmin(admin.ModelAdmin):
    autocomplete_fields = ("one_hour_tutors", "two_hour_tutors")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tutors",)


admin.site.register(Room)
