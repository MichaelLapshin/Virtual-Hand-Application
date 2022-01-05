"""
[DatasetSmoother.py]
@description: Script for processing the training data (eg. smoothing the data, velocity, acceleration, etc.)
@author: Michael Lapshin
"""
import os

from scripts import Log, Parameters, Constants, General
from scripts.backend.database import DatabaseDatasets
from scripts.logic import Job
from scripts.frontend.logic import DatasetRecorder

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # To remove the redundant warnings
import h5py
import scipy.signal

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


# Post-processing to obtain limb angular velocity/acceleration
def _generate_derivative_limb_data(original_list, frames_per_second):
    derivative_list = []
    for index in range(1, len(original_list)):
        derivative_list.append((original_list[index] - original_list[index - 1]) * frames_per_second)
    derivative_list.insert(0, derivative_list[0])  # assigns the first element to be that of the second
    return derivative_list


class JobSmooth(Job.Job):
    def __init__(self, dataset_id, dataset_parent_id, dataset_num_frames, dataset_fps,
                 sensor_savagol_distance, sensor_savagol_degree, angle_savagol_distance, angle_savagol_degree,
                 info=None):
        Job.Job.__init__(self, title="Smoothing Dataset: " + str(dataset_parent_id), info=info)
        self.dataset_id = dataset_id
        self.dataset_parent_id = dataset_parent_id
        self.dataset_num_frames = dataset_num_frames
        self.dataset_fps = dataset_fps
        self.sensor_savagol_distance = sensor_savagol_distance
        self.sensor_savagol_degree = sensor_savagol_degree
        self.angle_savagol_distance = angle_savagol_distance
        self.angle_savagol_degree = angle_savagol_degree

        # For the task
        self.set_max_progress(100)

    def perform_task(self):
        Log.info("Starting to smooth the dataset with id '" + str(self.dataset_parent_id) + "'")

        self.set_progress(0, "Starting the dataset smoothing.")

        # Obtains old file input
        reader = h5py.File(
            Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + str(
                self.dataset_parent_id) + Constants.DATASET_EXT, 'r')

        old_sensor_list = General.float_int_unknownArray2list(reader.get("sensor"))
        old_angle_list = General.float_int_unknownArray2list(reader.get("angle"))

        if DatasetRecorder.Recorder.RECORD_TIME is True:
            old_time_list = General.float_int_unknownArray2list(reader.get("time"))
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
        progress_points = 65
        for sensor_index in range(0, Constants.NUM_SENSORS):
            sensor_list[sensor_index] = \
                scipy.signal.savgol_filter(x=old_sensor_list[sensor_index],
                                           window_length=self.sensor_savagol_distance,
                                           polyorder=self.sensor_savagol_degree)
            self.add_progress(
                progress_points / float(Constants.NUM_SENSORS + Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER),
                "Smoothing the dataset sensors: " + str(sensor_index) + "/" + str(Constants.NUM_SENSORS))

        for finger_index in range(0, Constants.NUM_FINGERS):
            for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                angle_list[finger_index][limb_index] = \
                    scipy.signal.savgol_filter(x=old_angle_list[finger_index][limb_index],
                                               window_length=self.angle_savagol_distance,
                                               polyorder=self.angle_savagol_degree)
                self.add_progress(progress_points / float(
                    Constants.NUM_SENSORS + Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER),
                                  "Smoothing the dataset angles: " + str(finger_index * 3 + limb_index) + "/" + str(
                                      Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER))

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
                   == len(time_list) == len(sensor_list[0]) == self.dataset_num_frames
        else:
            assert len(angle_list[0][0]) == len(velocity_list[0][0]) == len(acceleration_list[0][0]) \
                   == len(sensor_list[0]) == self.dataset_num_frames

        self.dataset_num_frames = len(angle_list[0][0])
        self.set_progress(95, "Saving the temporary dataset file.")

        # Saves the training data
        file_name = Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH \
                    + str(self.dataset_id) + Constants.DATASET_EXT
        hf = h5py.File(file_name, 'w')
        if DatasetRecorder.Recorder.RECORD_TIME is True:
            hf.create_dataset("time", data=time_list)
        hf.create_dataset("sensor", data=sensor_list)
        hf.create_dataset("angle", data=angle_list)
        hf.create_dataset("velocity", data=velocity_list)
        hf.create_dataset("acceleration", data=acceleration_list)
        hf.close()

        self.complete_progress("The dataset file is saved.")
        Log.info("Done smoothing the dataset with id '" + str(self.dataset_id) + "'")
