from django.contrib import admin

# Register your models here.
from hknweb.indrel.models import UserResume


@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    fields = ["userInfo", "pdf", "current"]
    #readonly_fields = ["first_name", "last_name", "middle_name", "grad_year", "pdf", "current"]
    list_display = ("userInfo", "pdf", "current")
    list_filter = ["current"]
    