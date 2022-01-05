import base64
import io
import os

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


def image_to_bytesIO(image_path):
    bytes_io = io.BytesIO()
    image = PIL.Image.open(image_path)
    image.save(bytes_io, 'PNG')
    return bytes_io


"""
    For creating url-compatible strings
"""


def url_replacement_mapping(string):
    """
    Replaces characters in a string with the ones specified in the constants.
      - This helps avoid putting illegal characters into the url bar (e.g. spaces, &, etc.)
    :param string: the string to modify
    :return: return the same string, but with the illegal chars replaced
    """
    for k in Constants.URL_REPLACEMENT_MAP:
        string = string.replace(k, Constants.URL_REPLACEMENT_MAP.get(k))
    return string


def reverse_url_replacement_mapping(string):
    """
    Reverses the changes done by the function 'url_replacement_mapping()'
    :param string:the encoded string
    :return: return the string with the reverse-replacement done.

    WARNING: it may reverse-characters that have originally NOT been changed. This will
     occur if they use key characters that are used in the conversions.
    """
    for k in Constants.URL_REPLACEMENT_MAP:
        string = string.replace(Constants.URL_REPLACEMENT_MAP.get(k), k)
    return string


"""
    For transforming directories into encoded strings and decoding them into working directories.
    
    ? = command divisor
    @ file name @ file base 64 encoded content
    # = create amd enter directory (# followed by the directory name)
    $ = go up a directory level
"""


def encode_string_directory(dir_path: str):
    """
    Encodes the directory and all of its content into a string.
    :param dir_path: the directory to encode.
    :return: the encoded string
    """
    encoded_dir = "#" + dir_path[dir_path.rindex("\\") + 1::]

    def recursive_encoding(path):
        nonlocal encoded_dir
        content = os.listdir(path)

        Log.trace("Current path: " + path)
        Log.trace("Current encoding:" + encoded_dir)

        for name in content:
            encoded_dir += "?"

            if os.path.isdir(os.path.join(path, name)) is True:
                Log.debug("Encoding the directory: " + str(name))
                encoded_dir += "#" + name
                recursive_encoding(path + "\\" + name)

            else:  # is a file
                Log.debug("Encoding the file: " + str(name))
                with open(os.path.join(path, name), "rb") as file:
                    encoded_dir += "@" + name + "@" + str(base64.b64encode(file.read()))

        encoded_dir += "?$"

    recursive_encoding(dir_path)

    return encoded_dir


def decode_string_directory(base_directory: str, dir_string: str):
    """
    Decodes the string directory and adds it to the given directory.
    :param base_directory: the directory in which to spawn the
    :param dir_string: the encoded string directory
    :return: None
    """
    Log.info("Decoding the string directory to base_dir: " + str(base_directory))

    current_dir = base_directory
    string_dir_commands = dir_string.split("?")

    for command in string_dir_commands:
        Log.trace("Processing the command: " + command)

        if command[0] == "#":  # create directory & enters it
            dir_name = command.lstrip("#")

            # Create directory is does not already exist
            if os.path.isdir(os.path.join(current_dir, dir_name)) is False:
                os.mkdir(current_dir + dir_name)

            # Enters the directory
            current_dir = current_dir + dir_name + "\\"

        elif command[0] == "$":  # move up a directory
            Log.trace("Moving up a directory from: " + current_dir)
            current_dir = current_dir[:current_dir.rindex("\\"):]
            current_dir = current_dir[:current_dir.rindex("\\") + 1:]

        elif command[0] == "@":  # create file (overrides the file it already exists)
            file_name, file_encoded_data = command.lstrip("@").split("@")

            Log.trace("File name: " + file_name + "  File content: " + file_encoded_data)

            with open(current_dir + file_name, "wb") as writer:
                global file_data
                exec("file_data=" + file_encoded_data, globals())
                Log.trace("File data: " + str(file_data))
                writer.write(base64.b64decode(file_data))

        else:
            Log.warning("Could not identify a valid command. Found: " + str(command[0]))
