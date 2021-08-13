import flask

from scripts import Log


def flarg(argument):
    result = flask.request.args[argument]
    Log.debug("Fetching the flask.request argument '" + argument + "'. The result is '" + str(result) + "'")
    return result


def flreq(argument):
    file = flask.request.files[argument]
    Log.debug("Fetching the the flask.request files '" + argument + "'. The result is None: " + str(file is None))
    return file


def package(success, message):
    # Create and return the request package
    to_return = str((success, message))
    Log.debug("Packaging the request return: " + to_return)
    return to_return
