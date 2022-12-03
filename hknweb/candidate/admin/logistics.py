from django.contrib import admin

from hknweb.candidate.models import Logistics, EventReq, MiscReq, FormReq


admin.site.register(EventReq, admin.ModelAdmin)


@admin.register(MiscReq)
@admin.register(FormReq)
class ExternalReqAdmin(admin.ModelAdmin):
    filter_horizontal = ("completed",)


@admin.register(Logistics)
class LogisticsAdmin(admin.ModelAdmin):
    list_display = ("semester", "date_start", "date_end")
    filter_horizontal = ("event_reqs", "misc_reqs", "form_reqs")
