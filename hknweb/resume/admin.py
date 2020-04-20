from django.contrib import admin
from .models import Resume

class ResumeAdmin(admin.ModelAdmin):
    fields = ["name", "email", "notes", "document", "uploaded_at", "critiques"]
    readonly_fields = ['uploaded_at', "email", "name", "document"]
    list_display = ('name', 'notes', 'document', 'uploaded_at')
    list_filter = ('name', 'notes', 'document', 'uploaded_at')

admin.site.register(Resume, ResumeAdmin)