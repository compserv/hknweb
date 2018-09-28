from .common import *


#In prod mode, rigidly enforce using real secrets and fail if unavailiable
from .secrets import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v9lj^szduvr@a*31&r(l5ub+5q%ebszts70vlpzaiekt23s)gb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['hkn.eecs.berkeley.edu','hkn.mu']



