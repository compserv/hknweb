import csv
import re
from datetime import datetime

### For Markdownx Security Patch
from functools import partial, wraps
from random import randint

import bleach
import markdown
from django.conf import settings
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.staticfiles.finders import find
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from pytz import timezone

###


# constants

DATETIME_12_HOUR_FORMAT = "%m/%d/%Y %I:%M %p"
PACIFIC_TIMEZONE = timezone("US/Pacific")


# decorators
def _record_permission(permission):
    permissions_attr = "_permissions"

    def decorator(func):
        perms = list(getattr(func, permissions_attr, []))
        perms.append(permission)

        @wraps(func)
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)

        setattr(wrapped, permissions_attr, perms)
        return wrapped

    return decorator


def allow_public_access(func):
    return _record_permission(None)(func)


def _wrap_with_access_check(identifier, check):
    def decorator(func):
        return wraps(func)(  # preserves function attributes to the decorated function
            _record_permission(identifier)(
                login_required(login_url="/accounts/login/")(
                    # raises 403 error which invokes our custom 403.html
                    check(func)
                    if check is not None
                    else func
                )
            )
        )

    return decorator


allow_all_logged_in_users = _wrap_with_access_check(None, None)


def login_and_permission(permission_name):
    """First requires log in, but if you're already logged in but don't have permission,
    displays more info."""

    return _wrap_with_access_check(
        permission_name,
        permission_required(
            permission_name, login_url="/accounts/login/", raise_exception=True
        ),
    )


def access_level_required(access_level):
    def test_user(user):
        if get_access_level(user) > access_level:
            raise PermissionDenied
        return True

    return user_passes_test(test_user)


def login_and_access_level(access_level):
    return _wrap_with_access_check(
        f"Access level <= {access_level}",
        access_level_required(access_level),
    )


def method_login_and_permission(permission_name):
    return method_decorator(login_and_permission(permission_name), name="dispatch")


# photos


def get_all_photos():
    """This function is not used; it can be used to view all photos available."""
    with open(find("animal_photo_urls.txt")) as f:
        urls = f.readlines()
    return [url.strip() + "?w=400" for url in urls]


# images from pexels.com
def get_rand_photo(width=400):
    with open(find("animal_photo_urls.txt")) as f:
        urls = f.readlines()
    return urls[randint(0, len(urls) - 1)].strip() + "?w=" + str(width)


# date and time


def get_semester(date):
    """Returns a string representation of the candidate semester of this timezone object.
    Assumes that there are only spring and fall semesters, separated at 07/01.
    Example: "Spring 2020" """
    season = "Spring" if date.month < 7 else "Fall"
    return "{} {}".format(season, date.year)


def get_semester_bounds(date):
    """Returns the two dates that bound the current candidate semester.
    Assumes that there are only spring and fall semesters, separated at 07/01."""
    if date.month < 7:
        return datetime(date.year, 1, 1, tzinfo=PACIFIC_TIMEZONE), datetime(
            date.year, 7, 1, tzinfo=PACIFIC_TIMEZONE
        )
    else:
        return datetime(date.year, 7, 1, tzinfo=PACIFIC_TIMEZONE), datetime(
            date.year + 1, 1, 1, tzinfo=PACIFIC_TIMEZONE
        )


# Helper. @source: http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
def export_model_as_csv(model, queryset):
    meta = model.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response


def markdownify(text):
    # Bleach settings
    whitelist_tags = getattr(
        settings, "MARKDOWNIFY_WHITELIST_TAGS", bleach.sanitizer.ALLOWED_TAGS
    )
    whitelist_attrs = getattr(
        settings, "MARKDOWNIFY_WHITELIST_ATTRS", bleach.sanitizer.ALLOWED_ATTRIBUTES
    )
    whitelist_protocols = getattr(
        settings, "MARKDOWNIFY_WHITELIST_PROTOCOLS", bleach.sanitizer.ALLOWED_PROTOCOLS
    )

    # Markdown settings
    strip = getattr(settings, "MARKDOWNIFY_STRIP", True)
    extensions = getattr(settings, "MARKDOWNIFY_MARKDOWN_EXTENSIONS", [])

    # Bleach Linkify
    linkify = None
    linkify_text = getattr(settings, "MARKDOWNIFY_LINKIFY_TEXT", True)

    if linkify_text:
        linkify_parse_email = getattr(
            settings, "MARKDOWNIFY_LINKIFY_PARSE_EMAIL", False
        )
        linkify_callbacks = getattr(settings, "MARKDOWNIFY_LINKIFY_CALLBACKS", None)
        linkify_skip_tags = getattr(settings, "MARKDOWNIFY_LINKIFY_SKIP_TAGS", None)
        linkifyfilter = bleach.linkifier.LinkifyFilter

        linkify = [
            partial(
                linkifyfilter,
                callbacks=linkify_callbacks,
                skip_tags=linkify_skip_tags,
                parse_email=linkify_parse_email,
            )
        ]

    # Convert markdown to html
    html = markdown.markdown(text, extensions=extensions)

    # Sanitize html if wanted
    if getattr(settings, "MARKDOWNIFY_BLEACH", True):
        cleaner = bleach.Cleaner(
            tags=whitelist_tags,
            attributes=whitelist_attrs,
            protocols=whitelist_protocols,
            strip=strip,
            filters=linkify,
        )

        html = cleaner.clean(html)

    return mark_safe(html)


GROUP_TO_ACCESSLEVEL = {
    "officer": 0,
    "member": 0,
    "candidate": 1,
}


def get_access_level(user):
    access_level = 2  # See constants.py
    for group_name, access_value in GROUP_TO_ACCESSLEVEL.items():
        if user.groups.filter(name=group_name).exists():
            access_level = min(access_level, access_value)
    return access_level


def view_url(s: str) -> str:
    # For Google Drive urls
    re_pattern = "https:\/\/drive\.google\.com\/file\/d\/(.*)\/view\?usp=sharing"
    url_template = "https://drive.google.com/uc?export=view&id={id}"
    matches = re.match(re_pattern, s)
    if matches:
        id = matches.groups()[0]
        return url_template.format(id=id)

    # For Flickr urls
    re_pattern = "https:\/\/live\.staticflickr\.com\/(.*)\/(.*)\.jpg"
    url_template = "https://live.staticflickr.com/{group_id}/{picture_id}.jpg"
    matches = re.search(re_pattern, s)
    if matches:
        group_id, picture_id = matches.groups()
        return url_template.format(group_id=group_id, picture_id=picture_id)

    return s
