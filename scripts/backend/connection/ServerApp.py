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

from API_Helper import package
from AccountAPI import account_api
from FileTransferAPI import file_transfer_api
from DataProcessingAPI import data_processing_api
from DataFetchingAPI import data_fetching_api
from DataUpdatingAPI import data_updating_api

# Import miscellaneous scripts
from scripts import Log
from scripts.backend.database import Database

# Database
from scripts.logic import Worker

# Questionnaire for the server setup


HOST = "127.0.0.1"
PORT = 5000
start_server = Database.connect("server_database.db")
Database.create_all_new_tables(replace=False)
workers = []


class ConsoleReader(threading.Thread):
    def __init__(self, stop_processes_command):
        threading.Thread.__init__(self)
        self._stop_processes_command = stop_processes_command
        self._running = False
        self.daemon = True
        self._stopped = True

    def run(self):
        self._stopped = False
        while self._running is True:
            inp = input()
            if inp.lower() == "stop" or inp.lower() == "shutdown":
                # requests.get(HOST + ":" + str(PORT) + "/shutdown"
                print("[ServerApp] Stopping the processes.")
                self._stop_processes_command()
                print("[ServerApp] All processes have been stopped.")
                print("[ServerApp] You may now stop the (flask) server.")
            else:
                print("[ServerApp] Did not recognize the command.")
            time.sleep(3)
        self._stopped = True
        Log.info("The  console reader thread has stopped.")

    def start(self):
        Log.info("Starting the console reader thread...")
        self._running = True
        super().start()

    def stop(self):
        Log.info("Stopping the console reader thread...")
        self._running = False

    """
        Getters
    """

    def is_running(self):
        return self._running

    def is_stopped(self):
        return self._stopped


def stop_processes():
    # Stops the console reader
    if console_reader is not None:
        console_reader.stop()
        while console_reader.is_stopped() is False:
            time.sleep(1)

    # Stops the workers
    for w in workers:
        if w is not None:
            w.stop()

    # Waits until the workers are done their tasks
    for w in workers:
        while w.is_stopped() is False:
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
    console_reader = ConsoleReader(stop_processes)
    console_reader.start()

    # Creates workers
    Worker.dataset_worker = Worker.Worker()
    Worker.dataset_image_worker = Worker.Worker()
    Worker.model_worker = Worker.Worker()
    Worker.model_image_worker = Worker.Worker()

    # Appends all workers to a list
    workers.append(Worker.dataset_worker)
    workers.append(Worker.dataset_image_worker)
    workers.append(Worker.model_worker)
    workers.append(Worker.model_image_worker)

    # Starts the worker threads
    for w in workers:
        w.start()

    if __name__ == "__main__":
        server_app.run(host=HOST, port=PORT, threaded=True)


@server_app.route('/shutdown')
def shutdown():
    stop_processes()

    # Shutting down the flask server
    shutdown_func = flask.request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return package(True, "Shutting down the server...")


@server_app.route('/is_online')
def is_online():
    return package(True, "The server is online.")


@server_app.route('/')
def is_running_window():
    return package(True, "The server for the Virtual-Hand-Application is running.")
