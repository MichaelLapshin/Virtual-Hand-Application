import tkinter
import tkinter.colorchooser

from scripts import General
from scripts.frontend import Navigation, Constants
from scripts.frontend.custom_widgets import CustomButtons, CustomScales, CustomLabels
from scripts.frontend.pages import GenericPage

class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, navig_bar, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_SETTINGS)
        self.root = root
        self.navig_bar = navig_bar
        self.columnconfigure(0, weight=1)

        # Create settings title
        self.settings_title = CustomLabels.TitleLabel(root=self, column=0, row=0, text="Settings")

        # Create settings frame
        self.settings_frame = GenericPage.Frame(self, column=0, row=1)
        self.settings_frame.config(bd=2)
        self.settings_frame.config(padx=Constants.LONG_SPACING, pady=Constants.LONG_SPACING)
        self.settings_frame.grid(sticky=tkinter.N)
        self.settings_frame.grid(padx=Constants.LONG_SPACING, pady=Constants.LONG_SPACING)

        # Scaling Setting
        self.scale_variable = tkinter.DoubleVar()
        self.scale_slider = CustomScales.SettingsScale(self.settings_frame, label="Graphical User Interface Scale",
                                                       column=0, row=0, columnspan=2,
                                                       from_=0.5, to=5.0,
                                                       resolution=0.1, variable=self.scale_variable)

        # GUI update delay
        self.delay_variable = tkinter.DoubleVar()
        self.delay_slider = CustomScales.SettingsScale(self.settings_frame, label="Update Delay (in milliseconds)",
                                                       column=0, row=1, columnspan=2,
                                                       from_=10, to=10000,
                                                       resolution=10, variable=self.delay_variable)

        # Alpha Colour
        self.alpha_colour_variable = None
        self.alpha_colour_chooser = CustomButtons.SettingsButton(
            self.settings_frame, column=0, row=2, text="Select Alpha Colour", command=lambda: self.get_new_alpha_colour())

        # Bravo Colour
        self.bravo_colour_variable = None
        self.bravo_colour_chooser = CustomButtons.SettingsButton(
            self.settings_frame, column=1, row=2, text="Select Bravo Colour", command=lambda: self.get_new_bravo_colour())

        # Update/Save buttons
        self.save_settings_button = CustomButtons.InformationButton(
            self.settings_frame,
            column=0, row=3,
            command=self.save_to_constants_file, text="Save All Settings")
        self.update_settings_button = CustomButtons.InformationButton(
            self.settings_frame,
            column=1, row=3,
            command=self.update_program_constants, text="Update All Settings")

        # Update Program Settings
        self.update_program_constants()

    # General Methods
    def save_to_constants_file(self):
        Constants.clear_file_constants()

        # Add GUI variables
        Constants.add_file_constant("GUI_Scale = " + str(self.scale_variable.get()))
        Constants.add_file_constant("UPDATE_DELAY_MS = " + str(self.delay_variable.get()))

        # Add Colours
        Constants.add_file_constant("COLOUR_ALPHA = " + str(self.alpha_colour_variable))
        Constants.add_file_constant("COLOUR_BRAVO = " + str(self.bravo_colour_variable))

    def update_program_constants(self):
        # Write to the constants program file
        Constants.process_file_constants()

        # Updating Settings variables
        self.scale_variable.set(Constants.GUI_Scale)
        self.delay_variable.set(Constants.UPDATE_DELAY_MS)

        self.alpha_colour_variable = Constants.COLOUR_ALPHA
        self.bravo_colour_variable = Constants.COLOUR_BRAVO

        # Updates the program configurations
        # self.root.tk.call('tk', 'scaling', Constants.GUI_Scale)
        self.navig_bar.update_all_page_colour()
        self.update_colour()

    def update_content(self):
        super().update_content()

    def update_colour(self):
        super().update_colour()
        # Update page colours
        self.settings_title.update_colour()
        self.save_settings_button.update_colour()
        self.update_settings_button.update_colour()

        self.scale_slider.update_colour()
        self.delay_slider.update_colour()

        # Update colour button colours
        self.update_colour_button_colour()
        self.settings_frame.config(bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_B))

    def destroy(self):
        super().destroy()

    # Settings custom methods
    def get_new_alpha_colour(self):
        temp_colour = tkinter.colorchooser.askcolor(self.alpha_colour_variable)[0]
        if temp_colour is not None:
            self.alpha_colour_variable = temp_colour
        self.update_colour_button_colour()

    def get_new_bravo_colour(self):
        temp_colour = tkinter.colorchooser.askcolor(self.bravo_colour_variable)[0]
        if temp_colour is not None:
            self.bravo_colour_variable = temp_colour
        self.update_colour_button_colour()

    def update_colour_button_colour(self):
        self.alpha_colour_chooser.config(bg=General.washed_colour_hex(self.alpha_colour_variable, 1.0))
        self.bravo_colour_chooser.config(bg=General.washed_colour_hex(self.bravo_colour_variable, 1.0))

