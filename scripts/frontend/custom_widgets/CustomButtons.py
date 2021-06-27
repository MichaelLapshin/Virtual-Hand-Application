import tkinter
from scripts import Warnings, General

# Custom Buttons constants
from scripts.frontend import Constants

BUTTON_PADDING_X = 12
BUTTON_PADDING_Y = 8

"""
    Parent generic button
"""


class Button(tkinter.Button):

    def __init__(self, root, column, row, columnspan=1, rowspan=1, padx=5, pady=5, text=None, command=None):
        tkinter.Button.__init__(self, root, text=text, command=command, padx=padx, pady=pady)
        self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

    def select(self):
        Warnings.not_complete()

    def unselect(self):
        Warnings.not_complete()

    def toggle_select(self):
        Warnings.not_complete()

    def disable(self):
        self["state"] = tkinter.DISABLED

    def enable(self):
        self["state"] = tkinter.NORMAL


"""
    Custom buttons
"""


class NavigationButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.anchor(tkinter.CENTER)
        self.config(bg=General.washed_colour_hex(Constants.BASE_BLUE_COLOUR, Constants.Colour40))
        self.config(padx=8, pady=5)
        self.grid(padx=8, pady=8)


class InformationButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour60))
        self.config(padx=12, pady=5)
        self.grid(sticky='N')
        self.grid(padx=16, pady=16)


class SearchButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.anchor(tkinter.CENTER)


class PlotButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.anchor(tkinter.CENTER)
