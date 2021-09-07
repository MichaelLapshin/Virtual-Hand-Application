import tkinter

from scripts import General, Parameters, Constants

from scripts.frontend.custom_widgets.CustomButtons import NavigationButton

# Navigation constants
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

TITLE_MODELS = "Models"
TITLE_DATASETS = "Datasets"
TITLE_TRAINING_PROCESSES = "Training Processes"
TITLE_MODEL_PROCESSES = "Model Processes"
TITLE_HOW_TO = "How to"
TITLE_PROJECT_INFORMATION = "Project Information"
TITLE_ACCOUNT = "Account"
TITLE_SETTINGS = "Settings"

# Singleton variable
navig_bar = None


class NavigationBar(tkinter.Frame, WidgetInterface):

    def __init__(self, root, column, row, columnspan=1, rowspan=1):
        tkinter.Frame.__init__(self, root)

        # Navigation variables
        self.current_page = None
        self.buttons_page_map = {}

        """
            Navigation Bar configurations
        """
        self.config(bd=1, relief=tkinter.RIDGE)

        # Grid configurations
        self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

    def add_page(self, page):
        # Configures column eight
        self.columnconfigure(self.num_buttons(), weight=1)

        new_button = NavigationButton(
            self,
            column=self.num_buttons(), row=0,
            columnspan=1, rowspan=1,
            text=page.get_page_title(),
            command=lambda: self.select_new_page(page.get_page_title()))
        page.grid_remove()

        self.buttons_page_map[new_button] = page

    def select_new_page(self, new_page_name):
        # Asserts that the page exists
        assert new_page_name is not None

        # Replaces old page with the new
        new_page = None
        for p in self.buttons_page_map.values():
            if p.get_page_title() == new_page_name:
                new_page = p

        assert new_page is not None

        # Hides the old page, shows the new page
        if self.current_page is not None:
            self.current_page.grid_remove()
        new_page.grid()
        self.current_page = new_page

        # Updates button colour
        self.update_navig_buttons_colour()

        return self.current_page

    def update_navig_buttons_colour(self):
        # Sets button colours
        if self.current_page is not None:
            for b in self.buttons_page_map.keys():
                if b.cget("text") == self.current_page.get_page_title():
                    b.config(bg=NavigationButton.SELECTED_COLOUR)
                else:
                    b.config(bg=NavigationButton.UNSELECTED_COLOUR)

    def num_buttons(self):
        return len(self.buttons_page_map)

    def update_current_page_colour(self):
        self.current_page.update_colour()

    def update_all_page_colour(self):
        for page in self.buttons_page_map.values():
            page.update_colour()

        self.update_colour()

    def update_colour(self):
        super().update_colour()
        for button in self.buttons_page_map.keys():
            button.update_colour()

        self.update_navig_buttons_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))

    def update_content(self):
        super().update_content()
        """
            Updates current page (not the others)
        """
        self.current_page.update_content()

    def destroy(self):
        # Destroys navigation buttons
        for b in self.buttons_page_map.keys():
            self.buttons_page_map.get(b).destroy()
            b.destroy()

        # Destroys the frame
        super().destroy()
