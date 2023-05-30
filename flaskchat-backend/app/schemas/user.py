from . import ma
from .base import BaseSchema
from app.models.user import UserModel
from app.models.friend import FriendModel

class UserSchema(ma.SQLAlchemySchema, BaseSchema):
    class Meta:
        model = UserModel
        partial = True  # 允许部分字段


class FriendSchema(ma.SQLAlchemySchema,BaseSchema):
    user_id = ma.auto_field()
    friend = ma.Nested("UserSchema",many=True)
    class Meta:
        model = FriendModel
        partial = True
