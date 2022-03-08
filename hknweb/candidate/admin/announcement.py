from django.contrib import admin

from hknweb.candidate.models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):

    # NOTE: release_date is not readonly because we can reuse announcements from past semesters
    # The VP can just change the date and release it again
    fields = ["title", "text", "visible", "release_date"]
    list_display = ("title", "visible", "release_date")
    list_filter = ["visible", "release_date"]
    search_fields = ["title", "text"]

    actions = ["set_visible", "set_invisible"]

    def set_visible(self, request, queryset):
        queryset.update(visible=True)

    set_visible.short_description = "Set selected as visible"

    def set_invisible(self, request, queryset):
        queryset.update(visible=False)

    set_invisible.short_description = "Set selected as invisible"
