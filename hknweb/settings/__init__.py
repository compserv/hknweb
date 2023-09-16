import os
import sys

HKNWEB_MODE = os.getenv("HKNWEB_MODE", "dev").lower()

if HKNWEB_MODE == "dev":
    from .dev import *  # lgtm [py/polluting-import]
elif HKNWEB_MODE == "prod":
    from .prod import *  # lgtm [py/polluting-import]
else:
    print(f"HKNWEB_MODE {HKNWEB_MODE!r} is not a valid value")
    sys.exit()
