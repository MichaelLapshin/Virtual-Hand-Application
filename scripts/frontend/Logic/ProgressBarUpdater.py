import time

from scripts import Warnings, Log, Constants
from scripts.frontend import ClientConnection
from scripts.logic import Job, Worker


def remove_all_progress_bar_jobs():
    # Deletes all model image loading jobs
    to_remove_ids = []
    for q in Worker.worker.get_queue():
        if (q.get_info() is not None) and (type(q.get_info()) == dict) \
                and (q.get_info().get("progress_bar") == True):
            to_remove_ids.append(q.get_id())

    for id in to_remove_ids:
        Worker.worker.remove_queue_job(id)


class JobUpdateProgressBar(Job.Job):
    """
        For periodically sending requests to the server to update the progress bar.
    """

    def __init__(self, job_id, progress_bar_obj):
        Job.Job.__init__(self, title="Update progress bar task.", info={"progress_bar": True})
        self._job_id = job_id
        self._progress_bar_obj = progress_bar_obj
        self.set_max_progress(1)

    def perform_task(self):
        self.set_progress(0, "Starting to update the progress bar.")
        found_job, progress, max_progress, message = ClientConnection.get_worker_job_message(self._job_id)

        if found_job is True:
            Log.trace(
                "Updating the progress bar to: " + str(progress) + "/" + str(max_progress) + " with message " + message)

            # Updating the progress bar
            self._progress_bar_obj.set_count(progress)
            self._progress_bar_obj.set_max_count(max_progress)
            self._progress_bar_obj.set_metric_text(" Epochs.   Status: " + message)

            # Checks if another update should be made
            if progress < max_progress:
                time.sleep(Constants.UPDATE_PROGRESS_BAR_FREQ)
                Worker.worker.add_task(
                    job=JobUpdateProgressBar(job_id=self._job_id, progress_bar_obj=self._progress_bar_obj))

        self.complete_progress("The progress bar update is complete.")
