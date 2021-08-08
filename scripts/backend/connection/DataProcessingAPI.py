import flask

from API_Helper import flarg
from scripts import Warnings, Log
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts

data_processing_api = flask.Blueprint('data_processing_api', __name__)

"""
    Dataset REST API
"""


@data_processing_api.route("/merge_datasets")
def merge_datasets():
    Warnings.not_complete()


@data_processing_api.route("/merge_datasets_update")
def merge_datasets_update():
    Warnings.not_complete()


@data_processing_api.route("/delete_dataset")
def delete_dataset():
    Warnings.not_complete()


@data_processing_api.route("/fetch_datasets")
def fetch_datasets():
    sort_by = flarg("sort_by")
    direction = flarg("direction")
    user_name = flarg("user_name")

    # Fetches the data
    user_id = DatabaseAccounts.get_user_id(user_name=user_name)
    return DatabaseDatasets.fetch_ordered_datasets(sort_by=sort_by, direction=direction, user_id=user_id)


"""
    Models REST API
"""


@data_processing_api.route("/create_model")
def create_model():
    Warnings.not_complete()


@data_processing_api.route("/create_model_update")
def create_model_update():
    Warnings.not_complete()


@data_processing_api.route("/delete_model")
def delete_model():
    Warnings.not_complete()


@data_processing_api.route("/fetch_models")
def fetch_models():
    Warnings.not_complete()
