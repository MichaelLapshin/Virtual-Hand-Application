import time

from scripts import Log, Constants
from scripts.logic import Job, Worker
from scripts.frontend import ClientConnection


class JobDatasetFingers(Job.Job):
    def __init__(self, dataset_id, finger_index, metric_index, dest_obj, update_image_visibility_command,
                 info={"dataset_image": True, "load_attempts_left": Constants.IMAGE_ATTEMPT_MAX_TIMES}):
        Job.Job.__init__(self, title="Loading the dataset '" + str(dataset_id) + "' finger image with 'finger_index="
                                     + str(finger_index) + "' and 'metric_index=" + str(metric_index) + "'", info=info)
        # Parameters for retrieving the image
        self.dataset_id = dataset_id
        self.finger_index = finger_index
        self.metric_index = metric_index

        # Parameters for updating the client UI
        self.dest_obj = dest_obj
        self.update_image_visibility_command = update_image_visibility_command

        self.set_max_progress(4)
        Log.info("Created a Dataset Finger Image Loader job for dataset '" + str(dataset_id) + "'with 'finger_index="
                 + str(finger_index) + "' and 'metric_index=" + str(metric_index) + "'")

    def perform_task(self):
        Log.info("Started working on a Dataset Finger Image Loader job. title='" + self.get_title() + "'")

        # Sending the request
        self.set_progress(1, "Sending the server a request for the image.")

        # Attempt to fetch the error plot
        image = ClientConnection.fetch_dataset_finger_plot(
            dataset_id=self.dataset_id, finger=self.finger_index, metric=self.metric_index)
        if image is None or (image.size[0] == 0 and image.size[1] == 0):
            image = None

            # Decrements the attempt count and creates a follow-up job if attempts remain
            self._info["load_attempts_left"] -= 1
            if self.get_info().get("load_attempts_left") > 0:
                time.sleep(Constants.IMAGE_REQUEST_FREQ_S)
                Worker.worker.add_task(JobDatasetFingers(
                    dataset_id=self.dataset_id, finger_index=self.finger_index, metric_index=self.metric_index,
                    dest_obj=self.dest_obj, update_image_visibility_command=self.update_image_visibility_command,
                    info=self.get_info()))

        # Saving the image
        self.set_progress(2, "Saving the image into the destination object.")
        self.dest_obj.orig_image = image

        # Updating the Client UI
        self.set_progress(3, "Saving the image into the destination object.")
        self.update_image_visibility_command()

        self.set_progress(4, "The image loading is complete.")


class JobDatasetSensors(Job.Job):
    def __init__(self, dataset_id, sensor_index, dest_obj, update_image_visibility_command,
                 info={"dataset_image": True, "load_attempts_left": Constants.IMAGE_ATTEMPT_MAX_TIMES}):
        Job.Job.__init__(self, title="Loading the dataset '" + str(dataset_id) + "' sensor image with 'sensor_index="
                                     + str(sensor_index) + "'", info=info)
        # Parameters for retrieving the image
        self.dataset_id = dataset_id
        self.sensor_index = sensor_index

        # Parameters for updating the client UI
        self.dest_obj = dest_obj
        self.update_image_visibility_command = update_image_visibility_command

        self.set_max_progress(4)
        Log.info("Created a Dataset Sensor Image Loader job for dataset '" + str(dataset_id) + "' with 'sensor_index="
                 + str(sensor_index) + "'")

    def perform_task(self):
        Log.info("Started working on a Dataset Sensor Image Loader job. title='" + self.get_title() + "'")

        # Sending the request
        self.set_progress(1, "Sending the server a request for the image.")

        # Attempt to fetch the error plot
        image = ClientConnection.fetch_dataset_sensor_plot(dataset_id=self.dataset_id, sensor=self.sensor_index)
        if image is None or (image.size[0] == 0 and image.size[1] == 0):
            image = None

            # Decrements the attempt count and creates a follow-up job if attempts remain
            self._info["load_attempts_left"] -= 1
            if self.get_info().get("load_attempts_left") > 0:
                time.sleep(Constants.IMAGE_REQUEST_FREQ_S)
                Worker.worker.add_task(JobDatasetSensors(
                    dataset_id=self.dataset_id, sensor_index=self.sensor_index, dest_obj=self.dest_obj,
                    update_image_visibility_command=self.update_image_visibility_command, info=self.get_info()))

        # Saving the image
        self.set_progress(2, "Saving the image into the destination object.")
        self.dest_obj.orig_image = image

        # Updating the Client UI
        self.set_progress(3, "Saving the image into the destination object.")
        self.update_image_visibility_command()

        self.complete_progress("The image loading is complete.")


