import tkinter, tkinter.messagebox

from scripts import Constants, Warnings, General, Parameters, InputConstraints, Log
from scripts.frontend import ClientConnection
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.CustomButtons import SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock
from scripts.frontend.pages import GenericPage


class Frame(GenericPage.Frame):

    def __init__(self, root, column, row, search_values, default_search_value=None,
                 multi_select=False, sort_columnspan=2, select_change_command=None,
                 columnspan=1, rowspan=1,
                 title=None):
        GenericPage.Frame.__init__(self, root)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(sticky=tkinter.NSEW)

        # Configure weights
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Title
        self.title_label = None
        if title is not None:
            self.title_label = CustomLabels.TitleLabel(self, column=0, row=0, text=title)
            self.title_label.grid(padx=Constants.STANDARD_SPACING)

        # Scroll block
        self.scroll_block = ScrollBlock.Frame(self, multi_select=multi_select,
                                              select_change_command=select_change_command)
        self.scroll_block.grid(column=0, row=2)
        self.scroll_block.grid(columnspan=1, rowspan=1)

        # Buttons frame
        self.button_frame = GenericPage.Frame(self,
                                              column=0, row=1,
                                              columnspan=1, rowspan=1)
        self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

        # Configure button frame weights
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)
        for x in range(0, sort_columnspan):
            self.button_frame.columnconfigure(x, weight=1)

        # Search buttons & widgets
        self.search_button = SearchButton(
            self.button_frame, column=sort_columnspan - 1, row=0, text="Search", command=self.search_button_command)

        # Sorting
        self.button_search_frame = tkinter.Frame(self.button_frame)
        self.button_search_frame.grid(column=0, row=1, columnspan=sort_columnspan, sticky=tkinter.NSEW)
        self.button_search_frame.columnconfigure(1, weight=1)

        self.sort_label = SearchLabel(self.button_search_frame, column=0, row=0, text="Sort by:")
        self.sort_option_menu = SortOptionMenu(self.button_search_frame,
                                               column=1, row=0,
                                               values=search_values, value=default_search_value)
        self.sort_option_menu.grid(sticky=tkinter.NSEW)

        self.sort_direction_option_menu = SortOptionMenu(self.button_search_frame,
                                                         column=2, row=0,
                                                         values=Constants.SORT_DIRECTION.keys(),
                                                         value=list(Constants.SORT_DIRECTION.keys())[0])
        # Storage
        self.list_storage = []

    def update_colour(self):
        super().update_colour()
        if self.title_label is not None:
            self.title_label.update_colour()
        self.scroll_block.update_colour()
        self.button_frame.update_colour()
        self.search_button.update_colour()

        self.sort_label.update_colour()
        self.sort_option_menu.update_colour()
        self.sort_direction_option_menu.update_colour()

        self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
        self.button_search_frame.config(bg=self.button_frame.cget("bg"))
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

    def update_content(self):
        super().update_content()
        if self.title_label is not None:
            self.title_label.update_content()
        self.scroll_block.update_content()
        self.button_frame.update_content()
        self.search_button.update_content()

        self.sort_label.update_content()
        self.sort_option_menu.update_content()
        self.sort_direction_option_menu.update_content()

    def search_button_command(self):
        Warnings.not_overridden()

    def get_index_data(self, index):
        return self.list_storage[index]

    def get_index_entry(self, index, entry):
        Warnings.not_overridden()

    def get_selected_main_id(self):
        assert 0 == Constants.DATASET_ENTRY_TRANSFER_DATA.index("ID") and \
               0 == Constants.MODEL_ENTRY_TRANSFER_DATA.index("ID")
        if len(self.list_storage) <= 0:
            return None
        else:
            return self.list_storage[self.scroll_block.get_selected_main()][0]

    def get_selected_main_data(self):
        return self.get_index_data(self.scroll_block.get_selected_main())


