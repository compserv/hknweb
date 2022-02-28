import json, base64, datetime

import google.oauth2.service_account as service_account
from googleapiclient.discovery import build

from hknweb.events.models.google_calendar_credentials import GoogleCalendarCredentials


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


def create_event(
    summary: str,
    location: str,
    description: str,
    start: str,
    end: str,
) -> str:
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
            calendarId=CALENDAR_ID,
            body=event_resource,
        )
        .execute()
    )

    return event["id"]


def update_event(event_id: str, **kwargs) -> None:
    event_resource = create_event_resource(**kwargs)

    get_service().events().patch(
        calendarId=CALENDAR_ID,
        eventId=event_id,
        body=event_resource,
    ).execute()


def delete_event(event_id: str) -> None:
    get_service().events().delete(
        calendarId=CALENDAR_ID,
        eventId=event_id,
    ).execute()


def clear_calendar() -> None:
    events_to_delete = []
    page_token = None
    while True:
        events = (
            get_service()
            .events()
            .list(calendarId=CALENDAR_ID, pageToken=page_token)
            .execute()
        )
        for event in events["items"]:
            events_to_delete.append(event["id"])
        page_token = events.get("nextPageToken")
        if not page_token:
            break

    for e in events_to_delete:
        get_service().events().delete(calendarId=CALENDAR_ID, eventId=e).execute()


def get_calendar_link() -> None:
    calendar_id = CALENDAR_ID
    calendar_id_bytes = calendar_id.encode("utf-8")
    calendar_id_base64 = base64.b64encode(calendar_id_bytes)
    calendar_id = calendar_id_base64.decode().rstrip("=")

    link = SHARE_LINK_TEMPLATE.format(cid=calendar_id)
    return link
