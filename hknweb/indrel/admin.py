from django.contrib import admin

# Register your models here.
from hknweb.indrel.models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    fields = ["profile", "pdf", "current"]
    # readonly_fields = ["first_name", "last_name", "middle_name", "grad_year", "pdf", "current"]
    list_display = (
        "profile",
        "pdf",
        "current",
    )
    list_filter = ["current"]
