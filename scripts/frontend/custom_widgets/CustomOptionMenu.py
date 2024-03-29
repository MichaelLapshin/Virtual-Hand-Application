import tkinter
import tkinter.ttk

from scripts import General, Parameters, Constants
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

"""
    Parent generic option menu
"""


class OptionMenu(tkinter.OptionMenu, WidgetInterface):

    def __init__(self, root, column, row, variable, values, columnspan=1, rowspan=1, padx=5, pady=5):
        tkinter.OptionMenu.__init__(self, root, variable, *values)
        self._variable = variable
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=padx, pady=pady)

    def get(self):
        return self._variable.get()


"""
    Custom buttons
"""


class SortOptionMenu(OptionMenu):

    def __init__(self, root, column, row, values, columnspan=1, rowspan=1, value=None):
        # Create the options
        self.values = values

        if value is None:
            value = self.values[0]

        # Create the variable
        self.variable = tkinter.StringVar()
        self.variable.set(value)

        # Checks if the default value is valid
        assert (value in self.values)

        # Configure
        OptionMenu.__init__(self, root,
                            column=column, row=row,
                            columnspan=columnspan, rowspan=rowspan,
                            padx=8, pady=5,
                            variable=self.variable,
                            values=tuple(self.values))

        self.anchor(tkinter.CENTER)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_C))


class PermissionsOptionMenu(OptionMenu):

    def __init__(self, root, column, row, columnspan=1, rowspan=1, value=Constants.PERMISSION_PUBLIC):
        # Create the options
        self.values = Constants.PERMISSION_LEVELS.keys()

        if value is None:
            value = self.values[0]

        # Create the variable
        self.variable = tkinter.StringVar()
        self.variable.set(value)

        # Checks if the default value is valid
        assert (value in self.values)

        # Configure
        OptionMenu.__init__(self, root,
                            column=column, row=row,
                            columnspan=columnspan, rowspan=rowspan,
                            padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING,
                            variable=self.variable,
                            values=tuple(self.values))

        self.anchor(tkinter.CENTER)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_A))


class VideoSourceOptionMenu(OptionMenu):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, value="Video Camera"):
        # Create the options
        self.values = ["Video Camera", "Leap Motion"]

        if value is None:
            value = self.values[0]

        # Create the variable
        self.variable = tkinter.StringVar()
        self.variable.set(value)

        # Checks if the default value is valid
        assert (value in self.values)

        # Configure
        OptionMenu.__init__(self, root,
                            column=column, row=row,
                            columnspan=columnspan, rowspan=rowspan,
                            padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING,
                            variable=self.variable,
                            values=tuple(self.values))

        self.anchor(tkinter.CENTER)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_A))
