from datetime import timedelta
from types import prepare_class

import dateutil.parser
import requests

import app_config


class GermanSchoolHolidays:

    def __init__(self):
        pass

    def query(self, start, end):

        results = self.__query_for_year(start[0:4])

        # when spanning 2 years get both holiday calendars
        if start[0:4] != end[0:4]:
            results.extend(self.__query_for_year(end[0:4]))

        # while in January get also December holiday
        if start[5:7] == '01':
            previous_year = str(int(start[0:4])-1)
            results.extend(self.__query_for_year(previous_year))

        return [r for r in results if r['Date'] >= start and r['Date'] <= end]

    def __query_for_year(self, year):

        url = f"https://ferien-api.de/api/v1/holidays/{app_config.GERMAN_STATE}/{year}"

        results = requests.get(url).json()

        calendar_entries = []

        for result in results:
            calendar_entry = {
                'Description': str(result['name']).capitalize(),
                'Time': None,
                'AllDayEvent': True,
                'SchoolHoliday': True,
                'PublicHoliday': False
            }

            current = dateutil.parser.isoparse(result['start'])
            end = dateutil.parser.isoparse(result['end'])
            while current <= end:
                calendar_entry_instance = calendar_entry.copy()
                calendar_entry_instance['Date'] = current.strftime('%Y-%m-%d')
                current = current + timedelta(days=1)
                calendar_entries.append(calendar_entry_instance)

        return calendar_entries
