from flask.views import MethodView
from flask_smorest import Blueprint
from app.schemas.user import LoginSchema
from app.schemas.user import UserSelfSchema
from app.models.user import UserModel
from flask_login import login_user

from app.extensions.login_ext import User

loginblp = Blueprint("login", "login", url_prefix="/login")


@loginblp.route("")
class Login(MethodView):
    @loginblp.arguments(LoginSchema, location="form", as_kwargs=True)
    @loginblp.response(200, UserSelfSchema)
    def post(self, **login_data):
        user = UserModel.find_by_name(login_data["username"])
        current_login_user = User(user.id)
        login_user(current_login_user)
        return user
