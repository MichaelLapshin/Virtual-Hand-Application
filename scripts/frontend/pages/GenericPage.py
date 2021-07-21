import tkinter

from scripts import General
from scripts.frontend import Constants
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface


class Frame(tkinter.Frame, WidgetInterface):

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
        self.config(bd=1, relief=tkinter.RIDGE)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

    def update_content(self):
        pass

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_B))


class NavigationFrame(Frame):

    def __init__(self, root, page_title, column=0, row=0, columnspan=1, rowspan=1, base_frame=None):
        Frame.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       base_frame=base_frame)

        self.page_title = page_title

    def get_page_title(self):
        return self.page_title
