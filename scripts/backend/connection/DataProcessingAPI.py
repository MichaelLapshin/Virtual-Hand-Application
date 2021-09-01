import flask

from API_Helper import flarg, package
from scripts import Warnings, Log
from scripts.backend.connection import API_Helper
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts
from scripts.backend.logic import Worker, Job, DatasetSmoother, DatasetMerger

data_processing_api = flask.Blueprint('data_processing_api', __name__)

"""
    Dataset REST API
"""


@data_processing_api.route("/merge_datasets")
def merge_datasets():
    global dataset_ids

    # Obtains the dataset ids
    dataset_ids = None
    Log.info("Merging the datasets: " + API_Helper.reverse_url_replacement_mapping(flarg("dataset_ids")))
    exec("dataset_ids = " + API_Helper.reverse_url_replacement_mapping(flarg("dataset_ids")), globals())
    Log.debug("dataset_ids type: " + str(type(dataset_ids)))

    dataset_name = API_Helper.reverse_url_replacement_mapping(flarg("name"))
    dataset_owner_id = int(flarg("owner_id"))
    dataset_rating = int(flarg("rating"))
    dataset_fps = int(flarg("fps"))

    # Creates a merge job
    job = DatasetMerger.JobMerge(dataset_ids=dataset_ids, dataset_name=dataset_name, dataset_owner_id=dataset_owner_id,
                                 dataset_rating=dataset_rating, dataset_fps=dataset_fps)
    Worker.dataset_worker.add_task(job=job)

    return package(True, "The dataset merging process has begun.")


@data_processing_api.route("/delete_dataset")
def delete_dataset():
    # Obtains thew dataset id
    dataset_id = int(flarg("id"))

    # Deletes the dataset
    result = DatabaseDatasets.delete_dataset(dataset_id)
    return package(result, "The dataset with id '" + str(dataset_id) + "' was deleted.")


@data_processing_api.route("/smooth_dataset")
def smooth_dataset():
    # Get dataset information
    dataset_name = flarg("name")
    dataset_owner_id = int(flarg("owner_id"))
    dataset_date = flarg("date")
    dataset_permission = int(flarg("permission"))
    dataset_rating = int(flarg("rating"))
    dataset_is_raw = int(flarg("is_raw"))
    dataset_num_frames = int(flarg("num_frames"))
    dataset_fps = int(flarg("FPS"))

    # Get dataset smoothing information
    dataset_parent_id = flarg("parent_id")
    dataset_frames_shift = int(flarg("frames_shift"))
    sensor_savagol_distance = int(flarg("sensor_savagol_distance"))
    sensor_savagol_degree = int(flarg("sensor_savagol_degree"))
    angle_savagol_distance = int(flarg("angle_savagol_distance"))
    angle_savagol_degree = int(flarg("angle_savagol_degree"))

    # if result is True:

    job = DatasetSmoother.JobSmooth(
        dataset_parent_id=dataset_parent_id, dataset_num_frames=dataset_num_frames,
        dataset_fps=dataset_fps, dataset_frames_shift=dataset_frames_shift,
        sensor_savagol_distance=sensor_savagol_distance, sensor_savagol_degree=sensor_savagol_degree,
        angle_savagol_distance=angle_savagol_distance, angle_savagol_degree=angle_savagol_degree,
        dataset_name=dataset_name, dataset_owner_id=dataset_owner_id, dataset_date=dataset_date,
        dataset_permission=dataset_permission, dataset_rating=dataset_rating, dataset_is_raw=dataset_is_raw)

    Worker.dataset_worker.add_task(job=job)

    return package(True, "The dataset smoothing process has begun.")
    # else:
    #     return package(False, "The dataset smoothing process failed to begin.")


"""
    Models REST API
"""


@data_processing_api.route("/create_model")
def create_model():
    Warnings.not_complete()
    return package(None, "")


@data_processing_api.route("/delete_model")
def delete_model():
    Warnings.not_complete()
    return package(None, "")
