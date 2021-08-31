"""
[DatasetSmoother.py]
@description: Script for processing the training data (eg. smoothing the data, velocity, acceleration, etc.)
@author: Michael Lapshin
"""
import os

from scripts import Log, Parameters, Constants, Warnings
from scripts.backend.database import DatabaseDatasets
from scripts.backend.logic import Job
from scripts.frontend.logic import DatasetRecorder

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # To remove the redundant warnings
import numpy
import h5py
import math
import numpy as np
import scipy.signal
import time

"""
# Training data format
time | sensor | angle | velocity | acceleration

time: time in nanoseconds since the start of the training sequence
sensor: [sensor1,sensor2,...,sensorN]
    - zeroed-sensor readings
angle: [[[fingerAngles]*fingerLimb]*fingers]
    - angles of the finger limbs
velocity: [[[fingerAngularVelocities]*fingerLimb]*fingers]
    - velocity of the finger limbs
acceleration: [[[fingerAngularAcceleration]*fingerLimb]*fingers] 
    - acceleration of the finger limbs
* Note: the angle(and its derivatives) lists is in the 5 by 3 by N format
"""


# Original lists which the post-processing will be based off of
def _float_int_unknownArray2list(u_list):
    if type(u_list) == float or type(u_list) == int \
            or type(u_list) == numpy.int32 or type(u_list) == numpy.float64:
        return u_list
    elif type(u_list) != list:
        u_list = list(u_list)

    for i in range(0, len(u_list)):
        u_list[i] = _float_int_unknownArray2list(u_list[i])

    return u_list


# Post-processing to obtain limb angular velocity/acceleration
def _generate_derivative_limb_data(original_list, frames_per_second):
    derivative_list = []
    for index in range(1, len(original_list)):
        derivative_list.append((original_list[index] - original_list[index - 1]) * frames_per_second)
    derivative_list.insert(0, derivative_list[0])  # assigns the first element to be that of the second
    return derivative_list


