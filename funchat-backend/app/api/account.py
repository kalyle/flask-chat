from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import current_user

from app.schemas.user import RegisterSchema
from app.schemas.user import UserSelfSchema, UserOtherSchema
from app.models.user import UserModel
from app.models import db

accountblp = Blueprint("account", "account", url_prefix="/account")


@accountblp.route("/register")
class Register(MethodView):
    @accountblp.arguments(RegisterSchema(session=db.session), location="json")
    @accountblp.response(200, UserSelfSchema)
    def post(self, register_data):
        password = register_data["password"]
        del register_data["password"]
        user = UserModel(**register_data)
        user.password_salt = password
        id = user.save_to_db()
        return UserModel.find_by_id(id)


@accountblp.route("/<user_id>/info")
class Info(MethodView):
    @accountblp.response(200)
    def get(self, user_id):
        # 获取指定user info
        user = UserModel.find_by_id(user_id)
        if int(user_id) == current_user.id:
            response = UserSelfSchema().dump(user)
        else:
            response = UserOtherSchema().dump(user)
        return response

    @accountblp.arguments(UserSelfSchema)
    def patch(self, new_data: UserModel, user_id):
        if int(user_id) == current_user.id:
            UserModel.update_by_limit(user_id, new_data.__dict__)
            return UserModel.find_by_id(user_id)
        else:
            abort(400)


@accountblp.route("/<user_id>/password/reset")
class PasswordReset(MethodView):
    @accountblp.response(200)
    def patch(self, user_id):
        data = request.get_json()
        code = ""
        if data["password"] != data["password2"]:
            abort(400)
        if not code:
            # 手机验证码
            abort(400)
        UserModel.update_by_limit(user_id, data["password"])
        return {}