class DatasetSearchFrame(Frame):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, title=None, multi_select=False,
                 sort_columnspan=2, select_change_command=None, search_frame_command=None):
        Frame.__init__(self, root=root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       search_values=Constants.DATABASES_SORT_BY_OPTIONS.keys(),
                       default_search_value=list(Constants.DATABASES_SORT_BY_OPTIONS.keys())[0],
                       title=title, multi_select=multi_select, sort_columnspan=sort_columnspan,
                       select_change_command=select_change_command)
        self.search_frame_command = search_frame_command

    def update_colour(self):
        super().update_colour()

    def update_content(self):
        super().update_content()

    def search_button_command(self):
        if ClientConnection.is_logged_in() is True:
            sort_by = Constants.DATABASES_SORT_BY_OPTIONS.get(self.sort_option_menu.get())

            # Obtains the information
            user_id = ClientConnection.get_user_id()
            if user_id is None:
                user_id = "NULL"
            self.list_storage = ClientConnection.fetch_ordered_datasets(
                sort_by=sort_by,
                direction=Constants.SORT_DIRECTION.get(self.sort_direction_option_menu.get()),
                user_id=user_id)

            # Replaces the list
            replace_list = []
            replace_list_sorted = []
            if self.list_storage is not None:
                for item in self.list_storage:
                    replace_list.append(" " + str(item[Constants.DATASET_ENTRY_TRANSFER_DATA.index("Name")]))
                    replace_list_sorted.append(" " + str(item[Constants.DATASET_ENTRY_TRANSFER_DATA.index(sort_by)]))

            self.scroll_block.replace_list(replace_list, replace_list_sorted)
            if self.search_frame_command is not None:
                self.search_frame_command()
        else:
            tkinter.messagebox.showwarning("Warning!", "The registered server is currently unavailable.")

    def merge_selected_datasets(self):
        assert self.scroll_block.multi_select is True

        # Obtains the dataset ids to merge
        dataset_indices = self.scroll_block.get_selected_multi()
        dataset_ids = []
        for i in dataset_indices:
            dataset_ids.append(self.list_storage[i][Constants.DATASET_ENTRY_TRANSFER_DATA.index("ID")])

        # Performs the merging if datasets are selected
        if len(dataset_ids) > 0:
            Log.debug("Selected datasets to merge: " + str(dataset_ids))

            are_all_raw = True
            for i in dataset_indices:
                are_all_raw &= self.list_storage[i][Constants.DATASET_ENTRY_TRANSFER_DATA.index("Is_Raw")] == 1

            if are_all_raw is True:

                # Asserting that the fps of each dataset is the same
                are_all_fps_same = True
                cur_fps = None
                for i in dataset_indices:
                    if cur_fps is None:
                        cur_fps = self.list_storage[i][Constants.DATASET_ENTRY_TRANSFER_DATA.index("FPS")]
                    are_all_fps_same &= \
                        (cur_fps == self.list_storage[i][Constants.DATASET_ENTRY_TRANSFER_DATA.index("FPS")])

                if are_all_fps_same is True:
                    # Merging the datasets
                    Log.info("Merging the datasets: " + str(dataset_ids))

                    # Generates the merged dataset name
                    dataset_name = "Merged-"
                    for i in dataset_ids:
                        dataset_name += str(i) + ","
                    dataset_name = dataset_name.rstrip(",")

                    # Computes average rating of the datasets
                    rating = 0
                    for i in dataset_indices:
                        rating += self.list_storage[i][Constants.DATASET_ENTRY_TRANSFER_DATA.index("Rating")]
                    rating = int(rating / len(dataset_ids))

                    # Computes to number of combined frames
                    num_frames = 0
                    for i in dataset_indices:
                        num_frames += self.list_storage[i][Constants.DATASET_ENTRY_TRANSFER_DATA.index("Num_Frames")]

                    # Sends the request
                    result = ClientConnection.merge_datasets(dataset_ids=dataset_ids, dataset_name=dataset_name,
                                                             dataset_owner_id=ClientConnection.get_user_id(),
                                                             dataset_rating=rating,
                                                             dataset_num_frames=num_frames, dataset_fps=cur_fps)
                    if result is True:
                        tkinter.messagebox.showwarning("Success!", "The datasets have been merged.")
                        return True
                    else:
                        tkinter.messagebox.showwarning("Failed!", "The datasets failed to merge.")
                        return False
                else:
                    tkinter.messagebox.showwarning("Failed!",
                                                   "All selected datasets must have the same 'Frames per second'.")
                    return False
            else:
                tkinter.messagebox.showwarning("Failed!", "All selected datasets must be raw (not smoothed).")
                return False
        else:
            tkinter.messagebox.showwarning("Failed!", "No dataset is selected.")
            return False

    def get_index_entry(self, index, entry):
        return self.list_storage[index][Constants.DATASET_ENTRY_TRANSFER_DATA.index(entry)]


class ModelSearchFrame(Frame):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, title=None, multi_select=False,
                 sort_columnspan=2, select_change_command=None):
        Frame.__init__(self, root=root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       search_values=Constants.MODELS_SORT_BY_OPTIONS.keys(),
                       default_search_value=list(Constants.MODELS_SORT_BY_OPTIONS.keys())[0],
                       title=title, multi_select=multi_select, sort_columnspan=sort_columnspan,
                       select_change_command=select_change_command)

    def update_colour(self):
        super().update_colour()

    def update_content(self):
        super().update_content()

    def search_button_command(self):
        if ClientConnection.is_server_online() is True:
            sort_by = Constants.MODELS_SORT_BY_OPTIONS.get(self.sort_option_menu.get())

            # Obtains the information
            user_id = ClientConnection.get_user_id()
            if user_id is None:
                user_id = "NULL"
            self.list_storage = ClientConnection.fetch_ordered_models(
                sort_by=Constants.MODELS_SORT_BY_OPTIONS.get(self.sort_option_menu.get()),
                direction=Constants.SORT_DIRECTION.get(self.sort_direction_option_menu.get()),
                user_id=user_id)

            # Replaces the list
            replace_list = []
            replace_list_sorted = []
            if self.list_storage is not None:
                for item in self.list_storage:
                    replace_list.append(" " + str(item[Constants.MODEL_ENTRY_TRANSFER_DATA.index("Name")]))
                    replace_list_sorted.append(" " + str(item[Constants.MODEL_ENTRY_TRANSFER_DATA.index(sort_by)]))

            self.scroll_block.replace_list(replace_list, replace_list_sorted)
        else:
            tkinter.messagebox.showwarning("Warning!", "The registered server is currently unavailable.")

    def get_index_entry(self, index, entry):
        return self.list_storage[index][Constants.MODEL_ENTRY_TRANSFER_DATA.index(entry)]



