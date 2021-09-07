import tkinter

from scripts import General, Parameters, Constants
from scripts.frontend.custom_widgets import CustomButtons, CustomCanvas
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface


class Frame(tkinter.Frame, WidgetInterface):
    _progress = "Progress: "
    _percentage = "%"

    def __init__(self, root, column, row, metric_text, max_count=-1, is_default_percentage=False, columnspan=1,
                 rowspan=1):
        tkinter.Frame.__init__(self, root)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

        # Weights
        self.columnconfigure(0, weight=1)

        # Display related
        self.metric_text = metric_text
        self.is_percentage = is_default_percentage

        # Objects
        self.progress_bar = CustomCanvas.Canvas(self, column=0, row=0)
        self.progress_bar.config(height=Constants.LONG_SPACING)
        self.progress_bar.grid(sticky=tkinter.NSEW)

        self.metric_switch_button = CustomButtons.InformationButton(self, column=0, row=0, command=self.switch_metric)
        self.metric_switch_button.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)
        self.metric_switch_button.grid(padx=Constants.STANDARD_SPACING * 2, pady=Constants.STANDARD_SPACING * 2)
        # self.metric_switch_button.grid(sticky=tkinter.NSEW)

        # Count-related
        self.max_count = max_count
        self.count = -1
        self.old_count = -2
        self.reset()

        # Colour (None makes it mandatory to set)
        self.background_colour = None
        self.progress_colour = None

    def set_metric_text(self, text):
        self.metric_text = text

    def set_max_count(self, new_max_count):
        self.max_count = new_max_count

    def set_count(self, new_count):
        self.count = new_count

    def reset(self):
        self.count = -1
        self.old_count = -2

    def switch_metric(self):
        self.is_percentage = not self.is_percentage

    def update_content(self):
        super().update_content()

        # Progress bar
        if self.old_count != self.count:
            self.progress_bar.delete(tkinter.ALL)
            self.progress_bar.create_rectangle(0, 0,
                                               self.progress_bar.winfo_width() * (float(self.count) / self.max_count),
                                               self.progress_bar.winfo_height(),
                                               fill=self.progress_colour)
            self.old_count = self.count

        # Percentage vs numerical
        if self.is_percentage:
            self.metric_switch_button.config(
                text=Frame._progress + str(round(float(self.count * 100) / self.max_count)) + Frame._percentage)
        else:
            self.metric_switch_button.config(
                text=Frame._progress + str(int(self.count)) + "/" + str(int(self.max_count)) + self.metric_text)

    def update_colour(self):
        super().update_colour()

        # Metric
        self.metric_switch_button.update_colour()
        self.metric_switch_button.config(
            bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))

        # Update self
        self.progress_bar.update_colour()
        self.progress_bar.config(bg=self.background_colour)

    def set_background_colour(self, colour):
        self.background_colour = colour

    def set_progress_colour(self, colour):
        self.progress_colour = colour

    def clear(self):
        self.reset()
        self.set_max_count(-1)
        self.set_metric_text("")
