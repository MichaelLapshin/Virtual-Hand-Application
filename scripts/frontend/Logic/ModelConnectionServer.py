"""
    [ModelConnectionServer.py]
    Program that hosts a UDP server to host the models.
"""

import socket
import socketserver
import threading

from scripts import Log, Constants, Warnings


class ModelServer(socketserver.UDPServer):

    def __init__(self, server_address=Constants.MODEL_SERVER_HOST, port=Constants.MODEL_SERVER_PORT):
        socketserver.UDPServer.__init__(self, server_address=(server_address, port), RequestHandlerClass=None)

        self._running = False
        self._models = []
        self._thread = None

        Log.info("Created a Model Server.")

    def connect(self, models_dir_path, progress_bar):
        """
        Loads the models and starts the server
        :param model_id:
        :return:
        """

        # Loads in the models

        self._running = True
        self._thread = threading.Thread(target=self.run)
        self._thread.start()

    def disconnect(self):
        """
        Disconnects and stops the server.
        :return:
        """

        self._running = False

    def run(self):
        Warnings.not_complete()

    def handle_timeout(self):
        super().handle_timeout()
        Warnings.not_complete()

    def handle_request(self):
        super().handle_request()
        Warnings.not_complete()
