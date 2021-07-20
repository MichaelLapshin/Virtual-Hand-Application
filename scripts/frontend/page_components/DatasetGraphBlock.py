import tkinter

from scripts import General
from scripts.frontend import Constants
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.page_components import InformationBlock
from scripts.frontend.pages import GenericPage

TITLE = "Dataset Graphs"


class Frame(tkinter.Frame):
    """
        Limb box
    """

    class ButtonFrame(tkinter.Frame):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NS):
            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1,
                bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_C))
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.grid(sticky=sticky)

            # Title Label
            self.title_label = InformationBlock.Frame(self, title=TITLE,
                                                      frame_colour=Constants.COLOUR_BRAVO,
                                                      label_colour=Constants.COLOUR_BRAVO,
                                                      num_columns=1, num_rows=1,
                                                      column=0, row=0)
            self.title_label.add_info(column=0, row=0, text="Units: Degrees")

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

        def printHi(self, text):
            print(text)

    """
        Metric button box
    """

    class MetricButtonFrame(tkinter.Frame):
        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.EW):
            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1,
                bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_C))
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.grid(sticky=sticky)

            # Configure weights
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.columnconfigure(2, weight=1)
            self.columnconfigure(3, weight=1)

            # Angular Position button
            self.distal_button = CustomButtons.InformationButton(
                self, column=0, row=0,
                text="Angular Position", command=None)
            # Angular Velocity button
            self.middle_button = CustomButtons.InformationButton(
                self, column=1, row=0,
                text="Angular Velocity", command=None)
            # Angular Acceleration button
            self.proximal_button = CustomButtons.InformationButton(
                self, column=2, row=0,
                text="Angular Acceleration", command=None)
            # Loss button
            self.proximal_button = CustomButtons.InformationButton(
                self, column=3, row=0,
                text="Loss", command=None)

            # Increase the padding
            self.distal_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.middle_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.proximal_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

    """
        Image box
    """

    class ImageFrame(tkinter.Frame):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1,
                bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_C))
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.grid(sticky=sticky)

    """
        Self methods
    """

    def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.EW):
        # Creates self frame
        tkinter.Frame.__init__(
            self, root, relief=tkinter.RIDGE, bd=1,
            bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_B))
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=sticky)

        # Configure weights
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Frame
        self.button_frame = Frame.ButtonFrame(self, column=0, row=0, rowspan=2)
        self.image_frame = Frame.ImageFrame(self, column=1, row=1)
        self.metric_button_frame = Frame.MetricButtonFrame(self, column=1, row=0)
