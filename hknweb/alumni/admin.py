from django.contrib import admin
from .models import Alumnus


class AlumnusAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'perm_email', 'mailing_list',
              'grad_season', 'grad_year', 'grad_school', 'company',
              'job_title', 'salary', 'city', 'country_state', 'suggestions']
    list_display = ('name', 'perm_email', 'country_state', 'graduation_semester')
    list_filter = ['grad_year', 'mailing_list', 'created_at',
                   'updated_at', 'country_state']
    search_fields = ['first_name', 'last_name', 'perm_email', 'grad_school',
                     'company', 'city']


admin.site.register(Alumnus, AlumnusAdmin)
