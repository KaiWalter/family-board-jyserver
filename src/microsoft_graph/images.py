import logging

from injector import inject

import app_config
from microsoft_graph import MicrosoftGraph


class MicrosoftGraphImages:

    @inject
    def __init__(self, graph: MicrosoftGraph):

        self.graph = graph

    def query_images(self):
        images = self.graph.query(app_config.MSG_ENDPOINT_IMAGES).json()

        return images
