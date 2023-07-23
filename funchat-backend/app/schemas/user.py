import re

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.schemas.base import BaseSchema, UserOtherSchema
from marshmallow import (
    fields,
    ValidationError,
    validates,
    validates_schema,
    INCLUDE,
    pre_dump,
)
from app.models.user import UserModel
from app.schemas.group import GroupSchema


class UserSelfSchema(SQLAlchemyAutoSchema):
    friends = fields.Nested(UserOtherSchema, many=True)
    groups = fields.Nested(GroupSchema, many=True)
    token = fields.Str(dump_only=True)

    class Meta:
        model = UserModel
        load_instance = True
        unknown = INCLUDE
        # partial = True  #SQLAlchemyAutoSchema中不能使用
        # fields = ["friends_with_me", "groups_owned"]

    @pre_dump
    def serializer(self, user, **kwargs):
        user.friends = [friend for friend in user.friends if friend.apply_status == 1]
        return user


# SQLAlchemyAutoSchema back_populates会加载，使用backref会加载？
