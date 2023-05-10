from __future__ import print_function

import os.path
import re
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from game_release_calendar import Scraper

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
    finally:
        # Initialise scraper class and define url.
        url = 'https://gamerant.com/ps5-game-release-dates/'
        scraping = Scraper(url)
        scraping.scraper()

        # Create a calendar
        calendar = {
            'summary': 'PS5 Release Dates',
            'timeZone': 'Europe/London',
            'colorId': '18'
        }

        created_calendar = service.calendars().insert(body=calendar).execute()

        calendar_id = created_calendar['id']
        
        # Loop through <li> tags and add them to calendar.
        for date in scraping.li_tags:
            date, name = date.split(':')[0], date.split(':')[-1]
            if re.match(r'\w+\s\d{1,2}\s\d{4}', date):
                iso = datetime.strptime(date, '%B %d %Y').date()

            elif re.match(r'\w+\s\d{1,2},\s\d{4}', date):
                iso = datetime.strptime(date, '%B %d, %Y').date()

            elif re.match(r'\w+\s\d{1,2}\b', date):
                iso = datetime.strptime(f'{date} 2023', '%B %d %Y').date()

            else:
                continue

            event = {
                'summary': name,
                'start': {'date': iso.isoformat()},
                'end': {'date': iso.isoformat()},
            }

            service.events().insert(calendarId=calendar_id, body=event).execute()


if __name__ == '__main__':
    main()
