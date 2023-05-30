from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas.auth import LoginSchema

loginblp = Blueprint("login", "login", url_prefix="/login")


@loginblp.route("")
class Login(MethodView):
    @loginblp.arguments(LoginSchema, location="json")
    def post(self, login_data):
        print(login_data)

