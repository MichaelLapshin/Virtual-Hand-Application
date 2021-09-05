"""
[ServerApp.py]
@description: In charge of the connections between client GUI and server database
@author: Michael Lapshin
"""

# Import common libraries
import os
import threading
import time

import flask

# Import REST API scripts

from API_Helper import package, flarg
from AccountAPI import account_api
from FileTransferAPI import file_transfer_api
from DataProcessingAPI import data_processing_api
from DataFetchingAPI import data_fetching_api
from DataUpdatingAPI import data_updating_api

# Import miscellaneous scripts
from scripts import Log, Constants, Warnings
from scripts.backend.database import Database, DatabaseAccounts

# Database
from scripts.logic import Worker

# Questionnaire for the server setup


HOST = "127.0.0.1"
PORT = 5000
start_server = Database.connect("server_database.db")
Database.create_all_new_tables(replace=False)

# Create the Admin user (if does not already exist)
exists_admin = DatabaseAccounts.exists_user_by_name(user_name=Constants.ADMIN_USER_NAME) \
               and DatabaseAccounts.check_user(user_name=Constants.ADMIN_USER_NAME, password=Constants.ADMIN_PASSWORD)
if exists_admin is False:
    DatabaseAccounts.add_user(user_name=Constants.ADMIN_USER_NAME, password=Constants.ADMIN_PASSWORD,
                              permission=Constants.PERMISSION_LEVELS.get(Constants.PERMISSION_ADMIN))


# class ConsoleReader(threading.Thread):
#     def __init__(self, stop_processes_command):
#         threading.Thread.__init__(self)
#         self._stop_processes_command = stop_processes_command
#         self._running = False
#         self.daemon = True
#         self._stopped = True
#
#     def run(self):
#         self._stopped = False
#         while self._running is True:
#             inp = input()
#             if inp.lower() == "stop" or inp.lower() == "shutdown":
#                 # requests.get(HOST + ":" + str(PORT) + "/shutdown"
#                 print("[ServerApp] Stopping the processes.")
#                 self._stop_processes_command()
#                 print("[ServerApp] All processes have been stopped.")
#                 print("[ServerApp] You may now stop the (flask) server.")
#             else:
#                 print("[ServerApp] Did not recognize the command.")
#             time.sleep(3)
#         self._stopped = True
#         Log.info("The  console reader thread has stopped.")
#
#     def start(self):
#         Log.info("Starting the console reader thread...")
#         self._running = True
#         super().start()
#
#     def stop(self):
#         Log.info("Stopping the console reader thread...")
#         self._running = False
#
#     """
#         Getters
#     """
#
#     def is_running(self):
#         return self._running
#
#     def is_stopped(self):
#         return self._stopped


def stop_processes():
    # Stops the console reader
    # if console_reader is not None:
    #     console_reader.stop()
    #     while console_reader.is_stopped() is False:
    #         time.sleep(1)

    # Stops the worker
    if Worker.worker is not None:
        Worker.worker.stop()

    # Waits until the workers are done their tasks
    while Worker.worker.is_stopped() is False:
        time.sleep(1)

    # Disconnects the database
    Database.disconnect()


if start_server:

    # Flask application + configurations
    Log.info("Starting the server...")
    server_app = flask.Flask(__name__)
    server_app.config['SECRET_KEY'] = os.urandom(16)  # Random secret key
    server_app.register_blueprint(account_api, url_prefix="/account")
    server_app.register_blueprint(file_transfer_api, url_prefix="/transfer")
    server_app.register_blueprint(data_processing_api, url_prefix="/process")
    server_app.register_blueprint(data_fetching_api, url_prefix="/fetch")
    server_app.register_blueprint(data_updating_api, url_prefix="/update")

    # Create console reader
    # console_reader = ConsoleReader(stop_processes)
    # console_reader.start()

    # Creates & starts the worker thread
    Worker.worker = Worker.Worker()
    Worker.worker.start()

    if __name__ == "__main__":
        server_app.run(host=HOST, port=PORT, threaded=True)

"""
    Flask REST API
"""


class ShutDown(threading.Thread):
    """
        For shutting down the flask server.
    """

    def __init__(self, shutdown_func, delay_s=0):
        threading.Thread.__init__(self)
        self.shutdown_func = shutdown_func
        self.delay_s = delay_s

        # Thread
        self.daemon = True
        self.start()

    def run(self):
        time.sleep(self.delay_s)

        # Shuts down the flask server
        if self.shutdown_func is None:
            raise RuntimeError('Not running werkzeug')
        self.shutdown_func()


@server_app.route('/shutdown')
def shutdown():
    Log.debug("Received request to shutdown the server...")
    user_id = int(flarg("user_id"))

    if user_id == DatabaseAccounts.get_user_id(user_name=Constants.ADMIN_USER_NAME, password=Constants.ADMIN_PASSWORD):
        Log.info("Shutting down the server...")

        stop_processes()

        # Shutting down the flask server
        ShutDown(shutdown_func=flask.request.environ.get('werkzeug.server.shutdown'), delay_s=0)

        return package(True, "Shutting down the server...")
    else:
        return package(False, "Could not shutdown the server. The current user is not the Administrator.")


@server_app.route('/is_online')
def is_online():
    return package(True, "The server is online.")


@server_app.route('/')
def is_running_window():
    return package(True, "The server for the Virtual-Hand-Application is running.")
