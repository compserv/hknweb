from hknweb.events.views.aggregate_displays import (
    index,
    ical,
    get_leaderboard,
    photos,
)
from hknweb.events.views.rsvp_transactions import (
    rsvp,
    unrsvp,
    confirm_rsvp,
)
from hknweb.events.views.event_transactions import (
    EventUpdateView,
    add_event,
    show_details,
    EventDeleteView,
)
from hknweb.events.views.attendance import manage_attendance, submit_attendance
