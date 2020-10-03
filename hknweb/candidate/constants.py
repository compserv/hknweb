from django.conf import settings


REQUIREMENT_TITLES_TEMPLATE = "{name} ({num_required} required, {num_remaining} remaining)"
REQUIREMENT_TITLES_MANDATORY = "Mandatory Meetings (ALL required)"

REQUIREMENT_EVENTS = [
    settings.MANDATORY_EVENT,
    settings.FUN_EVENT,
    settings.BIG_FUN_EVENT,
    settings.SERV_EVENT,
    settings.PRODEV_EVENT,
]

class ATTR:
    TITLE = "title"
    STATUS = "status"
    COLOR = "color"
    CONFIRMED = "confirmed"
    UNCONFIRMED = "unconfirmed"
    NUM_PENDING = "num_pending"
    NUM_REJECTED = "num_rejected"
    NUM_CONFIRMED = "num_confirmed"
    NUM_BITBYTES = "num_bitbytes"
