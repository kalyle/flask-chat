import re
from app.schemas import ma
from app.schemas.base import BaseSchema
from app.schemas.info import InfoOtherSchema, InfoSelfSchema
from marshmallow import INCLUDE, post_dump, pre_load

from app.models.user import UserModel
from app.schemas.group_chat import GroupChatSchema
from app.schemas.group import GroupSchema


class UserSelfSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    information = ma.Nested(InfoSelfSchema)
    groups = ma.Nested(GroupSchema, many=True)
    friends = ma.Nested(InfoOtherSchema, many=True)
    group_chats = ma.Nested(GroupChatSchema, many=True)
    token = ma.Str(dump_only=True)

    class Meta:
        model = UserModel
        load_instance = True
        unknown = INCLUDE
        fields = ("id", "username", "information", "friends", "groups", "group_chats", "token")
        ordered = True


class UserOtherSchema(ma.SQLAlchemyAutoSchema, BaseSchema):
    information = ma.Nested(InfoOtherSchema)

    class Meta:
        model = UserModel
        load_instance = True
        unknown = INCLUDE
        fields = ("information",)
    @post_dump
    def serializer(self, data, **kwargs):
        info = data["information"]
        return info

    @pre_load
    def deserializer(self, data, **kwargs):
        real_data = {}
        real_data["information"] = data
        return real_data
# SQLAlchemyAutoSchema back_populates会加载，使用backref会加载？
# partial = True  #SQLAlchemyAutoSchema中不能使用