class JobModelPredictions(Job.Job):
    def __init__(self, model_id, finger_index, limb_index, dest_obj, update_image_visibility_command,
                 info={"model_image": True, "load_attempts_left": Constants.IMAGE_ATTEMPT_MAX_TIMES}):
        Job.Job.__init__(self, title="Loading the prediction image of model '" + str(model_id) + "' with 'finger_index="
                                     + str(finger_index) + "' and 'limb_index=" + str(limb_index) + "'", info=info)
        # Parameters for retrieving the image
        self.model_id = model_id
        self.finger_index = finger_index
        self.limb_index = limb_index

        # Parameters for updating the client UI
        self.dest_obj = dest_obj
        self.update_image_visibility_command = update_image_visibility_command

        self.set_max_progress(4)
        Log.info("Created a Model Prediction Image Loader job for dataset '" + str(model_id) + "'with 'finger_index="
                 + str(finger_index) + "' and 'limb_index=" + str(limb_index) + "'")

    def perform_task(self):
        Log.info("Started working on a Model Prediction Image Loader job. title='" + self.get_title() + "'")

        # Sending the request
        self.set_progress(1, "Sending the server a request for the image.")

        # Attempt to fetch the error plot
        image = ClientConnection.fetch_model_prediction_plot(
            model_id=self.model_id, finger=self.finger_index, limb=self.limb_index)
        if image is None or (image.size[0] == 0 and image.size[1] == 0):
            image = None

            # Decrements the attempt count and creates a follow-up job if attempts remain
            self._info["load_attempts_left"] -= 1
            if self.get_info().get("load_attempts_left") > 0:
                time.sleep(Constants.IMAGE_REQUEST_FREQ_S)
                Worker.worker.add_task(JobModelPredictions(
                    model_id=self.model_id, finger_index=self.finger_index, limb_index=self.limb_index,
                    dest_obj=self.dest_obj, update_image_visibility_command=self.update_image_visibility_command,
                    info=self.get_info()))

        # Saving the image
        self.set_progress(2, "Saving the image into the destination object.")
        self.dest_obj.orig_image = image

        # Updating the Client UI
        self.set_progress(3, "Saving the image into the destination object.")
        self.update_image_visibility_command()

        self.set_progress(4, "The image loading is complete.")


class JobModelErrors(Job.Job):
    def __init__(self, model_id, finger_index, limb_index, dest_obj, update_image_visibility_command,
                 info={"model_image": True, "load_attempts_left": Constants.IMAGE_ATTEMPT_MAX_TIMES}):
        Job.Job.__init__(self, title="Loading the error image of model '" + str(model_id) + "' with 'finger_index="
                                     + str(finger_index) + "' and 'limb_index=" + str(limb_index) + "'", info=info)
        # Parameters for retrieving the image
        self.model_id = model_id
        self.finger_index = finger_index
        self.limb_index = limb_index

        # Parameters for updating the client UI
        self.dest_obj = dest_obj
        self.update_image_visibility_command = update_image_visibility_command

        self.set_max_progress(4)
        Log.info("Created a Model Error Image Loader job for dataset '" + str(model_id) + "'with 'finger_index="
                 + str(finger_index) + "' and 'limb_index=" + str(limb_index) + "'")

    def perform_task(self):
        Log.info("Started working on a Model Error Image Loader job. title='" + self.get_title() + "'")

        # Sending the request
        self.set_progress(1, "Sending the server a request for the image.")

        # Attempt to fetch the error plot
        image = ClientConnection.fetch_model_error_plot(
            model_id=self.model_id, finger=self.finger_index, limb=self.limb_index)
        if image is None or (image.size[0] == 0 and image.size[1] == 0):
            image = None

            # Decrements the attempt count and creates a follow-up job if attempts remain
            self._info["load_attempts_left"] -= 1
            if self.get_info().get("load_attempts_left") > 0:
                time.sleep(Constants.IMAGE_REQUEST_FREQ_S)
                Worker.worker.add_task(JobModelErrors(
                    model_id=self.model_id, finger_index=self.finger_index, limb_index=self.limb_index,
                    dest_obj=self.dest_obj, update_image_visibility_command=self.update_image_visibility_command,
                    info=self.get_info()))

        # Saving the image
        self.set_progress(2, "Saving the image into the destination object.")
        self.dest_obj.orig_image = image

        # Updating the Client UI
        self.set_progress(3, "Saving the image into the destination object.")
        self.update_image_visibility_command()

        self.set_progress(4, "The image loading is complete.")
