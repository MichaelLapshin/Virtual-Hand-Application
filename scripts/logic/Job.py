import threading
import time

from scripts import Warnings, Log, Constants

job_id = 0


def get_job_id():
    global job_id
    job_id += 1
    return job_id


class Job:
    """
        Job for storing long-lasting tasks
    """

    def __init__(self, title, info=None):
        Log.debug("Created Job task with title '" + title + "'.")
        self._id = get_job_id()
        self._title = title
        self._progress_count = 0
        self._progress_max = 0
        self._info = info
        self._progress_message = ""

    def perform_task(self):
        Warnings.not_overridden()

    """
        Setters 
    """

    def set_max_progress(self, count):
        self._progress_max = count

    def set_progress(self, count, message=None):
        Log.trace("Setting the progress to: " + str(count) + "/" + str(self._progress_max) + " - " + str(message))
        if message is not None:
            self._progress_message = message
        self._progress_count = count

    def complete_progress(self, message=None):
        Log.trace("Setting the progress to: " +
                  str(self._progress_max) + "/" + str(self._progress_max) + " - " + str(message))
        if message is not None:
            self._progress_message = message
        self._progress_count = self._progress_max

    def add_progress(self, count, message=None):
        if message is not None:
            self._progress_message = message
        self._progress_count += count
        Log.trace("Adding progress. Setting it to: " + str(self._progress_count) + "/" + str(self._progress_max)
                  + " - " + str(message))

    """
        Getters
    """

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_progress(self):
        return self._progress_count

    def get_max_progress(self):
        return self._progress_max

    def get_progress_message(self):
        return self._progress_message

    def get_info(self):
        return self._info


class SimultaneousJobs(Job):
    """
        A type of job container for executing multiple jobs on separate threads (at the same time)
    """

    class ThreadedJob(threading.Thread):
        def __init__(self, job):
            threading.Thread.__init__(self)
            self._job = job
            self._is_complete = False

        def run(self):
            self._job.perform_task()
            self._is_complete = True

        def get_job(self):
            return self._job

        def is_complete(self):
            return self._is_complete

    def __init__(self, jobs, title, progress_message=None, complete_message=None, info=None,
                 check_delay=Constants.UPDATE_PROGRESS_BAR_FREQ):
        Job.__init__(self, title=title, info=info)

        self._progress_message = progress_message
        self._complete_message = complete_message
        self._check_delay = check_delay

        # Creates threaded jobs
        self._threaded_jobs = []
        for j in jobs:
            self._threaded_jobs.append(SimultaneousJobs.ThreadedJob(job=j))

        # Set max progress
        max_progress = 0
        for j in self._threaded_jobs:
            max_progress += j.get_job().get_max_progress()
        self.set_max_progress(max_progress)

    def perform_task(self):

        # Starts job threads
        for j in self._threaded_jobs:
            j.start()

        # Waits until all jobs are complete
        all_complete = False
        while all_complete is False:
            # Checks if a sub-task is complete
            all_complete = True
            for j in self._threaded_jobs:
                all_complete &= j.is_complete()

            # Compute progress
            progress = 0
            for j in self._threaded_jobs:
                progress += j.get_job().get_progress()
            self.set_progress(progress, self._progress_message)

            # Sleeps
            time.sleep(self._check_delay)
            print("Simultaneous Task Status:", all_complete)

        # Task is complete
        self.complete_progress(self._complete_message)
