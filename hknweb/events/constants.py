GCAL_INVITE_TEMPLATE_ATTRIBUTE_NAME = "gcal_link"
EVENT_NAME_ATTRIBUTE_NAME = "event_name"
START_TIME_ATTRIBUTE_NAME = "start_time"
END_TIME_ATTRIBUTE_NAME = "end_time"
DESCRIPTION_ATTRIBUTE_NAME = "description"
LOCATION_ATTRIBUTE_NAME = "location"

# See https://stackoverflow.com/questions/22757908/what-parameters-are-required-to-create-an-add-to-google-calendar-link
GCAL_INVITE_TEMPLATE = "https://calendar.google.com/calendar/render?action=TEMPLATE&text={%s}&dates={%s}/{%s}&details={%s}&location={%s}" % (
    EVENT_NAME_ATTRIBUTE_NAME,
    START_TIME_ATTRIBUTE_NAME,
    END_TIME_ATTRIBUTE_NAME,
    DESCRIPTION_ATTRIBUTE_NAME,
    LOCATION_ATTRIBUTE_NAME,
)

YEAR_ATTRIBUTE_NAME = "year"
MONTH_ATTRIBUTE_NAME = "month"
DAY_ATTRIBUTE_NAME = "day"
HOUR_ATTRIBUTE_NAME = "hour"
MINUTES_ATTRIBUTE_NAME = "minutes"
SECONDS_ATTRIBUTE_NAME = "seconds"
GCAL_DATETIME_TEMPLATE = "{%s:04n}{%s:02n}{%s:02n}T{%s:02n}{%s:02n}{%s:02n}Z" % (  # "T" is for GCal format, "Z" is to indicate UTC time
    YEAR_ATTRIBUTE_NAME,
    MONTH_ATTRIBUTE_NAME,
    DAY_ATTRIBUTE_NAME,
    HOUR_ATTRIBUTE_NAME,
    MINUTES_ATTRIBUTE_NAME,
    SECONDS_ATTRIBUTE_NAME,
)
