from injector import singleton

from authentication import AuthenticationHandler
from board import Board


def configure(binder):
    binder.bind(AuthenticationHandler, to=AuthenticationHandler, scope=singleton)
    binder.bind(Board, to=Board, scope=singleton)
