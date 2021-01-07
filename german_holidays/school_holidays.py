from datetime import timedelta
from types import prepare_class

import app_config
import dateutil.parser
import requests
from models import SchoolHolidayDayCalendarEntry


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

        return [r for r in results if r.date >= start and r.date <= end]

    def __query_for_year(self, year):

        url = f"https://ferien-api.de/api/v1/holidays/{app_config.GERMAN_STATE}/{year}"

        results = requests.get(url).json()

        calendar_entries = []

        for result in results:
            current = dateutil.parser.isoparse(result['start'])
            end = dateutil.parser.isoparse(result['end'])
            while current <= end:
                calendar_entries.append(SchoolHolidayDayCalendarEntry(description=str(result['name']).capitalize(), date=current.strftime('%Y-%m-%d')))
                current = current + timedelta(days=1)

        return calendar_entries
