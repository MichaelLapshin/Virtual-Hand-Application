import tkinter

from scripts.frontend import Navigation
from scripts import Parameters
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.page_components import InformationBlock
from scripts.frontend.pages import GenericPage


class Frame(GenericPage.NavigationFrame):
    TITLE = "Project Information"
    SUB_TITLE_FONT_SIZE = 12
    TEXT_FONT_SIZE = 9
    CREDITS_FONT_SIZE = 10

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_PROJECT_INFORMATION)
        self.columnconfigure(0, weight=1)

        # Create settings title
        self.settings_title = CustomLabels.TitleLabel(root=self, column=0, row=0, text="Project Information")

        # Credits
        self.credits = InformationBlock.Frame(self,
                                              column=0, row=1,
                                              num_columns=2, num_rows=1)
        self.credits.add_info(column=0, row=0, text="Author: Michael Lapshin\n\n"
                                                    "Project: On-going since November 2020")

        self.credits.add_info(column=1, row=0,
                              text="--- Ultimate Goal ---\n\n"
                                   "To create a hardware-software interface to accurately translate hand-produced\n"
                                   " forces into realistic, believable hand movements in a virtual environment.")
        self.credits.set_column_weight(1, weight=3)

        # Credits fonts
        self.credits.set_font(column=0, row=0, font_size=Frame.CREDITS_FONT_SIZE)
        self.credits.set_font(column=1, row=0, font_size=Frame.CREDITS_FONT_SIZE)

        # Creates the info block
        self.info_block = InformationBlock.Frame(self,
                                                 column=0, row=2,
                                                 num_columns=3, num_rows=6)
        self.info_block.set_column_weight(2, weight=2)

        # Main Components
        self.info_block.add_info(column=0, row=0, text="Main Components")
        self.info_block.set_font(column=0, row=0, font_size=Frame.SUB_TITLE_FONT_SIZE)
        self.info_block.add_info(column=0, row=1, text="Machine Learning Model")
        self.info_block.add_info(column=0, row=2, text="Physical Hand Environment")
        self.info_block.add_info(column=0, row=3, text="Virtual Hand Environment")
        self.info_block.add_info(column=0, row=4, text="Back-end - Application")
        self.info_block.add_info(column=0, row=5, text="Front-end - Application")

        for i in range(1, 6):
            # self.info_block.set_justify(column=0, row=i, justify=tkinter.LEFT)
            # self.info_block.set_anchor(column=0, row=i, anchor=tkinter.W)
            self.info_block.set_font(column=0, row=i, font_size=Frame.TEXT_FONT_SIZE)

        # Sub-Components
        self.info_block.add_info(column=1, row=0, text="Sub-Components")
        self.info_block.set_font(column=1, row=0, font_size=Frame.SUB_TITLE_FONT_SIZE)
        self.info_block.add_info(column=1, row=1, text="Data post-processing\n"
                                                       "Machine learning model training")
        self.info_block.add_info(column=1, row=2, text="Data gathering software:\n"
                                                       " - Hardware sensor feed\n"
                                                       " - Camera feed\n"
                                                       "\n"
                                                       "Hardware + electronics:\n"
                                                       " - Arduino, amplifiers\n"
                                                       " - Load-cell sensors")
        self.info_block.add_info(column=1, row=3, text="TCP connection handling:\n"
                                                       " - C# client, Python client"
                                                       " - Python server\n\n"
                                                       "Unity")
        self.info_block.add_info(column=1, row=4, text="REST API Server connection handling\n"
                                                       "Database manipulation\n"
                                                       "Sub-process running")
        self.info_block.add_info(column=1, row=5, text="Graphical user interface\n"
                                                       "REST API Client connection handling\n"
                                                       "Real time model connection & processing")
        for i in range(1, 6):
            self.info_block.set_justify(column=1, row=i, justify=tkinter.LEFT)
            self.info_block.set_anchor(column=1, row=i, anchor=tkinter.W)
            self.info_block.set_font(column=1, row=i, font_size=Frame.TEXT_FONT_SIZE)

        # Key Skills & Technologies
        self.info_block.add_info(column=2, row=0, text="Key Skills & Technologies")
        self.info_block.set_font(column=2, row=0, font_size=Frame.SUB_TITLE_FONT_SIZE)
        self.info_block.add_info(column=2, row=1, text="Programming Languages:  Python 3.8\n"
                                                       "\n"
                                                       "Key skills and APIs:\n"
                                                       " - Tensorflow, sequential models\n"
                                                       " - Multithreading\n"
                                                       " - Matplotlib library")
        self.info_block.add_info(column=2, row=2,
                                 text="Programming Languages: Arduino (C++), Python 3.8\n"
                                      "\n"
                                      "Key Skills:                                            Key APIs:\n"
                                      " - Object-oriented programming                  - Matplotlib library\n"
                                      " - Communication port interfaces                - OpenCV (camera API)\n"
                                      " - Multithreading                                        - Mediapipe (hand tracking API)")
        self.info_block.add_info(column=2, row=3, text="Programming Languages: C# .NET, Python 3.8\n"
                                                       "\n"
                                                       "Key skills:                               Key APIs:\n"
                                                       " - TCP socket programming                  - Tensorflow\n"
                                                       " - Object-oriented programming             - Unity\n"
                                                       " - Multithreading                         ")
        self.info_block.add_info(column=2, row=4, text="Programming Languages: SQLite, Python 3.8\n"
                                                       "\n"
                                                       "Key skills and APIs:\n"
                                                       " - Python Flask, REST API\n"
                                                       " - Multithreading")
        self.info_block.add_info(column=2, row=5, text="Programming Languages: Python 3.8\n"
                                                       "\n"
                                                       "Key skills and APIs:\n"
                                                       " - Tkinter (GUI) library\n"
                                                       " - Python flask, REST API\n"
                                                       " - Object-oriented programming\n"
                                                       " - Multithreading")
        for i in range(1, 6):
            self.info_block.set_justify(column=2, row=i, justify=tkinter.LEFT)
            self.info_block.set_anchor(column=2, row=i, anchor=tkinter.W)
            self.info_block.set_font(column=2, row=i, font_size=Frame.TEXT_FONT_SIZE)

    def update_colour(self):
        super().update_colour()

        self.settings_title.update_colour()

        self.credits.set_frame_colour(Parameters.COLOUR_ALPHA)
        self.credits.set_label_colour(Parameters.COLOUR_BRAVO)
        self.credits.update_colour()

        self.info_block.set_frame_colour(Parameters.COLOUR_ALPHA)
        self.info_block.set_label_colour(Parameters.COLOUR_BRAVO)
        self.info_block.update_colour()

    def update_content(self):
        super().update_content()
        pass

    def destroy(self):
        super().destroy()
