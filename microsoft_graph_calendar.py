import logging
import re
from datetime import date, timedelta

import dateutil.parser
from injector import inject

import app_config
from microsoft_graph import MicrosoftGraph


class MicrosoftGraphCalendar:

    @inject
    def __init__(self, graph: MicrosoftGraph):

        self.graph = graph

    def query_calendar(self, start, end):

        results = []

        pattern = re.compile(app_config.CALENDAR_PATTERN)

        calendars = self.graph.query(app_config.ENDPOINT_CALENDAR).json()

        isPrimary = True

        for calendar in calendars['value']:

            if pattern.match(calendar['name']):
                logging.info('query calendar %s', calendar['name'])

                url = f"{app_config.ENDPOINT_CALENDAR}/{calendar['id']}/calendarView?startDateTime={start}&endDateTime={end}&$select=subject,isAllDay,start,end"

                calendar_entries = self.graph.query(url, additional_headers={
                                                    'Prefer': f'outlook.timezone="{app_config.CALENDAR_TIMEZONE}"'}).json()['value']

                for entry in calendar_entries:
                    calendar_entry = {
                        'Description': entry['subject'],
                        'Date': entry['start']['dateTime'][0:10],
                        'Time': None,
                        'IsPrimary': isPrimary,
                        'AllDayEvent': entry['isAllDay'],
                        'SchoolHoliday': False,
                        'PublicHoliday': False
                    }

                    if entry['isAllDay']:
                        current = dateutil.parser.isoparse(
                            entry['start']['dateTime'])
                        end = dateutil.parser.isoparse(
                            entry['start']['dateTime'])
                        while current <= end:
                            calendar_entry['Date'] = current.strftime(
                                '%Y-%m-%d')
                            current = current + timedelta(days=1)
                            results.append(calendar_entry)
                    else:
                        calendar_entry['Time'] = entry['start']['dateTime'][11:16]
                        results.append(calendar_entry)

                    if isPrimary:
                        isPrimary = False

        return results
