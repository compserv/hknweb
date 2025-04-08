from django.contrib import admin

# Register your models here.
from hknweb.indrel.models import UserResume, ResumeBook


@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    fields = ["userInfo", "resume"]
    list_display = ("userInfo", "resume", "upload_date")
    ordering = ["-upload_date"]

@admin.register(ResumeBook)
class ResumeBookAdmin(admin.ModelAdmin):
    fields = ["comments", "pdf", "iso"]
    list_display = ("creation_date", "comments", "pdf", "iso")
    ordering = ["-creation_date"]