from django.conf import settings
from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.template.loader import render_to_string

from hknweb.utils import export_model_as_csv, get_rand_photo

from hknweb.candidate.models import BitByteActivity


@admin.register(BitByteActivity)
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
            BitByteActivityAdmin.send_bitbyte_confirm_email(request, obj, True)
        elif obj.is_rejected:
            BitByteActivityAdmin.send_bitbyte_confirm_email(request, obj, False)
        # if neither is true, it means it became someone changed the nullable boolean to 'Unknown'

    actions = ["export_as_csv", "confirm", "reject"]

    @staticmethod
    def send_bitbyte_confirm_email(request, bitbyte, confirmed):
        subject = "[HKN] Your bit-byte request was reviewed"
        participant_emails = [part.email for part in bitbyte.participants.all()]

        bitbyte_link = request.build_absolute_uri(reverse("candidate:bitbyte"))
        html_content = render_to_string(
            "candidate/bitbyte_confirm_email.html",
            {
                "subject": subject,
                "confirmed": confirmed,
                "participants": bitbyte.participants.all(),
                "bitbyte_link": bitbyte_link,
                "img_link": get_rand_photo(),
            },
        )
        msg = EmailMultiAlternatives(
            subject, subject, settings.NO_REPLY_EMAIL, participant_emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

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
