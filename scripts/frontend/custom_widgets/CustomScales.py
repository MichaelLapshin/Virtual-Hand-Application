import tkinter

from scripts import General
from scripts.frontend import Constants

"""
    Parent generic scales
"""


class Scale(tkinter.Scale):

    def __init__(self, root, column, row, from_, to, resolution, variable, columnspan=1, rowspan=1, label=None):
        tkinter.Scale.__init__(self, root,
                               label=label, variable=variable,
                               from_=from_, to=to, resolution=resolution)

        # Grid configurations
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(sticky=tkinter.NSEW)

        # Config
        self.anchor(tkinter.CENTER)
        self.config(bd=1, relief=tkinter.RIDGE)


"""
    Custom label
"""


class SettingsScale(Scale):
    def __init__(self, root, column, row, from_, to, resolution, variable, columnspan=1, rowspan=1, label=None):
        Scale.__init__(self, root,
                       column=column, row=row,
                       from_=from_, to=to,
                       resolution=resolution, variable=variable,
                       columnspan=columnspan, rowspan=rowspan,
                       label=label)

        self.config(activebackground=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_B))
        # self.config(digits=tkinter.DoubleVar)
        self.config(orient=tkinter.HORIZONTAL)
