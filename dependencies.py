from injector import singleton

from authentication import AuthenticationHandler
from board import Board
from microsoft_graph import MicrosoftGraph
from microsoft_graph_calendar import MicrosoftGraphCalendar
from microsoft_graph_images import MicrosoftGraphImages


def configure(binder):
    binder.bind(AuthenticationHandler, to=AuthenticationHandler, scope=singleton)
    binder.bind(Board, to=Board, scope=singleton)
    binder.bind(MicrosoftGraph, to=MicrosoftGraph, scope=singleton)
    binder.bind(MicrosoftGraphCalendar, to=MicrosoftGraphCalendar, scope=singleton)
    binder.bind(MicrosoftGraphImages, to=MicrosoftGraphImages, scope=singleton)
