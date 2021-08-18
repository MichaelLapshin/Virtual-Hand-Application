import tkinter
import tkinter.font

from scripts import Warnings, Constants
from scripts.frontend.custom_widgets import CustomEntries, CustomLabels, CustomOptionMenu
from scripts.frontend.custom_widgets.CustomLabels import InformationLabel
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

TITLE_FONT_SIZE = 8


class Frame(tkinter.Frame, WidgetInterface):
    VAR_PADDING = " :"

    def __init__(self, root, column, row, options,
                 title=None, columnspan=1, rowspan=1):

        # Creates self frame
        tkinter.Frame.__init__(self, root, relief=tkinter.RIDGE, bd=1)

        # Initializes the options
        self.options = options
        self.entries = {}
        for o in range(0, len(self.options)):
            self.entries[CustomLabels.InfoEntryLabel(self, column=0, row=o + 1,
                                                     text=self.options[o] + Frame.VAR_PADDING)] = \
                CustomEntries.InfoEntryEntry(self, column=1, row=o + 1)
            self.rowconfigure(o + 1, weight=1)

        # Saves the colour
        self.frame_colour = None
        self.label_colour = None

        self.grid(column=column, row=row,
                  columnspan=columnspan, rowspan=rowspan,
                  padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING,
                  sticky=tkinter.NSEW)

        # Configure weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Creates title bar
        self.titlebar = None
        if title is not None:
            self.titlebar = InformationLabel(self, text=title, column=0, row=0, columnspan=2)
            self.titlebar.config(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.titlebar.config(font=TITLE_FONT_SIZE)
            self.titlebar.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

    def update_content(self):
        super().update_content()

        if self.titlebar is not None:
            self.titlebar.update_content()

        for k in self.entries.keys():
            k.update_content()
            self.entries.get(k).update_content()

    def update_colour(self):
        super().update_colour()

        if self.titlebar is not None:
            self.titlebar.update_colour()
            self.titlebar.config(bg=self.label_colour)

        for k in self.entries.keys():
            k.update_colour()
            self.entries.get(k).update_colour()

        self.config(bg=self.frame_colour)
        # self.info_frame.config(bg=General.washed_colour_hex(self.frame_colour, Parameters.ColourGrad_B))


    def set_frame_colour(self, colour):
        self.frame_colour = colour

    def set_label_colour(self, colour):
        self.label_colour = colour

    def set_entry_value(self, name, value):
        for k in self.entries.keys():
            if name + Frame.VAR_PADDING == k.cget("text"):
                self.entries.get(k).set_entry(value)

    def disable_entry(self, name):
        for k in self.entries.keys():
            if name + Frame.VAR_PADDING == k.cget("text"):
                self.entries.get(k).disable()

    def enable_entry(self, name):
        for k in self.entries.keys():
            if name + Frame.VAR_PADDING == k.cget("text"):
                self.entries.get(k).enable()

    def set_perm_option_menu(self, name):
        for k in self.entries.keys():
            if name + Frame.VAR_PADDING == k.cget("text"):
                self.entries.get(k).destroy()
                self.entries[k] = CustomOptionMenu.PermissionsOptionMenu(self, column=1, row=k.grid_info()["row"])

    def set_video_source_option_menu(self, name):
        for k in self.entries.keys():
            if name + Frame.VAR_PADDING == k.cget("text"):
                self.entries.get(k).destroy()
                self.entries[k] = CustomOptionMenu.VideoSourceOptionMenu(self, column=1, row=k.grid_info()["row"])

    def exists_entry(self, entry_name):
        return entry_name in self.options

    def get_entries(self):
        return self.options

    def get_value(self, name):
        for k in self.entries.keys():
            if name + Frame.VAR_PADDING == k.cget("text"):
                return self.entries[k].get()
        Warnings.not_to_reach()
        return None
