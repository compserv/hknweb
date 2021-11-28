class ATTR:
    ACCESS_LEVEL = "access_level"
    ACTION = "action"
    CLASS = "class"
    COUNT = "count"
    CREATED_BY = "created_by"
    DATA = "data"
    DAY = "day"
    DISPLAY_VALUE = "display_value"
    DESCRIPTION = "description"
    END_TIME = "end_time"
    EVENT = "event"
    EVENT_NAME = "event_name"
    EVENTS = "events"
    EVENTS_DATA = "events_data"
    EVENT_TYPE = "event_type"
    EVENT_TYPES = "event_types"
    GCAL_INVITE_TEMPLATE = "gcal_link"
    HOUR = "hour"
    LOCATION = "location"
    MANDATORY = "Mandatory"
    MINUTES = "minutes"
    MONTH = "month"
    NAME = "name"
    PADDING = "padding"
    PAGE_PARAM = "page_param"
    RSVP_LIMIT = "rsvp_limit"
    SECONDS = "seconds"
    SLUG = "slug"
    START_TIME = "start_time"
    TITLE = "title"
    YEAR = "year"


# See https://stackoverflow.com/questions/22757908/what-parameters-are-required-to-create-an-add-to-google-calendar-link
GCAL_INVITE_TEMPLATE = "https://www.google.com/calendar/render?action=TEMPLATE&text={%s}&details={%s}&location={%s}&dates={%s}/{%s}" % (
    ATTR.EVENT_NAME,
    ATTR.DESCRIPTION,
    ATTR.LOCATION,
    ATTR.START_TIME,
    ATTR.END_TIME,
)

GCAL_DATETIME_TEMPLATE = (
    "{%s:04n}{%s:02n}{%s:02n}T{%s:02n}{%s:02n}{%s:02n}Z"
    % (  # "T" is for GCal format, "Z" is to indicate UTC time
        ATTR.YEAR,
        ATTR.MONTH,
        ATTR.DAY,
        ATTR.HOUR,
        ATTR.MINUTES,
        ATTR.SECONDS,
    )
)

RSVPS_PER_PAGE = 10

ACCESSLEVEL_TO_DESCRIPTION = {
    0: "Internal",
    1: "Candidate",
    2: "External",
}
