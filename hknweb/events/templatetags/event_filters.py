from django import template
import bleach

register = template.Library()


@register.filter
def event_name(name):
    return bleach.clean(name, tags=[], strip=True)
