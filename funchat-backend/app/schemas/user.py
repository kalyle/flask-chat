import re

from marshmallow_sqlalchemy import SQLAlchemySchema,SQLAlchemyAutoSchema
from app.schemas.base import BaseSchema,UserOtherSchema
from marshmallow import fields, ValidationError, validates,validates_schema
from app.models.user import UserModel
from app.schemas.group import GroupSchema



class UserSelfSchema(SQLAlchemyAutoSchema):
    friends = fields.Nested(UserOtherSchema, many=True)
    groups = fields.Nested(GroupSchema, many=True)

    class Meta:
        model = UserModel
        load_instance = True
        exclude = ["friends_with_me", "groups_owned"]
        # include = EXCLUDE
        # partial = True  #SQLAlchemyAutoSchema中不能使用

# SQLAlchemyAutoSchema back_populates会加载，使用backref会加载？



class LoginSchema(SQLAlchemySchema):
    verify_code = fields.Str(load_only=True,allow_none=False)

    class Meta:
        model = UserModel
        fields = ("username", "password","verify_code")

    @validates_schema
    def validate(self, data, **kwargs):
        if data["verify_code"]:
            pass
        else:
            raise ValidationError
        del data["verify_code"]
        return data


class RegisterSchema(SQLAlchemySchema, BaseSchema):
    password2 = fields.Str(load_only=True)

    class Meta:
        model = UserModel
        load_instance = True

    @validates_schema  # 验证多个字段
    def validate(self,data,**kwargs):
        if data["password"] != data["password2"]:
            raise ValidationError("密码输入错误")
        return data

    @validates("email")  # 验证单个字段
    def validate_email(self,email):
        if re.match("", email):
            raise ValidationError("邮箱格式错误")
        return email
