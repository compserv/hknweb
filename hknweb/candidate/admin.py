from django.contrib import admin
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import OffChallenge, Announcement
from .views import send_cand_confirm_email

import csv


class OffChallengeAdmin(admin.ModelAdmin):

    fields = ['requester', 'officer', 'name', 'officer_confirmed', 'csec_confirmed', 'description', 'proof', 'officer_comment', 'request_date']
    readonly_fields = ['request_date']
    list_display = ('name', 'requester', 'officer', 'officer_confirmed', 'csec_confirmed', 'request_date')
    list_filter = ['requester', 'officer', 'officer_confirmed', 'csec_confirmed', 'request_date']
    search_fields = ['requester__username', 'officer__username', 'name']

    actions = ["export_as_csv", "csec_confirm", "csec_reject"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "officer":
            kwargs["queryset"] = User.objects.all().order_by('username')
        return super(OffChallengeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if 'csec_confirmed' in form.changed_data:
            OffChallengeAdmin.check_send_email(request, obj)

    @staticmethod
    def check_send_email(request, obj):
        # officer has already confirmed, and now csec confirms
        if obj.csec_confirmed is True and obj.officer_confirmed is True:
            send_cand_confirm_email(request, obj, True)
        # officer has not already rejected, and now csec rejects
        elif obj.csec_confirmed is False and obj.officer_confirmed is not False:
            send_cand_confirm_email(request, obj, False)
        # if neither is true, either need to wait for officer to review,
        # or officer has already rejected

    # @source: http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

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


class AnnouncementAdmin(admin.ModelAdmin):

    # NOTE: release_date is not readonly because we can reuse announcements from past semesters
    # The VP can just change the date and release it again
    fields = ['title', 'text', 'visible', 'release_date']
    list_display = ('title', 'visible', 'release_date')
    list_filter = ['visible', 'release_date']
    search_fields = ['title', 'text']

    actions = ["set_visible", "set_invisible"]

    def set_visible(self, request, queryset):
        queryset.update(visible=True)

    set_visible.short_description = "Set selected as visible"

    def set_invisible(self, request, queryset):
        queryset.update(visible=False)
        
    set_invisible.short_description = "Set selected as invisible"


admin.site.register(OffChallenge, OffChallengeAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
