import logging
from datetime import timedelta

import dateutil.parser
import requests


class GermanSchoolHolidays:

    def __init__(self):
        pass

    def query(self, start, end):

        results = self.__query_for_year(start[0:4])

        if start[0:4] != end[0:4]:
            results.extend(self.__query_for_year(end[0:4]))

        return [r for r in results if r['Date'] >= start and r['Date'] <= end]

    def __query_for_year(self, year):

        url = f"https://ferien-api.de/api/v1/holidays/BW/{year}"

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
