from google_api.calendar import GoogleCalendar
from injector import Binder, singleton

from board import Board
from german_holidays import GermanPublicHolidays, GermanSchoolHolidays
from microsoft_graph import MicrosoftGraph, MicrosoftGraphAuthentication, MicrosoftGraphCalendar, MicrosoftGraphImages
from google_api import GoogleAuthenication, GoogleCalendar

def configure(binder:Binder) -> Binder:
    binder.bind(Board, to=Board, scope=singleton)
    binder.bind(MicrosoftGraphAuthentication, to=MicrosoftGraphAuthentication, scope=singleton)
    binder.bind(MicrosoftGraph, to=MicrosoftGraph, scope=singleton)
    binder.bind(MicrosoftGraphCalendar, to=MicrosoftGraphCalendar, scope=singleton)
    binder.bind(MicrosoftGraphImages, to=MicrosoftGraphImages, scope=singleton)
    binder.bind(GoogleAuthenication, to=GoogleAuthenication, scope=singleton)
    binder.bind(GoogleCalendar, to=GoogleCalendar, scope=singleton)
    binder.bind(GermanPublicHolidays, to=GermanPublicHolidays, scope=singleton)
    binder.bind(GermanSchoolHolidays, to=GermanSchoolHolidays, scope=singleton)
