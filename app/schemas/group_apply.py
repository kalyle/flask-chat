from app.schemas import ma
from marshmallow import fields, EXCLUDE
from app.schemas.base import BaseSchema
from app.models.group_apply import GroupApplyModel
from app.schemas.group_chat import GroupChatSchema
from app.schemas.info import InfoOtherSchema


class GroupApplySchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    group_chat = fields.Nested(GroupChatSchema, exclude=("owner", "members"))
    sender = fields.Nested(InfoOtherSchema)

    class Meta:
        model = GroupApplyModel
        load_instance = True
        partial = True
        unkonwn = EXCLUDE
