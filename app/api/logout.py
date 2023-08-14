from flask.views import MethodView
from flask_smorest import Blueprint
from flask_login import logout_user, login_required, current_user


logoutblp = Blueprint("logout", "logout", url_prefix="/logout")


@logoutblp.route("")
class Logout(MethodView):
    @logoutblp.response(200)
    @login_required
    def post(self):
        logout_user(current_user)
        return {}
