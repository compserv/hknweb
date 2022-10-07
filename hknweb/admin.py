from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from django.conf import settings
from django.shortcuts import redirect, render

from django.urls import path

from hknweb.models import (
    Announcement,
    Profile,
    CandidateProvisioningPassword,
    Committee,
    Election,
    Committeeship,
)
from hknweb.forms import ProvisionCandidatesForm


# Unregister the provided model admin
admin.site.unregister(User)

# Register out own model admin, based on the default UserAdmin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "officer",
        "candidate",
        "exec",
    )
    readonly_fields = ("officer", "candidate", "exec")

    actions = [
        "add_cand",
        "add_officer",
        "add_exec",
        "remove_cand",
        "remove_officer",
        "remove_exec",
    ]

    def officer(self, user):
        return "Y" if user.groups.filter(name=settings.OFFICER_GROUP).exists() else ""

    def candidate(self, user):
        return "Y" if user.groups.filter(name=settings.CAND_GROUP).exists() else ""

    def exec(self, user):
        return "Y" if user.groups.filter(name=settings.EXEC_GROUP).exists() else ""

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

    def add_exec(self, request, queryset):
        group = Group.objects.get(name=settings.EXEC_GROUP)
        for u in queryset:
            group.user_set.add(u)

    add_exec.short_description = "Add selected as execs"

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

    def remove_exec(self, request, queryset):
        group = Group.objects.get(name=settings.EXEC_GROUP)
        for u in queryset:
            group.user_set.remove(u)

    remove_exec.short_description = "Remove selected from execs"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "provision_candidate_accounts/",
                self.provision_candidate_accounts,
                name="auth_user_provision_candidate_accounts",
            ),
        ]
        return my_urls + urls

    def provision_candidate_accounts(self, request):
        form = ProvisionCandidatesForm(request.POST, request.FILES)
        if request.method == "POST" and form.is_valid():
            form.save()

            form.send_candidate_account_emails(request)
            form.add_messages(request)

            return redirect("candidate:officer_portal")

        context = {
            **self.admin_site.each_context(request),
            "form": form,
        }
        return render(request, "admin/provision_candidate_accounts.html", context)


class AnnouncementAdmin(admin.ModelAdmin):

    # NOTE: release_date is not readonly because we can reuse announcements from past semesters
    # The VP can just change the date and release it again
    fields = ["title", "text", "visible", "release_date"]
    list_display = ("title", "visible", "release_date")
    list_filter = ["visible", "release_date"]
    search_fields = ["title", "text"]

    actions = ["set_visible", "set_invisible"]

    def set_visible(self, request, queryset):
        queryset.update(visible=True)

    set_visible.short_description = "Set selected as visible"

    def set_invisible(self, request, queryset):
        queryset.update(visible=False)

    set_invisible.short_description = "Set selected as invisible"


@admin.register(Committeeship)
class CommitteeshipAdmin(admin.ModelAdmin):
    autocomplete_fields = ["officers", "assistant_officers", "committee_members"]


admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Profile)
admin.site.register(CandidateProvisioningPassword)
admin.site.register(Committee)
admin.site.register(Election)
