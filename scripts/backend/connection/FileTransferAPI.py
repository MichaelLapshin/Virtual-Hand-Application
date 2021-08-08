import flask

from API_Helper import flarg, flreq
from scripts import Warnings, Log, Constants, Parameters
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts

file_transfer_api = flask.Blueprint('file_transfer_api', __name__)


@file_transfer_api.route("/upload_dataset", methods=['POST'])
def upload_dataset():
    if flask.request.method == 'POST':
        Log.info("Received a 'POST' request for uploading a dataset.")

        # Get dataset information
        dataset_name = flarg("name")
        dataset_owner_name = flarg("owner_name")
        dataset_date = flarg("date")
        dataset_permission = flarg("permission")
        dataset_fps = flarg("FPS")

        dataset_owner_id = DatabaseAccounts.get_user_id(dataset_owner_name)

        Log.debug("Obtained the dataset information: "
                  + "name='" + dataset_name + "', "
                  + "owner_name='" + dataset_owner_name + "', "
                  + "date='" + dataset_date + "', "
                  + "permission='" + dataset_permission + "'")

        # Get dataset file
        file = flreq(Constants.UPLOAD_DATASET_KEY_WORD)
        Log.debug("Obtained the dataset file '" + dataset_name + "'.")

        # Save the file and create a dataset entry
        DatabaseDatasets.create_new_dataset(name=dataset_name, owner_id=dataset_owner_id,
                                            date=dataset_date, permission=dataset_permission, fps=dataset_fps)
        file.save(Parameters.PROJECT_PATH + dataset_name + ".ds")
        Log.info("Successfully stored the new dataset '" + dataset_name + "'.")
    else:
        Log.warning("The function 'upload_dataset' was called not from a POST request.")
        Warnings.not_to_reach()
        return "Warning. Must access this function using a POST request."
