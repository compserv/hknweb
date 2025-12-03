from django.contrib import admin

from hknweb.tutoring.models import Room, TutoringLogistics, Slot, CribSheet


@admin.register(TutoringLogistics)
class TutoringLogisticsAdmin(admin.ModelAdmin):
    autocomplete_fields = ("one_hour_tutors", "two_hour_tutors")


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tutors",)


@admin.register(CribSheet)
class CribSheetsAdmin(admin.ModelAdmin):
    fields = ["semester", "course", "pdf", "comment"]
    list_display = ["semester", "course", "pdf", "comment", "update_date"]
    list_display_links = ["pdf"]
    list_filter = ["update_date"]
    search_fields = ["course__title"]


admin.site.register(Room)
