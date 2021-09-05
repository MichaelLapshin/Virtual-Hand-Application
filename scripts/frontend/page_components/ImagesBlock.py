import math
import tkinter

from scripts import Constants, Parameters, General, Log, Warnings
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

"""
    Image box
"""


class ImagesFrame(tkinter.Frame, WidgetInterface):

    def __init__(self, root, image_columns, image_rows, column=0, row=0, columnspan=1, rowspan=1, sticky=tkinter.NSEW):
        # Creates self frame
        tkinter.Frame.__init__(self, root, relief=tkinter.RIDGE, bd=1)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=sticky)

        # Image storage dimensions
        self.image_columns = image_columns
        self.image_rows = image_rows

        # Weights
        for i in range(0, self.image_columns):
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
        labels = [[tkinter.Label(self) for a in range(0, self.image_columns)] for b in range(0, self.image_rows)]

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

    def change_image_layout(self, enabled_rows):
        assert type(enabled_rows) == list
        Log.debug("Updating the image layout with: " + str(enabled_rows))

        # Recalculates the weight of the grid
        for i in range(0, self.image_rows):
            if enabled_rows[i] is True:
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

    def load_new_images(self):
        Warnings.not_overridden()

    def clear_images(self):
        # Clears all images (destroys & re-instantiates)
        for r in range(0, len(self.stored_image_labels)):
            for l in range(0, len(self.stored_image_labels[r])):
                self.stored_image_labels[r][l].destroy()

        self.stored_image_labels = self.create_label_list()
