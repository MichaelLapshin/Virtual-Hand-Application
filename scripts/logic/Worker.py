import threading

# Workers
import time

from scripts import Log, General

dataset_worker = None
dataset_image_worker = None
model_worker = None
model_image_worker = None


class Worker(threading.Thread):
    """
        Thread performing long-lasting tasks
    """

    def __init__(self, sleep_delay=1):
        threading.Thread.__init__(self)
        self._running = False
        self.daemon = True
        self._queue = []
        self._complete = []
        self._start_time = []
        self._end_time = []
        self._stopped = True
        self._sleep_delay = sleep_delay

    def add_task(self, job):
        self._queue.append(job)

    def run(self):
        self._stopped = False
        while self._running is True:
            while len(self._queue) > 0:
                # TODO, change 'while' to 'if' once you get the worker tasks to be stored within the database
                self._start_time.append(General.get_current_slashed_date())
                self._queue[0].perform_task()
                self._end_time.append(General.get_current_slashed_date())

                # Transfers the task to the queue complete
                self._complete.append(self._queue[0])
                self._queue.pop(0)
            time.sleep(self._sleep_delay)

        self._stopped = True
        Log.info("The worker has stopped.")

    def start(self):
        Log.info("Starting the worker thread...")
        self._running = True
        super().start()

    def stop(self):
        Log.info("Stopping the worker thread...")
        self._running = False

    def clear_complete_queue(self):
        for i in range(0, len(self._complete)):
            self._start_time.pop(0)
            self._end_time.pop(0)
            self._complete.pop(0)

    """
        Getters
    """

    def is_running(self):
        return self._running

    def is_stopped(self):
        return self._stopped

    def get_queue(self):
        return self._queue

    def get_complete(self):
        return self._complete
