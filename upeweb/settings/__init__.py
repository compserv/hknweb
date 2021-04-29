import os
import sys

try:
    UPEWEB_MODE = os.environ['UPEWEB_MODE'].lower()
    if UPEWEB_MODE == 'dev':
        from .dev import *
    elif UPEWEB_MODE == 'prod':
        from .prod import *
    else:
        print("UPEWEB_MODE is not a valid value")
        sys.exit()
except KeyError:
    print("SETTINGS says: UPEWEB_MODE not supplied, so no data will be loaded into settings. You can still load of the subpackages manually.")
