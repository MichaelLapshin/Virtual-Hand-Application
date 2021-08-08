import flask


def flarg(argument):
    return flask.request.args[argument]


def flreq(argument):
    return flask.request.files[argument]
