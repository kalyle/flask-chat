
from app.models.friend import FriendModel
from app.schemas.base import BaseSchema
from app.schemas.info import InfoOtherSchema
from marshmallow import fields, EXCLUDE
from app.schemas import  ma


class ApplySchema(ma.SQLAlchemySchema):
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
    friend = fields.Nested(InfoOtherSchema)
    user = fields.Nested(InfoOtherSchema)

    class Meta:
        model = FriendModel
