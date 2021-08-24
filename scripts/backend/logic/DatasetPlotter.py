import PIL
import werkzeug.datastructures

from scripts import Warnings, Parameters, Constants, Log
from scripts.backend.database import DatabasePlots
from scripts.backend.logic import Job

import h5py
import matplotlib.pyplot as plt
import numpy as np


# import pandas as pd

class JobDatasetPlotter(Job.Job):
    def __init__(self, title, dataset_id, plot_vel_acc=False, info=None):
        Job.Job.__init__(self, title=title, info=info)
        self.dataset_id = dataset_id
        self.plot_vel_acc = plot_vel_acc

        Log.info("A new dataset plotting task has been created for dataset with id '" + str(self.dataset_id) + "'")

    def save_sensors_image(self, sensor_num):
        plot_path = Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_SENSORS_PATH + Constants.TEMP_SAVE_IMAGE_NAME
        plt.savefig(plot_path, bbox_inches='tight')
        plt.clf()

        # Stores the file inside the database
        file = PIL.Image.open(plot_path)
        DatabasePlots.create_dataset_sensor_image_entry(dataset_id=self.dataset_id, sensor_num=sensor_num, file=file)

    def save_finger_image(self, finger_num, metric):
        plot_path = Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_FINGERS_PATH + Constants.TEMP_SAVE_IMAGE_NAME
        plt.savefig(plot_path, bbox_inches='tight')
        plt.clf()

        # Stores the file inside the database
        file = PIL.Image.open(plot_path)
        DatabasePlots.create_dataset_finger_image_entry(
            dataset_id=self.dataset_id, finger_num=finger_num, metric=metric, file=file)

    def perform_task(self):

        self.set_progress(0, "Starting to plot the dataset with id '" + str(self.dataset_id) + "'")

        reader = h5py.File(Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + str(self.dataset_id) + ".ds", 'r')

        # Plots the data below
        # plt.title("Time")
        # plt.plot(np.array(reader.get("time")))
        # plt.xlabel("Frame")
        # plt.ylabel("Milliseconds since Start")
        # plt.savefig(training_name + "_Time.png", bbox_inches='tight')
        # self.save_image()

        # finger_name = ["Thumb Finger", "Index Finger", "Middle Finger", "Ring Finger", "Pinky Finger"]
        # limb_part = ["proximal", "middle", "distal"]
        # finger_label = ["thumb", "index", "middle", "ring", "pinky"]

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
            self.save_sensors_image(sensor_num=sensor)
            self.add_progress(1, "Plotting the sensors: " + str(sensor) + "/" + str(sensors_count))

        for finger in range(0, fingers_count):
            plt.plot(np.array(reader.get("angle")[finger][0]))
            plt.plot(np.array(reader.get("angle")[finger][1]))
            plt.plot(np.array(reader.get("angle")[finger][2]))
            plt.title(label=Constants.FINGER_TYPE[finger] + " Finger")
            plt.xlabel("Frame")
            plt.ylabel("Angle (radians)")
            plt.legend(Constants.LIMB_TYPE)
            self.save_finger_image(finger_num=finger, metric=Constants.METRIC.index("Angle"))
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
        self.set_progress(total_image, "The dataset plotting is complete.")
