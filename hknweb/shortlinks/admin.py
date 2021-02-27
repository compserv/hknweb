from django.contrib import admin
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):

    fields = ['name', 'redirect', 'active', 'created_by', 'created_at']

    readonly_fields = ['created_by', 'created_at']
    list_display = ('name', 'redirect', 'active', 'created_by', 'created_at')
    list_filter = ['created_at', 'created_by', 'active']
    search_fields = ['name', 'created_by__username', 'created_by__first_name', 'created_by__last_name']
    ordering = ['-created_at']
    autocomplete_fields = ['created_by']
