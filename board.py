import logging
import re
import time
from datetime import datetime, date, timedelta
import dateutil.parser

import requests
from injector import InstanceProvider, inject

import app_config
from authentication import AuthenticationHandler


class Board:

    @inject
    def __init__(self, authentication_handler: AuthenticationHandler):

        self.token = None
        self.authentication_handler = authentication_handler
        self.calendar_weeks = 3

    def main_loop(self, app):
        while True:

            try:
                self.update_calendar(app)
            except Exception as Argument:
                logging.exception("update_calendar")

            app.js.dom.message.innerHTML = "..."
            time.sleep(15)

    def query_graph(self, endpoint, token):

        headers = {
            'Authorization': f'{token["token_type"]} {token["access_token"]}',
            'Prefer': f'outlook.timezone="{app_config.CALENDAR_TIMEZONE}"'
        }

        return requests.get(endpoint, headers=headers)

    def __get_start_end_date(self):
        date_format = "%Y-%m-%d"
        today = date.today()
        start = today - timedelta(days=today.weekday())
        start_date = start.strftime(date_format)
        end = start + timedelta(days=(self.calendar_weeks*7)-1)
        end_date = end.strftime(date_format)
        return start, start_date, end, end_date

    def __update_token(self):
        self.token = None
        self.token = self.authentication_handler.get_token_from_cache()

    def __query_calendars(self):
        results = []

        _, start_date, _, end_date = self.__get_start_end_date()
        pattern = re.compile(app_config.CALENDAR_PATTERN)

        calendars = self.query_graph(
            app_config.ENDPOINT, self.token).json()

        isPrimary = True

        for calendar in calendars['value']:

            if pattern.match(calendar['name']):
                logging.info('query calendar %s', calendar['name'])

                calendar_entries = self.query_graph(
                    f"{app_config.ENDPOINT}/{calendar['id']}/calendarView?startDateTime={start_date}&endDateTime={end_date}&$select=subject,isAllDay,start,end", self.token).json()['value']

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
                        current = dateutil.parser.isoparse(entry['start']['dateTime'])
                        end = dateutil.parser.isoparse(entry['start']['dateTime'])
                        while current <= end:
                            calendar_entry['Date'] = current.strftime('%Y-%m-%d')
                            current = current + timedelta(days=1)
                            results.append(calendar_entry)
                    else:
                        calendar_entry['Time'] = entry['start']['dateTime'][11:16]
                        results.append(calendar_entry)

                    if isPrimary:
                        isPrimary = False

        return results

    def update_calendar(self, app):
        app.js.dom.message.innerHTML = "calendar refresh"
        app.js.dom.calendar.innerHTML = ""

        self.__update_token()
        if not self.token:
            app.js.dom.calendar.innerHTML = "token not valid"
            return

        calendar_entries = sorted(self.__query_calendars(),
                         key=lambda k: (k['Date'], k['Time']))

        start, _, end, _ = self.__get_start_end_date()

        html = ""

        for i in range(0, (self.calendar_weeks*7)):
            current_day = start + timedelta(days=i)
            current_day_compare = current_day.strftime('%Y-%m-%d')
            wd = current_day.weekday()

            if wd == 0:  # generate week number
                html += f"<div class='week_title'><br/><span class='weekofyear'>{current_day.isocalendar()[1]}</span></div>"

            if i == 0 or current_day.day == 1:
                month_title = current_day.strftime("%b")
            else:
                month_title = ""

            day_title = "<span class='monthofyear'>" + month_title + "</span><br/>"
            day_title += "<span class='dayofweek'>" + \
                current_day.strftime("%a") + "</span>&nbsp;"
            day_title += "<span class='dayofmonth'>" + \
                current_day.strftime("%d") + "</span>"

            day_content = ""

            # render all day events on top
            for calendar_entry in calendar_entries:
                if calendar_entry['Date'] == current_day_compare and calendar_entry['AllDayEvent']:
                    if calendar_entry['PublicHoliday']:
                        day_content += "<div class='public_holiday_day'>" + calendar_entry['Description'] + "</div>"
                    elif calendar_entry['SchoolHoliday']:
                        day_content += "<div class='school_holiday_day'>" + calendar_entry['Description'] + "</div>"
                    else:
                        ext_class = 'primary_calendar' if calendar_entry['IsPrimary'] else 'secondary_calendar'
                        day_content += f"<div class='all_day {ext_class}'>" + calendar_entry['Description'] + "</div>"

            # render other events below
            for calendar_entry in calendar_entries:
                if calendar_entry['Date'] == current_day_compare and not calendar_entry['AllDayEvent']:
                    day_content += "<div class='single_event primary_calendar'>" + calendar_entry['Time'] + "&nbsp;" + calendar_entry['Description'] + "</div>"

            html += f"<div id='day{i}' class='day'><div id='dayHeader'><div class='day_title'>{day_title}</div></div><div id='dayContent'>{day_content}</div></div>"

        app.js.dom.calendar.innerHTML = html
