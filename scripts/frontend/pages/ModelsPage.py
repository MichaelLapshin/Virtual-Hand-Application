import tkinter, tkinter.messagebox

from scripts import General, Warnings, Parameters, Constants, Log
from scripts.frontend import Navigation, ClientConnection
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock, InformationBlock, PredictionPreviewBlock, SearchBlock, \
    DataInfoBlock, ProgressBar
from scripts.frontend.pages import GenericPage

TITLE_SELECTED_MODEL_INFORMATION = "Selected Model Information"
TITLE_SELECTED_DATABASE_INFORMATION = "Selected Database Information"
TITLE_NEW_MODEL_INFORMATION = "New Model Information"


class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODELS)
        self.grid(padx=0, pady=0, sticky=tkinter.NSEW)
        self.config(bd=0, relief=None)

        # Weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Frames
        self.view_frame = ViewFrame(self, base_frame=base_frame)
        self.new_frame = NewFrame(self, base_frame=base_frame)
        self.view_frame.grid(row=0)
        self.new_frame.grid(row=0)

        # Swt switch frame functions
        self.view_frame.set_switch_to_new_frame(lambda: self._switch_to_frame(self.new_frame))
        self.new_frame.set_switch_to_view_frame(lambda: self._switch_to_frame(self.view_frame))

        # Default view the new frame
        self._switch_to_frame(self.view_frame)

    def _switch_to_frame(self, frame):
        self.view_frame.grid_remove()
        self.new_frame.grid_remove()

        # Set and switch display to current frame
        self.current_frame = frame
        self.current_frame.grid()

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_A))
        self.view_frame.update_colour()
        self.new_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.view_frame.update_content()
        self.new_frame.update_content()


class ViewFrame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODELS)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

        # Search space
        self.search_frame = SearchBlock.ModelSearchFrame(self, column=0, row=0, rowspan=2,
                                                         title="Model List", multi_select=False,
                                                         select_change_command=self.selected_entry_update_command)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Additional search buttons
        self.new_button = SearchButton(self.search_frame.button_frame, column=0, row=0, text="New Model",
                                       command=Warnings.not_overridden)

        # Info frame
        self.info_frame = DataInfoBlock.ModelInfo(
            self, column=1, row=0, title="Model Information",
            general_options_data={"Name": True, "ID_Owner": False, "Date_Created": False,
                                  "Permission": False, "Rating": True, "ID_Dataset": False, "Frames_Shift": False},
            right_options_data={"Num_Training_Frames": False, "Learning_Rate": False,
                                "Batch_Size": False, "Num_Epochs": False,
                                "Layer_Types": False, "Num_Layers": False, "Num_Nodes_Per_Layer": False},
            right_column_title="Training Information")

        # Additional buttons for the info frame
        self.button_frame = GenericPage.Frame(self,
                                              column=1, row=1,
                                              columnspan=1, rowspan=1)
        self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

        # Configure button frame weights
        for i in range(0, 3):
            self.button_frame.columnconfigure(i, weight=1)

        # Create info frame buttons
        self.training_progress_bar = ProgressBar.Frame(self.button_frame, column=0, row=0,
                                                       metric_text=" Training Epochs", max_count=1,
                                                       is_default_percentage=False)
        self.create_model_process_button = InformationButton(self.button_frame, column=1, row=0,
                                                             text="Create Model Process",
                                                             command=self.create_model_process_button_command)
        self.delete_button = InformationButton(self.button_frame, column=2, row=0, text="Delete",
                                               command=self.delete_button_command)

        # Prediction Preview frame
        self.prediction_preview_block = PredictionPreviewBlock.Frame(self, column=0, row=2, columnspan=2)

    def update_colour(self):
        super().update_colour()
        self.search_frame.update_colour()
        self.new_button.update_colour()
        self.info_frame.update_colour()

        # Button frame
        self.button_frame.update_colour()
        self.training_progress_bar.update_colour()
        self.create_model_process_button.update_colour()
        self.delete_button.update_colour()

        # Prediction block
        self.prediction_preview_block.update_colour()

    def update_content(self):
        super().update_content()
        self.search_frame.update_content()
        self.new_button.update_content()
        self.info_frame.update_content()

        # Button frame
        self.button_frame.update_content()
        self.training_progress_bar.update_content()
        self.create_model_process_button.update_content()
        self.delete_button.update_content()

        # Prediction block
        self.prediction_preview_block.update_content()

    def destroy(self):
        super().destroy()

    def selected_entry_update_command(self):
        # Obtains the data
        selected_index = self.search_frame.scroll_block.get_selected_main()
        data_at_index = self.search_frame.get_index_data(selected_index)

        # Prepares the entries
        entries = {}
        for i in range(0, len(Constants.MODEL_ENTRY_TRANSFER_DATA)):
            entries[Constants.MODEL_ENTRY_TRANSFER_DATA[i]] = data_at_index[i]
        owner_name = ClientConnection.get_user_name_of(entries.get("ID_Owner"))

        # Updates the info frame
        self.info_frame.update_entries(entries=entries, owner_name=owner_name)

        # Loads in the prediction and error images
        selected_dataset_id = self.search_frame.get_selected_main_id()
        self.prediction_preview_block.image_frame.load_new_images(model_id=selected_dataset_id)
        self.prediction_preview_block.button_frame.update_image_state()

    def create_model_process_button_command(self):
        Warnings.not_complete()  # TODO, finish this

    def delete_button_command(self):
        result = self.info_frame.delete_item(self.search_frame.scroll_block.is_selected_main(),
                                             self.search_frame.get_selected_main_id())
        Log.debug("The model deletion result is: " + str(result))
        if result is True:
            self.search_frame.search_button_command()
            self.prediction_preview_block.image_frame.clear_images()

    def set_switch_to_new_frame(self, command):
        self.new_button.config(command=command)


