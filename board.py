import time
import logging
import re

import requests
from injector import inject

import app_config
from authentication import AuthenticationHandler


class Board:

    @inject
    def __init__(self, authentication_handler: AuthenticationHandler):

        self.authentication_handler = authentication_handler

    def main_loop(self, app):
        while True:

            try:
                self.update_calendar(app)
            except Exception as Argument:
                logging.exception("update_calendar")

            app.js.dom.message.innerHTML = "..."
            time.sleep(15)

    def query_graph(self, endpoint, token):
        return requests.get(  # Use token to call downstream service
            endpoint,
            headers={
                'Authorization': f'{token["token_type"]} {token["access_token"]}'})

    def update_calendar(self, app):
        app.js.dom.message.innerHTML = "calendar refresh"
        app.js.dom.calendar.innerHTML = ""
        start_date = "2021-01-01"
        end_date = "2021-01-31"
        pattern = re.compile(app_config.CALENDAR_PATTERN)
        
        token = self.authentication_handler.get_token_from_cache()
        if not token:
            app.js.dom.calendar.innerHTML = "token not valid"
            return

        results = []

        calendars = self.query_graph(
            app_config.ENDPOINT, token).json()['value']

        for calendar in calendars:

            if pattern.match(calendar['name']):
                logging.info('query calendar %s', calendar['name'])

                calendar_entries = self.query_graph(
                    f"{app_config.ENDPOINT}/{calendar['id']}/calendarView?startDateTime={start_date}&endDateTime={end_date}&$select=subject,isAllDay,start,end", token).json()['value']

                for entry in calendar_entries:
                    results.append(entry)

        app.js.dom.calendar.innerHTML = str(len(results))
