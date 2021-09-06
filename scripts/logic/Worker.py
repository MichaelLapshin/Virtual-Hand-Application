import threading

# Workers
import time

from scripts import Log, General

worker = None


class Worker(threading.Thread):
    """
        Thread performing long-lasting tasks
    """

    def __init__(self, sleep_delay=1, thread_jobs=False):
        threading.Thread.__init__(self)
        self._running = False
        self.daemon = True
        self._queue = []
        self._complete = []
        self._start_time = []
        self._end_time = []
        self._stopped = True
        self._sleep_delay = sleep_delay
        self._thread_jobs = thread_jobs

    def add_task(self, job):
        Log.info("Added the job '" + job.get_title() + "'")
        self._queue.append(job)

    def run(self):
        self._stopped = False
        while self._running is True:
            while len(self._queue) > 0:
                # TODO, change 'while' to 'if' once you get the worker tasks to be stored within the database
                # Performs the task
                Log.info("Starting to process the job '" + self._queue[0].get_title() + "'")
                self._start_time.append(General.get_current_slashed_date())
                self._queue[0].perform_task()

                # Transfers the task to the queue complete
                Log.info("Completed the job '" + self._queue[0].get_title() + "'")
                self._end_time.append(General.get_current_slashed_date())
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

    def remove_queue_job(self, id: int):
        for q in self._queue:
            if id == q.get_id() and (len(self._queue) > 0 and self._queue[0].get_id() != id):
                self._queue.remove(q)
                break

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
