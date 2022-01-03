import math
import os
import time

import h5py
import numpy
import tensorflow
from tensorflow import keras

from scripts import Warnings, Log, Constants, Parameters
from scripts.backend.database import DatabaseModels
from scripts.backend.logic import ModelPlotter
from scripts.logic import Job, Worker

# Set the tensorflow to use the GPU
gpus = tensorflow.config.list_physical_devices('GPU')
if gpus:
    # Restrict TensorFlow to only allocate 1GB of memory on the first GPU
    try:
        tensorflow.config.set_logical_device_configuration(
            gpus[0], [tensorflow.config.LogicalDeviceConfiguration(memory_limit=Constants.MODEL_TRAINING_GPU_MEM_LIM)])
        logical_gpus = tensorflow.config.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Virtual devices must be set before GPUs have been initialized
        print(e)
Log.warning("List of local devices: " + str(tensorflow.config.list_physical_devices('GPU')))


class JobModelTrain(Job.Job):
    LOSS = "mse"
    METRIC = "mean_absolute_error"

    class CustomCallback(keras.callbacks.Callback):
        def __init__(self, job, finger_index, limb_index):
            self.job = job
            self.finger_index = finger_index
            self.limb_index = limb_index

        def on_epoch_end(self, epoch, logs=None):
            Log.trace("[finger_index=" + str(self.finger_index) + " and limb_index=" + str(self.limb_index)
                      + "] For epoch " + str(epoch) + ", the loss is '" + str(logs["loss"])
                      + "' and the absolute error is '" + str(logs[JobModelTrain.METRIC]) + "'")
            self.job.add_progress(1, "Processing training epochs...")
            time.sleep(Constants.BETWEEN_EPOCH_DELAY)

        def on_train_end(self, logs=None):
            Log.info("[finger_index=" + str(self.finger_index) + " and limb_index=" + str(self.limb_index)
                     + "] The training is complete. ")
            self.job.add_progress(0, "The training of the model for finger_index=" + str(self.finger_index)
                                  + " and limb_index=" + str(self.limb_index) + " is complete. "
                                  + "The final loss is: " + str(logs["loss"]))

    def __init__(self, model_id: int, finger_index: int, limb_index: int,
                 dataset_id: int, frames_shift: int, num_training_frames: int,
                 learning_rate: float, batch_size: int, num_epochs: int,
                 layer_type: str, num_layers: int, num_nodes_per_layer: int, info=None):
        Job.Job.__init__(self, title="Training a Model using the Dataset: " + str(dataset_id), info=info)

        self.model_id = model_id
        self.finger_index = finger_index
        self.limb_index = limb_index

        # Training parameters
        self.dataset_id = dataset_id
        self.frames_shift = frames_shift
        self.num_training_frames = num_training_frames
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.layer_type = layer_type
        self.num_layers = num_layers
        self.num_nodes_per_layer = num_nodes_per_layer

        # For the task
        self._model = None
        self._training_data = None
        self._label_data = None
        self.set_max_progress(self.num_epochs)

    def get_model(self):
        if self._model is None:
            Log.warning("get_model() was called while it is None.")
        return self._model

    def get_training_data(self):
        if self._training_data is None:
            Log.warning("get_training_data() was called while it is None.")
        return self._training_data

    def get_label_data(self):
        if self._label_data is None:
            Log.warning("get_label_data() was called while it is None.")
        return self._label_data

    def perform_task(self):
        self.set_progress(0, "Starting the model training.")
        Log.info(
            "Starting to train the model with id '" + str(self.model_id)
            + "' using the dataset with id '" + str(self.dataset_id) + "'")

        # Prepares additional model training parameters
        assert self.layer_type in Constants.MODEL_ACT_FUNC_OPTIONS
        hidden_layers = [self.layer_type for a in range(0, self.num_layers)]

        # Obtains training data
        data_set = h5py.File(
            Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + str(self.dataset_id) + Constants.DATASET_EXT, 'r')
        assert len(data_set["velocity"]) > 0 and data_set["velocity"] is not None

        # Gathers features list. Includes the shift in frames ([:-self.frames_shift:] & [self.frames_shift::])
        all_features = []
        for finger_index in range(0, Constants.NUM_FINGERS):
            for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                all_features.append(data_set.get("angle")[finger_index][limb_index][:-self.frames_shift:])
                all_features.append(data_set.get("velocity")[finger_index][limb_index][:-self.frames_shift:])
                # all_features.append(data_set.get("acceleration")[finger_index][limb_index][:-self.frames_shift:])

        for sensor_index in range(0, Constants.NUM_SENSORS):
            all_features.append(list(data_set.get("sensor")[sensor_index][:-self.frames_shift:]))

        # Get label data, includes the shift in the frames
        self._label_data = list(data_set.get("velocity")[self.finger_index][self.limb_index][self.frames_shift::])

        # Closes the dataset
        data_set.close()

        # Makes sure that data dimensions are valid
        for i in range(1, len(all_features)):
            if len(all_features[i]) != len(all_features[i - 1]):
                Log.blocker("len(all_features[i]) != len(all_features[i - 1]) : "
                            + str(len(all_features[i])) + " vs " + str(len(all_features[i - 1])))
                assert len(all_features[i]) == len(all_features[i - 1])
        if len(self._label_data) != len(all_features[0]):
            Log.blocker("len(self._label_data) != len(all_features[0]) : "
                        + str(len(self._label_data)) + " vs " + str(len(all_features[0])))
            assert len(self._label_data) == len(all_features[0])

        # Creating the training data
        self._training_data = []  # Training Input. Every index represents a new training feature
        for frame in range(0, self.num_training_frames):
            frame_data = []

            for i in range(0, len(all_features)):
                frame_data.append(all_features[i][frame])

            self._training_data.append(numpy.array(frame_data))

        # Additional assertion on the data
        # Checks the size is correct
        if len(self._label_data) != self.num_training_frames:
            Log.blocker("len(self._label_data) != self.num_training_frames : "
                        + str(len(self._label_data)) + " vs " + str(self.num_training_frames))
        assert len(self._training_data) == len(self._label_data) == self.num_training_frames

        # Checks that there are no infinite data points
        for frame_num, frame in enumerate(self._training_data):
            for val in frame:
                if math.isnan(val) or math.isinf(val):
                    Log.blocker("The training data contains NaN or infinite values in frame "
                                + str(frame_num) + ":\n" + str(frame))
                assert not math.isnan(val) and not math.isinf(val)


        # Converts to datasets to numpy array
        self._label_data = numpy.array(self._label_data)
        self._training_data = numpy.array(self._training_data)

        # Normalizes the input data
        normalizer_layer = keras.layers.experimental.preprocessing.Normalization()
        normalizer_layer.adapt(self._training_data)

        # Builds the model
        model_layers = [normalizer_layer, keras.layers.Input(shape=(Constants.NUM_FEATURES,))]
        for act in hidden_layers:
            model_layers.append(keras.layers.Dense(self.num_nodes_per_layer, activation=act, bias_initializer='zeros'))
        model_layers.append(keras.layers.Dense(1))
        self._model = keras.Sequential(model_layers)

        # Uses the CPU, prioritizes the use of the GPU
        device_to_use = "/CPU:0"
        if len(gpus) > 0:
            device_to_use = '/GPU:0'
        with tensorflow.device(device_to_use):
            # Compile the model
            # Gradient clipping info: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Optimizer#attributes_1
            self._model.compile(loss=JobModelTrain.LOSS,  # loss='mean_absolute_error',
                                # optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate, clipvalue=1),
                                optimizer=keras.optimizers.RMSprop(learning_rate=self.learning_rate, clipvalue=1),
                                metrics=[JobModelTrain.METRIC])

            # Trains the model
            training_history = self._model.fit(
                self._training_data, self._label_data,
                batch_size=self.batch_size, epochs=self.num_epochs, shuffle=True, verbose=0,
                callbacks=[
                    JobModelTrain.CustomCallback(job=self, finger_index=self.finger_index, limb_index=self.limb_index)])

        # Saves the model
        save_dir = Parameters.PROJECT_PATH + Constants.SERVER_MODEL_PATH + Constants.MODEL_DIR + str(self.model_id)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self._model.save(
            save_dir + "\\f-" + str(self.finger_index) + "_l-" + str(self.limb_index) + Constants.MODEL_EXT)

        # Creates a worker job to general an error plot
        Worker.worker.add_task(
            job=ModelPlotter.JobModelErrorPlotter(model_id=self.model_id, history=training_history,
                                                  finger_index=self.finger_index, limb_index=self.limb_index,
                                                  title="Loss for " + Constants.FINGER_TYPE[self.finger_index] + " " +
                                                        Constants.LIMB_TYPE[self.limb_index] + " finger limb")
        )

        self.complete_progress("The model training is complete. The loss plotting job was created.")
