from urllib.parse import urlparse

from django import template

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name="is_link")
def is_link(s: str):
    return urlparse(s).netloc
