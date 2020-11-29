from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.conf import settings
from .models import Announcement



# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'officer', 'candidate')
    readonly_fields = ('officer', 'candidate')

    actions = ['add_cand', 'add_officer', 'remove_cand', 'remove_officer']

    def officer(self, user):
        return 'Y' if user.groups.filter(name=settings.OFFICER_GROUP).exists() else ''

    def candidate(self, user):
        return 'Y' if user.groups.filter(name=settings.CAND_GROUP).exists() else ''

    def add_cand(self, request, queryset):
        group = Group.objects.get(name=settings.CAND_GROUP)
        for u in queryset:
            group.user_set.add(u)
    
    add_cand.short_description = "Add selected as candidates"

    def add_officer(self, request, queryset):
        group = Group.objects.get(name=settings.OFFICER_GROUP)
        for u in queryset:
            group.user_set.add(u)

    add_officer.short_description = "Add selected as officers"

    def remove_cand(self, request, queryset):
        group = Group.objects.get(name=settings.CAND_GROUP)
        for u in queryset:
            group.user_set.remove(u)

    remove_cand.short_description = "Remove selected from candidates"

    def remove_officer(self, request, queryset):
        group = Group.objects.get(name=settings.OFFICER_GROUP)
        for u in queryset:
            group.user_set.remove(u)

    remove_officer.short_description = "Remove selected from officers"


class AnnouncementAdmin(admin.ModelAdmin):

    # NOTE: release_date is not readonly because we can reuse announcements from past semesters
    # The VP can just change the date and release it again
    fields = ['title', 'text', 'visible', 'release_date']
    list_display = ('title', 'visible', 'release_date')
    list_filter = ['visible', 'release_date']
    search_fields = ['title', 'text']

    actions = ["set_visible", "set_invisible"]

    def set_visible(self, request, queryset):
        queryset.update(visible=True)

    set_visible.short_description = "Set selected as visible"

    def set_invisible(self, request, queryset):
        queryset.update(visible=False)
        
    set_invisible.short_description = "Set selected as invisible"

admin.site.register(Announcement, AnnouncementAdmin)
