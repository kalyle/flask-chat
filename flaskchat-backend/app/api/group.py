from flask.views import MethodView
from flask_smorest import Blueprint


from app.models.user import UserModel
from app.models.group import GroupModel, GroupApplyModel
from flask_login import login_required, current_user, login_user

from app.models.user_group_mapping import user_group_mapping
from app.schemas.group import getGroupApplySchema, GroupApplySchema

groupblp = Blueprint("group", "group", url_prefix="/group")


@groupblp.route("")
class GroupApply(MethodView):
    @groupblp.response(getGroupApplySchema(many=True))
    def get(self):

        user_id = current_user.id
        group_apply_list = GroupModel.find_by_limit({"own_id": user_id})
        group_apply_list.append(GroupModel.find_by_limit({"admin_id": user_id}))

        response = {}

        return response

    @groupblp.arguments(GroupApplySchema)
    @groupblp.response(getGroupApplySchema)
    def post(self, new_data):
        id = GroupApplyModel(**new_data).save_to_db()
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
        group_apply = GroupApplyModel.find_by_id(apply_id)
        group_id = group_apply.group_id
        bool_owner = user_group_mapping.select(group_id=group_id, user_id=current_user.id, role=2)
        bool_admin = user_group_mapping.select(group_id=group_id, user_id=current_user.id, role=1)

        if bool_admin and bool_owner:
            GroupApplyModel.update_by_limit(**new_data)
            group = GroupModel.find_by_id(group_id)
            group.members.append(UserModel.find_by_id(new_data["user_id"]))

            return GroupApplyModel.find_by_id(apply_id)

    @groupblp.response(204)
    # @login_required
    def delete(self, apply_id):
        group_apply = GroupApplyModel.find_by_id(apply_id)
        group_apply.delete_from_db()
        return {}
