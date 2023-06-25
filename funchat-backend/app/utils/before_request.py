from flask import request, make_response
from flask_jwt_extended import get_jwt_identity
from werkzeug.local import LocalProxy
from flask.globals import request_ctx
from app.models.user import UserModel
from werkzeug.exceptions import Unauthorized


def authorization():
    url = request.path
    if not any([url.endswith(i) for i in ("login", "register", "admin")]):
        token = request.headers.get("Authorization")
        if not token:
            # t = app.model.user.AnonyMous()
            user = None
        else:
            user_id = get_jwt_identity()
            # 身份过期
            # if not user_id:
            #     response = make_response({})
            #     Unauthorized()
            user = UserModel.find_by_id(user_id)
        request_ctx.current_user = user


current_user = LocalProxy(lambda: getattr(request_ctx, "current_user"))
