import os
import pickle

import app_config
import requests
from flask import url_for
from google_auth_oauthlib.flow import Flow
from googleapiclient.http import build_http
from oauthlib.oauth2 import WebApplicationClient
from requests.sessions import Request

from google_api import ClientConfigBuilder

# from: https://realpython.com/flask-google-login/#creating-your-own-web-application
# from: https://developers.google.com/calendar/quickstart/python

class GoogleAuthenication:

    def __init__(self):
        self.client = WebApplicationClient(app_config.GOOGLE_CLIENT_ID)

        if os.path.exists(app_config.GOOGLE_CACHE_FILE):
            with open(app_config.GOOGLE_CACHE_FILE, 'rb') as token:
                self.creds = pickle.load(token)

        self.google_provider_cfg = requests.get(
            app_config.GOOGLE_DISCOVERY_URL).json()

    def endpoint(self):
        authorization_endpoint = self.google_provider_cfg["authorization_endpoint"]

        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=url_for("google_authorized", _external=True),
            access_type='offline',
            scope=app_config.GOOGLE_SCOPE
        )

        return request_uri

    def create_token(self, request: Request):
        code = request.args.get("code")

        client_config = ClientConfigBuilder(
            client_type=ClientConfigBuilder.CLIENT_TYPE_WEB,
            client_id=app_config.GOOGLE_CLIENT_ID,
            client_secret=app_config.GOOGLE_CLIENT_SECRET,
            auth_uri=self.google_provider_cfg["authorization_endpoint"],
            token_uri=self.google_provider_cfg["token_endpoint"])

        flow = Flow.from_client_config(
            client_config=client_config.Build(),
            scopes=app_config.GOOGLE_SCOPE,
            redirect_uri=request.base_url)

        flow.fetch_token(code=code)

        self.creds = flow.credentials

        with open(app_config.GOOGLE_CACHE_FILE, 'wb') as token:
            pickle.dump(self.creds, token)

        return

    def get_creds(self):

        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())

        return self.creds
