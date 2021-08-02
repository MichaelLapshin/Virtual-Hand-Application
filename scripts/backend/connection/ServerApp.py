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
from scripts import Logger, Warnings
from scripts.backend.database import Database
from scripts.backend.connection import Session

# Questionnaire for the server setup


# Flask application + configurations
server_app = flask.Flask(__name__)
server_app.config['SECRET_KEY'] = os.urandom(16)  # Random secret key
server_app.register_blueprint(account_api, url_prefix="/account")
server_app.register_blueprint(file_transfer_api, url_prefix="/transfer")
server_app.register_blueprint(data_processing_api, url_prefix="/process")

# Database
Database.connect("server_database.db")

# Logger
logger = Logger.Log("ServerApp", log_lvl=4)

if __name__ == '__main__':
    server_app.run()


@server_app.route('/')
def is_running_window():
    return "Virtual-Hand-Application Server is running."
