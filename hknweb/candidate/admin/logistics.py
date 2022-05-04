from django.contrib import admin

from hknweb.candidate.models import Logistics, EventReq, MiscReq, FormReq


admin.site.register(EventReq, admin.ModelAdmin)
admin.site.register(MiscReq, admin.ModelAdmin)
admin.site.register(FormReq, admin.ModelAdmin)

@admin.register(Logistics)
class LogisticsAdmin(admin.ModelAdmin):
    list_display = ("semester", "date_start", "date_end")
