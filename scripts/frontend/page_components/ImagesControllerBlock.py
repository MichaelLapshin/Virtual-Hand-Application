import tkinter

from scripts import Constants, Parameters, General, Log
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface


class ButtonsFrame(tkinter.Frame, WidgetInterface):
    def __init__(self, root, button_labels: list, vertical_button: bool,
                 button_display_command, update_image_size_command,
                 column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW, button_grid_offset=0):

        # Creates self frame
        tkinter.Frame.__init__(self, root, relief=tkinter.RIDGE, bd=1)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=sticky)

        self.update_image_size_command = update_image_size_command

        # Creates buttons
        self.buttons = []
        for i in range(0, len(button_labels)):
            self.buttons.append(CustomButtons.PlotButton(self, column=0, row=0, text=button_labels[i],
                                                         command=lambda btn_indx=i: self.toggle_image_state(btn_indx)))

        # Updates button layout
        if vertical_button is True:
            for i in range(0, len(self.buttons)):
                self.buttons[i].grid(column=0, row=button_grid_offset + i)
                self.rowconfigure(button_grid_offset + i, weight=1)
        else:
            for i in range(0, len(self.buttons)):
                self.buttons[i].grid(column=button_grid_offset + i, row=0)
                self.buttons[i].grid(sticky=tkinter.EW)
                self.columnconfigure(button_grid_offset + i, weight=1)

        # Toggle states
        self.enabled_state = [None] * len(self.buttons)
        self.button_display_command = button_display_command

        # Default button states
        for i in range(0, len(self.buttons)):
            self.set_image_state(i, True)

        # Spacing around buttons
        for b in self.buttons:
            b.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

    def update_content(self):
        super().update_content()
        for b in self.buttons:
            b.update_content()

    def enable_all_buttons(self, enable=True):
        if enable is True:
            for b in self.buttons:
                b.enable()
        else:
            for b in self.buttons:
                b.disable()

    def set_image_state(self, button_index, state):
        self.enabled_state[button_index] = state
        if state is True:
            self.buttons[button_index].config(
                bg=General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_D))
        else:
            self.buttons[button_index].config(
                bg=General.washed_colour_hex(Constants.COLOUR_GREY, Parameters.ColourGrad_D))

    def toggle_image_state(self, button_index):
        assert 0 <= button_index < len(self.buttons)

        # Toggles button
        if self.enabled_state[button_index] is True:
            self.set_image_state(button_index, False)
        else:
            self.set_image_state(button_index, True)

        Log.debug("Toggling the state of button " + str(button_index) + " to " + str(self.enabled_state[button_index]))

        self.update_image_state()

    def update_image_state(self):
        self.button_display_command(self.enabled_state)
        self.update_image_size_command()
