from django.contrib import admin
from .models import OffChallenge
from hknweb.models import Profile


class OffChallengeAdmin(admin.ModelAdmin):

    fields = ['requester', 'officer', 'name', 'confirmed', 'description', 'proof', 'request_date']
    readonly_fields = ['request_date']
    list_display = ('name', 'requester', 'officer', 'confirmed', 'request_date')
    list_filter = ['requester', 'officer', 'request_date']
    search_fields = ['requester', 'officer', 'name']


admin.site.register(OffChallenge, OffChallengeAdmin)
