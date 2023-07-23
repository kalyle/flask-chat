import functools
import json

from flask import request, g
from werkzeug.local import LocalProxy
from flask.globals import request_ctx

from app.utils.reids import cache
from app.extensions.init_ext import socketio
from app.models.user import UserModel
from flask_jwt_extended import verify_jwt_in_request, utils


def request_intercept():
    # ip限制
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    # request 限制
    url = request.path
    auth = None
    if not any([url.endswith(u) for u in ["login", "register", "admin"]]):
        _, auth = verify_jwt_in_request()
    # 判断是否匿名用户
    if not auth:
        # t = app.model.user.AnonyMous()
        user = None
    else:
        user = UserModel.find_by_id(auth.get("id"))
    request_ctx.current_user = user


def verify(token):
    payload = utils.decode_token(token)
    return payload.get("id")


def socket_auth(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        token = getattr(socketio.server, "token")
        if not token:
            raise ConnectionRefusedError('authorized fail!')
        id = verify(token)
        if not id:
            raise ConnectionRefusedError('数据错误')
        else:
            data = cache.hash_get("user_info", id)
            if not data:
                raise ValueError("redis error")
            g.user = json.loads(data)
            return f(*args, **kwargs)

    return wrapped


current_user = LocalProxy(lambda: getattr(request_ctx, "current_user"))
socket_user = LocalProxy(lambda: getattr(g, "user"))
