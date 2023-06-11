from flask.views import MethodView
from flask_smorest import Blueprint

from flask_login import logout_user
from flask import request

from app.extensions.login_ext import User

logoutblp = Blueprint("logout", "logout", url_prefix="v1/logout")


@logoutblp.route("")
class Logout(MethodView):
    @logoutblp.response(200)
    def post(self):
        user_id = request.get_json()["user_id"]
        logout_user(User.get(user_id))
        return {}
