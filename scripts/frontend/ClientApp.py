import tkinter
import threading
import time

from scripts import Parameters, Constants
from scripts.frontend.pages import \
    GenericPage, ModelsPage, DatasetsPage, TrainingProcessesPage, \
    ModelProcessesPage, HowToPage, ProjectInformationPage, AccountPage, SettingsPage

from scripts.frontend import Navigation
from scripts.logic import Worker

"""
    Process client app/connection constants
"""

# App constants
APP_TITLE = "Virtual-Hand"
APP_ICON = "images\\virtualhand_icons\\virtualhand_icon_YuG_1.ico"

# Process User Constants File
Parameters.optimize_file_parameters()
Parameters.process_file_parameters()

"""
    Client connection to the server
"""

# client_conn = ClientConnection()

"""
    Client-Side GUI
"""

# Created the window
root = tkinter.Tk()
root.title(APP_TITLE)
root.iconbitmap(default=APP_ICON)
root.geometry(Constants.default_resolution)
root.tk.call('tk', 'scaling', Parameters.GUI_Scale)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Template frame for the pages to use
frame_window = GenericPage.Frame(
    root=root,
    column=0, row=1,
    columnspan=1, rowspan=1)
frame_window.grid()

# Creates the navigation bar and links them to the page
Navigation.navig_bar = Navigation.NavigationBar(root, column=0, row=0, columnspan=1, rowspan=1)

# Instantiates singleton pages
ModelsPage.models_page = ModelsPage.Frame(root, base_frame=frame_window)
DatasetsPage.datasets_page = DatasetsPage.Frame(root, base_frame=frame_window)
TrainingProcessesPage.training_processes_page = TrainingProcessesPage.Frame(root, base_frame=frame_window)
ModelProcessesPage.model_processes_page = ModelProcessesPage.Frame(root, base_frame=frame_window)
HowToPage.how_to_page = HowToPage.Frame(root, base_frame=frame_window)
ProjectInformationPage.project_information_page = ProjectInformationPage.Frame(root, base_frame=frame_window)
AccountPage.account_page = AccountPage.Frame(root, base_frame=frame_window)
SettingsPage.settings_page = SettingsPage.Frame(root, base_frame=frame_window)

# Creates and adds the pages
Navigation.navig_bar.add_page(ModelsPage.models_page)
Navigation.navig_bar.add_page(DatasetsPage.datasets_page)
Navigation.navig_bar.add_page(TrainingProcessesPage.training_processes_page)
Navigation.navig_bar.add_page(ModelProcessesPage.model_processes_page)
Navigation.navig_bar.add_page(HowToPage.how_to_page)
Navigation.navig_bar.add_page(ProjectInformationPage.project_information_page)
Navigation.navig_bar.add_page(AccountPage.account_page)
Navigation.navig_bar.add_page(SettingsPage.settings_page)

# Destroys reference frame
frame_window.destroy()

# Starts at the Account page by default
Navigation.navig_bar.select_new_page(Navigation.TITLE_ACCOUNT)
Navigation.navig_bar.update_colour()
Navigation.navig_bar.update_all_page_colour()


class UpdateThread(threading.Thread):
    """
        Thread for updating the GUI
    """

    def __init__(self, navig_bar):
        threading.Thread.__init__(self)
        self.navig_bar = navig_bar
        self.running = True
        self.daemon = True

    def run(self):
        while self.running:
            self.navig_bar.update_content()
            time.sleep(Parameters.UPDATE_DELAY_MS / 1000.0)
        print("The update thread has stopped.")

    def stop(self):
        print("Stopping the update thread...")
        self.running = False


# Starting worker threads
Worker.worker = Worker.Worker(sleep_delay=0.1)
Worker.worker.start()
updater = UpdateThread(navig_bar=Navigation.navig_bar)
updater.start()

# Starts the GUI
root.mainloop()

# Ending worker threads
updater.stop()
Worker.worker.stop()

print("The client application has ended.")
