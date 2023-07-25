from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.models.tag import TagModel
from app.models.user import UserModel
from app.models.user_tag_mapping import UserTagMappingModel
from app.schemas.tag import TagSchema
from app.schemas.user_tag_mapping import UserTagMappingSchema
from app.utils.before_request import current_user

tagblp = Blueprint("tag", "tag", url_prefix="/tag")


class Tag(MethodView):
    @tagblp.response(200, TagSchema(many=True))
    def get(self):
        tags = TagModel.find_tags()
        return tags

    @tagblp.arguments(TagSchema)
    @tagblp.response(200, TagSchema)
    def post(self, new_data: TagModel):
        new_data.save_to_db()
        return new_data


class UserTag(MethodView):
    @tagblp.response(200, UserTagMappingSchema(many=True))
    def get(self):
        uts = UserTagMappingModel.find_all_by_user(user_id=current_user.id)
        return uts


class UserTagById(MethodView):
    @tagblp.arguments(UserTagMappingSchema)
    @tagblp.response(200, UserTagMappingSchema)
    def patch(self, tag_id):
        ut = UserTagMappingModel.find_by_id(tag_id)
        if ut.user_id == current_user.id:
            # 修改内容,上传图片
            pass
        else:
            # 他人点赞
            user = UserModel.find_by_id(current_user.id)
            ut.liked_by.append(user)
        id = ut.save_to_db()
        return UserTagMappingModel.find_by_id(id)

    @tagblp.response(204)
    def delete(self, tag_id):
        ut = UserTagMappingModel.find_by_id(tag_id)
        ut.tag.delete_from_db()
        ut.delete_from_db()
        return
