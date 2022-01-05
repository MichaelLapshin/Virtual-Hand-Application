import math

from scripts import Warnings, Parameters, Constants, Log
from scripts.backend.database import DatabasePlots
from scripts.backend.logic import ModelTrainer
from scripts.logic import Job

import matplotlib.pyplot as plt


class JobModelErrorPlotter(Job.Job):
    def __init__(self, model_id, history, finger_index, limb_index, title="Loss", info=None):
        Job.Job.__init__(self, title="Plotting '" + title + "' for the Model with id '" + str(model_id) + "'",
                         info=info)

        # General parameters
        self._model_id = model_id
        self._history = history
        self._title = title
        self._finger_index = finger_index
        self._limb_index = limb_index

        # For the task
        self.set_max_progress(1)

    def perform_task(self):
        self.set_progress(0, "Starting to plot the image '" + self._title + "'")

        # Calculate the error history to display (relative to the lowest error value)
        cutoff_error = min((i for i in self._history.history['loss'] if not math.isnan(i)), default=1) \
                       * Constants.MODEL_ERROR_LOWEST_MULTIPLIER
        cutoff_index = 0
        for value in self._history.history['loss']:
            if value < cutoff_error:
                break
            cutoff_index += 1
        # history = self._history.history['loss'][cutoff_index::]

        # Creating the plot
        plt.plot(self._history.history['loss'], label='mean_absolute_error')
        plt.ylim([0, cutoff_error])
        plt.xlim([cutoff_index, len(self._history.history['loss'])])
        plt.xlabel('Epoch')
        plt.ylabel('Error [' + ModelTrainer.JobModelTrain.LOSS + ']')
        plt.title(self._title)
        plt.legend()
        plt.grid(True)

        # Stores the file inside the database
        image_id = DatabasePlots.create_model_error_image_entry(
            model_id=self._model_id, finger_index=self._finger_index, limb_index=self._limb_index)

        # Saves the image locally
        plt.savefig(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_MODELS_ERRORS_PATH
                    + str(image_id) + Constants.IMAGE_EXT, bbox_inches='tight')
        plt.clf()

        self.complete_progress("The error plot image '" + self._title + "' is complete.")


class JobModelPredictionPlotter(Job.Job):
    def __init__(self, model_id, get_model_func, get_training_data_func, get_label_data_func,
                 finger_index, limb_index, title="Prediction", info=None):
        Job.Job.__init__(self, title="Plotting '" + title + "' for the Model with id '" + str(model_id) + "'",
                         info=info)

        # General parameters
        self._model_id = model_id
        self._get_model_func = get_model_func
        self._get_training_data_func = get_training_data_func
        self._get_label_data_func = get_label_data_func

        self._title = title
        self._finger_index = finger_index
        self._limb_index = limb_index

        # For the task
        self.set_max_progress(1)

    def perform_task(self):
        self.set_progress(0, "Starting to plot the image '" + self._title + "'")

        # Obtain model training data
        self._model = self._get_model_func()
        self._training_data = self._get_training_data_func()
        self._label_data = self._get_label_data_func()

        if (self._model is None) or (self._training_data is None) or (self._label_data is None):
            Log.blocker(
                "One (or more) of the model inputs are None! self._model=" + str(self._model) + " self._training_data="
                + str(self._training_data) + " self._label_data=" + str(self._label_data))

        # Generates prediction data
        pred_interval = 1
        if Constants.MODEL_PRED_FRAMES < len(self._training_data):
            pred_interval = float(len(self._training_data)) / Constants.MODEL_PRED_FRAMES

        data = []
        label_data = []
        for i in range(0, min(Constants.MODEL_PRED_FRAMES, len(self._training_data))):
            index = int(i * pred_interval)
            to_predict = self._training_data[index].reshape(1, Constants.NUM_FEATURES)
            data.append(self._model(to_predict)[0][0].numpy())
            label_data.append(self._label_data[index])

        # Creating the plot
        plt.plot(data)
        plt.plot(label_data)
        plt.xlabel('Frame')
        plt.ylabel("Velocity (degrees/second)")
        plt.title(self._title)
        plt.legend(("Prediction", "Actual"))
        plt.grid(True)

        # Stores the file inside the database
        image_id = DatabasePlots.create_model_prediction_image_entry(
            model_id=self._model_id, finger_index=self._finger_index, limb_index=self._limb_index)

        # Saves the image locally
        plt.savefig(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_MODELS_PREDICTIONS_PATH
                    + str(image_id) + Constants.IMAGE_EXT, bbox_inches='tight')
        plt.clf()

        self.complete_progress("The prediction plot image '" + self._title + "' is complete.")
