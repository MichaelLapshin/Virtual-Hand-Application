import flask

from API_Helper import flarg, package
from scripts import Warnings, Log, Constants, General
from scripts.backend.connection import API_Helper
from scripts.backend.database import DatabaseDatasets, DatabaseModels
from scripts.backend.logic import DatasetSmoother, DatasetMerger, ModelTrainer, DatasetPlotter, ModelPlotter
from scripts.logic import Worker, Job

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
    dataset_num_frames = int(flarg("num_frames"))
    dataset_fps = int(flarg("fps"))

    # Saves the data on the database
    dataset_id = DatabaseDatasets.create_new_dataset(
        name=dataset_name, owner_id=dataset_owner_id, date_created=General.get_current_slashed_date(),
        permission=Constants.PERMISSION_LEVELS.get(Constants.PERMISSION_PUBLIC), rating=dataset_rating,
        num_frames=dataset_num_frames, fps=dataset_fps)

    # Creates a merge job
    job = DatasetMerger.JobMerge(dataset_id=dataset_id, dataset_ids=dataset_ids)
    Worker.worker.add_task(job=job)

    return package(True, "The dataset merging process has begun.")


@data_processing_api.route("/delete_dataset")
def delete_dataset():
    # Obtains thew dataset id
    dataset_id = int(flarg("id"))

    # Deletes the dataset
    result = DatabaseDatasets.delete_dataset(dataset_id)
    if result is True:
        Log.info("The dataset with id '" + str(dataset_id) + "' was deleted.")
        return package(True, "The dataset with id '" + str(dataset_id) + "' was deleted.")
    else:
        Log.warning("The deletion of dataset with id '" + str(dataset_id) + "' was not successful.")
        return package(False, "The deletion of dataset with id '" + str(dataset_id) + "' was not successful.")


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
    sensor_savagol_distance = int(flarg("sensor_savagol_distance"))
    sensor_savagol_degree = int(flarg("sensor_savagol_degree"))
    angle_savagol_distance = int(flarg("angle_savagol_distance"))
    angle_savagol_degree = int(flarg("angle_savagol_degree"))

    # Creates database entry
    dataset_id = DatabaseDatasets.create_new_dataset(
        name=dataset_name, owner_id=dataset_owner_id, date_created=dataset_date,
        permission=dataset_permission, rating=dataset_rating, is_raw=dataset_is_raw,
        num_frames=dataset_num_frames, fps=dataset_fps,
        sensor_savagol_distance=sensor_savagol_distance, sensor_savagol_degree=sensor_savagol_degree,
        angle_savagol_distance=angle_savagol_distance, angle_savagol_degree=angle_savagol_degree)

    # Creates smoothing job
    smooth_dataset_job = DatasetSmoother.JobSmooth(
        dataset_id=dataset_id,
        dataset_parent_id=dataset_parent_id, dataset_num_frames=dataset_num_frames,
        dataset_fps=dataset_fps,
        sensor_savagol_distance=sensor_savagol_distance, sensor_savagol_degree=sensor_savagol_degree,
        angle_savagol_distance=angle_savagol_distance, angle_savagol_degree=angle_savagol_degree)
    Worker.worker.add_task(job=smooth_dataset_job)

    # Creates image creation job
    create_image_job = DatasetPlotter.JobDatasetPlotter(
        title="Plotting Smoothed Dataset with id '" + str(dataset_id) + "'", dataset_id=dataset_id, plot_vel_acc=True)
    Worker.worker.add_task(job=create_image_job)

    return package(True, "The dataset smoothing process has begun.")


"""
    Models REST API
"""


