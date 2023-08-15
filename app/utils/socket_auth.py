from functools import wraps
from flask_login import current_user


def is_auth(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if current_user.is_authenticated:
            raise ConnectionRefusedError('authorized fail!')
        return func(*args, **kwargs)

    return wapper