class NewFrame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame, page_title=Navigation.TITLE_MODELS)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Search space
        self.search_frame = SearchBlock.DatasetSearchFrame(self, column=0, row=0, rowspan=3, title="Select Datasets",
                                                           multi_select=False,
                                                           select_change_command=self.selected_entry_update_command,
                                                           search_frame_command=self.search_frame_command)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Additional search button
        self.view_models_button = SearchButton(self.search_frame.button_frame, column=0, row=0, text="View Models",
                                               command=Warnings.not_complete)
        # Info frame
        self.database_info_frame = DataInfoBlock.DatasetInfo(
            self, column=1, row=0, title="Selected Dataset Information",
            general_options_data={"Name": False, "ID_Owner": False, "Date_Created": False,
                                  "Permission": False, "Rating": False, "Is_Raw": False},
            right_options_data={"Num_Frames": False, "FPS": False,
                                "Sensor_Savagol_Distance": False, "Sensor_Savagol_Degree": False,
                                "Angle_Savagol_Distance": False, "Angle_Savagol_Degree": False},
            right_column_title="Smoothing Information")

        self.new_model_info_frame = DataInfoBlock.ModelInfo(
            self, column=1, row=1, title="New Model Information",
            general_options_data={"Name": True, "ID_Owner": False, "Date_Created": False,
                                  "Permission": False, "Rating": True, "ID_Dataset": False, "Frames_Shift": True},
            right_options_data={"Num_Training_Frames": False, "Learning_Rate": True,
                                "Batch_Size": True, "Num_Epochs": True,
                                "Layer_Types": True, "Num_Layers": True, "Num_Nodes_Per_Layer": True},
            right_column_title="Training Information")
        self.new_model_info_frame.update_entries(
            entries={"Permission": Constants.PERMISSION_LEVELS.get(Constants.PERMISSION_PUBLIC)})

        # Buttons
        self.start_model_training_button = InformationButton(self, column=1, row=2, text="Begin Model Training",
                                                             command=self.start_model_training_button_command)

    def update_colour(self):
        super().update_colour()
        self.search_frame.update_colour()
        self.database_info_frame.update_colour()
        self.new_model_info_frame.update_colour()
        self.view_models_button.update_colour()
        self.start_model_training_button.update_colour()

    def update_content(self):
        super().update_content()
        self.search_frame.update_content()
        self.database_info_frame.update_content()
        self.new_model_info_frame.update_content()
        self.view_models_button.update_content()
        self.start_model_training_button.update_content()

        # Update model entries
        self.new_model_info_frame.update_entries(entries={"Date_Created": General.get_current_slashed_date(),
                                                          "ID_Owner": ClientConnection.get_user_id()},
                                                 owner_name=ClientConnection.get_user_name())

        if self.search_frame.scroll_block.is_selected_main() is True:
            self.new_model_info_frame.update_entries(entries={"ID_Dataset": self.search_frame.get_selected_main_id()})

            # Dynamically changes the Num_Training_Frames
            try:
                int(self.new_model_info_frame.get_value("Frames_Shift"))
                self.new_model_info_frame.update_entries(
                    entries={"Num_Training_Frames": str(int(self.database_info_frame.get_value("Num_Frames"))
                                                        - int(self.new_model_info_frame.get_value("Frames_Shift")))})
            except:
                self.new_model_info_frame.update_entries(
                    entries={"Num_Training_Frames": "< " + self.database_info_frame.get_value("Num_Frames")})

        else:
            self.new_model_info_frame.update_entries(entries={"Num_Training_Frames": ""})

    def destroy(self):
        self.search_frame.update_content()
        self.database_info_frame.update_content()
        self.new_model_info_frame.update_content()
        super().destroy()

    def selected_entry_update_command(self):
        # Obtains the data
        selected_index = self.search_frame.scroll_block.get_selected_main()
        data_at_index = self.search_frame.get_index_data(selected_index)

        # Prepares the entries
        entries = {}
        for i in range(0, len(Constants.DATASET_ENTRY_TRANSFER_DATA)):
            entries[Constants.DATASET_ENTRY_TRANSFER_DATA[i]] = data_at_index[i]
        owner_name = ClientConnection.get_user_name_of(entries.get("ID_Owner"))

        # Updates the info frame
        self.database_info_frame.update_entries(entries=entries, owner_name=owner_name)

    def search_frame_command(self):
        self.database_info_frame.clear_info_frame()

    def start_model_training_button_command(self):

        is_dataset_selected = self.search_frame.scroll_block.is_selected_main()

        if is_dataset_selected is True:

            is_raw = self.search_frame.list_storage[self.search_frame.scroll_block.get_selected_main()][
                Constants.DATASET_ENTRY_TRANSFER_DATA.index("Is_Raw")]

            if is_raw == 0:
                result = self.new_model_info_frame.create_model()

                if result is True:
                    Log.info("The model training process has been added to the queue.")
                    tkinter.messagebox.showinfo("Success!", "Added the model training to the queue.")
                else:
                    Log.warning("Could not add the model training process to the queue.")
                    tkinter.messagebox.showwarning("Failed!", "Could not add the model training process to the queue.")
            else:
                Log.trace("Could not start create model process. A raw dataset was selected.")
                tkinter.messagebox.showwarning("Warning!", "Could not add the model training process to the queue.\n"
                                                           "A non-raw dataset must be selected.")
        else:
            Log.trace("Could not add the model training process to the queue. No dataset is selected.")
            tkinter.messagebox.showwarning("Warning!", "No dataset is selected.")

    def set_switch_to_view_frame(self, command):
        self.view_models_button.config(command=command)
