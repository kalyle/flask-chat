from flask_login import current_user
from marshmallow_sqlalchemy import SQLAlchemySchema
from app.models.friend import FriendModel
from app.schemas.base import BaseSchema
from app.schemas.user import UserOtherSchema
from marshmallow import fields, EXCLUDE, post_dump


class ApplyBaseSchema(SQLAlchemySchema):
    user_id = fields.Integer(dump_only=True)
    friend_id = fields.Integer(dump_only=True)
    apply_note = fields.String()
    apply_status = fields.Integer()


class postApplySchema(ApplyBaseSchema):
    class Meta:
        model = FriendModel
        unknown = EXCLUDE


class getApplySchema(SQLAlchemySchema, ApplyBaseSchema,BaseSchema):
    friend = fields.Nested(UserOtherSchema)
    user = fields.Nested(UserOtherSchema)

    class Meta:
        model = FriendModel
        include_pk = True
        partial = True

    @post_dump
    def serialize(self, data, **kwargs):
        if data['user_id'] == current_user.id:
            data["fromApply"] = data["friend"]
        else:
            data["toApply"] = data["user"]
        del data["friend"]
        del data["user"]
        return data


class patchApplySchema(SQLAlchemySchema):
    class Meta:
        model = FriendModel
