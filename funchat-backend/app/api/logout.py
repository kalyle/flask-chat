from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request


logoutblp = Blueprint("logout", "logout", url_prefix="v1/logout")


@logoutblp.route("")
class Logout(MethodView):
    @logoutblp.response(200)
    def post(self):
        user_id = request.get_json()["user_id"]
        return {}
