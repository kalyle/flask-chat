from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.schemas.register import RegisterSchema
from app.schemas.info import InfoSelfSchema
from app.models.user import UserModel
from app.utils.before_request import current_user

accountblp = Blueprint("account", "account", url_prefix="/account")


@accountblp.route("/register")
class Register(MethodView):
    # @accountblp.arguments(RegisterSchema(session=db.session), location="json")
    @accountblp.arguments(RegisterSchema(), location="json")
    @accountblp.response(200, InfoSelfSchema)
    def post(self, register_data):
        password = register_data["password"]
        del register_data["password"]
        user = UserModel(**register_data)
        user.password_salt = password
        id = user.save_to_db()
        return UserModel.find_by_id(id)


@accountblp.route("/password/reset")
class PasswordReset(MethodView):
    @accountblp.arguments(InfoSelfSchema, location="json")
    @accountblp.response(200)
    def patch(self):
        user_id = 1
        data = request.get_json()
        code = ""
        if data["password"] != data["password2"]:
            abort(400)
        if not code:
            # 手机验证码
            abort(400)
        UserModel.update_by_limit(user_id, data["password"])
        return {}


@accountblp.route("/email")
class PasswordReset(MethodView):
    @accountblp.arguments(InfoSelfSchema, location="json")
    @accountblp.response(200)
    def post(self, new_data):
        code = ""
        if new_data["password"] != new_data["password2"]:
            abort(400)
        if not code:
            # 手机验证码
            abort(400)
        UserModel.update_by_limit(current_user.id, new_data["password"])
        return {}
