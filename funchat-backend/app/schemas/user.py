import re

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.schemas.base import BaseSchema, UserOtherSchema
from marshmallow import fields, ValidationError, validates, validates_schema, INCLUDE
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


# SQLAlchemyAutoSchema back_populates会加载，使用backref会加载？


class LoginSchema(SQLAlchemyAutoSchema):
    verify_code = fields.Str(load_only=True, allow_none=False)

    class Meta:
        model = UserModel
        fields = ("username", "password", "verify_code")
        unknown = INCLUDE

    @validates_schema
    def validate(self, data, **kwargs):
        if data["verify_code"]:
            pass
        else:
            raise ValidationError
        del data["verify_code"]
        return data


class RegisterSchema(SQLAlchemyAutoSchema):
    password2 = fields.Str(load_only=True)

    class Meta:
        model = UserModel
        fields = (
            "username",
            "password",
            "mobile",
            "nickname",
            "avatar",
            "email",
        )  # 不是include
        partial = True
        unknown = INCLUDE

    @validates_schema  # 验证多个字段
    def validate(self, data, **kwargs):
        if data["password"] != data["password2"]:
            raise ValidationError("密码输入错误")
        data["username"] = data["mobile"]
        del data["password2"]
        return data

    # @validates("email")  # 验证单个字段
    # def validate_email(self, email):
    #     if re.match("", email):
    #         raise ValidationError("邮箱格式错误")
    #     return email
