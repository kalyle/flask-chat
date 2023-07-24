from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema
from marshmallow import fields

from app.models.group_apply import GroupApplyModel
from app.models.group_chat import GroupChatModel
from app.schemas.base import BaseSchema
from app.schemas.info import InfoOtherSchema


class GroupChatSchema(SQLAlchemyAutoSchema):
    owner = fields.Nested(InfoOtherSchema)
    members = fields.Nested(InfoOtherSchema, many=True)

    class Meta:
        model = GroupChatModel
        load_instance = True
        partial = True
        order = True
        fields = ["id", "name", "avatar", "desc", "member_count", "owner", "members"]


class getGroupApplySchema(SQLAlchemySchema, BaseSchema):
    group = fields.Nested(GroupChatModel)

    class Meta:
        model = GroupApplyModel
