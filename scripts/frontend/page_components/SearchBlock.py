import tkinter

from scripts import Constants, Warnings, General, Parameters, InputConstraints
from scripts.frontend import ClientConnection
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.CustomButtons import SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock
from scripts.frontend.pages import GenericPage


class Frame(GenericPage.Frame):

    def __init__(self, root, column, row, search_values, default_search_value=None,
                 multi_select=False, sort_columnspan=2,
                 columnspan=1, rowspan=1,
                 title=None):
        GenericPage.Frame.__init__(self, root)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(sticky=tkinter.NS)

        # Configure weights
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Title
        self.title_label = None
        if title is not None:
            self.title_label = CustomLabels.TitleLabel(self, column=0, row=0, text=title)
            self.title_label.grid(padx=Constants.STANDARD_SPACING)

        # Scroll block
        self.scroll_block = ScrollBlock.Frame(self, multi_select=multi_select)
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
        Warnings.not_to_reach()

    def get_index_data(self, index):
        return self.list_storage[index]

    def get_index_element(self, index, element):
        Warnings.not_to_reach()

    def get_selected_entry_id(self):
        assert 0 == Constants.DATABASE_ENTRY_TRANSFER_DATA.index("ID") and \
               0 == Constants.MODEL_ENTRY_TRANSFER_DATA.index("ID")
        if len(self.scroll_block.get_selected()) <= 0:
            return None
        else:
            return self.list_storage[self.scroll_block.get_selected()[0]][0]


class DatasetSearchFrame(Frame):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, title=None, multi_select=False, sort_columnspan=2):
        Frame.__init__(self, root=root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       search_values=Constants.DATABASES_SORT_BY_OPTIONS.keys(),
                       default_search_value=list(Constants.DATABASES_SORT_BY_OPTIONS.keys())[0],
                       title=title, multi_select=multi_select, sort_columnspan=sort_columnspan)

    def update_colour(self):
        super().update_colour()

    def update_content(self):
        super().update_content()

    def search_button_command(self):
        sort_by = Constants.DATABASES_SORT_BY_OPTIONS.get(self.sort_option_menu.get())

        # Obtains the information
        self.list_storage = ClientConnection.fetch_ordered_datasets(
            sort_by=sort_by,
            direction=Constants.SORT_DIRECTION.get(self.sort_direction_option_menu.get()),
            user_name=ClientConnection.get_user_name())

        # Replaces the list
        replace_list = []
        replace_list_sorted = []
        if self.list_storage is not None:
            for item in self.list_storage:
                replace_list.append(" " + str(item[Constants.DATABASE_ENTRY_TRANSFER_DATA.index("Name")]))
                replace_list_sorted.append(" " + str(item[Constants.DATABASE_ENTRY_TRANSFER_DATA.index(sort_by)]))

        self.scroll_block.replace_list(replace_list, replace_list_sorted)

    def get_index_element(self, index, element):
        return self.list_storage[index][Constants.DATABASE_ENTRY_TRANSFER_DATA.index(element)]


class ModelSearchFrame(Frame):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, title=None, multi_select=False, sort_columnspan=2):
        Frame.__init__(self, root=root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       search_values=Constants.MODELS_SORT_BY_OPTIONS.keys(),
                       default_search_value=list(Constants.MODELS_SORT_BY_OPTIONS.keys())[0],
                       title=title, multi_select=multi_select, sort_columnspan=sort_columnspan)

    def update_colour(self):
        super().update_colour()

    def update_content(self):
        super().update_content()

    def search_button_command(self):
        # Obtains the information
        self.list_storage = ClientConnection.fetch_ordered_models(
            sort_by=Constants.MODELS_SORT_BY_OPTIONS.get(self.sort_option_menu.get()),
            direction=Constants.SORT_DIRECTION.get(self.sort_direction_option_menu.get()),
            user_name=ClientConnection.get_user_name())
        self.scroll_block.replace_list(self.list_storage[::][2])

    def get_index_element(self, index, element):
        return self.list_storage[index][Constants.MODEL_ENTRY_TRANSFER_DATA.index(element)]
