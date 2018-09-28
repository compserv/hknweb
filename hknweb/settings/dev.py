from .common import *

#In dev mode, attempt to use real secrets, but if unavailiable, fall back to dummy secrets
try:
    from .secrets import *
except ImportError:
    from .dummy_secrets import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','hkn.eecs.berkely.edu','hkn.mu']



