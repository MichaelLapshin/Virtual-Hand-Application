import tkinter, tkinter.messagebox

import requests
from PIL import Image, ImageTk

from scripts import General, Warnings, InputConstraints, Parameters, Constants, Log
from scripts.frontend import Navigation, ClientConnection
from scripts.frontend.logic import MediapipHandAngler, SensorListener, DatasetRecorder
from scripts.frontend.custom_widgets import CustomButtons, CustomLabels
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import \
    InformationBlock, ScrollBlock, DatasetGraphBlock, InfoInputBlock, ProgressBar, \
    StatusIndicator
from scripts.frontend.pages import GenericPage

TITLE_SELECTED_DATASET_INFORMATION = "Selected Dataset Information"
TITLE_NEW_DATASET_INFORMATION = "New Dataset Information"


class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_DATASETS)
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

        self.showing_view_frame = True

        # Swt switch frame functions
        self.view_frame.set_switch_to_new_frame(self._switch_to_new_frame)
        self.new_frame.set_switch_to_view_frame(self._switch_to_view_frame)

        # Default view the new frame
        self._switch_to_view_frame()

    def _switch_to_view_frame(self):
        # Visual Switch
        self.new_frame.grid_remove()
        self.current_frame = self.view_frame
        self.current_frame.grid()

        # Logical Switch
        self.new_frame.stop_new_frame_processes()

    def _switch_to_new_frame(self):
        # Visual Switch
        self.view_frame.grid_remove()
        self.current_frame = self.new_frame
        self.current_frame.grid()

        # Logical Switch
        self.new_frame.start_new_frame_processes()

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_A))
        self.view_frame.update_colour()
        self.new_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.view_frame.update_content()
        self.new_frame.update_content()

    def destroy(self):
        super().destroy()
        self.view_frame.destroy()
        self.new_frame.destroy()


class ViewFrame(GenericPage.NavigationFrame):
    class InfoFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self,
                                       root,
                                       column=column, row=row,
                                       columnspan=columnspan, rowspan=rowspan)
            self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure weights
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=0)

            # Information frame
            self.info_block = InformationBlock.Frame(self, title=TITLE_SELECTED_DATASET_INFORMATION,
                                                     num_columns=2, num_rows=2)
            self.info_block.config()
            self.info_block.grid(column=0, row=0)
            self.info_block.grid(columnspan=1, rowspan=1)

            # Buttons Frame
            self.button_frame = GenericPage.Frame(self,
                                                  column=0, row=1,
                                                  columnspan=1, rowspan=1)
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)
            self.button_frame.columnconfigure(2, weight=1)
            self.button_frame.columnconfigure(3, weight=1)

            # Create buttons
            self.favourite_button = \
                InformationButton(self.button_frame, column=0, row=0, text="Favourite", command=Warnings.not_complete)
            self.duplicate_button = \
                InformationButton(self.button_frame, column=1, row=0, text="Duplicate", command=Warnings.not_complete)
            self.smooth_button = \
                InformationButton(self.button_frame, column=2, row=0, text="Smooth Dataset",
                                  command=Warnings.not_complete)
            self.delete_button = \
                InformationButton(self.button_frame, column=3, row=0, text="Delete", command=Warnings.not_complete)

            """
                Additional information
            """
            # Fill in data for the information block
            self.info_block.add_info(1, 0, "hello world!")
            self.info_block.add_info(0, 1, "This is another test \n to check out \n what this type of stuff\n can do.")

        def update_colour(self):
            super().update_colour()
            self.button_frame.update_colour()

            self.favourite_button.update_colour()
            self.duplicate_button.update_colour()
            self.smooth_button.update_colour()
            self.delete_button.update_colour()

            self.info_block.set_frame_colour(Parameters.COLOUR_BRAVO)
            self.info_block.set_label_colour(Parameters.COLOUR_BRAVO)
            self.info_block.update_colour()

            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

    class SearchFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root)
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(sticky=tkinter.NS)

            # Configure weights
            self.rowconfigure(1, weight=1)
            self.columnconfigure(0, weight=1)

            # Scroll block
            self.scroll_models_block = ScrollBlock.Frame(self, selectable_items=True)
            self.scroll_models_block.grid(column=0, row=1)
            self.scroll_models_block.grid(columnspan=1, rowspan=1)

            # Buttons frame
            self.button_frame = GenericPage.Frame(self,
                                                  column=0, row=0,
                                                  columnspan=1, rowspan=1)
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.rowconfigure(0, weight=1)
            self.button_frame.rowconfigure(1, weight=1)
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)
            self.button_frame.columnconfigure(2, weight=1)

            # Search buttons & widgets
            self.new_dataset_button = SearchButton(
                self.button_frame, column=0, row=0, text="New", command=Warnings.not_complete)
            self.merge_selected_button = SearchButton(
                self.button_frame, column=1, row=0, text="Merge Selected", command=Warnings.not_complete)
            self.search_button = SearchButton(
                self.button_frame, column=2, row=0, text="Search", command=Warnings.not_complete)

            # Sorting
            self.button_search_frame = tkinter.Frame(self.button_frame)
            self.button_search_frame.grid(column=0, row=1, columnspan=3, sticky=tkinter.NSEW)
            self.button_search_frame.columnconfigure(1, weight=1)

            self.sort_label = SearchLabel(self.button_search_frame, column=0, row=0, text="Sort by:")
            self.sort_option_menu = SortOptionMenu(self.button_search_frame, column=1, row=0, columnspan=2)
            self.sort_option_menu.grid(sticky=tkinter.NSEW)

        def update_colour(self):
            super().update_colour()
            self.scroll_models_block.update_colour()
            self.button_frame.update_colour()
            self.new_dataset_button.update_colour()
            self.merge_selected_button.update_colour()
            self.search_button.update_colour()

            self.sort_label.update_colour()
            self.sort_option_menu.update_colour()

            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.button_search_frame.config(bg=self.button_frame.cget("bg"))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def update_content(self):
            super().update_content()
            self.scroll_models_block.update_content()

        def set_switch_frame_command(self, command):
            self.new_dataset_button.config(command=command)

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_DATASETS)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Search space
        self.search_frame = ViewFrame.SearchFrame(self, column=0, row=0)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Info frame
        self.info_frame = ViewFrame.InfoFrame(self, column=1, row=0)

        # Prediction Preview frame
        self.graph_frame = DatasetGraphBlock.Frame(self, column=0, row=1, columnspan=2)

    def update_colour(self):
        super().update_colour()
        self.search_frame.update_colour()
        self.info_frame.update_colour()
        self.graph_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.search_frame.update_content()

    def set_switch_to_new_frame(self, command):
        self.search_frame.set_switch_frame_command(command=command)


