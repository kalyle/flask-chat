from flask import request
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_smorest import Blueprint, abort

from app.schemas.register import RegisterSchema
from app.schemas.info import InfoSelfSchema,InfoOtherSchema
from app.models.user import UserModel
from app.schemas.user import UserSelfSchema
from app.utils.before_request import current_user

accountblp = Blueprint("account", "account", url_prefix="/account")


@accountblp.route("/register")
class Register(MethodView):
    @accountblp.arguments(RegisterSchema, location="json")
    @accountblp.response(200, UserSelfSchema)
    def post(self, new_data: UserModel):
        id = new_data.save_to_db()
        user = UserModel.find_by_id(id)
        user.token = create_access_token(identity=user)
        return user


@accountblp.route("/<user_id>/info")
class Info(MethodView):
    @accountblp.response(200)
    def get(self, user_id):
        # 获取指定user info
        user = UserModel.find_by_id(user_id)
        if user.id == current_user.id:
            response = InfoSelfSchema().dump(user.information)
        else:
            response = InfoOtherSchema().dump(user.information)
        return response

    @accountblp.arguments(InfoSelfSchema)
    @accountblp.response(200, InfoSelfSchema)
    def patch(self, new_data: UserModel, user_id):
        if int(user_id) == current_user.id:
            UserModel.update_by_limit(user_id, new_data.__dict__)
            return UserModel.find_by_id(user_id)
        else:
            abort(400)


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
