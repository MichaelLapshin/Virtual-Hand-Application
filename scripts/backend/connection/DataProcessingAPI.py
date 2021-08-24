import flask

from API_Helper import flarg, package
from scripts import Warnings, Log
from scripts.backend.database import Database, DatabaseDatasets, DatabaseAccounts
from scripts.backend.logic import Worker, Job, DatasetSmoother

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


# @data_processing_api.route("/duplicate_dataset")
# def duplicate_dataset():
#     dataset_id = flarg("id")
#     # TODO, complete this
#     Warnings.not_complete()
#     return package(None, "")


@data_processing_api.route("/delete_dataset")
def delete_dataset():
    dataset_id = flarg("id")
    # TODO, complete this
    # result = DatabaseDatasets.delete

    Warnings.not_complete()
    return package(None, "")


@data_processing_api.route("/smooth_dataset")
def smooth_dataset():
    # Get dataset information
    dataset_name = flarg("name")
    dataset_owner_name = flarg("owner_id")
    dataset_date = flarg("date")
    dataset_permission = int(flarg("permission"))
    dataset_rating = int(flarg("rating"))
    dataset_num_frames = int(flarg("num_frames"))
    dataset_fps = int(flarg("FPS"))

    # Get dataset smoothing information
    dataset_parent_id = flarg("parent_id")
    dataset_frames_shift = int(flarg("frames_shift"))
    sensor_savagol_distance = float(flarg("sensor_savagol_distance"))
    sensor_savagol_degree = float(flarg("sensor_savagol_degree"))
    angle_savagol_distance = float(flarg("angle_savagol_distance"))
    angle_savagol_degree = float(flarg("angle_savagol_degree"))

    # if result is True:

    job = DatasetSmoother.JobSmooth(
        title="Smoothing Dataset",
        dataset_parent_id=dataset_parent_id, dataset_num_frames=dataset_num_frames,
        dataset_fps=dataset_fps, dataset_frames_shift=dataset_frames_shift,
        sensor_savagol_distance=sensor_savagol_distance, sensor_savagol_degree=sensor_savagol_degree,
        angle_savagol_distance=angle_savagol_distance, angle_savagol_degree=angle_savagol_degree,
        dataset_name=dataset_name, dataset_owner_name=dataset_owner_name, dataset_date=dataset_date,
        dataset_permission=dataset_permission, dataset_rating=dataset_rating)

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


@data_processing_api.route("/create_model_update")
def create_model_update():
    Warnings.not_complete()
    return package(None, "")


@data_processing_api.route("/delete_model")
def delete_model():
    Warnings.not_complete()
    return package(None, "")
