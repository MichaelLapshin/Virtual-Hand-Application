import io
import tkinter

import flask
import PIL.Image
import base64

from API_Helper import flarg, flreq, package
from scripts import Warnings, Log, Constants, Parameters
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts, DatabasePlots
from scripts.backend.logic import DatasetPlotter
from scripts.logic import Worker

file_transfer_api = flask.Blueprint('file_transfer_api', __name__)


@file_transfer_api.route("/upload_dataset", methods=['POST'])
def upload_dataset():
    if flask.request.method == 'POST':
        Log.info("Received a 'POST' request for uploading a dataset.")

        # Get dataset information
        dataset_name = flarg("name")
        dataset_owner_id = flarg("owner_id")
        dataset_date = flarg("date")
        dataset_permission = int(flarg("permission"))
        dataset_rating = int(flarg("rating"))
        dataset_num_frames = int(flarg("num_frames"))
        dataset_fps = int(flarg("FPS"))

        Log.debug("Obtained the dataset information: "
                  + "name='" + dataset_name + "', "
                  + "owner_id='" + dataset_owner_id + "', "
                  + "date='" + dataset_date + "', "
                  + "permission='" + str(dataset_permission) + "', "
                  + "rating='" + str(dataset_rating) + "', "
                  + "num_frames='" + str(dataset_num_frames) + "', "
                  + "FPS='" + str(dataset_fps) + "'")

        # Get dataset file
        file = flreq(Constants.UPLOAD_KEY_WORD)
        Log.debug("Obtained the dataset file '" + dataset_name + "'.")

        # Save the file and create a dataset entry
        dataset_id = DatabaseDatasets.create_new_dataset(
            name=dataset_name, owner_id=dataset_owner_id,
            date_created=dataset_date, permission=dataset_permission, rating=dataset_rating,
            num_frames=dataset_num_frames, fps=dataset_fps)

        # Saves the dataset
        file.save(Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + str(dataset_id) + Constants.DATASET_EXT)

        # Creates image creation job
        job = DatasetPlotter.JobDatasetPlotter(
            title="Plotting Raw Dataset with id '" + str(dataset_id) + "'", dataset_id=dataset_id, plot_vel_acc=False)
        Worker.worker.add_task(job=job)

        Log.info("Successfully stored the new dataset '" + dataset_name + "'.")
        return package(True, "Successfully stored the new dataset '" + dataset_name + "'.")
    else:
        Log.warning("The function 'upload_dataset' was called not from a POST request.")
        Warnings.not_to_reach()
        return package(False, "Warning. Must access this function using a POST request.")


@file_transfer_api.route("/get_dataset_finger_image")
def get_dataset_finger_image():
    dataset_id = flarg("dataset_id")
    image_finger = flarg("finger")
    image_metric = flarg("metric")

    # Loads the image and sends the encoded version of it
    try:
        image = open(DatabasePlots.get_finger_image_file_path(dataset_id=dataset_id,
                                                              finger_num=image_finger, metric_num=image_metric), "rb")
        return package(None, base64.b64encode(image.read()))
    except:
        return package(None, "")


@file_transfer_api.route("/get_dataset_sensor_image")
def get_dataset_sensor_image():
    dataset_id = flarg("dataset_id")
    sensor = flarg("sensor")

    # Loads the image and sends the encoded version of it
    try:
        image = open(DatabasePlots.get_sensor_image_file_path(dataset_id=dataset_id, sensor_num=sensor), "rb")
        return package(None, base64.b64encode(image.read()))
    except:
        return package(None, "")
