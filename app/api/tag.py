from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models.tag import TagModel
from app.models.user import UserModel
from app.models.user_tag_mapping import UserTagMappingModel
from app.schemas.tag import TagSchema
from app.schemas.user_tag_mapping import UserTagMappingSchema
from app.utils.before_request import current_user

tagblp = Blueprint("tag", "tag", url_prefix="/tag")


@tagblp.route("")
class Tag(MethodView):
    @tagblp.response(200, TagSchema(many=True, exclude=("created_by",)))
    def get(self):
        return TagModel.find_tags()

    @tagblp.arguments(TagSchema)
    @tagblp.response(200, TagSchema)
    def post(self, new_data: TagModel):
        id = new_data.save_to_db()
        return TagModel.find_by_id(id)

    @tagblp.arguments(TagSchema)
    @tagblp.response(204)
    def delete(self, new_data: TagModel):
        new_data.delete_from_db()
        return


@tagblp.route("/<user_id>")
class UserTag(MethodView):
    @tagblp.response(200, UserTagMappingSchema(many=True))
    def get(self, user_id):
        uts = UserTagMappingModel.find_all_by_user(user_id=user_id)
        return uts

    @tagblp.arguments(TagSchema(many=True))
    @tagblp.response(200, UserTagMappingSchema(many=True))
    def post(self, new_data, user_id):
        for tag in new_data:
            ut = UserTagMappingModel()
            ut.tag = tag
            ut.user_id = int(user_id)
            ut.save_to_db()
        user = UserModel.find_by_id(user_id)
        return user.tags


@tagblp.route("/<tag_id>")
class UserTagById(MethodView):
    @tagblp.arguments(UserTagMappingSchema)
    @tagblp.response(200, UserTagMappingSchema)
    def patch(self, new_data: UserTagMappingModel, tag_id):
        # 修改内容,上传图片

        return new_data

    @tagblp.arguments(UserTagMappingSchema)
    @tagblp.response(204)
    def delete(self, new_data: UserTagMappingModel, tag_id):
        if new_data.id != tag_id:
            abort("参数错误")
        tag = new_data.tag
        if tag.created_by == current_user.id:
            tag.delete_from_db()
        new_data.delete_from_db()
        return


@tagblp.route("/<tag_id>/like")
class UserTagLike(MethodView):
    @tagblp.arguments(UserTagMappingSchema)
    @tagblp.response(200)
    def get(self, new_data: UserTagMappingModel, tag_id):
        if new_data.id != tag_id:
            abort("参数错误")
        liked_by_ids = {id for id in new_data.liked_by}
        friend_ids = {id for id in current_user.friends}
        now_liked_by_ids = friend_ids & liked_by_ids
        data = UserTagMappingSchema().dump(new_data)
        return [
            element for element in data if element["liked_by"]["id"] in now_liked_by_ids
        ]

    @tagblp.response(200, UserTagMappingSchema(many=True))
    def post(self, tag_id):
        # 他人点赞
        ut = UserTagMappingModel.find_by_id(tag_id)
        if ut.user_id == current_user.id:
            abort(401)
        ut.liked_by.append(current_user)
        id = ut.save_to_db()
        return UserTagMappingModel.find_by_id(id)
