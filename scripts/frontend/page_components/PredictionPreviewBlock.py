import tkinter

from scripts import General
from scripts.frontend import Constants
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.custom_widgets.CustomLabels import InformationLabel


class Frame(tkinter.Frame):
    title = "Prediction Preview"

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

            # Distal Phalanges button
            self.distal_button = CustomButtons.PlotButton(
                self, column=0, row=0,
                text="Distal Phalanges", command=lambda: self.printHi("A"))
            # Middle Phalanges button
            self.middle_button = CustomButtons.PlotButton(
                self, column=0, row=1,
                text="Middle Phalanges", command=lambda: self.printHi("B"))
            # Proximal Phalanges button
            self.proximal_button = CustomButtons.PlotButton(
                self, column=0, row=2,
                text="Proximal Phalanges", command=lambda: self.printHi("C"))

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



