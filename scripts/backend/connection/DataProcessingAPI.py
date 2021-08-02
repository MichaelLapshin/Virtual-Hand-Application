import flask

from scripts import Warnings
from scripts.backend.database import Database
from scripts.backend.connection import Session

data_processing_api = flask.Blueprint('data_processing_api', __name__)

@data_processing_api.route("/merge_datasets")
def merge_datasets():
    Warnings.not_complete()