"""
[SensorListener.py]
@description: API for receiving data from COM3 port.
@author: Michael Lapshin
"""
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # To remove the redundant warnings
import serial
import time
import threading

print("Imported the SensorListener.py class successfully.")


class _sensorReadingsListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)  # calls constructor of the Thread class
        self.daemon = True

        # Running variables
        self._buffer = ""  # Oldest element is first
        self._sensorReadings = {}
        self._wait4readings = True
        self._running = True

        try:
            self.port = serial.Serial('COM3', 9600, timeout=100)  # for COM3
            time.sleep(0.5)
        except Exception as e:
            print("Warning, was not able to establish communications with COM3 port.")
            print("Error: ", e)
            if self.port.isOpen():
                print("Closed the port.")
                self.port.close()

    def start_thread(self):
        self.start()

    # Simple quit function for the thread
    def stop(self):
        self._running = False
        time.sleep(1)
        if self.port.isOpen():
            self.port.close()

    # Once the thread starts, continuously read from the port and add any data to the _buffer
    def run(self):
        # Finds the first character
        while self._running:
            if self.port.inWaiting() > 0:
                next_char = self.port.read().decode("utf-8")
                self._buffer += next_char

                # Finds a space which can be potentially followed by a letter
                index = -1
                for i in range(0, len(self._buffer)):
                    if self._buffer[i] == ' ' or self._buffer[i] == '\n' or self._buffer[i] == '\r':
                        index = i
                        break

                if 0 <= index < len(self._buffer) - 1:
                    schar = str(self._buffer[index + 1])
                    self._buffer = self._buffer[index + 1::]
                    if schar not in [" ", "\r", "\n", ".", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                        break

        # Main decoding loop
        while self._running:

            if self.port.inWaiting() > 0:
                next_char = self.port.read().decode("utf-8")
                if next_char == "\r":
                    next_char = ""
                elif next_char == "\n":
                    next_char = ""

                self._buffer += next_char

                # Adds all sensor data accumulated in the _buffer to the dictionary
                raw__buffer_data = self._buffer.split(" ")
                if len(raw__buffer_data) > 0 and raw__buffer_data[0] == "":
                    raw__buffer_data.pop(0)
                if len(raw__buffer_data) > 2:
                    used = ""
                    for index in range(0, max(int(len(raw__buffer_data) / 2) - 1, 0)):
                        used += raw__buffer_data[index * 2] + " " + raw__buffer_data[index * 2 + 1] + " "

                        try:  # TODO. bad practice to rely on the try-catch statement, change to something else later
                            self._sensorReadings[raw__buffer_data[index * 2]] = int(raw__buffer_data[index * 2 + 1])
                        except:
                            self._buffer = ""

                    self._buffer = self._buffer.lstrip(used.rstrip(" "))
                    self._buffer = self._buffer.lstrip(" ")

                    # Checks if the dictionary is filled so that it can be used
                    all_keys_have_values = True
                    for readingKey in self._sensorReadings.keys():
                        if self._sensorReadings.get(readingKey) is None:
                            all_keys_have_values = False
                            break
                    if all_keys_have_values:
                        self._wait4readings = False

    # Returns unique keys, to be used after the system is setup for accuracy
    def get_key_list(self):
        return sorted(self._sensorReadings.keys())

    # Getter for the batch of sensor readings list
    def get_readings_frame(self):
        if not self._wait4readings:
            return self._dict_deepcopy(self._sensorReadings)
        return None

    # Adds a tag that will not allow data to return if the data set is not complete
    def wait4new_readings(self):
        for readingKey in self._sensorReadings.keys():
            self._sensorReadings[readingKey] = None
        self._wait4readings = True

    def print_raw_sensor_readings(self):
        # print("=== Sensor Readings ===")
        # for key in self._sensorReadings.keys():
        #     print(key, self._sensorReadings.get(key))
        print(str(self._sensorReadings))

    def _dict_deepcopy(self, dictionary):
        d = {}
        for k in dictionary.keys():
            d[k] = dictionary[k]
        return d