@data_processing_api.route("/create_model_training_process")
def create_model():
    # General parameters
    name = flarg("name")
    owner_id = int(flarg("owner_id"))
    date_created = flarg("date_created")
    permission = int(flarg("permission"))
    rating = int(flarg("rating"))

    # Training parameters
    dataset_id = int(flarg("dataset_id"))
    dataset_frames_shift = int(flarg("frames_shift"))
    num_training_frames = int(flarg("num_training_frames"))
    learning_rate = float(flarg("learning_rate"))
    batch_size = int(flarg("batch_size"))
    num_epochs = int(flarg("num_epochs"))
    layer_type = flarg("layer_type")
    num_layers = int(flarg("num_layers"))
    num_nodes_per_layer = int(flarg("num_nodes_per_layer"))

    # Adds model to database
    model_id = DatabaseModels.create_new_model(name=name, owner_id=owner_id, date_created=date_created,
                                               permission=permission, rating=rating,
                                               dataset_id=dataset_id, frames_shift=dataset_frames_shift,
                                               num_training_frames=num_training_frames,
                                               learning_rate=learning_rate, batch_size=batch_size,
                                               num_epochs=num_epochs,
                                               layer_type=layer_type, num_layers=num_layers,
                                               num_nodes_per_layer=num_nodes_per_layer)

    # Creates model training process
    training_jobs = []
    for finger_index in range(0, Constants.NUM_FINGERS):
        for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
            training_jobs.append(
                ModelTrainer.JobModelTrain(
                    model_id=model_id, finger_index=finger_index, limb_index=limb_index,
                    dataset_id=dataset_id, frames_shift=dataset_frames_shift, num_training_frames=num_training_frames,
                    learning_rate=learning_rate, batch_size=batch_size, num_epochs=num_epochs,
                    layer_type=layer_type, num_layers=num_layers, num_nodes_per_layer=num_nodes_per_layer)
            )
    multi_training_job = Job.SimultaneousJobs(jobs=training_jobs,
                                              title="Training model with id '" + str(model_id)
                                                    + "' using the dataset with id '" + str(dataset_id) + "'",
                                              progress_message="Model training in progress...",
                                              complete_message="Model training is complete.")
    Worker.worker.add_task(job=multi_training_job)

    # Creates error plotting job
    # error_plot_job = # Note: error plot is created within the training of the model

    # Creates prediction plotting job
    prediction_plot_jobs = []
    for finger_index in range(0, Constants.NUM_FINGERS):
        for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
            training_jobs_index = finger_index * 3 + limb_index

            Worker.worker.add_task(
                ModelPlotter.JobModelPredictionPlotter(
                    model_id=model_id,
                    get_model_func=training_jobs[training_jobs_index].get_model,
                    get_training_data_func=training_jobs[training_jobs_index].get_training_data,
                    get_label_data_func=training_jobs[training_jobs_index].get_label_data,
                    finger_index=finger_index, limb_index=limb_index,
                    title="Velocity predictions for model with id '" + str(model_id) + "', " + Constants.FINGER_TYPE[
                        finger_index] + " " + Constants.LIMB_TYPE[limb_index] + " finger limb")
            )
    # multi_imaging_job = Job.SimultaneousJobs(jobs=prediction_plot_jobs,
    #                                          title="Prediction Plot Generation for Model ID '" + str(model_id) + "'",
    #                                          progress_message="Generating the prediction plots Model ID '"
    #                                                           + str(model_id) + "'",
    #                                          complete_message="The prediction plots for Model ID '"
    #                                                           + str(model_id) + "' are complete.")
    # Worker.worker.add_task(job=multi_imaging_job)

    return package(True, "The model training process has begun.")


@data_processing_api.route("/delete_model")
def delete_model():
    # Obtains parameters
    model_id = int(flarg("id"))
    Log.info("Deleting the model with id '" + str(model_id) + "'")

    # Deletes the model
    result = DatabaseModels.delete_model(model_id=model_id)
    if result is True:
        Log.info("The model with id '" + str(model_id) + "' was deleted.")
        return package(True, "The model with id '" + str(model_id) + "' was deleted.")
    else:
        Log.warning("The deletion of model with id '" + str(model_id) + "' was not successful.")
        return package(False, "The deletion of model with id '" + str(model_id) + "' was not successful.")
