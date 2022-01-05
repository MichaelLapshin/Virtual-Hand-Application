import h5py

from scripts import Log, Parameters, Constants, General
from scripts.backend.database import DatabaseDatasets
from scripts.logic import Job
from scripts.frontend.logic import DatasetRecorder


class JobMerge(Job.Job):
    def __init__(self, dataset_id, dataset_ids, info=None):
        Job.Job.__init__(self, title="Merging Datasets: " + str(dataset_ids), info=info)
        self.dataset_id = dataset_id
        self.dataset_ids = dataset_ids
        self.set_max_progress(len(self.dataset_ids) + 3)

    def perform_task(self):

        # Empty lists to be filled by the program
        if DatasetRecorder.Recorder.RECORD_TIME is True:
            time_list = []
            Log.warning("The time list is probably having values appended to it.")
        sensor_list = [[] for a in range(0, Constants.NUM_FINGERS)]
        angle_list = [[[] for b in range(0, Constants.NUM_LIMBS_PER_FINGER)] for a in range(0, Constants.NUM_FINGERS)]

        # Merges the datasets
        for id in self.dataset_ids:
            # Reads the data from the hdf5 file (and asserts the lengths just in case)
            reader = h5py.File(
                Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + str(id) + Constants.DATASET_EXT, 'r')

            partial_sensor_list = General.float_int_unknownArray2list(reader.get("sensor"))
            partial_angle_list = General.float_int_unknownArray2list(reader.get("angle"))

            if DatasetRecorder.Recorder.RECORD_TIME is True:
                partial_time_list = General.float_int_unknownArray2list(reader.get("time"))
                assert len(partial_time_list) == len(partial_sensor_list[0]) == len(partial_angle_list[0][0])
            else:
                if len(partial_sensor_list[0]) != len(partial_angle_list[0][0]):
                    Log.blocker(
                        "Could not generate dataset since len(partial_sensor_list[0]) != len(partial_angle_list[0][0]. "
                        + str(len(partial_sensor_list[0])) + " != " + str(len(partial_angle_list[0][0])))
                assert len(partial_sensor_list[0]) == len(partial_angle_list[0][0])

            reader.close()

            # Appends the sensor data to the in-memory arrays
            for sensor_index in range(0, Constants.NUM_SENSORS):
                sensor_list[sensor_index] += partial_sensor_list[sensor_index]

            # Appends the finger data to the in-memory arrays
            for finger_index in range(0, Constants.NUM_FINGERS):
                for limb_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                    angle_list[finger_index][limb_index] += partial_angle_list[finger_index][limb_index]

            # Appends the time data to the in-memory arrays
            if DatasetRecorder.Recorder.RECORD_TIME is True:
                time_list += partial_time_list

        # Assertions of lengths (just in case)
        if DatasetRecorder.Recorder.RECORD_TIME is True:
            assert len(angle_list[0][0]) == len(time_list) == len(sensor_list[0])
        else:
            assert len(angle_list[0][0]) == len(sensor_list[0])

        dataset_num_frames = len(angle_list[0][0])
        self.set_progress(len(self.dataset_ids) + 1, "Saving the temporary dataset file.")

        # Saves the training data
        file_name = Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH \
                    + str(self.dataset_id) + Constants.DATASET_EXT
        hf = h5py.File(file_name, 'w')
        if DatasetRecorder.Recorder.RECORD_TIME is True:
            hf.create_dataset("time", data=time_list)
        hf.create_dataset("sensor", data=sensor_list)
        hf.create_dataset("angle", data=angle_list)
        hf.close()

        self.set_progress(len(self.dataset_ids) + 2, "Saving the merged dataset into the database.")

        self.complete_progress("The new merged dataset was saved into the database.")

        Log.info("The merged dataset was successfully saved locally.")
