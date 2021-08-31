"""
[DataObtainer.py]
@description: Script for obtaining finger angles and sensor readings.
@author: Michael Lapshin
"""
import os
import threading

from scripts import Constants, Parameters, Log

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # To remove the redundant warnings
import time
import h5py


def time_ms():
    return int(round(time.time() * 1000))


class Recorder(threading.Thread):
    RECORD_TIME = False

    def __init__(self, sensor_listener, hand_angler, init_sleep_seconds, training_length_seconds,
                 frames_per_second, progress_bar):
        threading.Thread.__init__(self)

        # Assert that the hand angler is running
        assert (sensor_listener is not None) and (hand_angler is not None)
        assert hand_angler.is_running()

        # Captures the input variables
        self.sensor_listener = sensor_listener
        self.hand_angler = hand_angler
        self.init_sleep_seconds = init_sleep_seconds
        self.training_length_seconds = training_length_seconds
        self.frames_per_second = frames_per_second
        self.progress_bar = progress_bar
        self._number_of_frames = None

        # Running variables
        self._zeroes = {}
        self._running = False
        self._success = False

    def run(self):
        # Pre-running
        self._success = False
        self.sensor_listener.start_reading()

        # Assert that they are running and are producing data
        assert self.sensor_listener.is_running() and self.hand_angler.is_running()
        assert self.sensor_listener.is_reading() and self.hand_angler.is_watching()

        # Initial sleep
        self.progress_bar.set_max_count(self.init_sleep_seconds)
        self.progress_bar.set_metric_text(" seconds left before zeroing")
        zero_start_time_ms = time_ms()
        while time_ms() - zero_start_time_ms < 1000 * self.init_sleep_seconds and self._running:
            time.sleep(0.0001)
            self.progress_bar.set_count(self.init_sleep_seconds - (time_ms() - zero_start_time_ms) / 1000.0)

        if self._running is False:
            self._success = False

        # Zeros the sensor data
        self._zeros = self.sensor_listener.get_readings_frame()

        """
        # Training data format
        time | sensor | angle | velocity | acceleration

        time: time in nanoseconds since the start of the training sequence
        sensor: [sensor1,sensor2,...,sensorN]
            - zeroed-sensor readings
        angle: [[fingerAngularVelocities]*fingers]
            - angles of the finger limbs
        velocity: [[fingerAngularVelocities]*fingers]
            - velocity of the finger limbs
        acceleration: [[fingerAngular acceleration]*fingers] 
            - acceleration of the finger limbs
        * Note: the angle(and its derivatives) lists is in the 5 by 3 by N format
        """

        # Starts the recording

        # Dictionaries
        time_list = None
        if Recorder.RECORD_TIME:
            time_list = []
        sensor_list = []
        angle_list = [[[] for b in range(0, 3)] for a in range(0, 5)]

        # Indexes the incoming sensor data (sensor key character -> number between 0 and total sensor count)
        sensor_to_index_map = {}
        key_list = self.sensor_listener.get_key_list()
        key_index = 0
        for key in key_list:
            sensor_to_index_map[key] = key_index
            key_index += 1
            sensor_list.append([])

        Log.info("Found the sensors key characters: " + str(self.sensor_listener.get_key_list()))

        # Update progress bar
        self.progress_bar.set_max_count(self.training_length_seconds)
        self.progress_bar.set_metric_text(" seconds of training")

        # The data gathering
        zero_time_ms = time_ms()
        for frame_num in range(0, self.training_length_seconds * self.frames_per_second):

            # Update progress bar
            self.progress_bar.set_count((time_ms() - zero_time_ms) / 1000.0)

            # Stop the data processing if the running is stopped
            if self._running is False:
                break

            # Halts the program until it is time to take the next frame of the training data
            while time_ms() - zero_time_ms < 1000 / float(self.frames_per_second) * frame_num:
                time.sleep(0.001)

            # Waits until new sensor data is available
            current_sensor_data = self.sensor_listener.get_readings_frame()

            """Stores the data"""

            # Adds sensor data
            for key in key_list:
                sensor_list[sensor_to_index_map[key]].append(current_sensor_data[key] - self._zeros[key])

            # sensor_data.wait4new_readings()
            # Adds limb angle data
            limb_data = self.hand_angler.get_all_limb_angles()
            for finger_index in range(0, 5):
                for limb_index in range(0, 3):
                    angle_list[finger_index][limb_index].append(limb_data[finger_index][limb_index])

            # Adds time data
            if time_list is not None:
                time_list.append(time_ms() - zero_time_ms)

        if self._running is True:
            # Saves the training data
            hf = h5py.File(Parameters.PROJECT_PATH + Constants.TEMP_DATASET_PATH + Constants.TEMP_SAVE_DATASET_NAME,
                           'w')
            if time_list is not None:
                hf.create_dataset("time", data=time_list)
            hf.create_dataset("sensor", data=sensor_list)
            hf.create_dataset("angle", data=angle_list)
            hf.close()
            self._success = True
            self._number_of_frames = len(sensor_list[0])

        # Post-running
        self._running = False
        self.sensor_listener.stop_reading()
        self.progress_bar.reset()

    def get_training_length_seconds(self):
        return self.training_length_seconds

    def is_successful(self):
        return self._success

    def start(self):
        self._running = True
        self._success = False
        super().start()

    def stop(self):
        self._running = False

    def is_running(self):
        return self._running

    def get_number_of_frames(self):
        return self._number_of_frames
