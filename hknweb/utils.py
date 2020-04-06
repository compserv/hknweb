from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.contrib.staticfiles.finders import find
from functools import wraps
from random import randint

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
