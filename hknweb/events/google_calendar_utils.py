import base64

import google.oauth2.service_account as service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from hknweb.events.models.google_calendar import GoogleCalendarCredentials


CALENDAR_ID = "hknwebsite@hkn.eecs.berkeley.edu"
TIMEZONE = "America/Los_Angeles"
SHARE_LINK_TEMPLATE = "https://calendar.google.com/calendar?cid={cid}"


def get_credentials():
    # Get the most recent GoogleCalendarCredentials
    django_creds = GoogleCalendarCredentials.objects.last()

    # Create credentials for a service account
    creds = service_account.Credentials.from_service_account_file(
        django_creds.file.path
    )

    return creds


def check_credentials_wrapper(fn):
    def new_fn(*args, **kwargs):
        if not GoogleCalendarCredentials.objects.exists():
            return
        return fn(*args, **kwargs)

    return new_fn


def get_service():
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    return service


def create_event_resource(
    summary: str = None,
    location: str = None,
    description: str = None,
    start: str = None,
    end: str = None,
) -> dict:
    event = dict()

    if summary is not None:
        event["summary"] = summary

    if location is not None:
        event["location"] = location

    if description is not None:
        event["description"] = description

    if start is not None:
        event["start"] = {
            "dateTime": start,
            "timeZone": TIMEZONE,
        }

    if end is not None:
        event["end"] = {
            "dateTime": end,
            "timeZone": TIMEZONE,
        }

    return event


@check_credentials_wrapper
def create_event(
    summary: str,
    location: str,
    description: str,
    start: str,
    end: str,
    calendar_id: str=CALENDAR_ID,
) -> str:
    if not calendar_id:
        return

    event_resource = create_event_resource(
        summary=summary,
        location=location,
        description=description,
        start=start,
        end=end,
    )

    event = (
        get_service()
        .events()
        .insert(
            calendarId=calendar_id,
            body=event_resource,
        )
        .execute()
    )

    return event["id"]


@check_credentials_wrapper
def update_event(event_id: str, calendar_id: str=CALENDAR_ID, **kwargs) -> None:
    if not calendar_id:
        return

    event_resource = create_event_resource(**kwargs)

    try:
        get_service().events().patch(
            calendarId=calendar_id,
            eventId=event_id,
            body=event_resource,
        ).execute()
    except HttpError as e:
        if e.resp["status"] not in ["404", "410"]:
            raise e


@check_credentials_wrapper
def delete_event(event_id: str, calendar_id: str=CALENDAR_ID) -> None:
    if not calendar_id:
        return

    try:
        get_service().events().delete(
            calendarId=calendar_id,
            eventId=event_id,
        ).execute()
    except HttpError as e:
        if e.resp["status"] not in ["404", "410"]:
            raise e


@check_credentials_wrapper
def clear_calendar(calendar_id: str=CALENDAR_ID) -> None:
    if not calendar_id:
        return

    events_to_delete = []
    page_token = None
    while True:
        events = (
            get_service()
            .events()
            .list(calendarId=calendar_id, pageToken=page_token)
            .execute()
        )
        for event in events["items"]:
            events_to_delete.append(event["id"])
        page_token = events.get("nextPageToken")
        if not page_token:
            break

    for e in events_to_delete:
        get_service().events().delete(calendarId=calendar_id, eventId=e).execute()


def get_calendar_link(calendar_id: str=CALENDAR_ID) -> str:
    calendar_id_bytes = calendar_id.encode("utf-8")
    calendar_id_base64 = base64.b64encode(calendar_id_bytes)
    calendar_id = calendar_id_base64.decode().rstrip("=")

    link = SHARE_LINK_TEMPLATE.format(cid=calendar_id)
    return link


@check_credentials_wrapper
def create_personal_calendar() -> str:
    calendar = {
        "summary": "HKN RSVPs",
        "timeZone": TIMEZONE,
    }

    created_calendar = get_service().calendars().insert(body=calendar).execute()

    rule = {
        "scope": {
            "type": "default",
        },
        "role": "reader"
    }
    get_service().acl().insert(calendarId=created_calendar["id"], body=rule).execute()

    return created_calendar["id"]
