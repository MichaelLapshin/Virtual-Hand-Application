import pathlib

import PIL

from scripts import Parameters, Constants, Log
from scripts.backend.database import DatabasePlots
from scripts.logic import Job

import h5py
import matplotlib.pyplot as plt
import numpy as np


class JobDatasetPlotter(Job.Job):
    def __init__(self, title, dataset_id, plot_vel_acc=False, info=None):
        Job.Job.__init__(self, title=title, info=info)
        self.dataset_id = dataset_id
        self.plot_vel_acc = plot_vel_acc

        Log.info("A new dataset plotting task has been created for dataset with id '" + str(self.dataset_id) + "'")

    def save_sensor_image(self, sensor_num):
        # Create a database entry
        image_id = DatabasePlots.create_dataset_sensor_image_entry(dataset_id=self.dataset_id, sensor_num=sensor_num)

        # Stores the file locally
        plt.grid(True)
        plt.savefig(pathlib.Path(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_SENSORS_PATH
                                 + str(image_id) + Constants.IMAGE_EXT, bbox_inches='tight'))
        plt.clf()

    def save_finger_image(self, finger_num, metric):
        # Stores the file inside the database
        image_id = DatabasePlots.create_dataset_finger_image_entry(dataset_id=self.dataset_id,
                                                                   finger_num=finger_num, metric=metric)

        # Saves the file locally
        plt.grid(True)
        plt.savefig(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_FINGERS_PATH
                    + str(image_id) + Constants.IMAGE_EXT, bbox_inches='tight')
        plt.clf()

    def perform_task(self):
        Log.info("The plotting of dataset with id '" + str(self.dataset_id) + "' has begun.")
        self.set_progress(0, "Starting to plot the dataset with id '" + str(self.dataset_id) + "'")

        reader = h5py.File(Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH
                           + str(self.dataset_id) + Constants.DATASET_EXT, 'r')

        # Plots the data below
        sensors_count = len(list(reader.get("sensor")))
        fingers_count = len(list(reader.get("angle")))

        total_image = sensors_count + fingers_count
        if self.plot_vel_acc is True:
            total_image += fingers_count * 2

        # For the task
        self.set_max_progress(total_image)

        # Saves/displays the graphs
        for sensor in range(0, sensors_count):
            plt.plot(np.array(reader.get("sensor")[sensor]))
            plt.legend(str(sensor))
            plt.title(label="Sensors")
            plt.xlabel("Frame")
            plt.ylabel("Sensor Reading")
            self.save_sensor_image(sensor_num=sensor)
            self.add_progress(1, "Plotting the sensors: " + str(sensor) + "/" + str(sensors_count))

        for finger in range(0, fingers_count):
            plt.plot(np.array(reader.get("angle")[finger][0]))
            plt.plot(np.array(reader.get("angle")[finger][1]))
            plt.plot(np.array(reader.get("angle")[finger][2]))
            plt.title(label=Constants.FINGER_TYPE[finger] + " Finger")
            plt.xlabel("Frame")
            plt.ylabel("Angle (radians)")
            plt.legend(Constants.LIMB_TYPE)
            self.save_finger_image(finger_num=finger, metric=Constants.METRIC.index("Position"))
            self.add_progress(1, "Plotting the angles: " + str(finger) + "/" + str(fingers_count))

        if self.plot_vel_acc is True:
            assert (reader.get("velocity") is not None) and (reader.get("acceleration") is not None)

            for finger in range(0, len(list(reader.get("velocity")))):
                plt.plot(np.array(reader.get("velocity")[finger][0]))
                plt.plot(np.array(reader.get("velocity")[finger][1]))
                plt.plot(np.array(reader.get("velocity")[finger][2]))
                plt.title(label=Constants.FINGER_TYPE[finger] + " Finger")
                plt.xlabel("Frame")
                plt.ylabel("Velocity (radians)")
                plt.legend(Constants.LIMB_TYPE)
                self.save_finger_image(finger_num=finger, metric=Constants.METRIC.index("Velocity"))
                self.add_progress(1, "Plotting the velocities: " + str(finger) + "/" + str(fingers_count))

            for finger in range(0, len(list(reader.get("acceleration")))):
                plt.plot(np.array(reader.get("acceleration")[finger][0]))
                plt.plot(np.array(reader.get("acceleration")[finger][1]))
                plt.plot(np.array(reader.get("acceleration")[finger][2]))
                plt.title(label=Constants.FINGER_TYPE[finger] + " Finger")
                plt.xlabel("Frame")
                plt.ylabel("Acceleration (radians)")
                plt.legend(Constants.LIMB_TYPE)
                self.save_finger_image(finger_num=finger, metric=Constants.METRIC.index("Acceleration"))
                self.add_progress(1, "Plotting the accelerations: " + str(finger) + "/" + str(fingers_count))

        reader.close()
        self.complete_progress("The dataset plotting is complete.")
        Log.info("The plotting of dataset with id '" + str(self.dataset_id) + "' is complete.")
