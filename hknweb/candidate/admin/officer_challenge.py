from django.contrib import admin
from django.contrib.auth.models import User

from hknweb.utils import export_model_as_csv

from hknweb.candidate.models import OffChallenge
from hknweb.candidate.utils import send_challenge_confirm_email


@admin.register(OffChallenge)
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
