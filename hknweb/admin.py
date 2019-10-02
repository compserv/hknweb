from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'officer', 'candidate')
    readonly_fields = ('officer', 'candidate')

    actions = ['add_cand', 'add_officer', 'remove_cand', 'remove_officer']

    def officer(self, user):
        return 'Y' if user.groups.filter(name="officer").exists() else ''

    def candidate(self, user):
        return 'Y' if user.groups.filter(name="candidate").exists() else ''

    def add_cand(self, request, queryset):
        group = Group.objects.get(name='candidate')
        for u in queryset:
            group.user_set.add(u)

    def add_officer(self, request, queryset):
        group = Group.objects.get(name='officer')
        for u in queryset:
            group.user_set.add(u)

    def remove_cand(self, request, queryset):
        group = Group.objects.get(name='candidate')
        for u in queryset:
            group.user_set.remove(u)

    def remove_officer(self, request, queryset):
        group = Group.objects.get(name='officer')
        for u in queryset:
            group.user_set.remove(u)

    add_cand.short_description = "Add selected as candidates"
    add_officer.short_description = "Add selected as officers"
    remove_cand.short_description = "Remove selected from candidates"
    remove_officer.short_description = "Remove selected from officers"

