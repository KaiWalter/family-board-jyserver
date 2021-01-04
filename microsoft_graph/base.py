import logging

import requests
from injector import inject

import app_config
from microsoft_graph import MicrosoftGraphAuthentication


class MicrosoftGraph:

    @inject
    def __init__(self, authentication_handler: MicrosoftGraphAuthentication):

        self.authentication_handler = authentication_handler


    def query(self, url, additional_headers=None):

        self.__update_token()

        result = None

        if self.token:

            headers = {
                'Authorization': f'{self.token["token_type"]} {self.token["access_token"]}'
            }

            if additional_headers:
                headers.update(additional_headers)

            result = requests.get(url, headers=headers)
        
        return result

    def __update_token(self):
        self.token = None
        self.token = self.authentication_handler.get_token_from_cache()
        if not self.token:
            logging.error('token not updated')

