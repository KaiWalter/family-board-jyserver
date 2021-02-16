from datetime import timedelta

import app_config
import dateutil.parser
from googleapiclient.discovery import build
from injector import inject
from models import AllDayCalendarEntry, CalendarEntry

from google_api import GoogleAuthenication


class GoogleCalendar:

    @inject
    def __init__(self, auth: GoogleAuthenication):

        self.auth = auth

    def query_calendar(self, start, end):

        results = []

        creds = self.auth.creds
        service = build('calendar', 'v3', credentials=creds,
                        cache_discovery=False)

        time_min = start + "T00:00:00Z"
        time_max = end + "T23:59:59Z"

        events_result = service.events().list(calendarId='primary', timeMin=time_min, timeMax=time_max,
                                              singleEvents=True, showDeleted=False, timeZone=app_config.CALENDAR_TIMEZONE,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])

        for event in events:

            if 'dateTime' in event['start'] and 'dateTime' in event['end']:
                results.append(CalendarEntry(description=event['summary'], date=event['start']
                                             ['dateTime'][0:10], time=event['start']['dateTime'][11:16], is_primary=False))
            elif 'date' in event['start'] and 'date' in event['end']:
                current = dateutil.parser.parse(
                    event['start']['date'])
                range_end = dateutil.parser.parse(
                    event['end']['date'])
                while current < range_end:
                    results.append(AllDayCalendarEntry(description=event['summary'], date=current.strftime(
                        '%Y-%m-%d'), is_primary=False))
                    current = current + timedelta(days=1)

        return results
