from .common import *
from .secrets import *
# In prod mode, rigidly enforce using real secrets and fail if unavailiable

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'v9lj^szduvr@a*31&r(l5ub+5q%ebszts70vlpzaiekt23s)gb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'upe.cs.berkeley.edu',
    'upe.mu',
    'dev-upe-cs-berkeley-edu.apphost.ocf.berkeley.edu',
    'dev-upe.cs.berkeley.edu',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = 'https://www.ocf.berkeley.edu/~upe/upeweb/static/'
STATIC_ROOT = '/home/h/hk/upe/public_html/upeweb/static/'

# Media files (user-uploaded files)
# https://docs.djangoproject.com/en/2.1/topics/files/
MEDIA_URL = 'https://www.ocf.berkeley.edu/~upe/upeweb/media/'
MEDIA_ROOT = '/home/h/hk/upe/public_html/upeweb/media/'
