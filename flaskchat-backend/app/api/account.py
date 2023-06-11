from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from flask_login import login_required, current_user, login_user

from app.extensions.login_ext import User
from app.schemas.user import RegisterSchema
from app.schemas.user import UserSelfSchema, UserOtherSchema
from app.models.user import UserModel


accountblp = Blueprint("account", "account", url_prefix="/account")


@accountblp.route("/register")
class Register(MethodView):
    @accountblp.arguments(RegisterSchema, location="json")
    @accountblp.response(200, UserSelfSchema)
    def post(self, new_data:UserModel):
        id = new_data.save_to_db()
        return UserModel.find_by_id(id)


@accountblp.route("/<user_id>/info")
class Info(MethodView):
    @accountblp.response(200)
    def get(self, user_id):
        #
        user = User(1)
        login_user(user)
        print("current", current_user, current_user.__dict__, current_user.id)
        #
        # 获取指定user info
        user = UserModel.find_by_id(user_id)
        if int(user_id) == current_user.id:
            response = UserSelfSchema().dump(user)
        else:
            response = UserOtherSchema().dump(user)
        return response

    @accountblp.arguments(UserSelfSchema)
    @login_required
    def patch(self,new_data:UserModel,user_id):
        if int(user_id) == current_user.id:
            UserModel.update_by_limit(user_id,new_data.__dict__)
            return UserModel.find_by_id(user_id)
        else:
            abort(400)


@accountblp.route("/<user_id>/password/reset")
class PasswordReset(MethodView):
    @login_required
    @accountblp.response(200)
    def patch(self,user_id):
        data = request.get_json()
        code = ""
        if data["password"] != data["password2"]:
            abort(400)
        if not code:
            # 手机验证码
            abort(400)
        UserModel.update_by_limit(user_id, data["password"])
        return {}

