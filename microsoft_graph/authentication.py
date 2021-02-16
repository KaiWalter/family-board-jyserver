import os

import msal
from flask import url_for

import app_config


class MicrosoftGraphAuthentication:

    def __init__(self):
        pass

    def load_cache(self):
        cache = msal.SerializableTokenCache()
        if os.path.exists(app_config.MSG_CACHE_FILE):
            cache.deserialize(open(app_config.MSG_CACHE_FILE, "r").read())
        return cache

    def save_cache(self, cache):
        open(app_config.MSG_CACHE_FILE, "w").write(cache.serialize())

    def build_msal_app(self, cache=None):
        return msal.ConfidentialClientApplication(
            app_config.MSG_CLIENT_ID, authority=app_config.MSG_AUTHORITY,
            client_credential=app_config.MSG_CLIENT_SECRET, token_cache=cache)

    def build_auth_code_flow(self):
        self.flow = self.build_msal_app().initiate_auth_code_flow(
            app_config.MSG_SCOPE or [],
            redirect_uri=url_for("msg_authorized", _external=True))

    def get_token_from_cache(self):
        cache = self.load_cache()  # This web app maintains one cache per session
        cca = self.build_msal_app(cache=cache)
        accounts = cca.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            result = cca.acquire_token_silent(
                scopes=app_config.MSG_SCOPE, account=accounts[0])
            self.save_cache(cache)
            return result
