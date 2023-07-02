from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from sqlalchemy import and_

from app.extensions.socketio import socketio
from app.models.friend import FriendModel
from app.models.user import UserModel
from app.schemas.friend import ApplySchema, getApplySchema
from app.schemas.query import QuerySchema
from app.schemas.user import UserOtherSchema
from app.utils.before_request import current_user

friendblp = Blueprint("friend", "friend", url_prefix="/friend")


@friendblp.route("")
class Friend(MethodView):
    @friendblp.arguments(
        QuerySchema, location="query", as_kwargs=True
    )  # 按照组名\首字母 分组 默认按照首字母分组
    @friendblp.response(200, UserOtherSchema(many=True))
    def get(self, **query_dict):
        user = UserModel.find_by_id(current_user.id)
        if query_dict["type"] == "name":
            # 按照姓名排序
            pass
        elif query_dict["type"] == "group":
            # 按照分组排序
            pass
        return user.friends

    @friendblp.response(200)
    def delete(self):
        friend_id = request.get_json()["friendId"]
        user_of_me = FriendModel.find_by_limit(
            {"user_id": current_user.id, "friend_id": friend_id}
        )
        friend_of_me = FriendModel.find_by_limit(
            {"user_id": friend_id, "friend_id": current_user.id}
        )

        user_of_me.delete_from_db()
        friend_of_me.delete_from_db()

        # emit status

        return {}


@friendblp.route("/apply")
class FriendApply(MethodView):
    @friendblp.response(200, getApplySchema(many=True))
    def get(self):
        # 自己发送的
        apply_list = FriendModel.query.filter_by(
            user_id=current_user.id, apply_status=0).all()
        val = FriendModel.query.filter_by(
            friend_id=current_user.id, apply_status=0).all()
        apply_list += val
        return apply_list

    @friendblp.arguments(ApplySchema)
    @friendblp.response(200)
    def post(self, new_data):
        count = FriendModel.find_by_limit(new_data)
        if count:
            id = count[0].id
        else:
            id = FriendModel(**new_data).save_to_db()

        apply = FriendModel.find_by_id(id)
        response = getApplySchema().dump(apply)
        # emit apply msg
        socketio.emit("friendApply", response, to=apply.friend_id, namespace="/notify")
        return response


@friendblp.route("/apply/<apply_id>")
class FriendApplyById(MethodView):
    @friendblp.response(200, getApplySchema)
    def patch(self, apply_id):  # 这里路径参数 和 请求参数 顺序（如果是正常的，则路径参数在后？作为关键字参数，则在前？)
        data = {"apply_status":1}
        FriendModel.update_by_limit(apply_id, data)
        apply = FriendModel.find_by_id(apply_id)
        # 同意
        fromMe = FriendModel.find_by_limit({"user_id": apply.friend_id,
                                            "friend_id": apply.user_id,
                                            }, many=False)
        if not fromMe:
            FriendModel(
                user_id=apply.friend_id,
                friend_id=apply.user_id,
                apply_status=data["apply_status"],
            ).save_to_db()
        else:
            FriendModel.update_by_limit(fromMe.id, data)
        # emit apply msg
        socketio.emit(
            "friendApply",
            {"apply": [apply.id, fromMe.id] if fromMe else [apply], "applyStatus": apply.apply_status},
            to=apply.friend_id
        )
        return apply

    @friendblp.response(204)
    def delete(self, apply_id):
        apply = FriendModel.find_by_id(apply_id)
        apply.delete_from_db()
        return {}


# @friendblp.route("<user_id>/SortByGroup")
# class SortByGroup(MethodView):
#     @friendblp.response(200)
#     def get(self, user_id):
#         return {}

#     @friendblp.response(200)
#     def post(self, user_id):
#         return {}

#     @friendblp.response(200)
#     def patch(self, user_id):
#         return {}


#     @friendblp.response(200)
#     def delete(self, user_id):
#         return {}
@friendblp.route("/history")
class Histroy(MethodView):
    def get(self, **query_dict):
        pass

    def delete(self, data):
        pass


@friendblp.route("/search")
class Search(MethodView):
    @friendblp.response(200, UserOtherSchema(many=True))
    def get(self):
        from flask_jwt_extended import get_jwt_identity

        user = get_jwt_identity()
        data = request.args
        users = UserModel.query.filter(
            UserModel.username.like(f"{data['filterKey']}%")
        ).all()
        return users
