from django.contrib import admin
from .models import ReviewSession

@admin.register(ReviewSession)
class ReviewSessionAdmin(admin.ModelAdmin):

    fields = ['name', 'slug', 'start_time', 'end_time', 'location', 'description', 'created_by', 'created_at']
    # NOTE: created_by should be read only, but I don't know how to set it to default to current user
    readonly_fields = ['created_at']
    list_display = ('name', 'start_time', 'location', 'created_by', 'created_at')
    list_filter = ['start_time', 'created_at', 'location', 'created_by']
    search_fields = ['name', 'created_by__username', 'created_by__first_name', 'created_by__last_name']
    ordering = ['-created_at']
    autocomplete_fields = ['created_by']
