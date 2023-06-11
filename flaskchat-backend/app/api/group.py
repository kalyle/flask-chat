from flask.views import MethodView
from flask_smorest import Blueprint, abort


from app.models.user import UserModel
from app.models.group import GroupModel, GroupApplyModel
from flask_login import login_required, current_user, login_user

from app.models import user_group_mapping
from app.schemas.group import getGroupApplySchema, GroupApplySchema
from flask import jsonify, request
from app.extensions.login_ext import User

groupblp = Blueprint("group", "group", url_prefix="/group")


@groupblp.route("")
class GroupApply(MethodView):
    @groupblp.response(200)
    def get(self):
        user_id = current_user.id
        group_id = request.get_json()["groupId"]
        if not group_id:
            group_apply_list = GroupModel.find_by_limit({"owner_id": user_id})
            group_apply_list.append(GroupModel.find_by_limit({"admin_id": user_id}))
            response = {}
            return response
        else:
            group_schema = GroupInfoSchema()
            group = GroupModel.find_by_id(group_id)
            return group_schema.dump(group)

    @groupblp.arguments(GroupInfoSchema)
    @groupblp.response(200)
    def patch(self, new_data: GroupModel):
        id = new_data.save_to_db()

        group_schema = GroupInfoSchema()
        group = GroupModel.find_by_id(id)
        return group_schema.dump(group)

    @groupblp.response(204)
    def delete(self):
        group_id = request.get_json()["groupId"]
        group = GroupModel.find_by_id(group_id)
        return {}


@groupblp.route("/user/setting")
class GroupUserSetting(MethodView):
    def post(self):
        user_id = request.get_json("userId")
        group_id = request.get_json("groupId")
        role = request.get_json("role")

        group = GroupModel.find_by_id(group_id)
        user = UserModel.find_by_id(user_id)
        if role is not None:
            group.admins.append(user)
        group.members.append(user)
        return {}

    @groupblp.response(204)
    def delete(self):
        user_id = request.get_json("userId")
        group_id = request.get_json("groupId")

        user = UserModel.find_by_id(user_id)
        group = GroupModel.find_by_id(group_id)
        if user in group.admins:
            group.admins.remove(user)
        group.members.remove(user)
        return {}


@groupblp.route("/apply")
class GroupApplyById(MethodView):
    def get(self, new_data):
        #
        login_user(User(1))
        #
        user_id = current_user.id
        groups = GroupModel.find_by_or_limit({"owner_id": user_id, "admin_id": user_id})
        group_ids = [group.id for group in groups]

        toApply = GroupApplyModel.query.filter(
            GroupApplyModel.user_id == user_id, GroupApplyModel.group_id._in(group_ids)
        ).all()
        fromApply = GroupApplyModel.find_by_limit({"user_id": user_id})
        response = {}
        response["toApply"] = getGroupApplySchema(many=True).dump(toApply)
        response["fromApply"] = getGroupApplySchema(many=True).dump(fromApply)

        return jsonify(response)

    # owner and admins操作
    @groupblp.arguments(GroupApplySchema)
    @groupblp.response(200)
    def post(self, new_data: GroupApplyModel):
        id = new_data.save_to_db()
        return GroupApplyModel.find_by_id(id)


@groupblp.route("/apply/{apply_id}")
class GroupApplyById(MethodView):
    # @login_required
    def get(self, apply_id):
        return GroupApplyModel.find_by_id(apply_id)

    # owner and admins操作
    @groupblp.arguments(GroupApplySchema)
    @groupblp.response(200)
    # @login_required
    def patch(self, new_data, apply_id):
        apply_id = new_data["apply_id"]
        group_id = new_data["group_id"]
        user_id = new_data["user_id"]
        current_user_id = current_user.id
        if user_id != current_user_id:
            abort(400)

        bool_owner = user_group_mapping.select(
            group_id=group_id, user_id=user_id, owner_id=user_id
        )
        bool_admin = user_group_mapping.select(
            group_id=group_id, user_id=user_id, admin_id=user_id
        )

        if bool_admin and bool_owner:
            GroupApplyModel.update_by_limit(**new_data)
            group = GroupModel.find_by_id(group_id)
            group.members.append(UserModel.find_by_id(user_id))

            return GroupApplyModel.find_by_id(apply_id)
        else:
            abort(403, "你无权修改")

    @groupblp.response(204)
    # @login_required
    def delete(self, apply_id):
        group_apply = GroupApplyModel.find_by_id(apply_id)
        group_apply.delete_from_db()
        return {}
