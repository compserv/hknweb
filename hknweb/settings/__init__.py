import os
import sys

try:
    HKNWEB_MODE = os.environ['HKNWEB_MODE'].lower()
    if HKNWEB_MODE == 'dev':
        from .dev import *
    elif HKNWEB_MODE == 'prod':
        from .prod import *
    else:
        print("HKNWEB_MODE is not a valid value")
        sys.exit()
except KeyError:
    print("SETTINGS says: HKNWEB_MODE not supplied, so no data will be loaded into settings. You can still load of the subpackages manually.")

