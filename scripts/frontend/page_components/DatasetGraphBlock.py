import math
import tkinter
import PIL.Image, PIL.ImageTk

from scripts import General, Warnings, Parameters, Constants, Log
from scripts.frontend import ClientConnection
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface
from scripts.frontend.logic import ImageLoader
from scripts.frontend.page_components import InformationBlock
from scripts.logic import Worker

TITLE = "Dataset Graphs"
NUM_IMAGES = 4


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
            assert 0 <= button_index < NUM_IMAGES

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

    class ImageFrame(tkinter.Frame, WidgetInterface):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
            # Creates self frame
            tkinter.Frame.__init__(self, root, relief=tkinter.RIDGE, bd=1)
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.grid(sticky=sticky)

            # Weights
            for i in range(0, Constants.NUM_FINGERS):
                self.columnconfigure(i, weight=1)

            # Stores images
            self.stored_image_labels = self.create_label_list()

            # Scaling variables
            self.old_width = None
            self.old_height = None

        def update_colour(self):
            super().update_colour()
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

        def update_image_size(self):
            self.old_width = None
            self.old_height = None

        def create_label_list(self):
            labels = [[tkinter.Label(self) for a in range(0, Constants.NUM_FINGERS)] for b in range(0, NUM_IMAGES)]

            # Sets variables
            for r in labels:
                for l in r:
                    l.orig_image = None
                    l.image = None

            return labels

        def update_content(self):
            super().update_colour()

            # Image scaling
            if self.old_width != self.winfo_width() or self.old_height != self.winfo_height():
                self.old_width = self.winfo_width()
                self.old_height = self.winfo_height()

                # Finds an image dimensions to sample # TODO, this assumes that all images have identical resolution
                image_sample_width = None
                image_sample_height = None

                for row in self.stored_image_labels:
                    for label in row:
                        if label.winfo_ismapped() and label.orig_image is not None:
                            image_sample_width = label.orig_image.width()
                            image_sample_height = label.orig_image.height()
                            break

                if image_sample_width is not None and image_sample_height is not None:
                    # Counts number of visible rows
                    shown_rows = 0
                    for row in self.stored_image_labels:
                        if row[0].winfo_ismapped():
                            shown_rows += 1

                    # Calculates the scale
                    scale = General.resizing_scale(width=image_sample_width, height=image_sample_height,
                                                   space_width=self.winfo_width() / float(Constants.NUM_FINGERS),
                                                   space_height=self.winfo_height() / float(shown_rows))

                    # More complex scaling calculations to combat the 1/scale issues
                    subsampling_scale: int
                    if scale < 1:
                        subsampling_scale = \
                            math.ceil(image_sample_width / (float(self.winfo_width()) / float(Constants.NUM_FINGERS)))
                        if image_sample_height * shown_rows / subsampling_scale > self.winfo_height():
                            subsampling_scale = \
                                math.ceil(image_sample_height / (float(self.winfo_height()) / float(shown_rows)))

                    # Resizes all images
                    for row in self.stored_image_labels:
                        for label in row:
                            if label.winfo_ismapped():
                                # Scales the original image
                                if label.orig_image is not None:
                                    if scale >= 1:
                                        label.image = label.orig_image.zoom(int(scale))
                                    else:
                                        label.image = label.orig_image.subsample(subsampling_scale)

                                # Applies the image to the label
                                label.config(image=label.image)

        def change_image_layout(self, enabled_buttons):
            Log.debug("Updating the image layout with: " + str(enabled_buttons))

            # Recalculates the weight of the grid
            for i in range(0, NUM_IMAGES):
                if enabled_buttons[i] is True:
                    # Grids the image
                    self.rowconfigure(i, weight=1)
                    Log.trace("Gridded the row: " + str(i))
                    for image_indx in range(0, len(self.stored_image_labels[i])):
                        if self.stored_image_labels[i][image_indx] is not None:
                            self.stored_image_labels[i][image_indx].grid(column=image_indx, row=i)
                else:
                    # Un-grids the image
                    Log.trace("Un-gridded the row: " + str(i))
                    self.rowconfigure(i, weight=0)
                    for image_indx in range(0, len(self.stored_image_labels[i])):
                        if self.stored_image_labels[i][image_indx] is not None:
                            self.stored_image_labels[i][image_indx].grid_remove()

        def load_new_images(self, dataset_id, is_raw, update_image_visibility_command):
            # Fetches finger images
            for image_index in range(0, Constants.NUM_FINGERS):
                row_index = Constants.METRIC.index("Position")
                # photoImage_image = ClientConnection.fetch_dataset_finger_plot(
                #     dataset_id=dataset_id, finger=image_index, metric=row_index)

                # Saves the image
                # self.stored_image_labels[row_index][image_index].orig_image = \
                #     photoImage_image.zoom(Constants.IMAGE_SAMPLING_ZOOM)

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
                        # photoImage_image = ClientConnection.fetch_dataset_finger_plot(
                        #     dataset_id=dataset_id, finger=image_index, metric=row_index)

                        # Saves the image
                        # self.stored_image_labels[row_index][image_index].orig_image = \
                        #     photoImage_image.zoom(Constants.IMAGE_SAMPLING_ZOOM)
                        job = ImageLoader.JobDatasetFingers(
                            dataset_id=dataset_id,
                            finger_index=image_index,
                            metric_index=row_index,
                            dest_obj=self.stored_image_labels[row_index][image_index],
                            update_image_visibility_command=update_image_visibility_command)
                        Worker.worker.add_task(job=job)

            # Fetches sensor images
            for image_index in range(0, Constants.NUM_SENSORS):
                # photoImage_image = ClientConnection.fetch_dataset_sensor_plot(dataset_id=dataset_id, sensor=image_index)

                # Saves the image
                # self.stored_image_labels[3][image_index].orig_image = \
                #     photoImage_image.zoom(Constants.IMAGE_SAMPLING_ZOOM)

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
        tkinter.Frame.__init__(
            self, root, relief=tkinter.RIDGE, bd=1)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=sticky)

        # Configure weights
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Frame
        self.image_frame = Frame.ImageFrame(self, column=1, row=1)
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

    def clear_images(self):
        # Clears all images (destroys & re-instantiates)
        for r in range(0, len(self.image_frame.stored_image_labels)):
            for l in range(0, len(self.image_frame.stored_image_labels[r])):
                self.image_frame.stored_image_labels[r][l].destroy()

        self.image_frame.stored_image_labels = self.image_frame.create_label_list()
