from scripts import Warnings, Log


class Job:
    """
        Job for storing long-lasting tasks
    """

    def __init__(self, title, info=None):
        Log.info("Created Job task with title '" + title + "'.")
        self._title = title
        self._progress_count = 0
        self._progress_max = 0
        self._info = info
        self._progress_message = ""

    def perform_task(self):
        Warnings.not_to_reach()

    """
        Setters 
    """

    def set_max_progress(self, count):
        self._progress_max = count

    def set_progress(self, count, message=None):
        Log.info("Setting the progress to: " + str(count) + " - " + message)
        if message is not None:
            self._progress_message = message
        self._progress_count = count

    def add_progress(self, count, message=None):
        if message is not None:
            self._progress_message = message
        self._progress_count += count

    """
        Getters
    """

    def get_title(self):
        return self._title

    def get_progress(self):
        return self._progress_count

    def get_max_progress(self):
        return self._progress_max

    def get_info(self):
        return self._info
