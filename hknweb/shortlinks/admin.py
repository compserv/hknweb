from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):

    fields = [
        "name",
        "redirect",
        "active",
        "created_by",
        "created_at",
        "modified_at",
        "last_accessed_at",
    ]

    readonly_fields = ["created_at", "modified_at", "last_accessed_at"]
    list_display = (
        "name",
        "redirect",
        "active",
        "created_by",
        "created_at",
        "modified_at",
        "last_accessed_at",
    )
    list_filter = [
        "created_at",
        "created_by",
        "active",
        "modified_at",
        "last_accessed_at",
    ]
    search_fields = [
        "name",
        "created_by__username",
        "created_by__first_name",
        "created_by__last_name",
    ]
    ordering = ["-created_at"]
    autocomplete_fields = ["created_by"]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ["created_by"]
        return self.readonly_fields

    actions = ["set_active", "set_inactive"]

    def set_active(self, request, queryset):
        queryset.update(active=True)

    set_active.short_description = "Set selected as active"

    def set_inactive(self, request, queryset):
        queryset.update(active=False)

    set_inactive.short_description = "Set selected as inactive"
