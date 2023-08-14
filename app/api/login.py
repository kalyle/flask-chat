from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas.login import LoginSchema
from app.schemas.user import UserSelfSchema
from app.models.user import UserModel
from flask_login import login_user
from app.extensions.login_ext import User

loginblp = Blueprint("login", "login", url_prefix="/login")


@loginblp.route("")
class Login(MethodView):
    @loginblp.arguments(LoginSchema, location="json", as_kwargs=True)
    @loginblp.response(200, UserSelfSchema)
    def post(self, **login_data):
        user = UserModel.query.filter_by(username=login_data["username"]).first()
        if not user or not user.check_password(user.password, login_data["password"]):
            abort(401)
        login_user(User(user.id))
        return user
