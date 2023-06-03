from flask.views import MethodView
from flask_smorest import Blueprint
from flask_login import login_required, current_user
from app.schemas.user import UserSelfSchema, UserOtherSchema, RegisterSchema
from app.models.user import UserModel
from app.models.info import InfoModel

from schemas.user import UserOtherSchema

accountblp = Blueprint("account", "account", url_prefix="/account")


@accountblp.route("/register")
class Register(MethodView):
    @accountblp.arguments(RegisterSchema, location="json")
    @accountblp.response(200, UserSelfSchema)
    def post(self, new_data):
        username = new_data.get("username")
        info: dict = new_data.get("info")
        id = UserModel(username=username).save_to_db()
        InfoModel(user_id=id, **info).save_to_db()
        return UserModel.find_by_id(id)


@accountblp.route("/<user_id>/info")
class Info(MethodView):
    @accountblp.response(200)
    def get(self, user_id):
        # 获取指定user info
        user = UserModel.find_by_id(user_id)
        if user_id == current_user.id:
            response = UserSelfSchema().dump(user)
        else:
            response = UserOtherSchema().dump(user)
        return response

    @login_required
    def patch(self):
        # 修改 user 信息
        return {}


@accountblp.route("/<user_id>/password/reset")
class PasswordReset(MethodView):
    @login_required
    def patch(self):
        return {}


@accountblp.route("/<user_id>/email/reset")
class EmailReset(MethodView):
    @login_required
    def patch(self):
        return {}
