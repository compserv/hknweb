import datetime

from django.contrib import messages
from django.utils.translation import ngettext

from hknweb.coursesemester.models import Semester


class SetSemesterMixin:
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


class SetVisibleAndSemesterMixin(SetSemesterMixin):
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
