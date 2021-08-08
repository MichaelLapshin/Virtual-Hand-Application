import tkinter
import tkinter.colorchooser

from scripts import General, Parameters, Constants
from scripts.frontend import Navigation
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
        self.scale_slider = CustomScales.SettingsScale(self.settings_frame, label="Graphical User Interface Scale (requires a restart)",
                                                       column=0, row=0, columnspan=6,
                                                       from_=0.5, to=5.0,
                                                       resolution=0.1, variable=self.scale_variable)

        # GUI update delay
        self.delay_variable = tkinter.DoubleVar()
        self.delay_slider = CustomScales.SettingsScale(self.settings_frame, label="Update Delay (in milliseconds)",
                                                       column=0, row=1, columnspan=6,
                                                       from_=10, to=10000,
                                                       resolution=10, variable=self.delay_variable)

        # Alpha Colour
        self.alpha_colour_variable = None
        self.alpha_colour_chooser = CustomButtons.SettingsButton(
            self.settings_frame,
            column=0, row=2,
            columnspan=3,
            text="Select Alpha Colour", command=lambda: self.get_new_alpha_colour())

        # Bravo Colour
        self.bravo_colour_variable = None
        self.bravo_colour_chooser = CustomButtons.SettingsButton(
            self.settings_frame,
            column=3, row=2,
            columnspan=3,
            text="Select Bravo Colour", command=lambda: self.get_new_bravo_colour())

        # Update/Save buttons
        self.save_settings_button = CustomButtons.InformationButton(
            self.settings_frame,
            column=0, row=3,
            columnspan=2,
            command=self.save_to_constants_file, text="Save All Settings")
        self.update_settings_button = CustomButtons.InformationButton(
            self.settings_frame,
            column=2, row=3,
            columnspan=2,
            command=self.update_program_constants, text="Update All Settings")
        self.default_settings_button = CustomButtons.InformationButton(
            self.settings_frame,
            column=4, row=3,
            columnspan=2,
            command=self.reset_all_settings, text="Reset All Settings\n"
                                                  "(requires a restart)")

        # Update Program Settings
        self.update_program_constants()

    # General Methods
    def save_to_constants_file(self):
        Parameters.clear_file_parameters()

        # Add GUI variables
        Parameters.add_file_parameters("GUI_Scale = " + str(self.scale_variable.get()))
        Parameters.add_file_parameters("UPDATE_DELAY_MS = " + str(self.delay_variable.get()))

        # Add Colours
        Parameters.add_file_parameters("COLOUR_ALPHA = " + str(self.alpha_colour_variable))
        Parameters.add_file_parameters("COLOUR_BRAVO = " + str(self.bravo_colour_variable))

    def update_program_constants(self):
        # Write to the constants program file
        Parameters.process_file_parameters()

        # Updating Settings variables
        self.scale_variable.set(Parameters.GUI_Scale)
        self.delay_variable.set(Parameters.UPDATE_DELAY_MS)

        self.alpha_colour_variable = Parameters.COLOUR_ALPHA
        self.bravo_colour_variable = Parameters.COLOUR_BRAVO

        # Updates the program configurations
        # self.root.tk.call('tk', 'scaling', Constants.GUI_Scale)
        self.navig_bar.update_all_page_colour()
        self.update_colour()

    def reset_all_settings(self):
        Parameters.clear_file_parameters()

    def update_content(self):
        super().update_content()

    def update_colour(self):
        super().update_colour()
        # Update page colours
        self.settings_title.update_colour()
        self.save_settings_button.update_colour()
        self.update_settings_button.update_colour()
        self.default_settings_button.update_colour()

        self.scale_slider.update_colour()
        self.delay_slider.update_colour()

        # Update colour button colours
        self.update_colour_button_colour()
        self.settings_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

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
