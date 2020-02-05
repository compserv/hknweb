#!/usr/bin/env python3
import datetime
import pickle
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def generate_token(token_path='./token.pickle', credential_path='./credentials.json'):
    """
    Based on:
    https://developers.google.com/calendar/quickstart/python?authuser=3

    What this script does is refresh the Google Calendar authentication token
    that is needed to update the calendar.
    
    How to Use:
    Open the https://developers.google.com/calendar/quickstart/python tutorial.
    (1) Follow step 1 and download credentials.json to this directory.
    (2) Run this script. It should pop up in a browser window.
    (3) Select the google account you want for calendar and authorize.
        THIS SHOULD NOT BE YOUR PERSONAL EMAIL OR ANY EMAIL WITH EXISTING
        CALENDAR DATA -- THE CALENDAR WILL BE DELETED AND OVERWRITTEN WITH
        THE HKN CALENDAR!!!
    The `token.pickle` will be saved in this folder. You can then scp it
    over to the server. Put it in the same directory
    (hknweb/events/google_calendar_creds/token.pickle) and the server should
    be able to update Google Calendar now.
    """
    creds = None
    print("Checking token status...")
    if os.path.exists(token_path):
        print("Token exists. Checking...")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
        if creds.valid:
            print("Token OK!")
            return
    if creds and creds.expired and creds.refresh_token:
        print("Token expired. Refreshing...")
        creds.refresh(Request())
    else:
        print("No valid token existed. Generating...")
        if not os.path.exists(credential_path):
            print(f"ERROR: No credentials file at {credential_path}")
            return
        flow = InstalledAppFlow.from_client_secrets_file(
            credential_path,
            ['https://www.googleapis.com/auth/calendar',
             'https://www.googleapis.com/auth/calendar.events'])
        creds = flow.run_local_server(port=0)
    print("Writing token...")
    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)
        print(f"Token written to {token_path}")

def main():
    generate_token()

if __name__ == "__main__":
    main()