from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.schemas.base import BaseSchema
from marshmallow import fields, ValidationError, validates_schema, EXCLUDE
from app.models.user import UserModel


class LoginSchema(SQLAlchemyAutoSchema, BaseSchema):
    verify_code = fields.Str(allow_none=False)

    class Meta:
        model = UserModel
        fields = ("username", "password", "verify_code")
        load_only = ("username", "password", "verify_code")
        unknown = EXCLUDE

    @validates_schema
    def validate(self, data, **kwargs):
        if not data["verify_code"]:
            raise ValidationError
        del data["verify_code"]
        return data
