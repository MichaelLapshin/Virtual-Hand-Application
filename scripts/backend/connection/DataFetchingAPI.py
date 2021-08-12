import flask

from API_Helper import flarg, package
from scripts import Warnings, Log
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts, DatabaseModels

data_fetching_api = flask.Blueprint('data_fetching_api', __name__)

"""
    All Fetch
"""


@data_fetching_api.route("/all_users")
def fetch_all_users():
    return package(True, str(DatabaseAccounts.get_all_account()))


@data_fetching_api.route("/all_datasets")
def fetch_all_datasets():
    return package(True, str(DatabaseDatasets.get_all_datasets()))


@data_fetching_api.route("/all_models")
def fetch_all_models():
    return package(True, str(DatabaseModels.get_all_models()))


"""
    Sorted Fetch
"""


@data_fetching_api.route("/sorted_datasets")
def fetch_datasets():
    sort_by = flarg("sort_by")
    direction = flarg("direction")
    user_name = flarg("user_name")

    # Fetches the data
    user_id = DatabaseAccounts.get_user_id(user_name=user_name)
    return package(True, DatabaseDatasets.fetch_ordered_datasets(sort_by=sort_by, direction=direction, user_id=user_id))


@data_fetching_api.route("/sorted_models")
def fetch_models():
    Warnings.not_complete()
    return package(None, "")
