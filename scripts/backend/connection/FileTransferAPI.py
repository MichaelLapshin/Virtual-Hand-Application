import flask

from scripts import Warnings
from scripts.backend.database import Database
from scripts.backend.connection import Session

file_transfer_api = flask.Blueprint('file_transfer_api', __name__)


@file_transfer_api.route("/upload_dataset")
def upload_dataset():
    Warnings.not_complete()

@file_transfer_api.route("/upload_dataset")
def upload_dataset():
    Warnings.not_complete()