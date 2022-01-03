"""
    [ModelConnectionServer.py]
    Program that hosts a UDP server to host the models.
"""

import socket
import socketserver
import threading
import time
from typing import Tuple

import numpy
import tensorflow

from scripts import Log, Constants, Warnings, Parameters, General, InputConstraints
from scripts.General import time_ms, dict_deepcopy
from scripts.frontend.logic import SensorListener


class ThreadedPredictions(threading.Thread):
    def __init__(self, model, to_predict):
        threading.Thread.__init__(self)
        # Prediction variables
        self.model = model
        self.to_predict = to_predict

        # Thread variables
        self.result = None
        self.done = False
        self.start()

    def run(self) -> None:
        self.result = General.constraint_number_value(
            self.model(self.to_predict)[0][0].numpy(),
            Constants.MODEL_MIN_VAL, Constants.MODEL_MAX_VAL)
        self.done = True


class ModelServer(socketserver.UDPServer):

    def __init__(self, server_address=(Constants.MODEL_SERVER_HOST, Constants.MODEL_SERVER_PORT)):
        socketserver.UDPServer.__init__(self, server_address=server_address,
                                        RequestHandlerClass=socketserver.DatagramRequestHandler)
        self.request_queue_size = 1  # Max queue size for requests

        # Server thread variables
        self._running = False
        self._serve_thread = None

        # Model logic variables
        self._models = []
        self._sensor_listener = None
        self._prediction_time = None
        self._progress_bar = None
        Log.info("Created a Model Server Request Handler.")

    # Server running methods
    def serve_forever(self, poll_interval: float = ...) -> None:
        self._running = True
        self._serve_thread = threading.Thread(target=super().serve_forever)
        self._serve_thread.setName("Server Model Thread")
        self._serve_thread.start()

    def shutdown(self) -> None:
        self._running = False
        super().shutdown()

    def is_running(self):
        return self._running

    # Method logic methods
    def zero_sensors(self):
        assert self._sensor_listener is not None
        self._sensor_listener.zero_sensor_readings()

    def connect_model(self, models_dir_path, progress_bar):
        """
        Loads the models and starts the server
        :param model_id:
        :return:
        """
        # Setting the progress bar
        self._progress_bar = progress_bar

        # Starts the sensor reader
        progress_bar.add_count(1)
        progress_bar.set_metric_text(" Server & Hand Controller.   Status: Starting the sensor listener...")

        try:
            self._sensor_listener = SensorListener.SensorReadingsListener()
            self._sensor_listener.start_running()
            self._sensor_listener.start_reading()
            self._sensor_listener.start()
        except:
            self.sensor_listener = None
            InputConstraints.warn(
                "Warning, was not able to establish communications with COM3 port.\n" +
                "Please ensure that the sensor reading device is connected.")
            return False

        Log.info("Connecting to a model.")

        progress_bar.add_count(1)
        progress_bar.set_metric_text(" Server.   Status: Connecting client to Unity...")

        # Loads in the models
        progress_bar.set_metric_text(" Server.   Status: Loading the limb models...")

        self._models = []
        for finger_index in range(0, Constants.NUM_FINGERS):
            self._models.append([])
            for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                self._models[finger_index].append(tensorflow.keras.models.load_model(
                    models_dir_path + "f-" + str(finger_index) + "_l-" + str(limb_index) + ".mod",
                    custom_objects=None, compile=True, options=None
                ))
            progress_bar.add_count(1)

        # Running the server
        progress_bar.add_count(1)
        progress_bar.set_metric_text(" Server & Hand Controller.   Status: Running...")
        return True

    def disconnect_model(self):
        """
        Disconnects and stops the server.
        :return:
        """

        # Stops the sensor listener
        self._sensor_listener.stop_reading()
        self._sensor_listener.stop_running()
        self._sensor_listener = None

        # Stops the server
        Log.info("Disconnecting from a model.")
        return True

    # finish_request handles the request (runs the inputs by the model)
    def finish_request(self, request: bytes, client_address: Tuple[str, int]) -> None:

        if (self._sensor_listener is None):
            Log.error("'self._sensor_listener' is 'None' when executing 'finish_request'.")

        # Obtains limb data from the C# Unity script
        # IMPORTANT: Convention assumes the format "angl1 vel1 angl2 vel2 ... angl15 vel15"
        string_limb_data = request[0].decode().split(" ")
        limb_data = []
        for i in range(0, len(string_limb_data)):
            limb_data.append(
                General.constraint_number_value(float(string_limb_data[i]),
                                                Constants.MODEL_MIN_VAL, Constants.MODEL_MAX_VAL)
            )
            # if i % 2 == 1:
            #     # TODO, this is currently multiplying the velocity by the FPS, why?
            # limb_data[i] = limb_data[i] * FRAMES_PER_SECOND

        # Obtains the sensors data
        current_sensor_data = self._sensor_listener.get_readings_frame()  # Retrieves the sensors dictionary
        sensors_data = []
        for k in self._sensor_listener.get_key_list():
            sensors_data.append(
                General.constraint_number_value(
                    current_sensor_data[k], Constants.MODEL_MIN_VAL, Constants.MODEL_MAX_VAL)
            )

        # Creates the features list
        features = numpy.array(limb_data + sensors_data)

        # Computes the velocities that the virtual hand limbs should acquire # TODO, multithread the prediction
        # threaded_predictions = []
        next_velocities = []
        for finger_index in range(0, Constants.NUM_FINGERS):
            # threaded_predictions.append([])
            for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                # threaded_predictions[finger_index].append([])

                # Prediction
                to_predict = features.reshape(1, Constants.NUM_FEATURES)
                # threaded_predictions[finger_index][limb_index] = ThreadedPredictions(
                #     self._models[finger_index][limb_index], to_predict)

                next_velocities.append(General.constraint_number_value(
                    self._models[finger_index][limb_index](to_predict)[0][0].numpy(),
                    Constants.MODEL_MIN_VAL, Constants.MODEL_MAX_VAL))

        # # Wait (and polls) until all threaded prediction tasks are complete
        # is_done = False
        # while is_done is False:
        #     is_done = True
        #     for finger_index in range(0, Constants.NUM_FINGERS):
        #         for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
        #             is_done &= threaded_predictions[finger_index][limb_index].done
        #
        # # Adds the velocity data
        # for finger_index in range(0, Constants.NUM_FINGERS):
        #     for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
        #         next_velocities.append(threaded_predictions[finger_index][limb_index].result)

        # Prepared the velocities to send to the unity script
        string_velocities = ""
        for i in range(0, Constants.NUM_LIMBS_PER_FINGER * Constants.NUM_FINGERS):
            string_velocities += str(next_velocities[i]) + " "
        string_velocities = string_velocities.rstrip(" ")

        super().finish_request(request=request, client_address=client_address)

        # Sends the torques to the unity script
        # Returns the value to the client
        client_request_socket, client_request_address = self.get_request()[0][1], self.get_request()[1]
        client_request_socket.sendto(string_velocities.encode(), client_request_address)

        # Displays the amount of time it has taken to predict to the progress bar
        if self._progress_bar is not None:
            if self._prediction_time is not None:
                self._progress_bar.set_metric_text(
                    " Server & Hand Controller.   Status: Running..."
                    "   Time since last prediction: " + str(General.time_ms() - self._prediction_time) + " ms")
            self._prediction_time = General.time_ms()
