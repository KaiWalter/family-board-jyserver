#!/usr/env/bin python3

import argparse
import json
import locale
import logging
import sys

import jyserver.Flask as jsf
import msal
import requests
from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)
from flask_injector import FlaskInjector
from injector import inject

import app_config
from board import Board
from dependencies import configure
from flask_session import Session
from microsoft_graph_authentication import AuthenticationHandler

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


@jsf.use(app)
class App:
    def __init__(self):
        pass

    @jsf.task
    def main(self, board: Board):
        board.main_loop(self)


@inject
@app.route('/')
def index(board: Board):
    App.main(board)
    return App.render(render_template('index.html'))


@app.route('/api/board/refresh', methods=['POST'])
def refresh_board(board: Board):
    board.refresh()
    result = {'status': 'Ok'}
    return jsonify(result)


@app.route('/api/board/message', methods=['PUT'])
def put_board_message(board: Board):
    payload = request.get_json()
    if 'message' in payload:
        board.set_message(payload['message'])
    result = {'status': 'Ok'}
    return jsonify(result)


@inject
@app.route("/login")
def login(authentication_handler: AuthenticationHandler):
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = authentication_handler.build_auth_code_flow()
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)


# Its absolute URL must match your app's redirect_uri set in AAD
@inject
@app.route(app_config.MSG_REDIRECT_PATH)
def authorized(authentication_handler: AuthenticationHandler):
    try:
        cache = authentication_handler.load_cache()
        result = authentication_handler.build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("error.html", result=result)
        authentication_handler.save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))


@inject
@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.MSG_AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--logfile', required=False,
                        dest='logfile', help='Name of log file.', type=str, default='server.log')
    parser.add_argument('-a', '--ip', required=False,
                        dest='address', help='IP address to host on.', type=str, default='127.0.0.1')
    parser.add_argument('-p', '--port', required=False,
                        dest='port', help='Port to host on.', type=int, default=8080)
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    args = parser.parse_args()

    return args


def print_info(message: str):
    print(message)
    logging.info(message)


if __name__ == "__main__":

    if app_config.MSG_CLIENT_ID and app_config.MSG_CLIENT_SECRET and app_config.MSG_AUTHORITY:

        # configuration
        args = parse_args()

        logging.basicConfig(
            filename=args.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=args.loglevel)

        locale.setlocale(locale.LC_ALL, app_config.MSG_LOCALE)

        FlaskInjector(app=app, modules=[configure])

        # main process
        print_info(f'hosting on http://{args.address}:{args.port}')
        app.run(host=args.address, port=args.port)

    else:
        sys.exit(1)
