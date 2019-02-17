from django.contrib import admin
from .models import OffChallenge
from django.contrib.auth.models import User


class OffChallengeAdmin(admin.ModelAdmin):

    fields = ['requester', 'officer', 'name', 'reviewed', 'confirmed', 'description', 'proof', 'officer_comment', 'request_date']
    readonly_fields = ['request_date']
    list_display = ('name', 'requester', 'officer', 'reviewed', 'confirmed', 'request_date')
    list_filter = ['requester', 'officer', 'request_date']
    search_fields = ['requester', 'officer', 'name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "officer":
            kwargs["queryset"] = User.objects.all().order_by('username')
        return super(OffChallengeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(OffChallenge, OffChallengeAdmin)
