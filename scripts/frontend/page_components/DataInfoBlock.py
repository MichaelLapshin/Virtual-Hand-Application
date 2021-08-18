import tkinter.messagebox

from scripts import Constants, Warnings, Log, Parameters, General
from scripts.frontend import ClientConnection
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.page_components import InformationBlock, InfoInputBlock
from scripts.frontend.pages import GenericPage


class Frame(GenericPage.Frame):

    def __init__(self, root, column, row, title,
                 general_options_data, right_options_data,
                 GENERAL_BANK, RIGHT_BANK,
                 columnspan=1, rowspan=1, right_column_title=None):
        GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)
        self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

        self.general_options_data = general_options_data
        self.right_options_data = right_options_data

        # Configure weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        # Assert option type
        assert type(self.general_options_data) == dict
        assert type(self.right_options_data) == dict

        # Assert option content {label: boolean}
        assert True in (g in GENERAL_BANK.keys() for g in self.general_options_data.keys())
        assert False not in (type(g) == bool for g in self.general_options_data.values())
        assert True in (r in RIGHT_BANK.keys() for r in self.right_options_data.keys())
        assert False not in (type(r) == bool for r in self.right_options_data.values())

        # Prepares the entries to display
        general_options = []
        for k in self.general_options_data.keys():
            general_options.append(GENERAL_BANK.get(k))

        right_options = []
        for k in self.right_options_data.keys():
            right_options.append(RIGHT_BANK.get(k))

        # Generate Title and tables
        self.info_block = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=2, text=title)
        self.general_frame = InfoInputBlock.Frame(self, column=0, row=1,
                                                  title="General Information", options=general_options)
        self.right_frame = InfoInputBlock.Frame(self, column=1, row=1, title=right_column_title, options=right_options)

        # Disables the right entries
        for k in self.general_options_data:
            if self.general_options_data.get(k) is False:
                self.general_frame.disable_entry(GENERAL_BANK.get(k))

        for k in self.right_options_data:
            if self.right_options_data.get(k) is False:
                self.right_frame.disable_entry(RIGHT_BANK.get(k))

    def update_colour(self):
        super().update_colour()
        # Set colour
        self.general_frame.set_frame_colour(General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
        self.general_frame.set_label_colour(General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_D))

        self.right_frame.set_frame_colour(General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
        self.right_frame.set_label_colour(General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_D))

        # Update colour
        self.info_block.update_colour()
        self.general_frame.update_colour()
        self.right_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.info_block.update_content()
        self.general_frame.update_content()
        self.right_frame.update_content()

    def save_to_database(self, id):
        Warnings.not_to_reach()

    def get_value(self, entry_name):
        if self.general_frame.exists_entry(entry_name=entry_name):
            return self.general_frame.get_value(name=entry_name)
        elif self.right_frame.exists_entry(entry_name=entry_name):
            return self.right_frame.get_value(name=entry_name)
        else:
            Warnings.not_to_reach()
            return None


class DatasetInfo(Frame):
    def __init__(self, root, column, row, title,
                 general_options_data, right_options_data,
                 columnspan=1, rowspan=1, right_column_title=None):
        Frame.__init__(self, root=root, column=column, row=row, title=title,
                       general_options_data=general_options_data, right_options_data=right_options_data,
                       GENERAL_BANK=Constants.DATABASE_GENERAL_INFORMATION_OPTIONS,
                       RIGHT_BANK=Constants.DATABASE_SMOOTHING_INFORMATION_OPTIONS,
                       columnspan=columnspan, rowspan=rowspan, right_column_title=right_column_title)

    def save_to_database(self, dataset_id):

        if ClientConnection.is_logged_in():

            new_values = {}

            # Adds editable values from the general frame
            for k in self.general_options_data:
                if self.general_options_data.get(k) is True:  # if enabled entries
                    new_values[k] = self.general_frame.get_value(Constants.DATABASE_GENERAL_INFORMATION_OPTIONS.get(k))

            # Adds editable values from the smoothing frame
            for k in self.right_options_data:
                if self.right_options_data.get(k) is True:  # if enabled entries
                    new_values[k] = self.right_frame.get_value(Constants.DATABASE_SMOOTHING_INFORMATION_OPTIONS.get(k))

            # Sends the update to the server
            result = ClientConnection.update_dataset_entry(dataset_id, new_values)

            if result is True:
                Log.info("The dataset update was successful.")
                tkinter.messagebox.showwarning("Success!", "The dataset information was updated.")
            else:
                Log.info("The dataset update was not successful.")
                tkinter.messagebox.showwarning("Failed!", "Could not update the dataset information.")
        else:
            tkinter.messagebox.showwarning(
                "Failed!", "Could not update the dataset information. The user is not logged-in.")


class ModelInfo(Frame):
    def __init__(self, root, column, row, title,
                 general_options_data, right_options_data,
                 columnspan=1, rowspan=1, right_column_title=None):
        Frame.__init__(self, root=root, column=column, row=row, title=title,
                       general_options_data=general_options_data, right_options_data=right_options_data,
                       GENERAL_BANK=Constants.MODEL_GENERAL_INFORMATION_OPTIONS,
                       RIGHT_BANK=Constants.MODEL_TRAINING_INFORMATION_OPTIONS,
                       columnspan=columnspan, rowspan=rowspan, right_column_title=right_column_title)

    def save_to_database(self, model_id):

        if ClientConnection.is_logged_in():

            new_values = {}

            # Adds editable values from the general frame
            for k in self.general_options_data:
                if self.general_options_data.get(k) is True:  # if enabled entries
                    new_values[k] = self.general_frame.get_value(Constants.MODEL_GENERAL_INFORMATION_OPTIONS.get(k))

            # Adds editable values from the smoothing frame
            for k in self.right_options_data:
                if self.right_options_data.get(k) is True:  # if enabled entries
                    new_values[k] = self.right_frame.get_value(Constants.MODEL_TRAINING_INFORMATION_OPTIONS.get(k))

            # Sends the update to the server
            result = ClientConnection.update_model_entry(model_id, new_values)

            if result is True:
                Log.info("The model update was successful.")
                tkinter.messagebox.showwarning("Success!", "The model information was updated.")
            else:
                Log.info("The model update was not successful.")
                tkinter.messagebox.showwarning("Failed!", "Could not update the model information.")
        else:
            tkinter.messagebox.showwarning(
                "Failed!", "Could not update the model information. The user is not logged-in.")
