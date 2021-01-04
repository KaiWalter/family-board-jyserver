from injector import Scope, singleton

from board import Board
from german_public_holidays import GermanPublicHolidays
from german_school_holidays import GermanSchoolHolidays
from microsoft_graph import MicrosoftGraph
from microsoft_graph_authentication import AuthenticationHandler
from microsoft_graph_calendar import MicrosoftGraphCalendar
from microsoft_graph_images import MicrosoftGraphImages


def configure(binder):
    binder.bind(AuthenticationHandler, to=AuthenticationHandler, scope=singleton)
    binder.bind(Board, to=Board, scope=singleton)
    binder.bind(MicrosoftGraph, to=MicrosoftGraph, scope=singleton)
    binder.bind(MicrosoftGraphCalendar, to=MicrosoftGraphCalendar, scope=singleton)
    binder.bind(MicrosoftGraphImages, to=MicrosoftGraphImages, scope=singleton)
    binder.bind(GermanPublicHolidays, to=GermanPublicHolidays, scope=singleton)
    binder.bind(GermanSchoolHolidays, to=GermanSchoolHolidays, scope=singleton)
