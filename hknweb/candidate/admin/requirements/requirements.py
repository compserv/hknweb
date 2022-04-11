from django.contrib import admin

from hknweb.candidate.models import (
    CandidateForm,
    CandidateFormDoneEntry,
    CommitteeProject,
    CommitteeProjectDoneEntry,
    DuePayment,
    DuePaymentPaidEntry,
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


@admin.register(RequirementMergeRequirement)
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


@admin.register(DuePaymentPaidEntry)
@admin.register(CandidateFormDoneEntry)
@admin.register(CommitteeProjectDoneEntry)
class MiscRequirementEntryAdmin(admin.ModelAdmin):
    filter_horizontal = ("users",)
