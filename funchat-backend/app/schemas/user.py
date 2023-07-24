import re

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.schemas.base import BaseSchema
from app.schemas.info import InfoOtherSchema
from marshmallow import (
    fields,
    ValidationError,
    validates_schema,
    INCLUDE,
)
from app.models.user import UserModel
from app.schemas.group_chat import Grou
from app.schemas.group import GroupModel


class UserSelfSchema(SQLAlchemyAutoSchema, BaseSchema):
    groups = fields.Nested()
    friends = fields.Nested(InfoOtherSchema, many=True)
    group_chats = fields.Nested()
    token = fields.Str(dump_only=True)

    class Meta:
        model = UserModel
        load_instance = True
        unknown = INCLUDE
        fields = ("id", "username", "friends", "groups", "group_chats", "token")


# SQLAlchemyAutoSchema back_populates会加载，使用backref会加载？
# partial = True  #SQLAlchemyAutoSchema中不能使用
