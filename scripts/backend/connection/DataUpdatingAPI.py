import flask

from API_Helper import flarg, package
from scripts import Warnings, Log, Constants
from scripts.backend.connection import API_Helper
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts, DatabaseModels

data_updating_api = flask.Blueprint('data_updating_api', __name__)

"""
    Update requests
"""


@data_updating_api.route("/dataset_entry")
def update_dataset_entry():
    dataset_id = flarg("id")
    dataset_new_values = API_Helper.reverse_url_replacement_mapping(flarg("new_values"))

    # Updates the dataset
    update_success_status = DatabaseDatasets.update_dataset_entry(dataset_id, dataset_new_values)

    if update_success_status is True:
        return package(True, "The dataset with id '" + dataset_id + "' was successfully updated.")
    else:
        return package(False, "The dataset with id '" + dataset_id + "' was not successfully updated.")


@data_updating_api.route("/model_entry")
def update_model_entry():
    model_id = flarg("id")
    model_new_values = API_Helper.reverse_url_replacement_mapping(flarg("new_values"))

    # Updates the model
    update_success_status = DatabaseModels.update_model_entry(model_id, model_new_values)

    if update_success_status is True:
        return package(True, "The model with id '" + model_id + "' was successfully updated.")
    else:
        return package(False, "The model with id '" + model_id + "' was not successfully updated.")
