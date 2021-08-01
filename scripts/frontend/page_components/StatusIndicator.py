from scripts import General
from scripts.frontend import Constants, Parameters
from scripts.frontend.custom_widgets import CustomLabels


class Label(CustomLabels.InformationLabel):
    _text_status = "Status: "
    _text_running = "Running"
    _text_stopped = "Stopped"

    def __init__(self, root, column, row, default_status=False):
        CustomLabels.InformationLabel.__init__(self, root=root, column=column, row=row)
        self._running = default_status

    def update_content(self):
        super().update_content()

        if self._running is True:
            self.config(text="Status: Running")
            self.config(bg=General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_D))
        else:
            self.config(text="Status: Stopped")
            self.config(bg=General.washed_colour_hex(Constants.COLOUR_RED, Parameters.ColourGrad_D))

    def update_colour(self):
        super().update_colour()

    def set_status(self, status):
        if status is True:
            self.set_running()
        else:
            self.set_stopped()

    def is_running(self):
        return self._running

    def set_running(self):
        self._running = True

    def set_stopped(self):
        self._running = False

