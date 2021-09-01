import io

import PIL.Image
import flask

from scripts import Log, Constants

worker = None


def flarg(argument):
    result = flask.request.args.get(argument)
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


def url_replacement_mapping(string):
    for k in Constants.URL_REPLACEMENT_MAP:
        string = string.replace(k, Constants.URL_REPLACEMENT_MAP.get(k))
    return string


def reverse_url_replacement_mapping(string):
    for k in Constants.URL_REPLACEMENT_MAP:
        string = string.replace(Constants.URL_REPLACEMENT_MAP.get(k), k)
    return string


def image_to_bytesIO(image_path):
    bytes_io = io.BytesIO()
    image = PIL.Image.open(image_path)
    image.save(bytes_io, 'PNG')
    return bytes_io
