from .base import BaseSchema
from app.models.user import UserModel
from app.models.info import InfoModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema, auto_field
from marshmallow import fields, validates_schema, ValidationError, EXCLUDE, pre_load


class UserSelfInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InfoModel
        ordered = True
        partial = True


class UserOtherInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = InfoModel
        fields = ["nickname", "avatar", "gender", "note"]


class UserSelfSchema(SQLAlchemySchema, BaseSchema):
    username = auto_field()
    login_time = auto_field()
    info = fields.Nested(UserSelfInfoSchema)

    class Meta:
        model = UserModel
        # partial = True  # 允许部分字段


class UserOtherSchema(SQLAlchemySchema, BaseSchema):
    info = fields.Nested(UserOtherInfoSchema)

    class Meta:
        model = UserModel


class RegisterSchema(SQLAlchemySchema, BaseSchema):
    username = fields.String()
    info = fields.Nested(UserSelfInfoSchema)
    verify_code = fields.String(load_only=True)

    @validates_schema
    def validate(self, data, **kwargs):
        # redis中获取
        # code = 1111
        # if code != data:
        #     raise ValidationError("验证码错误")
        if "verify_code" in data:
            print("code", data["verify_code"])
        del data["verify_code"]

    @pre_load
    def deserialize(self, data, **kwargs):
        data["username"] = data["info"]["mobile"]
        return data
