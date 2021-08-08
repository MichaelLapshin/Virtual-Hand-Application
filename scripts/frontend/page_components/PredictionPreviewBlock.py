import tkinter

from scripts import General, Parameters, Constants
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface
from scripts.frontend.page_components import InformationBlock

TITLE = "Prediction Preview"


class Frame(tkinter.Frame, WidgetInterface):
    """
        Button box
    """

    class ButtonFrame(tkinter.Frame, WidgetInterface):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NS):
            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1)
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.grid(sticky=sticky)

            # Title Label
            self.title_label = InformationBlock.Frame(self, title=TITLE,
                                                      num_columns=1, num_rows=1,
                                                      column=0, row=0)
            self.title_label.add_info(column=0, row=0, text="Units: Degrees Angular Velocity")

            # Distal Phalanges button
            self.distal_button = CustomButtons.PlotButton(
                self, column=0, row=1,
                text="Distal Phalanges", command=lambda: self.printHi("A"))
            # Middle Phalanges button
            self.middle_button = CustomButtons.PlotButton(
                self, column=0, row=2,
                text="Middle Phalanges", command=lambda: self.printHi("B"))
            # Proximal Phalanges button
            self.proximal_button = CustomButtons.PlotButton(
                self, column=0, row=3,
                text="Proximal Phalanges", command=lambda: self.printHi("C"))

        def update_colour(self):
            super().update_colour()

            self.distal_button.update_colour()
            self.middle_button.update_colour()
            self.proximal_button.update_colour()

            self.title_label.set_label_colour(Parameters.COLOUR_BRAVO)
            self.title_label.set_frame_colour(Parameters.COLOUR_BRAVO)
            self.title_label.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

        def printHi(self, text):
            print(text)

    """
        Image box
    """

    class ImageFrame(tkinter.Frame, WidgetInterface):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1)
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.grid(sticky=sticky)

        def update_colour(self):
            super().update_colour()
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

    """
        Self methods
    """

    def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.EW):
        # Creates self frame
        tkinter.Frame.__init__(
            self, root, relief=tkinter.RIDGE, bd=1)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=sticky)

        # Configure weights
        self.columnconfigure(1, weight=1)

        # Frame
        self.button_frame = Frame.ButtonFrame(self, column=0, row=0)
        self.image_frame = Frame.ImageFrame(self, column=1, row=0)

    def update_colour(self):
        super().update_colour()
        self.button_frame.update_colour()
        self.image_frame.update_colour()

        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
