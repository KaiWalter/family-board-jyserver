import requests

import app_config


class GermanPublicHolidays:

    def __init__(self):
        pass

    def query(self, start, end):

        results = self.__query_for_year(start[0:4])

        # when spanning 2 years get both holiday calendars
        if start[0:4] != end[0:4]:
            results.extend(self.__query_for_year(end[0:4]))

        return [r for r in results if r['Date'] >= start and r['Date'] <= end]

    def __query_for_year(self, year):

        url = f"https://feiertage-api.de/api/?nur_land={app_config.GERMAN_STATE}&jahr={year}"

        results = requests.get(url).json()

        calendar_entries = []

        for key, value in results.items():
            calendar_entry = {
                'Description': key,
                'Date': value['datum'],
                'Time': None,
                'AllDayEvent': True,
                'SchoolHoliday': False,
                'PublicHoliday': True
            }

            calendar_entries.append(calendar_entry)

        return calendar_entries
