from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema
from marshmallow import fields, post_dump

from app.models.group_apply import GroupApplyModel
from app.models.group_chat import GroupChatModel
from app.schemas.base import BaseSchema, UserOtherSchema


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GroupChatModel
        fields = ["id", "name", "avatar", "member_count", "desc"]


class GroupApplySchema(SQLAlchemySchema):
    sender_id = fields.Integer()
    group_id = fields.Integer()
    apply_note = fields.String()
    apply_status = fields.Integer()

    class Meta:
        model = GroupApplyModel
        load_instance = True


class getGroupApplySchema(SQLAlchemySchema, BaseSchema):
    group = fields.Nested(GroupSchema)
    user = fields.Nested(UserOtherSchema)

    class Meta:
        model = GroupApplyModel

    # @post_dump
    # def serializer(self, data, **kwargs):
    #     if current_user.id == data["user"]["id"]:
    #         del data["user"]
    #     else:
    #         del data["group"]
    #     return data
