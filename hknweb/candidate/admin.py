from django.contrib import admin
from .models import OffChallenge
from hknweb.models import Profile


class OffChallengeAdmin(admin.ModelAdmin):

    fields = ['requester', 'officer', 'name', 'confirmed', 'description', 'proof']
    list_display = ('name', 'requester', 'officer', 'confirmed', 'description')
    list_filter = ['requester', 'officer']
    search_fields = ['requester', 'officer', 'name']


admin.site.register(OffChallenge, OffChallengeAdmin)
