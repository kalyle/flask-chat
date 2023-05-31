from . import ma
from .base import BaseSchema
from app.models.user import UserModel
from app.models.friend import FriendModel
from app.models.info import InfoModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,SQLAlchemySchema,auto_field
from marshmallow_sqlalchemy.fields import Nested

class SelfInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InfoModel

class OtherInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InfoModel
        fields = ["nickname","avatar","gender","note"]

class UserSelfSchema(SQLAlchemySchema, BaseSchema):
    username = auto_field()
    login_time = auto_field()
    info = Nested(SelfInfoSchema)
    class Meta:
        model = UserModel
        # partial = True  # 允许部分字段


class UserOtherSchema(SQLAlchemySchema,BaseSchema):
    info = Nested(OtherInfoSchema)
    class Meta:
        model = UserModel
        exclude = ["create_time","update_time"]
