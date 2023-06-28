from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions.reids import cache


logoutblp = Blueprint("logout", "logout", url_prefix="v1/logout")


@logoutblp.route("")
class Logout(MethodView):
    @logoutblp.response(200)
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        cache.hash_del("user_info", user_id)
        return {}
