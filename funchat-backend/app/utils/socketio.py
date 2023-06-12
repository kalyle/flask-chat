import functools
from flask import request
from flask_login import current_user
from flask_socketio import disconnect


def authenticated_only(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return func(*args, **kwargs)

    return wrapped
