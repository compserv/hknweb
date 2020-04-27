from django.contrib import admin
from .models import IndrelMailer,IndrelMailerUnderlying
# Register your models here.
class IndrelMailerAdmin(admin.ModelAdmin):
    fields=['sender','receiver','conf_receiver','subject']
    readonly_fields=['sender','receiver','conf_receiver','subject']
    list_display = ('sender', 'receiver', 'conf_receiver', 'subject')
    list_filter=['sender', 'receiver', 'conf_receiver', 'subject']
    search_fields=['sender','subject','receiver']

admin.site.register(IndrelMailerUnderlying,IndrelMailerAdmin)

