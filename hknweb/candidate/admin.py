from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.utils.translation import ngettext

from hknweb.utils import export_model_as_csv
from hknweb.coursesemester.models import Semester

from .models import (
    Announcement,
    BitByteActivity,
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
    OffChallenge,
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
    RequirementMandatory,
    RequirementMergeRequirement,
)
from .utils import send_bitbyte_confirm_email, send_challenge_confirm_email

import datetime


class OffChallengeAdmin(admin.ModelAdmin):

    fields = [
        "requester",
        "officer",
        "name",
        "officer_confirmed",
        "csec_confirmed",
        "description",
        "proof",
        "officer_comment",
        "request_date",
    ]
    readonly_fields = ["request_date"]
    list_display = (
        "name",
        "requester",
        "officer",
        "officer_confirmed",
        "csec_confirmed",
        "request_date",
    )
    list_filter = [
        "requester",
        "officer",
        "officer_confirmed",
        "csec_confirmed",
        "request_date",
    ]
    search_fields = [
        "requester__username",
        "requester__first_name",
        "requester__last_name",
        "officer__username",
        "officer__first_name",
        "officer__last_name",
        "name",
    ]
    autocomplete_fields = ["requester", "officer"]

    actions = ["export_as_csv", "csec_confirm", "csec_reject"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "officer":
            kwargs["queryset"] = User.objects.all().order_by("username")
        return super(OffChallengeAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "csec_confirmed" in form.changed_data:
            OffChallengeAdmin.check_send_email(request, obj)

    @staticmethod
    def check_send_email(request, obj):
        # officer has already confirmed, and now csec confirms
        if obj.csec_confirmed is True and obj.officer_confirmed is True:
            send_challenge_confirm_email(request, obj, True)
        # officer has not already rejected, and now csec rejects
        elif obj.csec_confirmed is False and obj.officer_confirmed is not False:
            send_challenge_confirm_email(request, obj, False)
        # if neither is true, either need to wait for officer to review,
        # or officer has already rejected

    def export_as_csv(self, request, queryset):
        return export_model_as_csv(self, queryset)

    export_as_csv.short_description = "Export selected as csv"

    def csec_confirm(self, request, queryset):
        for obj in queryset:
            if obj.csec_confirmed is not True:
                obj.csec_confirmed = True
                obj.save()
                self.check_send_email(request, obj)

    csec_confirm.short_description = "Mark selected as confirmed (csec)"

    def csec_reject(self, request, queryset):
        for obj in queryset:
            if obj.csec_confirmed is not False:
                obj.csec_confirmed = False
                obj.save()
                self.check_send_email(request, obj)

    csec_reject.short_description = "Mark selected as rejected (csec)"


class BitByteActivityAdmin(admin.ModelAdmin):

    fields = ["participants", "confirmed", "proof", "notes", "request_date"]
    readonly_fields = ["request_date"]
    list_display = (
        "participant_usernames",
        "confirmed",
        "request_date",
        "proof",
        "notes",
    )
    list_filter = ["confirmed", "request_date"]
    search_fields = [
        "participants__username",
        "participants__first_name",
        "participants__last_name",
        "proof",
        "notes",
    ]
    autocomplete_fields = ["participants"]

    def participant_usernames(self, obj):
        return ", ".join([c.username for c in obj.participants.all()])

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "confirmed" in form.changed_data:
            BitByteActivityAdmin.check_send_email(request, obj)

    @staticmethod
    def check_send_email(request, obj):
        if obj.is_confirmed:
            send_bitbyte_confirm_email(request, obj, True)
        elif obj.is_rejected:
            send_bitbyte_confirm_email(request, obj, False)
        # if neither is true, it means it became someone changed the nullable boolean to 'Unknown'

    actions = ["export_as_csv", "confirm", "reject"]

    def export_as_csv(self, request, queryset):
        return export_model_as_csv(self, queryset)

    export_as_csv.short_description = "Export selected as csv"

    def confirm(self, request, queryset):
        for obj in queryset:
            if obj.confirmed is not True:
                obj.confirmed = True
                obj.save()
                self.check_send_email(request, obj)

    confirm.short_description = "Mark selected as confirmed"

    def reject(self, request, queryset):
        for obj in queryset:
            if obj.confirmed is not False:
                obj.confirmed = False
                obj.save()
                self.check_send_email(request, obj)

    reject.short_description = "Mark selected as rejected"


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


class CandidateFormAdmin(admin.ModelAdmin):
    fields = ["name", "link", "visible", "duedate", "candidateSemesterActive"]
    list_display = ("name", "link", "visible", "duedate", "candidateSemesterActive")
    list_filter = ["visible", "duedate", "candidateSemesterActive"]
    search_fields = ["name", "link"]

    actions = [
        "set_visible",
        "set_invisible",
        "set_fall_this_year",
        "set_spring_this_year",
        "set_summer_this_year",
    ]

    def set_visible(self, request, queryset):
        queryset.update(visible=True)

    set_visible.short_description = "Set selected as visible"

    def set_invisible(self, request, queryset):
        queryset.update(visible=False)

    set_invisible.short_description = "Set selected as invisible"

    def set_fall_this_year(self, request, queryset):
        RequirementAdminGeneral.set_current_semester(self, request, queryset, "Fall")

    def set_spring_this_year(self, request, queryset):
        RequirementAdminGeneral.set_current_semester(self, request, queryset, "Spring")

    def set_summer_this_year(self, request, queryset):
        RequirementAdminGeneral.set_current_semester(self, request, queryset, "Summer")

    set_fall_this_year.short_description = (
        "Set to Fall semester of this year ({})".format(datetime.datetime.now().year)
    )
    set_spring_this_year.short_description = (
        "Set to Spring semester of this year ({})".format(datetime.datetime.now().year)
    )
    set_summer_this_year.short_description = (
        "Set to Summer semester of this year ({})".format(datetime.datetime.now().year)
    )


class MiscRequirementAdmin(admin.ModelAdmin):
    fields = ["name", "instructions", "visible", "duedate", "candidateSemesterActive"]
    list_display = (
        "name",
        "instructions",
        "visible",
        "duedate",
        "candidateSemesterActive",
    )
    list_filter = ["visible", "duedate", "candidateSemesterActive"]
    search_fields = ["name", "instructions"]

    actions = [
        "set_visible",
        "set_invisible",
        "set_fall_this_year",
        "set_spring_this_year",
        "set_summer_this_year",
    ]

    def set_visible(self, request, queryset):
        queryset.update(visible=True)

    set_visible.short_description = "Set selected as visible"

    def set_invisible(self, request, queryset):
        queryset.update(visible=False)

    set_invisible.short_description = "Set selected as invisible"

    def set_fall_this_year(self, request, queryset):
        RequirementAdminGeneral.set_current_semester(self, request, queryset, "Fall")

    def set_spring_this_year(self, request, queryset):
        RequirementAdminGeneral.set_current_semester(self, request, queryset, "Spring")

    def set_summer_this_year(self, request, queryset):
        RequirementAdminGeneral.set_current_semester(self, request, queryset, "Summer")

    set_fall_this_year.short_description = (
        "Set to Fall semester of this year ({})".format(datetime.datetime.now().year)
    )
    set_spring_this_year.short_description = (
        "Set to Spring semester of this year ({})".format(datetime.datetime.now().year)
    )
    set_summer_this_year.short_description = (
        "Set to Summer semester of this year ({})".format(datetime.datetime.now().year)
    )


class RequirementAdminGeneral(admin.ModelAdmin):
    actions = [
        "set_enable",
        "set_disable",
        "set_fall_this_year",
        "set_spring_this_year",
        "set_summer_this_year",
    ]

    def set_enable(self, request, queryset):
        queryset.update(enable=True)

    set_enable.short_description = "Enable selected"

    def set_disable(self, request, queryset):
        queryset.update(enable=False)

    set_disable.short_description = "Disable selected"

    def set_current_semester(self, request, queryset, sem):
        now = datetime.datetime.now()
        candidateSemester = Semester.objects.filter(semester=sem, year=now.year).first()
        if candidateSemester is None:
            result_text = "Requirements failed to set to {} {}. Please make sure a Semester object for it exist under HKNWEB.".format(
                sem, now.year
            )
            self.message_user(
                request,
                ngettext(
                    result_text,
                    result_text,
                    0,
                ),
                messages.ERROR,
            )
            return
        updated = queryset.update(candidateSemesterActive=candidateSemester)
        result_text = "%d requirement{} successfully set to {} {}.".format(
            "{}", sem, now.year
        )
        self.message_user(
            request,
            ngettext(
                result_text.format(""),
                result_text.format("s"),
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def set_fall_this_year(self, request, queryset):
        self.set_current_semester(request, queryset, "Fall")

    def set_spring_this_year(self, request, queryset):
        self.set_current_semester(request, queryset, "Spring")

    def set_summer_this_year(self, request, queryset):
        self.set_current_semester(request, queryset, "Summer")

    set_fall_this_year.short_description = (
        "Set to Fall semester of this year ({})".format(datetime.datetime.now().year)
    )
    set_spring_this_year.short_description = (
        "Set to Spring semester of this year ({})".format(datetime.datetime.now().year)
    )
    set_summer_this_year.short_description = (
        "Set to Summer semester of this year ({})".format(datetime.datetime.now().year)
    )


class RequirementMandatoryAdmin(RequirementAdminGeneral):
    filter_horizontal = ("events",)


class RequirementMergeAdmin(RequirementAdminGeneral):
    actions = RequirementAdminGeneral.actions + ["link", "clear_links"]

    def link(self, request, queryset):
        queryset = list(queryset)
        for i, node in enumerate(queryset):
            print(i, node)
            node.linkedRequirement = (
                queryset[i + 1] if (i + 1 < len(queryset)) else None
            )
            node.save()

    link.short_description = "Link together selected (overwrites current links)"

    def clear_links(self, request, queryset):
        queryset.update(linkedRequirement=None)

    clear_links.short_description = "Clear links of Merges"


class DuePaymentPaidEntryAdmin(admin.ModelAdmin):
    filter_horizontal = ("users",)


class CandidateFormDoneEntryAdmin(admin.ModelAdmin):
    filter_horizontal = ("users",)


class CommitteeProjectDoneEntryAdmin(admin.ModelAdmin):
    filter_horizontal = ("users",)


admin.site.register(OffChallenge, OffChallengeAdmin)
admin.site.register(BitByteActivity, BitByteActivityAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(RequriementEvent, RequirementAdminGeneral)
admin.site.register(RequirementHangout, RequirementAdminGeneral)
admin.site.register(RequirementMandatory, RequirementMandatoryAdmin)
admin.site.register(RequirementMergeRequirement, RequirementMergeAdmin)
admin.site.register(RequirementBitByteActivity, RequirementAdminGeneral)

admin.site.register(CandidateForm, CandidateFormAdmin)
admin.site.register(CandidateFormDoneEntry, CandidateFormDoneEntryAdmin)

admin.site.register(DuePayment, MiscRequirementAdmin)
admin.site.register(DuePaymentPaidEntry, DuePaymentPaidEntryAdmin)

admin.site.register(CommitteeProject, MiscRequirementAdmin)
admin.site.register(CommitteeProjectDoneEntry, CommitteeProjectDoneEntryAdmin)
