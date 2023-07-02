from marshmallow_sqlalchemy import SQLAlchemySchema
from app.models.friend import FriendModel
from app.schemas.base import BaseSchema
from app.schemas.user import UserOtherSchema
from marshmallow import fields, EXCLUDE, post_dump, pre_load, pre_dump

from app.utils.before_request import current_user


class ApplySchema(SQLAlchemySchema):
    user_id = fields.Integer()
    friend_id = fields.Integer()
    apply_note = fields.String()
    apply_status = fields.Integer()

    class Meta:
        model = FriendModel
        partial = True


class postApplySchema(ApplySchema):
    class Meta:
        model = FriendModel
        unknown = EXCLUDE


class getApplySchema(ApplySchema, BaseSchema):
    friend = fields.Nested(UserOtherSchema)
    user = fields.Nested(UserOtherSchema)

    class Meta:
        model = FriendModel
