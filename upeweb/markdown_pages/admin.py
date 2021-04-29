from django.contrib import admin

from markdownx.admin import MarkdownxModelAdmin
from .models import MarkdownPage

admin.site.register(MarkdownPage, MarkdownxModelAdmin)
