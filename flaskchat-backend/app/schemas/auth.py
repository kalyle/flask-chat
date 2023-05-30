import re

from . import ma
from .base import BaseSchema
from marshmallow import fields, ValidationError, validates,validates_schema
from app.models.user import User


class LoginSchema(ma.Schema):
    verify_code = fields.Str(load_only=True)

    class Meta:
        model = User
        fields = ("username", "password")


class RegisterSchema(ma.SQLAlchemySchema, BaseSchema):
    # email_code = fields.Str(load_only=True)
    password2 = fields.Str(load_only=True)

    class Meta:
        model = User
        exclude = ("note",)

    @validates_schema  # 验证多个字段
    def validate(self,data):
        if data["password"] != data["password2"]:
            raise ValidationError("密码输入错误")
        return data

    @validates("email")  # 验证单个字段
    def validate_email(self,email):
        if re.match("", email):
            raise ValidationError("邮箱格式错误")
        return email



