"""
[Logger.py]
@description: A class used to log data of different priorities
"""
import sys

class Logger:
    def __init__(self, log_name):
        self.log_lvl = 0  # Logs everything
        sys.stdout = open("..\\logs\\" + log_name + ".log", 'w')

    def __init__(self, file_name, log_lvl):
        self.__init__(file_name)
        self.log_lvl = log_lvl

    def print_on_lvl(self, text, lvl):
        if self.log_lvl <= lvl:
            print(text)

    def log(self, text):
        if self.log_lvl <= 0:
            print(text)

    def info(self, text):
        if self.log_lvl <= 1:
            print(text)

    def debug(self, text):
        if self.log_lvl <= 2:
            print(text)

    def critical(self, text):
        if self.log_lvl <= 3:
            print(text)

    def error(self, text):
        if self.log_lvl <= 4:
            print(text)

    def set_log_lvl(self, log_lvl):
        self.log_lvl = log_lvl