class NewFrame(GenericPage.NavigationFrame):
    class DataRecInfoFrame(GenericPage.Frame):

        def __init__(self, root, hand_angler, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self,
                                       root,
                                       column=column, row=row,
                                       columnspan=columnspan, rowspan=rowspan)
            self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure weights
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)

            # Data Recording Information
            self.record_options = ["Sensor zeroing delay (seconds)", "Training length (seconds)", "Frames per second"]
            self.input_frame = InfoInputBlock.Frame(self, column=0, row=0,
                                                    options=self.record_options,
                                                    title="Data Recording Information")

            # Input frame
            self.input_frame.set_entry_value("Sensor zeroing delay (seconds)",
                                             Constants.RECORDING_DEFAULT_SENSOR_ZEROING_DELAY)
            self.input_frame.set_entry_value("Training length (seconds)", Constants.RECORDING_DEFAULT_TRAINING_LENGTH)
            self.input_frame.set_entry_value("Frames per second", Constants.RECORDING_DEFAULT_FRAMES_PER_SECOND)

            # Main frames
            self.process_frame = GenericPage.Frame(self, column=1, row=0)
            self.process_frame.columnconfigure(0, weight=1)
            self.process_frame.columnconfigure(1, weight=1)
            self.process_frame.rowconfigure(1, weight=1)
            self.process_frame.rowconfigure(2, weight=1)

            # Progress start/stop
            self.start_stop_title = CustomLabels.TitleLabel(self.process_frame,
                                                            column=0, row=0, columnspan=3,
                                                            text="Data Recording Control Panel")
            self.start_progress_button = CustomButtons.InformationButton(self.process_frame,
                                                                         column=0, row=1, text="Start Data Gathering")
            self.status_label = StatusIndicator.Label(self.process_frame, column=1, row=1)
            self.stop_progress_button = CustomButtons.InformationButton(self.process_frame,
                                                                        column=2, row=1, text="Stop Data Gathering")
            self.progress_bar = ProgressBar.Frame(self.process_frame, column=0, row=2, columnspan=3,
                                                  metric_text=" seconds", max_count=100)

            # Progress start/stop configuration
            self.start_stop_title.grid(padx=Constants.STANDARD_SPACING)
            self.start_progress_button.grid(sticky=tkinter.EW, padx=Constants.LONG_SPACING)
            self.status_label.grid(padx=Constants.SHORT_SPACING)
            self.stop_progress_button.grid(sticky=tkinter.EW, padx=Constants.LONG_SPACING)

            # Camera + default parameters
            self.hand_angler = hand_angler

            self.camera_frame = GenericPage.Frame(self, column=0, row=1, columnspan=2)
            self.camera_frame.columnconfigure(0, weight=1)
            self.camera_frame.rowconfigure(0, weight=1)
            self.camera_label = CustomLabels.TitleLabel(self.camera_frame, column=0, row=0)
            self.camera_label.grid(sticky=tkinter.N)

        def update_colour(self):
            # Set colour
            self.input_frame.set_frame_colour(
                General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.input_frame.set_label_colour(
                General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_D))

            self.progress_bar.set_background_colour(
                General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))
            self.progress_bar.set_progress_colour(
                General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_F))

            # Update colour
            self.input_frame.update_colour()
            self.process_frame.update_colour()
            self.progress_bar.update_colour()
            self.start_stop_title.update_colour()
            self.start_progress_button.update_colour()
            self.status_label.update_colour()
            self.stop_progress_button.update_colour()
            self.camera_frame.update_colour()
            self.camera_label.update_colour()

            # Set colours
            self.start_stop_title.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_D))
            self.process_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def update_content(self):
            self.input_frame.update_content()
            self.process_frame.update_content()
            self.progress_bar.update_content()
            self.camera_frame.update_content()
            self.camera_label.update_content()

            self.start_progress_button.update_content()
            self.status_label.update_content()
            self.stop_progress_button.update_content()

            # Paint the camera
            if (self.hand_angler is not None) and (self.hand_angler.get_raw_image() is not None):
                image = Image.fromarray(self.hand_angler.get_processed_image())

                # Resize image
                ratio = self.camera_frame.winfo_width() / float(image.width)
                if int(ratio * image.height) > self.camera_frame.winfo_height():
                    ratio = self.camera_frame.winfo_height() / float(image.height)
                    image = image.resize((int(ratio * image.width), int(ratio * image.height)))
                else:
                    image = image.resize((int(ratio * image.width), int(ratio * image.height)))

                # Apply image
                imageTk = ImageTk.PhotoImage(image=image)
                self.camera_label.config(image=imageTk)
                self.camera_label.image = imageTk

        def stop_hand_angler(self):
            if (self.hand_angler is not None) \
                    and self.hand_angler.is_running():
                self.hand_angler.stop()

        def destroy(self):
            self.stop_hand_angler()
            super().destroy()

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_DATASETS)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        # self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=5)

        # Cancel Button
        self.cancel_new_dataset = CustomButtons.SearchButton(self, column=0, row=0, text="View Datasets")

        # Frames
        self.general_options = ["Name", "Owner", "Date created", "Access permissions"]
        self.general_info_frame = InfoInputBlock.Frame(self,
                                                       column=0, row=1,
                                                       options=self.general_options,
                                                       title="General Information")
        self.general_info_frame.disable_entry("Owner")  # Note: Owner entry is automatically updated
        self.general_info_frame.disable_entry("Date created")  # Note: Date created entry is automatically updated

        self.general_info_frame.set_perm_option_menu("Access permissions")

        self.upload_dataset_button = CustomButtons.SearchButton(self.general_info_frame,
                                                                column=0, row=5, columnspan=2,
                                                                command=self.upload_dataset_to_server,
                                                                text="Upload Dataset to Server")

        # Cam Control Info
        self.cam_control_options = ["Video source", "Width", "Height", "Zoom %", "Frames per second"]
        self.cam_control_frame = InfoInputBlock.Frame(self,
                                                      column=0, row=2,
                                                      options=self.cam_control_options,
                                                      title="Camera Control")
        self.cam_control_frame.set_video_source_option_menu("Video source")
        self.apply_cam_settings = CustomButtons.SearchButton(self.cam_control_frame,
                                                             column=0, row=6, columnspan=2,
                                                             command=self.reconfigure_hand_angler,
                                                             text="Apply Camera Settings")

        # Give default camera settings variables
        self.cam_control_frame.set_entry_value("Width", Constants.CAMERA_DEFAULT_RESOLUTION_X)
        self.cam_control_frame.set_entry_value("Height", Constants.CAMERA_DEFAULT_RESOLUTION_Y)
        self.cam_control_frame.set_entry_value("Zoom %", Constants.CAMERA_DEFAULT_ZOOM_PERCENT)
        self.cam_control_frame.set_entry_value("Frames per second", Constants.CAMERA_DEFAULT_FRAMES_PER_SECOND)

        """
            logic threads and objects
        """

        # Setup Hand Angler
        self.hand_angler = MediapipHandAngler.HandAngleReader()
        self.hand_angler.start()

        # Setup Sensor Reader & Data Recorder
        self.sensor_listener = None
        self.data_recorder = None

        # Data recording frame
        self.data_rec_info_frame = NewFrame.DataRecInfoFrame(self, hand_angler=self.hand_angler,
                                                             column=1, row=0, rowspan=3)
        self.data_rec_info_frame.start_progress_button.config(command=self.start_dataset_recording)
        self.data_rec_info_frame.stop_progress_button.config(command=self.stop_dataset_recording)
        self.reconfigure_hand_angler()

    def update_colour(self):
        super().update_colour()

        # Label colour
        self.general_info_frame.set_frame_colour(
            General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
        self.general_info_frame.set_label_colour(
            General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_D))

        self.cam_control_frame.set_frame_colour(
            General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
        self.cam_control_frame.set_label_colour(
            General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_D))

        # Update colour
        self.cancel_new_dataset.update_colour()
        self.general_info_frame.update_colour()
        self.upload_dataset_button.update_colour()
        self.cam_control_frame.update_colour()
        self.data_rec_info_frame.update_colour()
        self.apply_cam_settings.update_colour()

    def update_content(self):
        super().update_content()
        self.general_info_frame.update_content()
        self.upload_dataset_button.update_content()
        self.cam_control_frame.update_content()
        self.data_rec_info_frame.update_content()
        self.cancel_new_dataset.update_content()
        self.apply_cam_settings.update_content()

        # Updates user and date
        owner = ClientConnection.get_user_name()
        if owner is None:
            owner = ""
        self.general_info_frame.set_entry_value("Owner", owner)
        self.general_info_frame.set_entry_value("Date created", General.get_current_slashed_date())

        # Updates data recorder
        if self.data_recorder is not None:
            self.data_rec_info_frame.status_label.set_status(self.data_recorder.is_running())

        # Enables uploading to the server
        if (self.data_recorder is not None) and (self.data_recorder.is_successful() is True) \
                and (self.data_recorder.is_recording_used() is False):
            self.upload_dataset_button.enable()
            self.temp_dataset_FPS = self.data_rec_info_frame.input_frame.get_value("Frames per second")
        else:
            self.upload_dataset_button.disable()

    def destroy(self):
        if self.data_recorder is not None:
            self.data_recorder.stop()
        if self.sensor_listener is not None:
            self.sensor_listener.stop_reading()
            self.sensor_listener.stop_running()
        if self.hand_angler is not None:
            self.hand_angler.stop_watching()
            self.hand_angler.stop()
        super().destroy()

    def upload_dataset_to_server(self):
        # Extract values
        name = self.general_info_frame.get_value("Name")
        owner_name = self.general_info_frame.get_value("Owner")
        date_created = self.general_info_frame.get_value("Date created")
        access_permissions = self.general_info_frame.get_value("Access permissions")
        frames_per_second = self.temp_dataset_FPS

        # Assert the input constraints
        can_upload = True
        can_upload &= InputConstraints.assert_string_non_empty("Name", name)
        can_upload &= InputConstraints.assert_string_non_empty("Owner", owner_name)
        can_upload &= InputConstraints.assert_string_non_empty("Date created", date_created)
        can_upload &= InputConstraints.assert_string_from_set("Access permissions", access_permissions,
                                                              Constants.PERMISSION_LEVELS.keys())
        can_upload &= InputConstraints.assert_int_positive("Frames per second", frames_per_second)

        # Uploads to the server if the input constraints are satisfied
        if can_upload is True:
            Log.info("Uploading the dataset '" + name + "' to the server: " + ClientConnection.get_server_address())

            assert self.data_recorder is not None
            assert self.data_recorder.is_successful()

            # Uploads the dataset to the server
            access_perm_level = Constants.PERMISSION_LEVELS.get(access_permissions)
            result = ClientConnection.upload_dataset(name, owner_name, date_created, access_perm_level,
                                                     frames_per_second)

            if result is True:
                tkinter.messagebox.showinfo("Upload: Success!",
                                            "The dataset '" + name + "' was successfully uploaded to the server.")
                Log.info("Successfully uploaded the dataset named '" + name + "'.")
                self.data_recorder.use_recording()
            else:
                tkinter.messagebox.showwarning("Upload: Failed!", "The dataset failed to upload to the server.\n"
                                                                  "Does a dataset with the same name already exist?")
                Log.warning("Was not able to upload the dataset named '" + name + "'.")

        else:
            InputConstraints.warn("The dataset was not uploaded to the server. Input constraints were not satisfied.")

    def set_switch_to_view_frame(self, command):
        self.cancel_new_dataset.config(command=command)

    def reconfigure_hand_angler(self):
        video_source = self.cam_control_frame.get_value("Video source")
        width = self.cam_control_frame.get_value("Width")
        height = self.cam_control_frame.get_value("Height")
        zoom_percent = self.cam_control_frame.get_value("Zoom %")
        frames_per_second = self.cam_control_frame.get_value("Frames per second")

        # Checks if the reset is allowed
        reconfigure = True
        reconfigure &= InputConstraints.assert_int_non_negative("Video source", video_source)
        reconfigure &= InputConstraints.assert_int_positive("Width", width)
        reconfigure &= InputConstraints.assert_int_positive("Height", height)
        reconfigure &= InputConstraints.assert_int_positive("Zoom %", zoom_percent)
        reconfigure &= InputConstraints.assert_int_positive("Frames per second", frames_per_second)

        # Performs reset if allowed
        if reconfigure is True:
            self.hand_angler.set_configurations(
                video_source=int(video_source), width=int(width), height=int(height), zoom=int(zoom_percent),
                frames_per_second=int(frames_per_second))

    def start_dataset_recording(self):
        # Retrieves the data
        init_sleep_seconds = self.data_rec_info_frame.input_frame.get_value("Sensor zeroing delay (seconds)")
        training_length_seconds = self.data_rec_info_frame.input_frame.get_value("Training length (seconds)")
        frames_per_second = self.data_rec_info_frame.input_frame.get_value("Frames per second")

        # Assert the training constrains
        begin_training = True
        begin_training &= InputConstraints.assert_int_range_inclusive("Sensor zeroing delay (seconds)",
                                                                      init_sleep_seconds, 5, 60)
        begin_training &= InputConstraints.assert_int_positive("Training length (seconds)", training_length_seconds)
        begin_training &= InputConstraints.assert_int_positive("Frames per second", frames_per_second)

        if (begin_training is True) and (self.data_recorder is None or self.data_recorder.is_running() is False):
            # Sets up the sensor lost
            if self.sensor_listener is None:
                try:
                    self.sensor_listener = SensorListener.SensorReadingsListener()
                    self.sensor_listener.start_running()
                    self.sensor_listener.start()
                except:
                    self.sensor_listener = None
                    InputConstraints.warn(
                        "Warning, was not able to establish communications with COM3 port.\n" +
                        "Please ensure that the sensor reading device is connected.")

            if self.sensor_listener is not None:
                # Starts the data processing
                self.data_recorder = DatasetRecorder.Recorder(sensor_listener=self.sensor_listener,
                                                              hand_angler=self.hand_angler,
                                                              init_sleep_seconds=int(init_sleep_seconds),
                                                              training_length_seconds=int(training_length_seconds),
                                                              frames_per_second=int(frames_per_second),
                                                              progress_bar=self.data_rec_info_frame.progress_bar)
                self.data_recorder.start()

    def stop_dataset_recording(self):
        self.data_rec_info_frame.progress_bar.reset()

        if (self.sensor_listener is None) or (self.data_recorder is None) or (self.data_recorder.is_running() is False):
            InputConstraints.warn("The dataset recording process is not running.")
        else:
            if self.data_recorder is not None:
                self.data_recorder.stop()
            self.sensor_listener.stop_reading()

    def start_new_frame_processes(self):
        # Starts watching hand angler
        assert self.data_rec_info_frame.hand_angler is not None
        self.hand_angler.start_watching()

        if self.sensor_listener is not None:
            self.sensor_listener.start_reading()

    def stop_new_frame_processes(self):
        # Stop hand angler
        self.hand_angler.stop_watching()

        if self.sensor_listener is not None:
            self.sensor_listener.stop_reading()
