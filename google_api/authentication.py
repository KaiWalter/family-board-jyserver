import json
import os

import app_config
import requests
from flask import url_for
from oauthlib.oauth2 import WebApplicationClient
from requests.sessions import Request

# from: https://realpython.com/flask-google-login/#creating-your-own-web-application
# from: https://developers.google.com/calendar/quickstart/python

class GoogleAuthenication:

    def __init__(self):
        self.client = WebApplicationClient(app_config.GOOGLE_CLIENT_ID)

        if os.path.exists(app_config.GOOGLE_CACHE_FILE):
            token_str = open(app_config.GOOGLE_CACHE_FILE, "r").read()
            self.client.parse_request_body_response(token_str)

        self.google_provider_cfg = requests.get(
            app_config.GOOGLE_DISCOVERY_URL).json()

    def endpoint(self):
        authorization_endpoint = self.google_provider_cfg["authorization_endpoint"]

        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=url_for("google_authorized", _external=True),
            scope=app_config.GOOGLE_SCOPE
        )

        return request_uri

    def create_token(self, request:Request):
        code = request.args.get("code")

        token_endpoint = self.google_provider_cfg["token_endpoint"]

        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(app_config.GOOGLE_CLIENT_ID,
                  app_config.GOOGLE_CLIENT_SECRET),
        )

        token_str = json.dumps(token_response.json())

        self.client.parse_request_body_response(token_str)

        open(app_config.GOOGLE_CACHE_FILE, "w").write(token_str)

        return 

