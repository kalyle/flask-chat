from flask.views import MethodView
from flask_smorest import Blueprint, abort

from app.extensions.init_ext import socketio
from app.models.friend_apply import FriendApplyModel
from app.models.user import UserModel
from app.models.group import GroupModel
from app.schemas.group import GroupSchema
from app.schemas.friend import ApplySchema, getApplySchema
from app.schemas.query import QuerySchema
from app.schemas.info import InfoOtherSchema
from flask_login import current_user, login_required

friendblp = Blueprint("friend", "friend", url_prefix="/friend")


@friendblp.route("")
class Friend(MethodView):
    @friendblp.arguments(
        QuerySchema, location="query", as_kwargs=True
    )  # 按照组名\首字母 分组 默认按照首字母分组
    @friendblp.response(200, InfoOtherSchema(many=True))
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
        apply_list = []
        send_from_me = FriendApplyModel.find_send_from_me()
        send_to_me = FriendApplyModel.find_send_to_me()
        apply_list += send_from_me + send_to_me
        return sorted(apply_list, lambda apply: apply.create_time)

    @friendblp.arguments(ApplySchema)
    @friendblp.response(200)
    def post(self, new_data: FriendApplyModel):
        exist = FriendApplyModel.is_exist()
        if exist:
            id = exist.id
        else:
            id = new_data.save_to_db()
        response = getApplySchema().dump(FriendApplyModel.find_by_id(id))
        # emit apply msg
        socketio.emit("friendApply", response, to=id, namespace="/")
        return response


@friendblp.route("/apply/<apply_id>")
class FriendApplyById(MethodView):
    @friendblp.response(200, getApplySchema)
    # 这里路径参数 和 请求参数 顺序（如果是正常的，则路径参数在后？作为关键字参数，则在前？)
    def patch(self, apply_id):
        data = {"apply_status": 1}
        FriendModel.update_by_limit(apply_id, data)
        apply = FriendModel.find_by_id(apply_id)
        # 同意
        fromMe = FriendModel.find_by_limit(
            {
                "user_id": apply.friend_id,
                "friend_id": apply.user_id,
            },
            many=False,
        )
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
            {
                "apply": [apply.id, fromMe.id] if fromMe else [apply],
                "applyStatus": apply.apply_status,
            },
            to=apply.friend_id,
        )
        return apply

    @friendblp.response(204)
    def delete(self, apply_id):
        apply = FriendApplyModel.find_by_id(apply_id)
        apply.delete_from_db()
        return {}


@friendblp.route("/GroupBy")
class GroupBy(MethodView):
    @friendblp.response(200, GroupSchema(many=True))
    def get(self):
        return {}

    @friendblp.arguments(GroupSchema)
    @friendblp.response(200)
    def post(self, new_data: GroupModel):
        id = new_data.save_to_db()
        return GroupModel.find_by_id(id)

    # 修改好友分组
    @friendblp.response(200)
    def patch(self):
        return {}

    @friendblp.arguments(GroupSchema)
    @friendblp.response(204)
    def delete(self, new_data: GroupModel):
        new_data.delete_from_db()
        return {}


@friendblp.route("/search")
class Search(MethodView):
    @friendblp.response(200, InfoOtherSchema(many=True))
    def get(self):
        data = request.args
        users = UserModel.query.filter(
            UserModel.username.like(f"{data['filterKey']}%")
        ).all()
        return users
