from google_api import GoogleAuthenication
from injector import inject
from models import AllDayCalendarEntry, CalendarEntry

class GoogleCalendar:

    @inject
    def __init__(self, auth: GoogleAuthenication):

        self.auth = auth

    def query_calendar(self, start, end):

        results = []

        return results