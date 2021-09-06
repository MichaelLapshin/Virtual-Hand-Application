import tkinter

from scripts import General, Parameters, Constants, Warnings
from scripts.frontend.custom_widgets import CustomButtons
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface
from scripts.frontend.logic import ImageLoader
from scripts.frontend.page_components import InformationBlock, ImagesBlock, ImagesControllerBlock
from scripts.logic import Worker

TITLE = "Prediction Preview"


class Frame(tkinter.Frame, WidgetInterface):
    """
        Button box
    """

    class ButtonFrame(ImagesControllerBlock.ButtonsFrame, WidgetInterface):

        def __init__(self, root, button_display_command, update_image_size_command,
                     column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NS):
            # Creates self frame
            ImagesControllerBlock.ButtonsFrame.__init__(
                self, root,
                button_labels=["Distal Phalanges Predictions", "Middle Phalanges Predictions",
                               "Proximal Phalanges Predictions", "Distal Phalanges Errors",
                               "Middle Phalanges Errors", "Proximal Phalanges Errors"], vertical_button=True,
                button_display_command=button_display_command, update_image_size_command=update_image_size_command,
                column=column, row=row, columnspan=columnspan, rowspan=rowspan, sticky=sticky, button_grid_offset=1)

            # Title Label
            self.title_label = InformationBlock.Frame(self, title=TITLE, num_columns=1, num_rows=1, column=0, row=0)
            self.title_label.add_info(column=0, row=0, text="Prediction Units: Degrees Angular Velocity")

            # Default states
            self.set_image_state(0, True)
            self.set_image_state(1, True)
            self.set_image_state(2, True)
            self.set_image_state(3, False)
            self.set_image_state(4, False)
            self.set_image_state(5, False)

        def update_colour(self):
            super().update_colour()
            # Note: the button are update in the parent class
            self.title_label.set_label_colour(Parameters.COLOUR_BRAVO)
            self.title_label.set_frame_colour(Parameters.COLOUR_BRAVO)
            self.title_label.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))

        def update_content(self):
            super().update_content()
            # Note: the button are update in the parent class
            self.title_label.update_content()

    """
        Image box
    """

    class ModelImageFrame(ImagesBlock.ImagesFrame):

        def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
            # Creates self frame
            ImagesBlock.ImagesFrame.__init__(self, root, image_columns=Constants.NUM_FINGERS,
                                             image_rows=Constants.NUM_LIMBS_PER_FINGER * 2,
                                             column=column, row=row, columnspan=columnspan, rowspan=rowspan,
                                             sticky=sticky)

        def load_new_images(self, model_id):
            # Fetches the prediction plots
            for row_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                for image_index in range(0, self.image_columns):
                    job = ImageLoader.JobModelPredictions(
                        model_id=model_id,
                        finger_index=image_index,
                        limb_index=row_index,
                        dest_obj=self.stored_image_labels[row_index][image_index],
                        update_image_visibility_command=self.update_image_size)
                    Worker.worker.add_task(job=job)

            # Fetches the error plots
            for row_index in range(0, Constants.NUM_LIMBS_PER_FINGER):
                for image_index in range(0, self.image_columns):
                    job = ImageLoader.JobModelErrors(
                        model_id=model_id,
                        finger_index=image_index,
                        limb_index=row_index,
                        dest_obj=self.stored_image_labels[row_index + Constants.NUM_LIMBS_PER_FINGER][image_index],
                        update_image_visibility_command=self.update_image_size)
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
        self.rowconfigure(0, weight=1)

        # Frame
        self.image_frame = Frame.ModelImageFrame(self, column=1, row=0)
        self.button_frame = Frame.ButtonFrame(self, column=0, row=0,
                                              button_display_command=self.image_frame.change_image_layout,
                                              update_image_size_command=self.image_frame.update_image_size)

    def update_colour(self):
        super().update_colour()
        self.button_frame.update_colour()
        self.image_frame.update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))

    def update_content(self):
        super().update_content()
        self.button_frame.update_colour()
        self.image_frame.update_content()
