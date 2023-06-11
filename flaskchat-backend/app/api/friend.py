from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify, request

from app.extensions.login_ext import User
from app.models.friend import FriendModel
from app.models.user import UserModel
from app.schemas.friend import ApplySchema,getApplySchema
from flask_login import current_user, login_user

from app.schemas.user import UserOtherSchema

friendblp = Blueprint("friend", "friend", url_prefix="/friend")


@friendblp.route("")
class Friend(MethodView):
    # @friendblp.arguments(QuerySchema,location="query",as_kwargs=True)  # 按照组名\首字母 分组 默认按照首字母分组
    @friendblp.response(200,UserOtherSchema(many=True))
    def get(self):
        #
        user = User(1)
        login_user(user)
        print("current", current_user, current_user.__dict__, current_user.id)
        #
        user = UserModel.find_by_id(current_user.id)
        return user.friends

    @friendblp.response(200)
    def delete(self):
        friend_id = request.get_json()["friendId"]
        user_of_me = FriendModel.find_by_limit({"user_id": current_user.id, "friend_id": friend_id})
        friend_of_me = FriendModel.find_by_limit({"user_id": friend_id, "friend_id": current_user.id})

        user_of_me.delete_from_db()
        friend_of_me.delete_from_db()

        # emit status

        return {}


@friendblp.route("/apply")
class FriendApply(MethodView):
    @friendblp.response(200)
    def get(self):
        #
        login_user(User(1))
        #
        # 自己发送的
        apply_from = FriendModel.find_by_limit({"user_id": current_user.id})
        apply_to = FriendModel.find_by_limit({"friend_id": current_user.id})

        response = {}
        response["fromApply"] = getApplySchema(many=True).dump(apply_from)
        response["toApply"] = getApplySchema(many=True).dump(apply_to)

        return jsonify(response)

    @friendblp.arguments(ApplySchema, location="json")
    @friendblp.response(200, getApplySchema)
    # @login_user
    def post(self, new_data:FriendModel):
        # 重定向到好友聊天列表，并生成chatlist
        id = new_data.save_to_db()
        # emit apply msg
        # emit(user,apply_response)
        return FriendModel.find_by_id(id)


@friendblp.route("/apply/<apply_id>")
class FriendApplyById(MethodView):
    @friendblp.response(200,getApplySchema)
    def get(self,apply_id):
        print("type",type(apply_id))
        return FriendModel.find_by_id(apply_id)

    @friendblp.arguments(ApplySchema, location="json", as_kwargs=True)
    @friendblp.response(200, getApplySchema)
    def patch(self, apply_id, **data):  # 这里路径参数 和 请求参数 顺序（如果是正常的，则路径参数在后？作为关键字参数，则在前？)
        apply_status = data["apply_status"]
        FriendModel.update_by_limit(apply_id, data)
        if apply_status == 1:  # 同意
            # 成为好友
            FriendModel(user_id=data["friend_id"], friend_id=data["user_id"], apply_status=apply_status).save_to_db()
        response = FriendModel.find_by_id(apply_id)
        # emit apply msg
        # emit(user,apply_response)

        return response

    @friendblp.response(204)
    def delete(self, apply_id):
        apply = FriendModel.find_by_id(apply_id)
        apply.delete_from_db()
        return {}
