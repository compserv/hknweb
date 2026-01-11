from django.contrib import admin

from hknweb.candidate.models import BitByteGroup


@admin.register(BitByteGroup)
class BitByteGroupAdmin(admin.ModelAdmin):
    fields = ["semester", "bytes", "bits"]
    list_display = (
        "semester",
        "bytes_usernames",
        "bits_usernames",
    )
    list_filter = ["semester"]
    search_fields = [
        "bytes__username",
        "bytes__first_name",
        "bytes__last_name",
        "bits__username",
        "bits__first_name",
        "bits__last_name",
    ]
    autocomplete_fields = ["bytes", "bits"]

    def bytes_usernames(self, obj):
        return ", ".join([user.username for user in obj.bytes.all()])

    def bits_usernames(self, obj):
        return ", ".join([user.username for user in obj.bits.all()])

