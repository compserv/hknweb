from django.contrib import admin

from hknweb.candidate.models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    fields = ["slug", "destination_url", "description", "created_by", "active"]
    list_display = ("slug", "destination_url", "click_count", "created_by", "active", "created_at")
    list_filter = ["active", "created_at"]
    search_fields = ["slug", "destination_url", "description"]
    readonly_fields = ["click_count", "created_at", "updated_at"]

    actions = ["activate", "deactivate", "reset_clicks"]

    def activate(self, request, queryset):
        queryset.update(active=True)

    activate.short_description = "Activate selected shortlinks"

    def deactivate(self, request, queryset):
        queryset.update(active=False)

    deactivate.short_description = "Deactivate selected shortlinks"

    def reset_clicks(self, request, queryset):
        queryset.update(click_count=0)

    reset_clicks.short_description = "Reset click count to 0"
