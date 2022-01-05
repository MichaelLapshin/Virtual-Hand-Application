import tkinter.messagebox

from scripts import Constants, Warnings, Log, Parameters, General, InputConstraints
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

        self.GENERAL_BANK = GENERAL_BANK
        self.RIGHT_BANK = RIGHT_BANK

        self.general_options_data = general_options_data
        self.right_options_data = right_options_data

        # Configure weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        # Functions
        self.type_name = None
        self.save_function = None
        self.delete_function = None

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
            general_options.append(self.GENERAL_BANK.get(k))

        right_options = []
        for k in self.right_options_data.keys():
            right_options.append(self.RIGHT_BANK.get(k))

        # Generate Title and tables
        self.info_block = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=2, text=title)
        self.general_frame = InfoInputBlock.Frame(self, column=0, row=1,
                                                  title="General Information", options=general_options)
        self.right_frame = InfoInputBlock.Frame(self, column=1, row=1, title=right_column_title, options=right_options)

        # Disables the appropriate
        self.disable_enable_entries(self.general_options_data, self.right_options_data)

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

    def update_entries(self, entries, owner_name=""):
        # Assert option type
        assert type(entries) == dict

        # Assert option content {label: value}
        assert True in ((e in self.GENERAL_BANK.keys()) or (e in self.RIGHT_BANK.keys()) for e in entries.keys())

        # Sets the entry values
        for k in entries:
            if k in self.GENERAL_BANK.keys():
                self.general_frame.set_entry_value(self.GENERAL_BANK.get(k), entries.get(k))

                # Exceptions
                if k == "Permission":
                    for p in Constants.PERMISSION_LEVELS.keys():
                        if int(Constants.PERMISSION_LEVELS.get(p)) == int(entries.get(k)):
                            self.general_frame.set_entry_value(self.GENERAL_BANK.get(k), p)
                elif k == "Is_Raw":
                    self.general_frame.set_entry_value(self.GENERAL_BANK.get(k), str(entries.get(k) == 1))
                elif k == "ID_Owner":
                    self.general_frame.set_entry_value(self.GENERAL_BANK.get(k), owner_name)

            elif k in self.RIGHT_BANK.keys():
                self.right_frame.set_entry_value(self.RIGHT_BANK.get(k), entries.get(k))

    def _disable_enable_entries_helper(self, frame, entries, bank):
        if entries is not None:

            # Assert option type
            assert type(entries) == dict

            # Assert option content {label: boolean}
            assert True in (g in bank.keys() for g in entries.keys())
            assert False not in (type(g) == bool for g in entries.values())

            # Disables the right entries
            for k in entries:
                if entries.get(k) is False:
                    frame.disable_entry(bank.get(k))
                else:
                    frame.enable_entry(bank.get(k))

    def disable_enable_entries(self, general_entries, right_entries):
        self._disable_enable_entries_helper(self.general_frame, general_entries, self.GENERAL_BANK)
        self._disable_enable_entries_helper(self.right_frame, right_entries, self.RIGHT_BANK)

    def get_value(self, entry_name):
        if self.general_frame.exists_entry(entry_name=self.GENERAL_BANK.get(entry_name)):
            return self.general_frame.get_value(name=self.GENERAL_BANK.get(entry_name))
        elif self.right_frame.exists_entry(entry_name=self.RIGHT_BANK.get(entry_name)):
            return self.right_frame.get_value(name=self.RIGHT_BANK.get(entry_name))
        else:
            Log.critical("This part should not be reached. Received the entry name: " + entry_name)
            Warnings.not_to_reach()
            return None

    # Button functions
    def save_item(self, is_selected, item_id):
        if is_selected is True:

            # TODO, assert value type

            if ClientConnection.is_logged_in():

                new_values = {}

                # Adds editable values from the general frame
                for k in self.general_options_data:
                    if self.general_options_data.get(k) is True:  # if enabled entries
                        new_values[k] = self.general_frame.get_value(self.GENERAL_BANK.get(k))

                # Adds editable values from the smoothing frame
                for k in self.right_options_data:
                    if self.right_options_data.get(k) is True:  # if enabled entries
                        new_values[k] = self.right_frame.get_value(self.RIGHT_BANK.get(k))

                # Sends the update to the server
                result = self.save_function(item_id, new_values)

                if result is True:
                    Log.info("The " + self.type_name + " update was successful.")
                    tkinter.messagebox.showwarning("Success!", "The " + self.type_name + " information was updated.")
                    return True
                else:
                    Log.info("The " + self.type_name + " update was not successful.")
                    tkinter.messagebox.showwarning("Failed!",
                                                   "Could not update the " + self.type_name + " information.")
                    return False
            else:
                tkinter.messagebox.showwarning(
                    "Failed!", "Could not update the " + self.type_name + " information. The user is not logged-in.")
                return False
        else:
            tkinter.messagebox.showwarning("Warning!", "No " + self.type_name + " is selected.")
            return False

    def delete_item(self, is_selected, item_id):
        if is_selected is True:
            if ClientConnection.is_logged_in():

                confirm_delete = tkinter.messagebox.askyesno(
                    "Confirmation",
                    "Do you wish to delete the " + self.type_name + " with the id '" + str(item_id) + "'?")
                Log.info("The user confirmed to delete the " + self.type_name + ": " + str(confirm_delete))

                if confirm_delete is True:
                    result = self.delete_function(item_id)
                    if result is True:
                        Log.info("The " + self.type_name + " was successfully deleted.")
                        return True
                    else:
                        Log.warning("The " + self.type_name + " was not successfully deleted.")
                        return False
            else:
                tkinter.messagebox.showwarning(
                    "Failed!", "Could not update the " + self.type_name + " information. The user is not logged-in.")
                return False
        else:
            tkinter.messagebox.showwarning("Warning!", "No " + self.type_name + " is selected.")
            return False

    def toggle_favourite_item(self, item_id):
        Warnings.not_complete()

    def clear_info_frame(self):
        for v in self.GENERAL_BANK.values():
            self.general_frame.set_entry_value(v, "")
        for v in self.RIGHT_BANK.values():
            self.right_frame.set_entry_value(v, "")


