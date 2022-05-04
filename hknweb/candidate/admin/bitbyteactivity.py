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
