import tkinter

import cv2
from PIL import Image, ImageTk

from scripts import General, Warnings, InputConstraints
from scripts.frontend import Navigation, Constants, Parameters, User
from scripts.frontend.Logic import MediapipHandAngler
from scripts.frontend.custom_widgets import CustomButtons, CustomLabels, CustomOptionMenu, CustomCanvas
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import \
    InformationBlock, ScrollBlock, PredictionPreviewBlock, DatasetGraphBlock, InfoInputBlock, ProgressBar
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

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
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
            self.record_options = ["Recording delay (seconds)", "Training length (seconds)", "Frames per second"]
            self.input_frame = InfoInputBlock.Frame(self, column=0, row=0,
                                                    options=self.record_options,
                                                    title="Data Recording Information")

            # Input frame
            self.input_frame.set_entry_value("Frames per second", Constants.CAMERA_DEFAULT_FRAMES_PER_SECOND)

            # Main frames
            self.process_frame = GenericPage.Frame(self, column=1, row=0)
            self.process_frame.columnconfigure(0, weight=1)
            self.process_frame.columnconfigure(1, weight=1)
            self.process_frame.rowconfigure(1, weight=1)
            self.process_frame.rowconfigure(2, weight=1)

            # Progress start/stop
            self.start_stop_title = CustomLabels.TitleLabel(self.process_frame,
                                                            column=0, row=0, columnspan=2,
                                                            text="Data Recording Control Panel")
            self.start_progress_button = CustomButtons.InformationButton(self.process_frame,
                                                                         column=0, row=1, text="Start Data Gathering")
            self.stop_progress_button = CustomButtons.InformationButton(self.process_frame,
                                                                        column=1, row=1, text="Stop Data Gathering")
            self.progress_bar = ProgressBar.Frame(self.process_frame, column=0, row=2, columnspan=2,
                                                  metric_text=" seconds", max_count=100)

            # Progress start/stop configuration
            self.start_stop_title.grid(padx=Constants.STANDARD_SPACING)
            self.start_progress_button.grid(sticky=tkinter.EW, padx=Constants.LONG_SPACING)
            self.stop_progress_button.grid(sticky=tkinter.EW, padx=Constants.LONG_SPACING)

            # Camera + default parameters
            self.hand_angler = None
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
            self.stop_progress_button.update_content()

            # Paint the camera
            if (self.hand_angler is not None) and (self.hand_angler.get_image() is not None):
                image = Image.fromarray(self.hand_angler.get_image())

                # Resize image
                ratio = self.camera_frame.winfo_width() / float(image.width)
                if int(ratio * image.height) > self.winfo_height():
                    ratio = self.camera_frame.winfo_height() / float(image.height)
                    image = image.resize((int(ratio * image.width), int(ratio * image.height)))
                else:
                    image = image.resize((int(ratio * image.width), int(ratio * image.height)))

                # Apply image
                imageTk = ImageTk.PhotoImage(image=image)
                self.camera_label.config(image=imageTk)
                self.camera_label.image = imageTk

        def restart_hand_angler(self, width=None, height=None, zoom_percent=None):
            # Checks if the reset is allowed
            can_reset = True
            can_reset &= InputConstraints.assert_int_positive("Width", int(width))
            can_reset &= InputConstraints.assert_int_positive("Height", int(height))
            can_reset &= InputConstraints.assert_int_positive("Zoom %", int(zoom_percent))
            can_reset &= InputConstraints.assert_int_positive("Frames per second",
                                                              int(self.input_frame.get_value("Frames per second")))

            # Performs reset if allowed
            if can_reset is True:
                if (self.hand_angler is not None) and self.hand_angler.is_running():
                    self.hand_angler.stop()

                self.hand_angler = MediapipHandAngler.HandAngleReader(
                    width=int(width), height=int(height), zoom=int(zoom_percent),
                    frames_per_second=int(self.input_frame.get_value("Frames per second")))
                self.hand_angler.start()

            Warnings.not_complete()  # TODO, remove this soon

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
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=3)

        # Cancel Button
        self.cancel_new_dataset = CustomButtons.SearchButton(self, column=0, row=0, text="View Datasets")

        # Frames
        self.general_options = ["Name", "Owner", "Date created", "Access Permissions"]
        self.general_info_frame = InfoInputBlock.Frame(self,
                                                       column=0, row=1,
                                                       options=self.general_options,
                                                       title="General Information")
        self.general_info_frame.set_entry_value("Owner", User.get_name())
        self.general_info_frame.disable_entry("Owner")

        self.general_info_frame.set_entry_value("Date created", General.get_current_slashed_date())
        self.general_info_frame.disable_entry("Date created")

        self.general_info_frame.set_perm_option_menu("Access Permissions")

        # Data recording frame
        self.data_rec_info_frame = NewFrame.DataRecInfoFrame(self, column=1, row=0, rowspan=3)

        # Cam Control Info
        self.cam_control_options = ["Width", "Height", "Zoom %"]  # TODO, rename 'Zoom %' since it might be a percentage
        self.cam_control_frame = InfoInputBlock.Frame(self,
                                                      column=0, row=2,
                                                      options=self.cam_control_options,
                                                      title="Camera Control")
        self.apply_cam_settings = CustomButtons.SearchButton(self.cam_control_frame,
                                                             column=0, row=4, columnspan=2,
                                                             command=self.restart_hand_angler,
                                                             text="Apply Camera Settings")
        # Give default camera settings variables
        self.cam_control_frame.set_entry_value("Width", Constants.CAMERA_DEFAULT_RESOLUTION_X)
        self.cam_control_frame.set_entry_value("Height", Constants.CAMERA_DEFAULT_RESOLUTION_Y)
        self.cam_control_frame.set_entry_value("Zoom %", Constants.CAMERA_DEFAULT_ZOOM_PERCENT)

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
        self.cam_control_frame.update_colour()
        self.data_rec_info_frame.update_colour()
        self.apply_cam_settings.update_colour()

    def update_content(self):
        super().update_content()
        self.general_info_frame.update_content()
        self.cam_control_frame.update_content()
        self.data_rec_info_frame.update_content()
        self.cancel_new_dataset.update_content()
        self.apply_cam_settings.update_content()

    def set_switch_to_view_frame(self, command):
        self.cancel_new_dataset.config(command=command)

    def restart_hand_angler(self):
        self.data_rec_info_frame.restart_hand_angler(self.cam_control_frame.get_value("Width"),
                                                     self.cam_control_frame.get_value("Height"),
                                                     self.cam_control_frame.get_value("Zoom %"))

    def start_new_frame_processes(self):
        # Starts hand angler
        if self.data_rec_info_frame.hand_angler is None:
            self.restart_hand_angler()
        elif self.data_rec_info_frame.hand_angler.is_running() is False:
            self.data_rec_info_frame.hand_angler.start()
        else:
            Warnings.not_to_reach()

    def stop_new_frame_processes(self):
        # Stop hand angler
        self.data_rec_info_frame.stop_hand_angler()
