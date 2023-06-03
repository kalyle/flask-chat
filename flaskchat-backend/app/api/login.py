from flask.views import MethodView
from flask_smorest import Blueprint
from app.schemas.auth import LoginSchema
from app.schemas.user import UserSelfSchema
from app.models.user import UserModel
from flask_login import login_user

loginblp = Blueprint("login", "login", url_prefix="v1/login")


@loginblp.route("")
class Login(MethodView):
    @loginblp.arguments(LoginSchema, location="form",as_kwargs=True)
    @loginblp.response(200,UserSelfSchema)
    def post(self, **login_data):
        print("login get",login_data)
        user = UserModel.find_by_name(login_data["username"])
        login_user(user)
        return user

