import datetime
import pickle
import os.path

from django.urls import reverse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import GoogleAuthError

from . import models

class InitError(Exception):
    pass

class GoogleCalendar:
    def __init__(self, token_path='./google_calendar_creds/token.pickle'):
        """
        Based on:
        https://developers.google.com/calendar/quickstart/python?authuser=3
        """
        if not os.path.exists(token_path):
            raise InitError(f"No token found at {token_path}")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        if creds.expired:
            if creds.refresh_token:
                try:
                    creds.refresh(Request())
                except GoogleAuthError:
                    raise InitError("Failed to refresh token")
        try:
            self.cal = build('calendar', 'v3', credentials=creds)
        except GoogleAuthError:
            raise InitError("Failed to build calendar")

    def delete_all(self):
        self.cal.calendars().clear(calendarId='primary').execute()
    
    def description(self, event):
        # TODO: Make this link not hardcoded
        link = "https://dev-hkn.eecs.berkeley.edu" + reverse('events:detail', kwargs={'id':event.id})
        rsvps = [rsvp.user.get_full_name() for rsvp in event.rsvp_set.all()]
        if rsvps:
            rsvps = ", ".join(rsvps)
        else:
            rsvps = None
        fields = [
            f'Description: {event.description}',
            f'Event Type: {event.event_type}',
            f'RSVP Limit: {event.rsvp_limit}',
            f'RSVPS: {rsvps}',
            f'View on <a href={link}>HKN website</a>',
        ]
        return '\n'.join(fields)

    def add_event(self, event):
        event = {
            'summary': event.name,
            'location': event.location,
            'description': self.description(event),
            'start': {
                'dateTime': event.start_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': event.end_time.isoformat(),
                'timeZone': 'America/Los_Angeles',
            }
        }
        self.cal.events().insert(calendarId='primary', body=event).execute()

    def add_all(self):
        for event in models.Event.objects.all():
            self.add_event(event)

def relative(path):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(file_dir, path)

def update():
    # TODO: Maybe save the calendar object somehow instead of recreating it every time
    try:
        cal = GoogleCalendar(relative('google_calendar_creds/token.pickle'))
    except InitError as e:
        # TODO: Replace with logging once we have it.
        print(f"Calendar update failed with error: {e}")
        return
    cal.delete_all()
    cal.add_all()