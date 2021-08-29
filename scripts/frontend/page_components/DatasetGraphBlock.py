import tkinter

from scripts import General, Warnings, Parameters, Constants, Log
from scripts.frontend import ClientConnection
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface
from scripts.frontend.page_components import InformationBlock

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
        def __init__(self, root, button_display_command, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.EW):
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
            self.distal_button = CustomButtons.InformationButton(
                self, column=0, row=0,
                text="Angular Position", command=lambda: self.toggle_image_state(0))
            # Angular Velocity button
            self.middle_button = CustomButtons.InformationButton(
                self, column=1, row=0,
                text="Angular Velocity", command=lambda: self.toggle_image_state(1))
            # Angular Acceleration button
            self.proximal_button = CustomButtons.InformationButton(
                self, column=2, row=0,
                text="Angular Acceleration", command=lambda: self.toggle_image_state(2))
            # Loss button
            self.sensors_button = CustomButtons.InformationButton(
                self, column=3, row=0,
                text="Sensor Readings", command=lambda: self.toggle_image_state(3))

            # Toggle states
            self.enabled_state = [True] + [False] * (NUM_IMAGES - 2) + [True]
            print(self.enabled_state)
            self.button_display_command = button_display_command

            # Increase the padding
            self.distal_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.middle_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.proximal_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.sensors_button.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

        def update_colour(self):
            super().update_colour()
            self.distal_button.update_colour()
            self.middle_button.update_colour()
            self.proximal_button.update_colour()
            self.sensors_button.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

        def toggle_image_state(self, button_index):
            assert 0 <= button_index < NUM_IMAGES

            # Toggles button
            if self.enabled_state[button_index] is True:
                self.enabled_state[button_index] = False
            else:
                self.enabled_state[button_index] = True

            Log.debug(
                "Toggling the state of button " + str(button_index) + " to " + str(self.enabled_state[button_index]))

            self.update_image_state()

        def update_image_state(self):
            self.button_display_command(self.enabled_state)

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
            self.stored_images = [[None for a in range(0, Constants.NUM_FINGERS)]
                                  for b in range(0, NUM_IMAGES)]
            self.stored_image_labels = [[tkinter.Label(self) for a in range(0, Constants.NUM_FINGERS)]
                                        for b in range(0, NUM_IMAGES)]

        def update_colour(self):
            super().update_colour()
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

        def update_content(self):
            super().update_colour()

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


        def load_new_images(self, dataset_id, is_raw):
            Warnings.not_complete()

            # Fetches finger images
            for image_index in range(0, Constants.NUM_FINGERS):
                row_index = Constants.METRIC.index("Position")
                photoImage_image = ClientConnection.fetch_dataset_finger_plot(
                    dataset_id=dataset_id, finger=image_index, metric=row_index)

                # self.stored_images[row_index][image_index] = photoImage_image
                self.stored_image_labels[row_index][image_index].image = photoImage_image
                self.stored_image_labels[row_index][image_index].config(
                    image=self.stored_image_labels[row_index][image_index].image)

                # self.stored_image_labels[row_index][image_index].config(image=photoImage_image)

                # self.stored_images[row_index][image_index] = \
                #     self.stored_image_labels[row_index][image_index].cget("image")
                # self.stored_image_labels[row_index][image_index]["image"] = \
                #     self.stored_images[row_index][image_index]

            Log.trace("is_raw is: " + str(is_raw))
            if is_raw == 0:
                for row_index in range(0, len(Constants.METRIC)):
                    for image_index in range(0, Constants.NUM_FINGERS):
                        photoImage_image = ClientConnection.fetch_dataset_finger_plot(
                            dataset_id=dataset_id, finger=image_index, metric=row_index)

                        # self.stored_images[row_index][image_index] = photoImage_image
                        self.stored_image_labels[row_index][image_index].image = photoImage_image
                        self.stored_image_labels[row_index][image_index].config(
                            image=self.stored_image_labels[row_index][image_index].image)

                        # self.stored_image_labels[row_index][image_index].config(image=photoImage_image)

                        # self.stored_images[row_index][image_index] = \
                        #     self.stored_image_labels[row_index][image_index].cget("image")
                        # self.stored_image_labels[row_index][image_index]["image"] = \
                        #     self.stored_images[row_index][image_index]
                        # self.new = tkinter.Label(self, image=photoImage_image)
                        # self.new.grid(column=0, row=0)

            # Fetches sensor images
            for image_index in range(0, Constants.NUM_SENSORS):
                photoImage_image = ClientConnection.fetch_dataset_sensor_plot(dataset_id=dataset_id,
                                                                              sensor=image_index)
                # self.stored_image_labels[3][image_index].config(image=photoImage_image)
                # self.stored_images[3][image_index] = self.stored_image_labels[3][image_index].cget("image")
                # print(self.stored_images[3][image_index])
                # self.stored_image_labels[3][image_index].image = photoImage_image

                self.stored_image_labels[3][image_index].image = photoImage_image
                self.stored_image_labels[3][image_index].config(
                    image=self.stored_image_labels[3][image_index].image)

                # self.stored_image_labels[3][image_index].config(image=photoImage_image)

                # self.stored_image_labels[3][image_index]["image"] = self.stored_images[3][image_index]

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
        self.rowconfigure(1, weight=1)

        # Frame
        self.image_frame = Frame.ImageFrame(self, column=1, row=1)
        # self.button_frame = Frame.ButtonFrame(self, column=0, row=0, rowspan=2)
        self.metric_button_frame = Frame.MetricButtonFrame(self,
                                                           button_display_command=self.image_frame.change_image_layout,
                                                           column=1, row=0)

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
