import tkinter

from scripts import General
from scripts.frontend import Constants
from scripts.frontend.custom_widgets import CustomButtons, CustomEntries
from scripts.frontend.page_components import InformationBlock

TITLE = "Sensor Readings Buffer"


class Frame(tkinter.Frame):
    """
        Button box
    """

    class ButtonFrame(tkinter.Frame):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NS):
            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1,
                bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour40))
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.grid(sticky=sticky)

            # Title Label
            self.title_label = InformationBlock.Frame(self, title=TITLE,
                                                      frame_colour=Constants.BASE_GREEN_COLOUR,
                                                      label_colour=Constants.BASE_GREEN_COLOUR,
                                                      num_columns=1, num_rows=1,
                                                      column=0, row=0)
            self.title_label.add_info(column=0, row=0, text="Enter new buffer size:")

            # Enter button field

            self.set_buffer_entry = CustomEntries.PlotEntry(
                self, column=0, row=1,
            )

            # Set buffer button
            self.set_buffer_button = CustomButtons.PlotButton(
                self, column=0, row=2,
                text="Set Buffer Size", command=lambda: self.printHi("New Buffer"))

        def printHi(self, text):
            print(text)

    """
        Image box
    """

    class ImageFrame(tkinter.Frame):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1,
                bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour40))
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
            bg=General.washed_colour_hex(Constants.BASE_BLUE_COLOUR, Constants.Colour20))
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=sticky)

        # Configure weights
        self.columnconfigure(1, weight=1)

        # Frame
        self.button_frame = Frame.ButtonFrame(self, column=0, row=0)
        self.image_frame = Frame.ImageFrame(self, column=1, row=0)
