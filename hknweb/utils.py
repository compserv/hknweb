from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.staticfiles.finders import find
from functools import wraps
from random import randint
from datetime import datetime

# constants

DATETIME_12_HOUR_FORMAT = '%m/%d/%Y %I:%M %p'

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
