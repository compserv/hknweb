from django.contrib import admin

from hknweb.candidate.models import (
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
    MergeEventsEntry,
    RequirementBitByteActivity,
    RequriementEvent,
    RequirementHangout,
    RequirementMandatory,
    RequirementMergeRequirement,
)
from hknweb.candidate.admin.requirements.mixins import (
    SetSemesterMixin,
    SetVisibleAndSemesterMixin,
)


@admin.register(RequriementEvent)
@admin.register(RequirementHangout)
@admin.register(RequirementBitByteActivity)
class RequirementAdminGeneral(admin.ModelAdmin, SetSemesterMixin):
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


@admin.register(CandidateForm)
class CandidateFormAdmin(admin.ModelAdmin, SetVisibleAndSemesterMixin):
    fields = ["name", "link", "visible", "duedate", "candidateSemesterActive"]
    list_display = ("name", "link", "visible", "duedate", "candidateSemesterActive")
    list_filter = ["visible", "duedate", "candidateSemesterActive"]
    search_fields = ["name", "link"]


@admin.register(DuePayment)
@admin.register(CommitteeProject)
class MiscRequirementAdmin(admin.ModelAdmin, SetVisibleAndSemesterMixin):
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


@admin.register(RequirementMandatory)
class RequirementMandatoryAdmin(RequirementAdminGeneral):
    filter_horizontal = ("events",)

class MergeEventsEntryInline(admin.TabularInline):
    model = MergeEventsEntry
    extra = 1

@admin.register(RequirementMergeRequirement)
class RequirementMergeAdmin(RequirementAdminGeneral):
    actions = RequirementAdminGeneral.actions + ["clear_merge_entries"]
    inlines = [MergeEventsEntryInline]

    def clear_merge_entries(self, request, queryset):
        for merge in queryset:
            merge.MergeEventsEntry_set.all().delete()

    clear_merge_entries.short_description = "Clear Merges entries"


@admin.register(DuePaymentPaidEntry)
@admin.register(CandidateFormDoneEntry)
@admin.register(CommitteeProjectDoneEntry)
class MiscRequirementEntryAdmin(admin.ModelAdmin):
    filter_horizontal = ("users",)
