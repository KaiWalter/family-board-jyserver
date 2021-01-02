#!/usr/env/bin python3

import argparse
import logging
import os
import sys

import jyserver.Flask as jsf
import msal
import requests
from flask import Flask, redirect, render_template, request, session, url_for

import app_config
import board
from authentication import AuthenticationHandler
from flask_session import Session

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


@jsf.use(app)
class App:
    def __init__(self):
        pass

    @jsf.task
    def main(self):
        board.main_loop(self)


@app.route('/')
def index():
    App.main()
    return App.render(render_template('index.html'))


@app.route("/login")
def login():
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    session["flow"] = authentication_handler.build_auth_code_flow()
    return render_template("login.html", auth_url=session["flow"]["auth_uri"], version=msal.__version__)


# Its absolute URL must match your app's redirect_uri set in AAD
@app.route(app_config.REDIRECT_PATH)
def authorized():
    try:
        cache = authentication_handler.load_cache()
        result = authentication_handler.build_msal_app(cache=cache).acquire_token_by_auth_code_flow(
            session.get("flow", {}), request.args)
        if "error" in result:
            return render_template("error.html", result=result)
        authentication_handler.save_cache(cache)
    except ValueError:  # Usually caused by CSRF
        pass  # Simply ignore them
    return redirect(url_for("graphcall"))


@app.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("index", _external=True))


@app.route("/graphcall")
def graphcall():
    token = authentication_handler.get_token_from_cache()
    if not token:
        return redirect(url_for("login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config.ENDPOINT,
        headers={'Authorization': f'{token["token_type"]} {token["access_token"]}'}
    ).json()
    return render_template('display.html', result=graph_data)


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cachefile', required=False,
                        dest='cachefile', help='Name of cache file.', type=str, default='server_cache.bin')
    parser.add_argument('-o', '--logfile', required=False,
                        dest='logfile', help='Name of log file.', type=str, default='server.log')
    parser.add_argument('-a', '--ip', required=False,
                        dest='address', help='IP address to host on.', type=str, default='127.0.0.1')
    parser.add_argument('-p', '--port', required=False,
                        dest='port', help='Port to host on.', type=int, default=8080)
    args = parser.parse_args()

    return args


def print_info(message: str):
    print(message)
    logging.info(message)


if __name__ == "__main__":

    if app_config.CLIENT_ID and app_config.CLIENT_SECRET and app_config.AUTHORITY:

        # configuration
        args = parse_args()

        logging.basicConfig(
            filename=args.logfile, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        authentication_handler = AuthenticationHandler(
            app_config=app_config, cachefile=args.cachefile)

        app.jinja_env.globals.update(
            _build_auth_code_flow=authentication_handler.build_auth_code_flow)  # Used in template

        # main process
        print_info(f'hosting on http://{args.address}:{args.port}')
        app.run(host=args.address, port=args.port)

    else:
        sys.exit(1)
