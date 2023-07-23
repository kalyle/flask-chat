from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, ValidationError, validates_schema, EXCLUDE
from app.models.user import UserModel

from app.schemas.info import InfoSelfSchema


class RegisterSchema(SQLAlchemyAutoSchema):
    information = InfoSelfSchema()
    password2 = fields.Str(load_only=True)

    class Meta:
        model = UserModel
        fields = ("username", "password", "information")
        load_instance = True
        partial = True
        unknown = EXCLUDE

    @validates_schema  # 验证多个字段
    def validate(self, data, **kwargs):
        if data["password"] != data["password2"]:
            raise ValidationError("密码输入错误")
        data["username"] = data["information"]["mobile"]
        del data["password2"]
        return data

    # @validates("email")  # 验证单个字段
    # def validate_email(self, email):
    #     if re.match("", email):
    #         raise ValidationError("邮箱格式错误")
    #     return email
