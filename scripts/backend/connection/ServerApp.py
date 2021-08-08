"""
[ServerApp.py]
@description: In charge of the connections between client GUI and server database
@author: Michael Lapshin
"""

# Import common libraries
import os
import flask

# Import REST API scripts
from AccountAPI import account_api
from FileTransferAPI import file_transfer_api
from DataProcessingAPI import data_processing_api

# Import miscellaneous scripts
from scripts import Log, Warnings
from scripts.backend.database import Database

# Questionnaire for the server setup


# Database
start_server = Database.connect("server_database.db")
Database.create_all_new_tables()

if start_server:
    # Flask application + configurations
    Log.info("Starting the server...")
    server_app = flask.Flask(__name__)
    server_app.config['SECRET_KEY'] = os.urandom(16)  # Random secret key
    server_app.register_blueprint(account_api, url_prefix="/account")
    server_app.register_blueprint(file_transfer_api, url_prefix="/transfer")
    server_app.register_blueprint(data_processing_api, url_prefix="/process")

    if __name__ == "__main__":
        server_app.run()


@server_app.route('/shutdown')
def shutdown():
    Database.disconnect()

    # Shutting down the flask server
    shutdown_func = flask.request.environ.get('werkzeug.server.shutdown')
    if shutdown_func is None:
        raise RuntimeError('Not running werkzeug')
    shutdown_func()
    return "Shutting down the server..."


@server_app.route('/is_alive')
def is_alive():
    return True


@server_app.route('/')
def is_running_window():
    return "The server for the Virtual-Hand-Application is running."
