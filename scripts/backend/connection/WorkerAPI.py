import flask

from API_Helper import flarg, package
from scripts import Warnings, Log, Constants
from scripts.logic import Worker

worker_api = flask.Blueprint('worker_api', __name__)

"""
    Worker
"""


def get_model_queue_data(job):
    """
    Formats the queued model data to return to the server
    :return: [(id:int, model_id:int, title:str, progress:int, max_progress:int), ...]
    """
    return (job.get_id(), job.get_info().get("model_id"), job.get_title(), job.get_progress(), job.get_max_progress())


@worker_api.route("/get_model_training_queue")
def fetch_model_training_queue():
    Log.debug("Fetching the model training queue.")
    model_queue = []
    for q in Worker.worker.get_queue():
        if (q.get_info() is not None) and (type(q.get_info()) == dict) and (q.get_info().get("is_model") == True):
            model_queue.append(get_model_queue_data(q))

    return package(None, model_queue)


@worker_api.route("/get_model_complete_queue")
def fetch_model_complete_queue():
    Log.debug("Fetching the model complete queue.")
    model_queue = []
    for q in Worker.worker.get_complete():
        if (q.get_info() is not None) and (type(q.get_info()) == dict) and (q.get_info().get("is_model") == True):
            model_queue.append(get_model_queue_data(q))

    return package(None, model_queue)


@worker_api.route("/get_job_progress")
def fetch_job_progress():
    """
    Fetches the progress message of the job
    """

    id = int(flarg("id"))

    found_job = False
    message = ""
    progress = 0
    max_progress = 100
    for q in Worker.worker.get_queue():
        if q.get_id() == id:
            found_job = True
            progress = q.get_progress()
            max_progress = q.get_max_progress()
            message = q.get_progress_message()
            break

    if len(message) == 0:
        for q in Worker.worker.get_complete():
            if q.get_id() == id:
                found_job = True
                progress = q.get_progress()
                max_progress = q.get_max_progress()
                message = q.get_progress_message()
                break

    return package(None, (found_job,progress, max_progress, message))


@worker_api.route("/clear_complete_queue")
def clear_complete_queue():
    Worker.worker.clear_complete_queue()
    return package(True, "The worker complete queue has been cleared.")
