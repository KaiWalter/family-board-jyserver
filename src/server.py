#!/usr/env/bin python3

import argparse
import locale
import logging
import os
import sys

import jyserver.Flask as jsf
from flask import (Flask, jsonify, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_injector import FlaskInjector
from injector import inject

import app_config
from board import Board
from dependencies import configure
from google_api import GoogleAuthenication
from microsoft_graph import MicrosoftGraphAuthentication

# initialize Flask session
app = Flask(__name__)

# Flask app
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


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


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


@app.route('/api/board/status', methods=['PUT'])
def put_board_status(board: Board):
    board.set_status(request.get_json())
    result = {'status': 'Ok'}
    return jsonify(result)


@app.route('/api/health', methods=['GET'])
def get_health():
    result = {'status': 'Ok'}
    return jsonify(result)


@inject
@app.route("/login")
def login(msg_auth_handler: MicrosoftGraphAuthentication, google_auth_handler: GoogleAuthenication):
    msg_auth_handler.build_auth_code_flow()
    msg_auth_url = msg_auth_handler.flow["auth_uri"]

    google_auth_url = google_auth_handler.endpoint()

    return render_template("login.html", msg_auth_url=msg_auth_url, google_auth_url=google_auth_url)


@inject
@app.route(app_config.MSG_REDIRECT_PATH)
def msg_authorized(msg_auth_handler: MicrosoftGraphAuthentication):
    try:
        cache = msg_auth_handler.load_cache()
        result = msg_auth_handler.build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            msg_auth_handler.flow, request.args)
        if "error" in result:
            return render_template("error.html", result=result)
        msg_auth_handler.save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("index"))


@inject
@app.route(app_config.GOOGLE_REDIRECT_PATH)
def google_authorized(google_auth_handler: GoogleAuthenication):
    google_auth_handler.create_token(request)
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
