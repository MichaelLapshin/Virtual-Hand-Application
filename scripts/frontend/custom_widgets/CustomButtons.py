import tkinter
from scripts import Warnings, General, Parameters, Constants

# Custom Buttons constants
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

BUTTON_PADDING_X = 12
BUTTON_PADDING_Y = 8

"""
    Parent generic button
"""


class Button(tkinter.Button, WidgetInterface):

    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None, command=Warnings.not_complete):
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
    UNSELECTED_COLOUR = None
    SELECTED_COLOUR = None

    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=Warnings.not_complete):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)

        # Configurations
        self.config(padx=8, pady=5)
        self.grid(padx=8, pady=8)
        self.grid(sticky=tkinter.NSEW)

    def update_colour(self):
        super().update_colour()
        NavigationButton.UNSELECTED_COLOUR = General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_C)
        NavigationButton.SELECTED_COLOUR = General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_D)

        self.config(bg=NavigationButton.UNSELECTED_COLOUR)


class InformationButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=Warnings.not_complete):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)

        self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

        self.grid(sticky=tkinter.NSEW)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_C))


class AccountButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=Warnings.not_complete):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.config(padx=12, pady=5)
        self.grid(sticky=tkinter.N)
        self.grid(padx=16, pady=16)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_E))


class SearchButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=Warnings.not_complete):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_C))


class PlotButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=Warnings.not_complete):
        Button.__init__(self, root, column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.anchor(tkinter.CENTER)

        self.config(padx=12, pady=5)
        self.grid(sticky=tkinter.N)
        self.grid(padx=16, pady=16)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_C))


class SettingsButton(Button):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None, command=Warnings.not_complete):
        Button.__init__(self, root,
                        column=column, row=row,
                        columnspan=columnspan, rowspan=rowspan,
                        text=text, command=command)
        self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

        self.grid(sticky=tkinter.NSEW)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_C))
