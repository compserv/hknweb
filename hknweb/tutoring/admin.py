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
    fields = [
        "semester",
        "course",
        "title",
        "fileID",
        "comment",
        "public",
        "upload_date",
    ]
    readonly_fields = ["upload_date"]
    list_display = ("semester", "course", "title", "fileID", "public", "upload_date")
    list_filter = ("semester", "course", "public")
    search_fields = ("title", "course__title", "semester__year", "semester__semester")

    ordering = ("-upload_date",)


admin.site.register(Room)
