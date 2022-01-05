import io
import shutil
import tkinter

import flask
import PIL.Image
import base64

from API_Helper import flarg, flreq, package
from scripts import Warnings, Log, Constants, Parameters
from scripts.backend.connection import API_Helper
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts, DatabasePlots, DatabaseModels
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
    # Obtains the parameters
    dataset_id = flarg("dataset_id")
    image_finger = flarg("finger")
    image_metric = flarg("metric")

    # Loads the image and sends the encoded version of it
    try:
        with open(DatabasePlots.get_dataset_finger_image_file_path(
                dataset_id=dataset_id, finger_num=image_finger, metric_num=image_metric), "rb") as image:
            return package(None, base64.b64encode(image.read()))
    except:
        return package(None, "")


@file_transfer_api.route("/get_dataset_sensor_image")
def get_dataset_sensor_image():
    # Obtains the parameters
    dataset_id = flarg("dataset_id")
    sensor = flarg("sensor")

    # Loads the image and sends the encoded version of it
    try:
        with open(DatabasePlots.get_sensor_image_file_path(dataset_id=dataset_id, sensor_num=sensor), "rb") as image:
            return package(None, base64.b64encode(image.read()))
    except:
        return package(None, "")


@file_transfer_api.route("/get_model_prediction_image")
def get_model_prediction_image():
    # Obtains the parameters
    model_id = flarg("model_id")
    finger = flarg("finger")
    limb = flarg("limb")

    # Loads the image and sends the encoded version of it
    try:
        with open(DatabasePlots.get_model_prediction_image_file_path(
                model_id=model_id, finger_num=finger, limb_num=limb), "rb") as image:
            return package(None, base64.b64encode(image.read()))
    except:
        return package(None, "")


@file_transfer_api.route("/get_model_error_image")
def get_model_error_image():
    # Obtains the parameters
    model_id = flarg("model_id")
    finger = flarg("finger")
    limb = flarg("limb")

    # Loads the image and sends the encoded version of it
    try:
        with open(DatabasePlots.get_model_error_image_file_path(
                model_id=model_id, finger_num=finger, limb_num=limb), "rb") as image:
            return package(None, base64.b64encode(image.read()))
    except:
        return package(None, "")


@file_transfer_api.route("/get_model")
def get_model():
    # Obtains the parameters
    model_id = int(flarg("model_id"))

    # Loads the image and sends the encoded version of it
    try:
        if DatabaseModels.exists_dataset_by_id(model_id) is True:
            dir_path = Parameters.PROJECT_PATH + Constants.SERVER_MODEL_PATH + Constants.MODEL_DIR + str(model_id)
            Log.info("Attempting to retrieve the model from the directory: " + dir_path)
            return package(None, API_Helper.encode_string_directory(dir_path))
            # Zips the file
            # zip_path = Parameters.PROJECT_PATH + Constants.SERVER_MODEL_PATH + str(
            #     model_id) + Constants.TEMP_ZIP_MODEL_SUFFIX
            #
            # shutil.make_archive(
            #     zip_path, "zip",
            #     Parameters.PROJECT_PATH + Constants.SERVER_MODEL_ZIP_PATH + str(model_id) + Constants.MODEL_EXT)
            #
            # # Sends back the zip file
            # with open(zip_path) as reader:
            #     zip_file = reader.read()
            # return package(None, zip_file)
        else:
            return package(False, "The model with id '" + str(model_id) + "' does not exist in the database.")
    except Exception as e:
        Log.warning("Failed to retrieve and send the model directory back.")
        Log.debug("Error: " + str(e))
        return package(False, "Failed to retrieve and send the model directory back.")
