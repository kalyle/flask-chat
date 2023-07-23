from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import current_user
from app.schemas.info import InfoSelfSchema, InfoOtherSchema
from app.models.user import UserModel

infoblp = Blueprint("info", "info", url_prefix="/info")


@infoblp.route("/<user_id>")
class Info(MethodView):
    @infoblp.response(200)
    @infoblp.response(200, InfoSelfSchema)
    def get(self, user_id):
        # 获取指定user info
        user = UserModel.find_by_id(user_id)
        if int(user_id) == current_user.id:
            response = InfoSelfSchema().dump(user)
        else:
            response = InfoOtherSchema().dump(user)
        return response

    @infoblp.arguments(InfoSelfSchema)
    @infoblp.response(200, InfoSelfSchema)
    def post(self, user_id):
        # 获取指定user info
        user = UserModel.find_by_id(user_id)
        if int(user_id) == current_user.id:
            response = InfoSelfSchema().dump(user)
        else:
            response = InfoOtherSchema().dump(user)
        return response

    @infoblp.arguments(InfoSelfSchema)
    @infoblp.response(200, InfoSelfSchema)
    def patch(self, new_data: UserModel, user_id):
        if int(user_id) == current_user.id:
            UserModel.update_by_limit(user_id, new_data.__dict__)
            return UserModel.find_by_id(user_id)
        else:
            abort(400)
