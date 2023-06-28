from flask_jwt_extended import current_user
from marshmallow_sqlalchemy import SQLAlchemySchema
from app.models.friend import FriendModel
from app.schemas.base import BaseSchema
from app.schemas.user import UserOtherSchema
from marshmallow import fields, EXCLUDE, post_dump, pre_load


class ApplySchema(SQLAlchemySchema):
    user_id = fields.Integer()
    friend_id = fields.Integer()
    apply_note = fields.String()
    apply_status = fields.Integer()

    class Meta:
        model = FriendModel
        partial = True
        # include = EXCLUDE


class postApplySchema(ApplySchema):
    class Meta:
        model = FriendModel
        unknown = EXCLUDE


class getApplySchema(ApplySchema, BaseSchema):
    friend = fields.Nested(UserOtherSchema)
    user = fields.Nested(UserOtherSchema)

    class Meta:
        model = FriendModel

    @post_dump
    def serializer(self, data, **kwargs):
        if data['user_id'] == 9:
            data["fromApply"] = data["friend"]
        else:
            data["toApply"] = data["user"]
        del data["friend"]
        del data["user"]
        return self.snake_to_camel(data)

    @pre_load
    def deserializer(self, data, **kwargs):
        if data['user_id'] == 9:
            data["friend"] = data["fromApply"]
        else:
            data["user"] = data["toApply"]
        del data["fromApply"]
        del data["toApply"]
        return self.camel_to_sanke(data)
