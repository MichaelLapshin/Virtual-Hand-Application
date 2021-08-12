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


def _dict_deepcopy(dictionary):
    d = {}
    for k in dictionary.keys():
        d[k] = dictionary[k]
    return d


class SensorReadingsListener(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)  # calls constructor of the Thread class
        self.daemon = True

        # Running variables
        self._buffer = ""  # Oldest element is first
        self._sensorReadings = {}
        self._running = False
        self._is_reading = False

        try:
            self.port = serial.Serial('COM3', 9600, timeout=100)  # for COM3
            time.sleep(0.5)
        except Exception as e:
            print("Warning, was not able to establish communications with COM3 port.")
            print("Error: ", e)
            if self.port.isOpen():
                print("Closed the port.")
                self.port.close()

    # Reading start/stop methods
    def start_reading(self):
        self._is_reading = True

    def stop_reading(self):
        self._is_reading = False

    def is_reading(self):
        return self._is_reading

    # Thread start/stop methods
    def start_running(self):
        self._running = True

    def stop_running(self):
        self._running = False
        self._is_reading = False
        time.sleep(1)
        if self.port.isOpen():
            self.port.close()

    def is_running(self):
        return self._running

    # Once the thread starts, continuously read from the port and add any data to the buffer
    def run(self):

        while self._running:
            time.sleep(1)

            self._buffer = ""
            # Finds the first character
            while self._is_reading and self._running and self.port.isOpen():
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
            while self._is_reading and self._running and self.port.isOpen():

                if self.port.inWaiting() > 0:
                    next_char = self.port.read().decode("utf-8")
                    if next_char == "\r":
                        next_char = ""
                    elif next_char == "\n":
                        next_char = ""

                    self._buffer += next_char

                    # Adds all sensor data accumulated in the _buffer to the dictionary
                    raw_buffer_data = self._buffer.split(" ")
                    if len(raw_buffer_data) > 0 and raw_buffer_data[0] == "":
                        raw_buffer_data.pop(0)
                    if len(raw_buffer_data) > 2:
                        used = ""
                        for index in range(0, max(int(len(raw_buffer_data) / 2) - 1, 0)):
                            used += raw_buffer_data[index * 2] + " " + raw_buffer_data[index * 2 + 1] + " "

                            # TODO: bad practice to rely on the try-catch statement, change to something else later
                            try:
                                self._sensorReadings[raw_buffer_data[index * 2]] = int(raw_buffer_data[index * 2 + 1])
                            except:
                                self._buffer = ""

                        self._buffer = self._buffer.lstrip(used.rstrip(" "))
                        self._buffer = self._buffer.lstrip(" ")

    # Returns unique keys, to be used after the system is setup for accuracy
    def get_key_list(self):
        return sorted(self._sensorReadings.keys())

    # Getter for the batch of sensor readings list
    def get_readings_frame(self):
        return _dict_deepcopy(self._sensorReadings)

    def print_raw_sensor_readings(self):
        print(str(self._sensorReadings))