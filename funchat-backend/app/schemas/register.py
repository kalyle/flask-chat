from marshmallow import fields, ValidationError, validates_schema, EXCLUDE,post_load
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app.models.user import UserModel
from app.schemas import ma
from app.schemas.info import InfoSelfSchema


class RegisterSchema(ma.SQLAlchemyAutoSchema):
    information = ma.Nested(InfoSelfSchema, exclude=("user",))
    password2 = ma.Str()

    class Meta:
        model = UserModel
        fields = ("username", "password", "password2", "information")
        load_only = ("password","password2")
        load_instance = True
        partial = True
        unknown = EXCLUDE

    @validates_schema  # 验证多个字段
    def validate(self, data, **kwargs):
        if data["password"] != data["password2"]:
            raise ValidationError("密码输入错误")
        data["username"] = getattr(data["information"], "mobile")
        del data["password2"]
        return data

    @post_load
    def deserializer(self,data,**kwargs):
        data["password"] = pbkdf2_sha256.hash(data["password"])
        return data



    # @validates("email")  # 验证单个字段
    # def validate_email(self, email):
    #     if re.match("", email):
    #         raise ValidationError("邮箱格式错误")
    #     return email
