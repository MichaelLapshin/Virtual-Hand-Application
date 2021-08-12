import flask

from API_Helper import flarg, package
from scripts import Warnings, Log
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts

data_processing_api = flask.Blueprint('data_processing_api', __name__)

"""
    Dataset REST API
"""


@data_processing_api.route("/merge_datasets")
def merge_datasets():
    Warnings.not_complete()
    return package(None, "")


@data_processing_api.route("/merge_datasets_update")
def merge_datasets_update():
    Warnings.not_complete()
    return package(None, "")


@data_processing_api.route("/delete_dataset")
def delete_dataset():
    Warnings.not_complete()
    return package(None, "")


"""
    Models REST API
"""


@data_processing_api.route("/create_model")
def create_model():
    Warnings.not_complete()
    return package(None, "")


@data_processing_api.route("/create_model_update")
def create_model_update():
    Warnings.not_complete()
    return package(None, "")


@data_processing_api.route("/delete_model")
def delete_model():
    Warnings.not_complete()
    return package(None, "")
