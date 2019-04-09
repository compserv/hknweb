from .common import *
from .secrets import SECRET_KEY
# In prod mode, rigidly enforce using real secrets and fail if unavailiable

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'v9lj^szduvr@a*31&r(l5ub+5q%ebszts70vlpzaiekt23s)gb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'hkn.eecs.berkeley.edu',
    'hkn.mu',
    'dev-hkn-eecs-berkeley-edu.apphost.ocf.berkeley.edu',
    'dev-hkn.eecs.berkeley.edu',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = 'https://www.ocf.berkeley.edu/~hkn/hknweb/static/'
STATIC_ROOT = '/home/h/hk/hkn/public_html/hknweb/static/'

# Media files (user-uploaded files)
# https://docs.djangoproject.com/en/2.1/topics/files/
MEDIA_URL = 'https://www.ocf.berkeley.edu/~hkn/hknweb/media/'
MEDIA_ROOT = '/home/h/hk/hkn/public_html/hknweb/media/'
