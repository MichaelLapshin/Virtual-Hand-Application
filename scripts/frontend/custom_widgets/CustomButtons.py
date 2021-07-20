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

    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None, command=None):
        tkinter.Button.__init__(self, root, text=text, command=command, padx=padx, pady=pady)
        self.anchor(tkinter.CENTER)
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
    UNSELECTED_COLOUR = General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_C)
    SELECTED_COLOUR = General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_D)

    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)

        # Configurations
        self.config(bg=NavigationButton.UNSELECTED_COLOUR)
        self.config(padx=8, pady=5)
        self.grid(padx=8, pady=8)
        self.grid(sticky=tkinter.NSEW)

class InformationButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.config(bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_C))
        self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

        self.grid(sticky=tkinter.NSEW)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)


class AccountButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.config(bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_E))
        self.config(padx=12, pady=5)
        self.grid(sticky=tkinter.N)
        self.grid(padx=16, pady=16)


class SearchButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.config(bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_C))
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

class PlotButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.anchor(tkinter.CENTER)

        self.config(bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_C))
        self.config(padx=12, pady=5)
        self.grid(sticky=tkinter.N)
        self.grid(padx=16, pady=16)

class SettingsButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=None):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.config(bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_C))
        self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

        self.grid(sticky=tkinter.NSEW)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)