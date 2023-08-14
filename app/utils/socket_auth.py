from functools import wraps
from flask_login import current_user


def is_auth():
    @wraps
    def wapper(func):
        if not current_user.id:
            raise ConnectionRefusedError('authorized fail!')
        func()

    return wapper
