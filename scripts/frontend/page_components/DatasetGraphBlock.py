import math
import tkinter
import PIL.Image, PIL.ImageTk

from scripts import General, Warnings, Parameters, Constants, Log
from scripts.frontend import ClientConnection
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface
from scripts.frontend.logic import ImageLoader
from scripts.frontend.page_components import InformationBlock, ImagesBlock
from scripts.logic import Worker

TITLE = "Dataset Graphs"
NUM_ROWS = 4


class Frame(tkinter.Frame, WidgetInterface):
    """
        Limb box
    """

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

    """
        Metric button box
    """

    class MetricButtonFrame(tkinter.Frame, WidgetInterface):
        def __init__(self, root, button_display_command, update_image_size_command,
                     column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.EW):

            self.update_image_size_command = update_image_size_command

            # Creates self frame
            tkinter.Frame.__init__(
                self, root, relief=tkinter.RIDGE, bd=1)
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
            self.position_toggle_button = CustomButtons.InformationButton(
                self, column=0, row=0,
                text="Angular Position", command=lambda: self.toggle_image_state(0))
            # Angular Velocity button
            self.velocity_toggle_button = CustomButtons.InformationButton(
                self, column=1, row=0,
                text="Angular Velocity", command=lambda: self.toggle_image_state(1))
            # Angular Acceleration button
            self.acceleration_toggle_button = CustomButtons.InformationButton(
                self, column=2, row=0,
                text="Angular Acceleration", command=lambda: self.toggle_image_state(2))
            # Loss button
            self.sensors_toggle_button = CustomButtons.InformationButton(
                self, column=3, row=0,
                text="Sensor Readings", command=lambda: self.toggle_image_state(3))

            # Toggle states
            self.enabled_state = [None] * 4
            self.enabled_buttons = [self.position_toggle_button, self.velocity_toggle_button,
                                    self.acceleration_toggle_button, self.sensors_toggle_button]
            self.button_display_command = button_display_command

            # Default button states
            self.set_image_state(0, True)
            self.set_image_state(1, False)
            self.set_image_state(2, False)
            self.set_image_state(3, True)

            # Increase the padding
            self.position_toggle_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.velocity_toggle_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.acceleration_toggle_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.sensors_toggle_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

        def update_colour(self):
            super().update_colour()
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

        def enable_all_buttons(self, enable=True):
            self.enable_vel_acc_buttons(enable=enable)
            if enable is True:
                self.position_toggle_button.enable()
                self.sensors_toggle_button.enable()
            else:
                self.position_toggle_button.disable()
                self.sensors_toggle_button.disable()

        def enable_vel_acc_buttons(self, enable=True):
            if enable is True:
                self.velocity_toggle_button.enable()
                self.acceleration_toggle_button.enable()
            else:
                self.velocity_toggle_button.disable()
                self.acceleration_toggle_button.disable()

        def set_image_state(self, button_index, state):
            self.enabled_state[button_index] = state
            if state is True:
                self.enabled_buttons[button_index].config(
                    bg=General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_D))
            else:
                self.enabled_buttons[button_index].config(
                    bg=General.washed_colour_hex(Constants.COLOUR_GREY, Parameters.ColourGrad_D))

        def toggle_image_state(self, button_index):
            assert 0 <= button_index < NUM_ROWS

            # Toggles button
            if self.enabled_state[button_index] is True:
                self.set_image_state(button_index, False)
            else:
                self.set_image_state(button_index, True)

            Log.debug(
                "Toggling the state of button " + str(button_index) + " to " + str(self.enabled_state[button_index]))

            self.update_image_state()

        def update_image_state(self):
            self.button_display_command(self.enabled_state)
            self.update_image_size_command()

    """
        Image box
    """

    class DatasetImageFrame(ImagesBlock.ImagesFrame):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
            # Creates self frame
            ImagesBlock.ImagesFrame.__init__(self, root, image_columns=Constants.NUM_FINGERS, image_rows=NUM_ROWS,
                                             column=column, row=row, columnspan=columnspan, rowspan=rowspan,
                                             sticky=sticky)

        def load_new_images(self, dataset_id, is_raw, update_image_visibility_command):
            # Fetches finger images
            for image_index in range(0, Constants.NUM_FINGERS):
                row_index = Constants.METRIC.index("Position")

                job = ImageLoader.JobDatasetFingers(
                    dataset_id=dataset_id,
                    finger_index=image_index,
                    metric_index=row_index,
                    dest_obj=self.stored_image_labels[row_index][image_index],
                    update_image_visibility_command=update_image_visibility_command)
                Worker.worker.add_task(job=job)

            Log.trace("is_raw is: " + str(is_raw))
            if is_raw == 0:
                for row_index in range(0, len(Constants.METRIC)):
                    for image_index in range(0, Constants.NUM_FINGERS):
                        job = ImageLoader.JobDatasetFingers(
                            dataset_id=dataset_id,
                            finger_index=image_index,
                            metric_index=row_index,
                            dest_obj=self.stored_image_labels[row_index][image_index],
                            update_image_visibility_command=update_image_visibility_command)
                        Worker.worker.add_task(job=job)

            # Fetches sensor images
            for image_index in range(0, Constants.NUM_SENSORS):
                job = ImageLoader.JobDatasetSensors(
                    dataset_id=dataset_id,
                    sensor_index=image_index,
                    dest_obj=self.stored_image_labels[3][image_index],
                    update_image_visibility_command=update_image_visibility_command)
                Worker.worker.add_task(job=job)

    """
        Self methods
    """

    def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
        # Creates self frame
        tkinter.Frame.__init__(self, root, relief=tkinter.RIDGE, bd=1)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=sticky)

        # Configure weights
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Frame
        self.image_frame = Frame.DatasetImageFrame(self, column=1, row=1)
        # self.button_frame = Frame.ButtonFrame(self, column=0, row=0, rowspan=2)
        self.metric_button_frame = Frame.MetricButtonFrame(self,
                                                           button_display_command=self.image_frame.change_image_layout,
                                                           column=1, row=0,
                                                           update_image_size_command=self.image_frame.update_image_size)

    def update_colour(self):
        super().update_colour()
        # self.button_frame.update_colour()
        self.image_frame.update_colour()
        self.metric_button_frame.update_colour()

        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))

    def update_content(self):
        super().update_content()
        # self.button_frame.update_colour()
        self.image_frame.update_content()
        self.metric_button_frame.update_content()
