import os
from flask import url_for
import msal


class AuthenticationHandler:

    def __init__(self, app_config, cachefile):

        self.app_config = app_config
        self.cachefile = cachefile

    def load_cache(self):
        cache = msal.SerializableTokenCache()
        if os.path.exists(self.cachefile):
            cache.deserialize(open(self.cachefile, "r").read())
        return cache

    def save_cache(self, cache):
        open(self.cachefile, "w").write(cache.serialize())

    def build_msal_app(self, cache=None):
        return msal.ConfidentialClientApplication(
            self.app_config.CLIENT_ID, authority=self.app_config.AUTHORITY,
            client_credential=self.app_config.CLIENT_SECRET, token_cache=cache)


    def build_auth_code_flow(self):
        return self.build_msal_app().initiate_auth_code_flow(
            self.app_config.SCOPE or [],
            redirect_uri=url_for("authorized", _external=True))

    def get_token_from_cache(self):
        cache = self.load_cache()  # This web app maintains one cache per session
        cca = self.build_msal_app(cache=cache)
        accounts = cca.get_accounts()
        if accounts:  # So all account(s) belong to the current signed-in user
            result = cca.acquire_token_silent(scopes=self.app_config.SCOPE, account=accounts[0])
            self.save_cache(cache)
            return result