class DatasetInfo(Frame):
    def __init__(self, root, column, row, title,
                 general_options_data, right_options_data,
                 columnspan=1, rowspan=1, right_column_title=None):
        Frame.__init__(self, root=root, column=column, row=row, title=title,
                       general_options_data=general_options_data, right_options_data=right_options_data,
                       GENERAL_BANK=Constants.DATASET_GENERAL_INFORMATION_OPTIONS,
                       RIGHT_BANK=Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS,
                       columnspan=columnspan, rowspan=rowspan, right_column_title=right_column_title)

        # Override to dataset-based commends and text
        self.save_function = ClientConnection.update_dataset_entry
        self.delete_function = ClientConnection.delete_dataset_entry
        self.type_name = "dataset"

    def smooth_dataset(self, owner_id, dataset_id):
        # Obtain inputs (general parameters)
        name = self.get_value("Name")
        owner_id = owner_id  # self.get_value("ID_Owner")
        date_created = self.get_value("Date_Created")
        access_permission = self.get_value("Permission")
        rating = self.get_value("Rating")
        is_raw = self.get_value("Is_Raw")

        # Obtain inputs (smoothing parameters)
        num_frames = self.get_value("Num_Frames")
        fps = self.get_value("FPS")
        sensor_savagol_distance = self.get_value("Sensor_Savagol_Distance")
        sensor_savagol_degree = self.get_value("Sensor_Savagol_Degree")
        angle_savagol_distance = self.get_value("Angle_Savagol_Distance")
        angle_savagol_degree = self.get_value("Angle_Savagol_Degree")

        # Check assertions that inputs are integers
        can_smooth = True

        # Assertions on the general parameters
        can_smooth &= InputConstraints.assert_string_non_empty(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Name"), name)
        can_smooth &= InputConstraints.assert_string_non_empty(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("ID_Owner"), owner_id)
        can_smooth &= InputConstraints.assert_string_non_empty(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Date_Created"), date_created)
        can_smooth &= InputConstraints.assert_string_from_set(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Permission"), access_permission,
            Constants.PERMISSION_LEVELS.keys())
        can_smooth &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Rating"), rating, Constants.MAX_RATING)
        can_smooth &= InputConstraints.assert_string_from_set(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Is_Raw"), is_raw, Constants.BOOLEANS.keys())

        # Assertions on the smoothing parameters
        can_smooth &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Num_Frames"), num_frames)
        can_smooth &= InputConstraints.assert_int_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("FPS"), fps)
        can_smooth &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Sensor_Savagol_Distance"), sensor_savagol_distance)
        can_smooth &= InputConstraints.assert_int_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Sensor_Savagol_Degree"), sensor_savagol_degree)
        can_smooth &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Angle_Savagol_Distance"), angle_savagol_distance)
        can_smooth &= InputConstraints.assert_int_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Angle_Savagol_Degree"), angle_savagol_degree)

        if can_smooth is True:
            # Additional smoothing assertions (degree < window)
            can_smooth &= InputConstraints.assert_int_less_than(
                value1_name=Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Sensor_Savagol_Degree"),
                value1=sensor_savagol_degree,
                value2_name=Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Sensor_Savagol_Distance"),
                value2=sensor_savagol_distance)
            can_smooth &= InputConstraints.assert_int_less_than(
                value1_name=Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Angle_Savagol_Degree"),
                value1=angle_savagol_degree,
                value2_name=Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Angle_Savagol_Distance"),
                value2=angle_savagol_distance)

            # Additional smoothing assertions (degree & window are odd)
            can_smooth &= InputConstraints.assert_odd_integer(
                Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Sensor_Savagol_Distance"),
                sensor_savagol_distance)
            can_smooth &= InputConstraints.assert_odd_integer(
                Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Sensor_Savagol_Degree"), sensor_savagol_degree)
            can_smooth &= InputConstraints.assert_odd_integer(
                Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Angle_Savagol_Distance"), angle_savagol_distance)
            can_smooth &= InputConstraints.assert_odd_integer(
                Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Angle_Savagol_Degree"), angle_savagol_degree)

            if can_smooth is True:
                if ClientConnection.is_logged_in():

                    result = ClientConnection.smooth_dataset(
                        # General parameters
                        name=name,
                        owner_id=int(owner_id),
                        date_created=date_created,
                        permission=int(Constants.PERMISSION_LEVELS.get(access_permission)),
                        rating=int(rating),
                        is_raw=int(Constants.BOOLEANS.get(is_raw)),

                        # Smoothing parameters
                        dataset_id=int(dataset_id),
                        num_frames=int(num_frames),
                        frames_per_second=int(fps),
                        sensor_savagol_distance=int(sensor_savagol_distance),
                        sensor_savagol_degree=int(sensor_savagol_degree),
                        angle_savagol_distance=int(angle_savagol_distance),
                        angle_savagol_degree=int(angle_savagol_degree))

                    if result is True:
                        Log.info("The dataset was successfully smoothed.")
                        tkinter.messagebox.showinfo("Success!", "The dataset was successfully smoothed.")
                        return True
                    else:
                        Log.warning("The dataset was not successfully smoothed.")
                        tkinter.messagebox.showwarning("Failed!", "The dataset was not successfully smoothed.")
                        return False

                else:
                    tkinter.messagebox.showwarning("Failed!",
                                                   "Could not smooth the dataset. The user is not logged-in.")
                    return False
            else:
                tkinter.messagebox.showwarning(
                    "Failed!", "Could not smooth the dataset. Input constraints where not satisfied.")
                return False
        else:
            tkinter.messagebox.showwarning(
                "Failed!", "Could not smooth the dataset. Input constraints where not satisfied.")
            return False


class ModelInfo(Frame):
    def __init__(self, root, column, row, title,
                 general_options_data, right_options_data,
                 columnspan=1, rowspan=1, right_column_title=None):
        Frame.__init__(self, root=root, column=column, row=row, title=title,
                       general_options_data=general_options_data, right_options_data=right_options_data,
                       GENERAL_BANK=Constants.MODEL_GENERAL_INFORMATION_OPTIONS,
                       RIGHT_BANK=Constants.MODEL_TRAINING_INFORMATION_OPTIONS,
                       columnspan=columnspan, rowspan=rowspan, right_column_title=right_column_title)

        # Override to model-based commends and text
        self.save_function = ClientConnection.update_model_entry
        self.delete_function = ClientConnection.delete_model_entry
        self.type_name = "model"

    def create_model(self):
        # Obtain inputs (general parameters)
        name = self.get_value("Name")
        owner_id = ClientConnection.get_user_id()  # self.get_value("ID_Owner")
        date_created = self.get_value("Date_Created")
        access_permission = self.get_value("Permission")
        rating = self.get_value("Rating")
        dataset_id = self.get_value("ID_Dataset")
        frames_shift = self.get_value("Frames_Shift")

        # Obtain inputs (smoothing parameters)
        num_training_frames = self.get_value("Num_Training_Frames")
        learning_rate = self.get_value("Learning_Rate")
        batch_size = self.get_value("Batch_Size")
        num_epochs = self.get_value("Num_Epochs")
        layer_type = self.get_value("Layer_Types")
        num_layers = self.get_value("Num_Layers")
        num_nodes_per_layer = self.get_value("Num_Nodes_Per_Layer")

        # Check assertions for model inputs
        can_create = True

        # Assertions on the general parameters
        can_create &= InputConstraints.assert_string_non_empty(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Name"), name)
        can_create &= InputConstraints.assert_string_non_empty(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("ID_Owner"), owner_id)
        can_create &= InputConstraints.assert_string_non_empty(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Date_Created"), date_created)
        can_create &= InputConstraints.assert_string_from_set(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Permission"), access_permission,
            Constants.PERMISSION_LEVELS.keys())
        can_create &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Rating"), rating, Constants.MAX_RATING)
        can_create &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("ID_Dataset"), dataset_id)
        can_create &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Frames_Shift"), frames_shift)

        # Assertions on the smoothing parameters
        can_create &= InputConstraints.assert_int_non_negative(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Num_Training_Frames"), num_training_frames)
        can_create &= InputConstraints.assert_float_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Learning_Rate"), learning_rate)
        can_create &= InputConstraints.assert_int_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Batch_Size"), batch_size)
        can_create &= InputConstraints.assert_int_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Num_Epochs"), num_epochs)
        can_create &= InputConstraints.assert_string_from_set(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Layer_Types"), layer_type,
            Constants.MODEL_ACT_FUNC_OPTIONS)
        can_create &= InputConstraints.assert_int_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Num_Layers"), num_layers)
        can_create &= InputConstraints.assert_int_positive(
            Constants.DATASET_SMOOTHING_INFORMATION_OPTIONS.get("Num_Nodes_Per_Layer"), num_nodes_per_layer)

        if can_create is True:

            if ClientConnection.is_logged_in():

                result = ClientConnection.create_model_training_process(
                    # General parameters
                    name=name,
                    owner_id=int(owner_id),
                    date_created=date_created,
                    permission=int(Constants.PERMISSION_LEVELS.get(access_permission)),
                    rating=int(rating),

                    # Model Training parameters
                    dataset_id=int(dataset_id),
                    frames_shift=frames_shift,
                    num_training_frames=int(num_training_frames),
                    learning_rate=float(learning_rate),
                    batch_size=int(batch_size),
                    num_epochs=int(num_epochs),
                    layer_type=layer_type,
                    num_layers=int(num_layers),
                    num_nodes_per_layer=int(num_nodes_per_layer))

                if result is True:
                    Log.info("The dataset was successfully smoothed.")
                    return True
                else:
                    Log.warning("The dataset was not successfully smoothed.")
                    return False

            else:
                tkinter.messagebox.showwarning("Failed!",
                                               "Could not create a model training process. The user is not logged-in.")
                return False

        else:
            tkinter.messagebox.showwarning(
                "Failed!", "Could not create a model training process. Input constraints where not satisfied.")
            return False
