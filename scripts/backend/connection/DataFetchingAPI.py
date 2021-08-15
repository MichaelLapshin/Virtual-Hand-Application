import flask

from API_Helper import flarg, package
from scripts import Warnings, Log
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts, DatabaseModels

data_fetching_api = flask.Blueprint('data_fetching_api', __name__)

"""
    All Fetch
"""


@data_fetching_api.route("/all_user_names")
def fetch_user_names():
    return package(None, DatabaseAccounts.get_user_name_list())


@data_fetching_api.route("/all_users")
def fetch_all_users():
    return package(None, DatabaseAccounts.get_all_account())


@data_fetching_api.route("/all_datasets")
def fetch_all_datasets():
    return package(None, DatabaseDatasets.get_all_datasets())


@data_fetching_api.route("/all_models")
def fetch_all_models():
    return package(None, DatabaseModels.get_all_models())


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
    return package(None, DatabaseDatasets.fetch_ordered_datasets(sort_by=sort_by, direction=direction, user_id=user_id))


@data_fetching_api.route("/sorted_models")
def fetch_models():
    sort_by = flarg("sort_by")
    direction = flarg("direction")
    user_name = flarg("user_name")

    # Fetches the data
    user_id = DatabaseAccounts.get_user_id(user_name=user_name)
    return package(None, DatabaseModels.fetch_ordered_models(sort_by=sort_by, direction=direction, user_id=user_id))


"""
    Fetch dependencies
"""


@data_fetching_api.route("/dataset_dependencies")
def fetch_dataset_dependencies():
    Warnings.not_complete()
    return package(None, "")



