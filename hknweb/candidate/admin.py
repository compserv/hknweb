from django.contrib import admin
from .models import OffChallenge
from django.contrib.auth.models import User
from django.http import HttpResponse

import csv


class OffChallengeAdmin(admin.ModelAdmin):

    fields = ['requester', 'officer', 'name', 'reviewed', 'confirmed', 'description', 'proof', 'officer_comment', 'request_date']
    readonly_fields = ['request_date']
    list_display = ('name', 'requester', 'officer', 'reviewed', 'confirmed', 'request_date')
    list_filter = ['requester', 'officer', 'request_date']
    search_fields = ['requester', 'officer', 'name']

    actions = ["export_as_csv"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "officer":
            kwargs["queryset"] = User.objects.all().order_by('username')
        return super(OffChallengeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # @source: http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected as csv"


admin.site.register(OffChallenge, OffChallengeAdmin)
