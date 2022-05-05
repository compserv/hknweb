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
        "request_date",
    )
    list_filter = [
        "requester",
        "officer",
        "officer_confirmed",
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "officer":
            kwargs["queryset"] = User.objects.all().order_by("username")
        return super(OffChallengeAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )
