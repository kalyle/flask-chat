from .base import BaseSchema
from app.models.user import UserModel
from app.models.info import InfoModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema,SQLAlchemySchema,auto_field
from marshmallow_sqlalchemy.fields import Nested

class UserSelfInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InfoModel

class UserOtherInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InfoModel
        fields = ["nickname","avatar","gender","note"]

class UserSelfSchema(SQLAlchemySchema, BaseSchema):
    username = auto_field()
    login_time = auto_field()
    info = Nested(UserSelfInfoSchema)
    class Meta:
        model = UserModel
        # partial = True  # 允许部分字段


class UserOtherSchema(SQLAlchemySchema,BaseSchema):
    info = Nested(UserOtherInfoSchema)
    class Meta:
        model = UserModel
