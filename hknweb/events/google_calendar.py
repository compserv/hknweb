import datetime
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from . import models

class GoogleCalendar:
    def __init__(self, token_path, credential_path):
        """
        Based on:
        https://developers.google.com/calendar/quickstart/python?authuser=3
        """
        creds = None
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credential_path,
                    ['https://www.googleapis.com/auth/calendar',
                    'https://www.googleapis.com/auth/calendar.events'])
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.cal = build('calendar', 'v3', credentials=creds)

    def delete_all(self):
        self.cal.calendars().clear(calendarId='primary').execute()
    
    def description(self, event):
        rsvps = [rsvp.user.get_full_name() for rsvp in event.rsvp_set.all()]
        if rsvps:
            rsvps = ", ".join(rsvps)
        else:
            rsvps = None
        fields = {
            'Description': event.description,
            'Event Type': event.event_type,
            'RSVP Limit': event.rsvp_limit,
            'RSVPS': rsvps
        }
        return '\n'.join([f'{k}: {v}' for k, v in fields.items()])

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

def update():
    # Change this if you want to store the token and credentials somewhere else
    cal = GoogleCalendar('./google_calendar/token.pickle', './google_calendar/credentials.json')
    cal.delete_all()
    cal.add_all()