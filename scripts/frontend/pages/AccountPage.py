import tkinter

import requests

from scripts import General, Parameters, Constants, InputConstraints, Log, Warnings
from scripts.frontend import Navigation, ClientConnection
from scripts.frontend.custom_widgets import CustomLabels, CustomButtons, CustomEntries
from scripts.frontend.custom_widgets.CustomButtons import AccountButton
from scripts.frontend.custom_widgets.CustomEntries import AccountEntry
from scripts.frontend.custom_widgets.CustomLabels import AccountLabel
from scripts.frontend.page_components import InformationBlock
from scripts.frontend.pages import GenericPage

# Account constants
ENTRY_WIDTH = 16

STATUS_LOGGED_IN = "Status: Logged in"
STATUS_LOGGED_OUT = "Status: Logged out"
STATUS_FAILED_LOGIN = "Status: Log-in failed"
LOGIN_TEXT = "Log in"
LOGOUT_TEXT = "Log out"
CREATE_USER_TEXT = "Create user"
DELETE_USER_TEXT = "Delete user"

USERNAME_ENTRY = "Username:"
PASSWORD_ENTRY = "Password:"
VERIFY_PASSWORD_ENTRY = "Verify Password:"

# Server
STATUS_SERVER_UNKNOWN = "Server status: Unknown"
STATUS_SERVER_ONLINE = "Server status: Online"
STATUS_SERVER_OFFLINE = "Server status: Offline"
SERVER_IP_ENTRY = "IP Address:"
SERVER_PORT_ENTRY = "Port:"
CHECK_STATUS = "Check Status"
REGISTER_TEXT = "Register"

# User list
USER_LIST_TITLE = "User Names List"
USER_LIST_UPDATE_BUTTON = "Update User List"
USER_LIST_COLUMN_LABEL = "Number of Columns"
USER_LIS_COLUMN_NUM_DEFAULT = 5


