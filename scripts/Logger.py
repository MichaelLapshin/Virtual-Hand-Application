"""
[Logger.py]
@description: A class used to log data of different priorities
"""
import sys

class Log:
    def __init__(self, file_name, log_lvl=00):
        self.__init__(file_name)
        self.log_lvl = log_lvl
        self.file = open("..\\logs\\" + file_name + ".log", 'w')

    def print_on_lvl(self, text, lvl):
        if self.log_lvl <= lvl:
            self.file.write(text + "\n")

    def log(self, text):
        self.print_on_lvl(text, 0)

    def info(self, text):
        self.print_on_lvl(text, 1)

    def debug(self, text):
        self.print_on_lvl(text, 2)

    def critical(self, text):
        self.print_on_lvl(text, 3)

    def error(self, text):
        self.print_on_lvl(text, 4)

    def set_log_lvl(self, log_lvl):
        self.log_lvl = log_lvl