class JobSmooth(Job.Job):
    def __init__(self, title, dataset_parent_id, dataset_num_frames, dataset_fps, dataset_frames_shift,
                 sensor_savagol_distance, sensor_savagol_degree, angle_savagol_distance, angle_savagol_degree,
                 dataset_name, dataset_owner_name, dataset_date, dataset_permission, dataset_rating, dataset_is_raw,
                 info=None):
        Job.Job.__init__(self, title=title, info=info)
        self.dataset_parent_id = dataset_parent_id
        self.dataset_num_frames = dataset_num_frames
        self.dataset_fps = dataset_fps
        self.dataset_frames_shift = dataset_frames_shift
        self.sensor_savagol_distance = sensor_savagol_distance
        self.sensor_savagol_degree = sensor_savagol_degree
        self.angle_savagol_distance = angle_savagol_distance
        self.angle_savagol_degree = angle_savagol_degree
        self.dataset_name = dataset_name
        self.dataset_owner_name = dataset_owner_name
        self.dataset_date = dataset_date
        self.dataset_permission = dataset_permission
        self.dataset_rating = dataset_rating
        self.is_raw = dataset_is_raw

        # For the task
        self.set_max_progress(100)

    def perform_task(self):
        Log.info("Starting to smooth the dataset with id '" + str(self.dataset_parent_id) + "'")

        self.set_progress(0, "Starting the dataset smoothing.")

        # Obtains old file input
        reader = h5py.File(
            Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + str(self.dataset_parent_id) + ".ds", 'r')

        old_sensor_list = _float_int_unknownArray2list(reader.get("sensor"))
        old_angle_list = _float_int_unknownArray2list(reader.get("angle"))

        if DatasetRecorder.Recorder.RECORD_TIME is True:
            old_time_list = _float_int_unknownArray2list(reader.get("time"))
            assert len(old_time_list) == len(old_sensor_list[0]) == len(old_angle_list[0][0])
        else:
            assert len(old_sensor_list[0]) == len(old_angle_list[0][0])

        reader.close()

        self.set_progress(5, "Loaded in the raw dataset")

        # Empty lists to be filled by the program
        if DatasetRecorder.Recorder.RECORD_TIME is True:
            time_list = []
            Log.warning("The time list is probably having values appended to it.")
        sensor_list = [[] for a in range(0, Constants.NUM_FINGERS)]
        angle_list = [[[] for b in range(0, Constants.NUM_LIMBS_PER_FINGER)] for a in range(0, Constants.NUM_FINGERS)]
        velocity_list = [[[] for b in range(0, Constants.NUM_LIMBS_PER_FINGER)] for a in
                         range(0, Constants.NUM_FINGERS)]
        acceleration_list = [[[] for b in range(0, Constants.NUM_LIMBS_PER_FINGER)] for a in
                             range(0, Constants.NUM_FINGERS)]

        # Smooths the dataset
        progress_points = 60
        for sensor_index in range(0, Constants.NUM_SENSORS):
            sensor_list[sensor_index] = \
                scipy.signal.savgol_filter(x=old_sensor_list[sensor_index],
                                           window_length=self.sensor_savagol_distance,
                                           polyorder=self.sensor_savagol_degree)
            self.add_progress(progress_points / float(Constants.NUM_SENSORS),
                              "Smoothing the dataset sensors: " + str(sensor_index) + "/" + str(Constants.NUM_SENSORS))

        for finger_index in range(0, Constants.NUM_FINGERS):
            for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                angle_list[finger_index][limb_index] = \
                    scipy.signal.savgol_filter(x=old_angle_list[finger_index][limb_index],
                                               window_length=self.angle_savagol_distance,
                                               polyorder=self.angle_savagol_degree)
                self.add_progress(progress_points / float(Constants.NUM_SENSORS),
                                  "Smoothing the dataset angles: " + str(finger_index * 3 + limb_index) + "/" + str(
                                      Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER))

        # Shifts the frame
        progress_points = 10
        for sensor_index in range(0, Constants.NUM_SENSORS):
            sensor_list[sensor_index] = sensor_list[sensor_index][:-self.dataset_frames_shift:]
            self.add_progress(
                progress_points / float(Constants.NUM_SENSORS + Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER)
                , "Shifting data (cropping sensors list from the back)")

        for finger_index in range(0, Constants.NUM_FINGERS):
            for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                angle_list[finger_index][limb_index] = angle_list[finger_index][limb_index][self.dataset_frames_shift::]
                self.add_progress(
                    progress_points / float(
                        Constants.NUM_SENSORS + Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER)
                    , "Shifting data (cropping angles list from the front)")

        # Generates derivative data
        progress_points = 20
        for finger_index in range(0, Constants.NUM_FINGERS):
            for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                # Calculated limb velocities based on the limb angles
                velocity_list[finger_index][limb_index] = _generate_derivative_limb_data(
                    angle_list[finger_index][limb_index], frames_per_second=self.dataset_fps)

                # Calculated limb accelerations based on the limb velocities
                acceleration_list[finger_index][limb_index] = _generate_derivative_limb_data(
                    velocity_list[finger_index][limb_index], frames_per_second=self.dataset_fps)

                self.add_progress(progress_points / float(Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER),
                                  "Calculating the derivative values of the angles.")

        # Just in case
        if DatasetRecorder.Recorder.RECORD_TIME is True:
            assert len(angle_list[0][0]) == len(velocity_list[0][0]) == len(acceleration_list[0][0]) \
                   == len(time_list) == len(sensor_list[0] == self.dataset_num_frames)
        else:
            assert len(angle_list[0][0]) == len(velocity_list[0][0]) == len(acceleration_list[0][0]) \
                   == len(sensor_list[0] == self.dataset_num_frames)

        self.dataset_num_frames = len(angle_list[0][0])
        self.set_progress(95, "Saving the temporary dataset file.")

        # Saves the training data
        file_name = Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + Constants.TEMP_SAVE_DATASET_NAME
        hf = h5py.File(file_name, 'w')
        if DatasetRecorder.Recorder.RECORD_TIME is True:
            hf.create_dataset("time", data=time_list)
        hf.create_dataset("sensor", data=sensor_list)
        hf.create_dataset("angle", data=angle_list)
        hf.create_dataset("velocity", data=velocity_list)
        hf.create_dataset("acceleration", data=acceleration_list)
        hf.close()

        self.set_progress(98, "Saving the smoothed dataset into the database.")

        # Saves the data on the database
        result = DatabaseDatasets.create_new_dataset(
            name=self.dataset_name, owner_id=self.dataset_owner_name, date=self.dataset_date,
            permission=self.dataset_permission, rating=self.dataset_rating, is_raw=self.is_raw,
            num_frames=self.dataset_num_frames, fps=self.dataset_fps, frames_shift=self.dataset_frames_shift,
            sensor_savagol_distance=self.sensor_savagol_distance, sensor_savagol_degree=self.sensor_savagol_degree,
            angle_savagol_distance=self.angle_savagol_distance, angle_savagol_degree=self.angle_savagol_degree,
            file=file_name, contains_vel_acc_data=True)

        self.set_progress(100, "The dataset was saved into the database.")

        if result is True:
            Log.info("The smoothed dataset was saved on the database.")
        else:
            Log.warning("The smoothed dataset was not saved on the database.")
