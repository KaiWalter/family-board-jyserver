from injector import Binder, singleton

from board import Board
from german_holidays import GermanPublicHolidays, GermanSchoolHolidays
from microsoft_graph import MicrosoftGraph, MicrosoftGraphAuthentication, MicrosoftGraphCalendar, MicrosoftGraphImages


def configure(binder:Binder) -> Binder:
    binder.bind(Board, to=Board, scope=singleton)
    binder.bind(MicrosoftGraphAuthentication, to=MicrosoftGraphAuthentication, scope=singleton)
    binder.bind(MicrosoftGraph, to=MicrosoftGraph, scope=singleton)
    binder.bind(MicrosoftGraphCalendar, to=MicrosoftGraphCalendar, scope=singleton)
    binder.bind(MicrosoftGraphImages, to=MicrosoftGraphImages, scope=singleton)
    binder.bind(GermanPublicHolidays, to=GermanPublicHolidays, scope=singleton)
    binder.bind(GermanSchoolHolidays, to=GermanSchoolHolidays, scope=singleton)
