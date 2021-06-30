import tkinter

from scripts import General
from scripts.frontend import Constants


class BaseFrame(tkinter.Frame):

    def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, base_frame=None):
        tkinter.Frame.__init__(self, root)

        if base_frame is not None:
            # Uses base_face dimensions
            self.grid(column=base_frame.grid_info()["column"], row=base_frame.grid_info()["row"],
                      columnspan=base_frame.grid_info()["columnspan"], rowspan=base_frame.grid_info()["rowspan"])
        else:
            # Uses input (or default) dimensions
            self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

        # Default page configurations
        self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour20))
        self.config(bd=1, relief=tkinter.RIDGE)
        self.grid(sticky='WE', padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
