import csv

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.staticfiles.finders import find
from functools import wraps
from random import randint
from datetime import datetime

from pytz import timezone

# constants

DATETIME_12_HOUR_FORMAT = '%m/%d/%Y %I:%M %p'
PACIFIC_TIMEZONE = timezone('US/Pacific')

# decorators

def login_and_permission(permission_name):
    """ First requires log in, but if you're already logged in but don't have permission,
        displays more info. """
    def decorator(func):
        return wraps(func)( # preserves function attributes to the decorated function
                login_required(login_url='/accounts/login/')(
                    # raises 403 error which invokes our custom 403.html
                    permission_required(permission_name, login_url='/accounts/login/', raise_exception=True)(
                        func # decorates function with both login_required and permission_required
                    )
                )
            )
    return decorator

def method_login_and_permission(permission_name):
    return method_decorator(login_and_permission(permission_name), name='dispatch')

# photos

def get_all_photos():
    """ This function is not used; it can be used to view all photos available. """
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
    """ Returns a string representation of the candidate semester of this timezone object.
        Assumes that there are only spring and fall semesters, separated at 07/01.
        Example: "Spring 2020" """
    season = "Spring" if date.month < 7 else "Fall"
    return "{} {}".format(season, date.year)

def get_semester_bounds(date):
    """ Returns the two dates that bound the current candidate semester.
        Assumes that there are only spring and fall semesters, separated at 07/01. """
    if date.month < 7:
        return datetime(date.year, 1, 1), datetime(date.year, 7, 1)
    else:
        return datetime(date.year, 7, 1), datetime(date.year + 1, 1, 1)


# Helper. @source: http://books.agiliq.com/projects/django-admin-cookbook/en/latest/export.html
def export_model_as_csv(model, queryset):
    meta = model.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])

    return response

from functools import partial


from django.conf import settings
from django.utils.safestring import mark_safe

import markdown
import bleach


def markdownify(text):

    # Bleach settings
    whitelist_tags = getattr(settings, 'MARKDOWNIFY_WHITELIST_TAGS', bleach.sanitizer.ALLOWED_TAGS)
    whitelist_attrs = getattr(settings, 'MARKDOWNIFY_WHITELIST_ATTRS', bleach.sanitizer.ALLOWED_ATTRIBUTES)
    whitelist_styles = getattr(settings, 'MARKDOWNIFY_WHITELIST_STYLES', bleach.sanitizer.ALLOWED_STYLES)
    whitelist_protocols = getattr(settings, 'MARKDOWNIFY_WHITELIST_PROTOCOLS', bleach.sanitizer.ALLOWED_PROTOCOLS)

    # Markdown settings
    strip = getattr(settings, 'MARKDOWNIFY_STRIP', True)
    extensions = getattr(settings, 'MARKDOWNIFY_MARKDOWN_EXTENSIONS', [])

    # Bleach Linkify
    linkify = None
    linkify_text = getattr(settings, 'MARKDOWNIFY_LINKIFY_TEXT', True)

    if linkify_text:
        linkify_parse_email = getattr(settings, 'MARKDOWNIFY_LINKIFY_PARSE_EMAIL', False)
        linkify_callbacks = getattr(settings, 'MARKDOWNIFY_LINKIFY_CALLBACKS', None)
        linkify_skip_tags = getattr(settings, 'MARKDOWNIFY_LINKIFY_SKIP_TAGS', None)
        linkifyfilter = bleach.linkifier.LinkifyFilter

        linkify = [partial(linkifyfilter,
                callbacks=linkify_callbacks,
                skip_tags=linkify_skip_tags,
                parse_email=linkify_parse_email
                )]

    # Convert markdown to html
    html = markdown.markdown(text, extensions=extensions)

    # Sanitize html if wanted
    if getattr(settings, 'MARKDOWNIFY_BLEACH', True):

        cleaner = bleach.Cleaner(tags=whitelist_tags,
                                 attributes=whitelist_attrs,
                                 styles=whitelist_styles,
                                 protocols=whitelist_protocols,
                                 strip=strip,
                                 filters=linkify,
                                 )
        print("Original html")
        print(html)
        print("-----")
        html = cleaner.clean(html)
        print("cleaned html")
        print(html)
        print("-----")

    return mark_safe(html)
