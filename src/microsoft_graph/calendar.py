import logging
import re
from datetime import timedelta

import app_config
import dateutil.parser
from injector import inject
from models import AllDayCalendarEntry, CalendarEntry

from microsoft_graph import MicrosoftGraph


class MicrosoftGraphCalendar:

    @inject
    def __init__(self, graph: MicrosoftGraph):

        self.graph = graph

    def query_calendar(self, start, end):

        results = []

        pattern = re.compile(app_config.MSG_CALENDAR_PATTERN)

        calendars = self.graph.query(app_config.MSG_ENDPOINT_CALENDAR).json()

        is_primary = True

        for calendar in calendars['value']:

            if pattern.match(calendar['name']):
                logging.info('query calendar %s', calendar['name'])

                url = f"{app_config.MSG_ENDPOINT_CALENDAR}/{calendar['id']}/calendarView?startDateTime={start}&endDateTime={end}&$select=subject,isAllDay,start,end"

                calendar_entries = self.graph.query(url, additional_headers={
                                                    'Prefer': f'outlook.timezone="{app_config.CALENDAR_TIMEZONE}"'}).json()['value']

                for entry in calendar_entries:
                    if entry['isAllDay']:
                        current = dateutil.parser.isoparse(
                            entry['start']['dateTime'])
                        range_end = dateutil.parser.isoparse(
                            entry['end']['dateTime'])
                        while current < range_end:
                            results.append(AllDayCalendarEntry(description=entry['subject'], date=current.strftime(
                                '%Y-%m-%d'), is_primary=is_primary))
                            current = current + timedelta(days=1)
                    else:
                        results.append(CalendarEntry(description=entry['subject'], date=entry['start']['dateTime'][0:10], time=entry['start']['dateTime'][11:16], is_primary=is_primary))

                if is_primary:
                    is_primary = False

        return results