class Frame(GenericPage.NavigationFrame):
    class LoginFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)

            # Create login frame
            self.config(bd=2)
            self.grid(sticky=tkinter.N)

            # Logged is as labels
            self.title = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=2, text="Log-in Management")
            self.title.grid(padx=Constants.STANDARD_SPACING)

            # Labels and Entries
            self.label_status = AccountLabel(
                self, text=STATUS_LOGGED_OUT,
                column=0, row=1,
                columnspan=2, rowspan=1)

            # Credentials entry field
            self.label_logged_as_username = AccountLabel(
                self, text=USERNAME_ENTRY,
                column=0, row=2,
                columnspan=1, rowspan=1)

            self.entry_username = AccountEntry(
                self,
                column=1, row=2,
                columnspan=1, rowspan=1,
                width=ENTRY_WIDTH, trace_command=self.login_button_enabling_update)

            self.label_logged_as_password = AccountLabel(
                self, text=PASSWORD_ENTRY,
                column=0, row=3,
                columnspan=1, rowspan=1)

            self.entry_password = AccountEntry(
                self,
                column=1, row=3,
                columnspan=1, rowspan=1,
                width=ENTRY_WIDTH, trace_command=self.login_button_enabling_update)

            # Log in button
            self.button_UserLogin = AccountButton(
                self, command=self.login_button_function,
                text=LOGIN_TEXT,
                column=0, row=4,
                columnspan=1, rowspan=1)

            # Log out button
            self.button_UserLogout = AccountButton(
                self, command=self.logout_button_function,
                text=LOGOUT_TEXT,
                column=1, row=4,
                columnspan=1, rowspan=1)

            self.login_button_enabling_update(reset_login=True)

        def logout_button_function(self):
            ClientConnection.log_out()
            self.login_button_enabling_update()

        def login_button_function(self):

            # Obtains the input
            user_name = self.entry_username.get()
            password = self.entry_password.get()

            # Input constraint assertion
            can_login = True
            can_login &= InputConstraints.assert_string_non_empty(USERNAME_ENTRY, user_name)
            can_login &= InputConstraints.assert_string_non_empty(PASSWORD_ENTRY, password)

            if can_login is True:
                ClientConnection.log_in(user_name=user_name, password=password)
                self.login_button_enabling_update()

                # Update the labels
                if ClientConnection.is_logged_in() is False:
                    self.label_status.config(text=STATUS_FAILED_LOGIN)
                    self.label_status.config(
                        bg=General.washed_colour_hex(Constants.COLOUR_RED, Parameters.ColourGrad_E))

        def login_button_enabling_update(self, reset_login=False, *args):
            if (reset_login is False) and (ClientConnection.is_logged_in() is True):
                # Disable/enable buttons
                self.entry_username.disable()
                self.entry_password.disable()
                self.button_UserLogin.disable()
                self.button_UserLogout.enable()

                # Update the labels
                self.label_status.config(text=STATUS_LOGGED_IN)
                self.label_status.config(bg=General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_E))

            else:
                # Disable/enable buttons
                self.entry_username.enable()
                self.entry_password.enable()
                self.button_UserLogin.enable()
                self.button_UserLogout.disable()

                # Update the labels
                self.label_status.config(text=STATUS_LOGGED_OUT)
                self.label_status.config(bg=General.washed_colour_hex(Constants.COLOUR_GREY, Parameters.ColourGrad_E))

        def update_colour(self):
            super().update_colour()
            self.title.update_colour()
            self.label_status.update_colour()
            self.label_logged_as_username.update_colour()
            self.entry_username.update_colour()
            self.label_logged_as_password.update_colour()
            self.entry_password.update_colour()
            self.button_UserLogin.update_colour()
            self.button_UserLogout.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def destroy(self):
            # Destroys login widgets
            self.entry_username.destroy()
            self.entry_password.destroy()
            self.button_UserLogin.destroy()
            self.button_UserLogout.destroy()

            super().destroy()

    class UserManagerFrame(GenericPage.Frame):
        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)

            # Create login frame
            self.config(bd=2)
            self.grid(sticky=tkinter.N)

            # Title
            self.title = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=2, text="Account Management")
            self.title.grid(padx=Constants.STANDARD_SPACING)

            # Credentials entry field
            self.label_logged_as_username = AccountLabel(
                self, text=USERNAME_ENTRY,
                column=0, row=2,
                columnspan=1, rowspan=1)

            self.entry_username = AccountEntry(
                self,
                column=1, row=2,
                columnspan=1, rowspan=1,
                width=ENTRY_WIDTH)

            self.label_logged_as_password = AccountLabel(
                self, text=PASSWORD_ENTRY,
                column=0, row=3,
                columnspan=1, rowspan=1)

            self.entry_password = AccountEntry(
                self,
                column=1, row=3,
                columnspan=1, rowspan=1,
                width=ENTRY_WIDTH)

            self.label_logged_as_verify_password = AccountLabel(
                self, text=VERIFY_PASSWORD_ENTRY,
                column=0, row=4,
                columnspan=1, rowspan=1)

            self.entry_verify_password = AccountEntry(
                self,
                column=1, row=4,
                columnspan=1, rowspan=1,
                width=ENTRY_WIDTH)

            # Edit account buttons
            self.create_user_button = AccountButton(
                self, command=self.create_user,
                text=CREATE_USER_TEXT,
                column=0, row=5,
                columnspan=1, rowspan=1)

            self.delete_user_button = AccountButton(
                self, command=self.delete_user,
                text=DELETE_USER_TEXT,
                column=1, row=5,
                columnspan=1, rowspan=1)

        def update_colour(self):
            super().update_colour()
            self.title.update_colour()
            self.label_logged_as_username.update_colour()
            self.entry_username.update_colour()
            self.label_logged_as_password.update_colour()
            self.entry_password.update_colour()
            self.label_logged_as_verify_password.update_colour()
            self.entry_verify_password.update_colour()
            self.create_user_button.update_colour()
            self.delete_user_button.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def destroy(self):
            # Destroys widgets

            super().destroy()

        def create_user(self):
            Log.info("Attempting to create a new user.")

            # Obtains inputs
            username = self.entry_username.get()
            password = self.entry_password.get()
            verify_password = self.entry_verify_password.get()

            if password == verify_password:

                # Assert user name
                can_create = True
                can_create &= InputConstraints.assert_string_non_empty("Username", username)
                can_create &= InputConstraints.assert_string_non_empty("Password", password)

                # logic for creating the user
                if can_create is True:
                    result = ClientConnection.create_user(user_name=username, password=password)

                    Warnings.not_complete()

                    if result is True:
                        Log.info("The user named '" + username + "' was created.")
                    else:
                        Log.info("The user named '" + username + "' was not created.")

                else:
                    InputConstraints.warn("Could not create the user. Input constraints were not met.")
            else:
                Log.info("Password and verify password do not match!")
                InputConstraints.warn("The password verification does not match the original.")

        def delete_user(self):
            Log.info("Attempting to delete a new user.")

            # Obtains inputs
            username = self.entry_username.get()
            password = self.entry_password.get()
            verify_password = self.entry_verify_password.get()

            if password == verify_password:
                # Assert user name
                can_delete = True
                can_delete &= InputConstraints.assert_string_non_empty("Username", username)
                can_delete &= InputConstraints.assert_string_non_empty("Password", password)

                # logic for creating the user
                if can_delete is True:

                    is_deleted = ClientConnection.delete_user(user_name=username, password=password)

                    Warnings.not_complete()

                    if is_deleted is True:
                        Log.info("The user named '" + username + "' was deleted.")
                    else:
                        Log.info("The user named '" + username + "' was not deleted.")
                else:
                    InputConstraints.warn("Could not delete the user. Input constraints were not met.")

            else:
                Log.info("Password and verify password do not match!")
                InputConstraints.warn("The password verification does not match the original.")

    class ServerManagerFrame(GenericPage.Frame):
        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)

            self.root = root

            # Create login frame
            self.config(bd=2)
            self.grid(sticky=tkinter.N)

            # Title
            self.title = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=6, text="Server Management")
            self.title.grid(padx=Constants.STANDARD_SPACING)

            # Labels and Entries
            self.label_status = AccountLabel(
                self, text=STATUS_SERVER_UNKNOWN,
                column=0, row=1,
                columnspan=2, rowspan=1)

            # Server information fields
            self.label_server_ip = AccountLabel(
                self, text=SERVER_IP_ENTRY,
                column=0, row=2,
                columnspan=1, rowspan=1)

            self.entry_server_ip = AccountEntry(
                self, text=Parameters.SERVER_IP_ADDRESS,
                column=1, row=2,
                columnspan=1, rowspan=1,
                width=ENTRY_WIDTH,
                trace_command=self.neutralize_server_status)
            self.entry_server_ip.config(validatecommand=self.neutralize_server_status)

            self.label_server_port = AccountLabel(
                self, text=SERVER_PORT_ENTRY,
                column=0, row=3,
                columnspan=1, rowspan=1)

            self.entry_server_port = AccountEntry(
                self, text=Parameters.SERVER_PORT,
                column=1, row=3,
                columnspan=1, rowspan=1,
                width=ENTRY_WIDTH,
                trace_command=self.neutralize_server_status)
            self.entry_server_port.config(validatecommand=self.neutralize_server_status)

            # Server registration buttons
            self.button_check_server_status = AccountButton(
                self, command=self.check_server_status,
                text=CHECK_STATUS,
                column=0, row=4,
                columnspan=1, rowspan=1)

            self.button_register_server = AccountButton(
                self, command=self.register_server,
                text=REGISTER_TEXT,
                column=1, row=4,
                columnspan=1, rowspan=1)

        def update_colour(self):
            super().update_colour()
            self.title.update_colour()
            self.label_status.update_colour()
            self.label_server_ip.update_colour()
            self.entry_server_ip.update_colour()
            self.label_server_port.update_colour()
            self.entry_server_port.update_colour()
            self.button_check_server_status.update_colour()
            self.button_register_server.update_colour()

        def update_content(self):
            super().update_content()
            self.title.update_content()
            self.label_status.update_content()
            self.label_server_ip.update_content()
            self.entry_server_ip.update_content()
            self.label_server_port.update_content()
            self.entry_server_port.update_content()
            self.button_check_server_status.update_content()
            self.button_register_server.update_content()

        def neutralize_server_status(self, *args):
            self.label_status.config(text=STATUS_SERVER_UNKNOWN)
            self.label_status.config(bg=General.washed_colour_hex(Constants.COLOUR_GREY, Parameters.ColourGrad_E))

        def check_server_status(self):
            # Obtains values
            ip_address = self.entry_server_ip.get()
            port = self.entry_server_port.get()

            result = ClientConnection.is_server_online(ip_address=ip_address, port=port)

            if result is True:
                self.label_status.config(text=STATUS_SERVER_ONLINE)
                self.label_status.config(bg=General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_E))
            else:
                self.label_status.config(text=STATUS_SERVER_OFFLINE)
                self.label_status.config(bg=General.washed_colour_hex(Constants.COLOUR_RED, Parameters.ColourGrad_E))

        def register_server(self):
            # Obtains values
            ip_address = self.entry_server_ip.get()
            port = self.entry_server_port.get()

            # Saves address to the file
            Parameters.add_file_parameters("SERVER_IP_ADDRESS = '" + ip_address + "'")
            Parameters.add_file_parameters("SERVER_PORT = '" + port + "'")

            # Overrides current values
            Parameters.SERVER_IP_ADDRESS = ip_address
            Parameters.SERVER_PORT = port

            # Logs out the user
            self.root.login_frame.logout_button_function()

    class UsersListFrame(GenericPage.Frame):
        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)

            # Create login frame
            self.config(bd=2)
            self.grid(sticky=tkinter.N)
            self.rowconfigure(0, weight=1)

            # Lists all users
            self.user_list = InformationBlock.Frame(self, column=0, row=0, columnspan=3,
                                                    num_columns=1, num_rows=1,
                                                    title=USER_LIST_TITLE)
            self.update_list_button = CustomButtons.AccountButton(self, column=0, row=1,
                                                                  text=USER_LIST_UPDATE_BUTTON,
                                                                  command=self.update_list)
            self.num_columns_label = CustomLabels.AccountLabel(self, column=1, row=1, text=USER_LIST_COLUMN_LABEL + ":")
            self.num_columns_entry = CustomEntries.AccountEntry(self, column=2, row=1,
                                                                width=ENTRY_WIDTH,
                                                                text=str(USER_LIS_COLUMN_NUM_DEFAULT))

        def update_colour(self):
            super().update_colour()
            self.user_list.set_frame_colour(Parameters.COLOUR_BRAVO)
            self.user_list.set_label_colour(Parameters.COLOUR_ALPHA)

            self.user_list.update_colour()
            self.update_list_button.update_colour()
            self.num_columns_label.update_colour()
            self.num_columns_entry.update_colour()

        def update_content(self):
            super().update_content()
            if self.user_list is not None:
                self.user_list.update_content()
            self.update_list_button.update_content()
            self.num_columns_label.update_content()
            self.num_columns_entry.update_content()

        def update_list(self):
            # Get the input
            num_columns = self.num_columns_entry.get()

            if InputConstraints.assert_int_positive(USER_LIST_COLUMN_LABEL, num_columns, 100) is True:
                self.user_list.destroy()
                self.user_list = InformationBlock.Frame(self, column=0, row=0, columnspan=3,
                                                        num_columns=int(num_columns), num_rows=1,
                                                        title=USER_LIST_TITLE)
                # Adds the users to the table
                user_names = ClientConnection.get_all_user_names()
                if user_names is not None:
                    col = 0
                    for name in user_names:
                        self.user_list.add_info(col, 0, name + "\n")

                        # Loops the name listing
                        col += 1
                        if col >= int(num_columns):
                            col = 0
                self.update_colour()

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_ACCOUNT)

        # Weight configurations
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Frames
        self.server_manager_frame = Frame.ServerManagerFrame(self, column=0, row=0)
        self.login_frame = Frame.LoginFrame(self, column=1, row=0)
        self.user_manager_frame = Frame.UserManagerFrame(self, column=2, row=0)
        self.user_list_frame = Frame.UsersListFrame(self, column=0, row=1, columnspan=3)

    def update_colour(self):
        super().update_colour()
        self.server_manager_frame.update_colour()
        self.login_frame.update_colour()
        self.user_manager_frame.update_colour()
        self.user_list_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.server_manager_frame.update_content()
        self.login_frame.update_content()
        self.user_manager_frame.update_content()
        self.user_list_frame.update_content()

    def destroy(self):
        self.server_manager_frame.destroy()
        self.login_frame.destroy()
        self.user_manager_frame.destroy()
        self.user_list_frame.destroy()
        super().destroy()
