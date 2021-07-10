import tkinter

from scripts import General
from scripts.frontend import Constants

"""
    Parent generic option menu
"""


class OptionMenu(tkinter.OptionMenu):

    def __init__(self, root, column, row, variable, values, columnspan=1, rowspan=1, padx=5, pady=5):
        tkinter.OptionMenu.__init__(self, root, variable, *values)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=padx, pady=pady)


"""
    Custom buttons
"""


class SortOptionMenu(OptionMenu):

    def __init__(self, root, column, row, columnspan=1, rowspan=1, value=None):
        # Create the options
        self.values = ["Name", "Identification Number", "Number of Training Frames",
                       "Average Loss", "Personal Rating",
                       "Newest", "Oldest",
                       "Batch Size", "Number of Epoch",
                       "Number of Layers", "Number of Nodes per Layer"]

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
                            values=self.values)

        self.anchor(tkinter.CENTER)
        self.config(bg=General.washed_colour_hex(Constants.BASE_BLUE_COLOUR, Constants.Colour40))
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

    def get_value(self):
        return self.variable.get()