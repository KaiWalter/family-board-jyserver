import logging
import random
import time
from datetime import date, timedelta

import dateutil.parser
from injector import inject

from german_holidays import GermanPublicHolidays, GermanSchoolHolidays
from microsoft_graph import MicrosoftGraphImages, MicrosoftGraphCalendar
from google_api import GoogleCalendar


class Board:

    @inject
    def __init__(self, graph_calendar: MicrosoftGraphCalendar, graph_images: MicrosoftGraphImages, google_calendar: GoogleCalendar, public_holidays: GermanPublicHolidays, school_holidays: GermanSchoolHolidays):

        self.graph_calendar = graph_calendar
        self.graph_images = graph_images
        self.google_calendar = google_calendar
        self.public_holidays = public_holidays
        self.school_holidays = school_holidays
        self.calendar_weeks = 3
        self.next_calendar_update_cycle = 0
        self.next_image_update_cycle = 0
        self.__message = ""
        self.__status = ""
        self.__presence = True

    def main_loop(self, app):

        while True:

            try:
                app.js.dom.status.innerHTML = self.__status
            except Exception as Argument:
                logging.exception("update_status")

            if self.__presence and self.next_calendar_update_cycle == 0:
                self.next_calendar_update_cycle = 7
                try:
                    self.__update_calendar(app)
                except Exception as Argument:
                    logging.exception("update_calendar")
            else:
                self.next_calendar_update_cycle -= 1

            if self.__presence and self.next_image_update_cycle == 0:
                self.next_image_update_cycle = 3
                try:
                    self.__update_image(app)
                except Exception as Argument:
                    logging.exception("update_image")
            else:
                self.next_image_update_cycle -= 1

            try:
                app.js.dom.message.innerHTML = self.__message
            except Exception as Argument:
                logging.exception("update_message")

            time.sleep(15)

    def refresh(self):
        self.next_calendar_update_cycle = 0
        self.next_image_update_cycle = 0

    def set_message(self, message):
        self.__message = message
        self.refresh()

    def set_status(self, payload):
        status = payload['status']
        presence = payload['presence']

        refresh = self.__presence != presence

        self.__status = status if status else ''
        self.__presence = presence

        if refresh:
            self.refresh()

    def __get_start_end_date(self):
        date_format = "%Y-%m-%d"
        today = date.today()
        start = today - timedelta(days=today.weekday())
        start_date = start.strftime(date_format)
        end = start + timedelta(days=(self.calendar_weeks*7)-1)
        end_date = end.strftime(date_format)
        return start, start_date, end, end_date

    def __query_images(self):
        return self.graph_images.query_images()

    def __update_image(self, app):
        app.js.dom.message.innerHTML = "image refresh"

        images_response = self.__query_images()

        if 'value' in images_response:
            images = images_response['value']

            selected_image_index = random.randint(0, len(images))

            selected_image = images[selected_image_index]
            download_url = selected_image['@microsoft.graph.downloadUrl']
            image_created = ""

            if 'photo' in selected_image:
                photo = selected_image['photo']
                if 'takenDateTime' in photo:
                    image_created = dateutil.parser.isoparse(
                        photo['takenDateTime']).strftime('%b %Y')

            app.js.dom.image.src = download_url
            app.js.dom.image.alt = image_created

    def __query_calendars(self):
        results = []

        _, start_date, _, end_date = self.__get_start_end_date()

        results = []

        try:
            results.extend(self.school_holidays.query(
                start=start_date, end=end_date))
        except Exception as Argument:
            logging.exception("school_holidays")

        try:
            results.extend(self.public_holidays.query(
                start=start_date, end=end_date))
        except Exception as Argument:
            logging.exception("school_holidays")

        try:
            results.extend(self.graph_calendar.query_calendar(
                start=start_date, end=end_date))
        except Exception as Argument:
            logging.exception("graph_calendar")

        try:
            results.extend(self.google_calendar.query_calendar(
                start=start_date, end=end_date))
        except Exception as Argument:
            logging.exception("google_calendar")

        return results

    def __update_calendar(self, app):
        app.js.dom.message.innerHTML = "calendar refresh"

        calendar_entries = sorted(self.__query_calendars(),
                                  key=lambda k: (k.date, k.time))

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

            day_class = 'today' if date.today() == current_day else 'day'

            day_title = "<span class='monthofyear'>" + month_title + "</span><br/>"
            day_title += "<span class='dayofweek'>" + \
                current_day.strftime("%a") + "</span>&nbsp;"
            day_title += "<span class='dayofmonth'>" + \
                current_day.strftime("%d") + "</span>"

            day_content = ""

            # render all day events on top
            for calendar_entry in calendar_entries:
                if calendar_entry.date == current_day_compare and calendar_entry.all_day:
                    if calendar_entry.public_holiday:
                        day_content += "<div class='public_holiday_day'>" + \
                            calendar_entry.description + "</div>"
                    elif calendar_entry.school_holiday:
                        day_content += "<div class='school_holiday_day'>" + \
                            calendar_entry.description + "</div>"
                    else:
                        ext_class = 'primary_calendar' if calendar_entry.is_primary else 'secondary_calendar'
                        day_content += f"<div class='all_day {ext_class}'>" + \
                            calendar_entry.description + "</div>"

            # render other events below
            for calendar_entry in calendar_entries:
                if calendar_entry.date == current_day_compare and not calendar_entry.all_day:
                    day_content += "<div class='single_event primary_calendar'>" + \
                        calendar_entry.time + "&nbsp;" + \
                        calendar_entry.description + "</div>"

            html += f"<div id='day{i}' class='{day_class}'><div id='dayHeader'><div class='day_title'>{day_title}</div></div><div id='dayContent'>{day_content}</div></div>"

        app.js.dom.calendar.innerHTML = html
